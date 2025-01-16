# TODO - Fix all documentation when i have time

import requests
import time
import hashlib
import hmac
import json

class Exchange:
    """
    Provides a personal set of connections to an exchanges api (bybit for this project)

    Mostly sourced from https://bybit-exchange.github.io/docs/v5/info & 
    https://github.com/bybit-exchange/api-usage-examples/tree/master, very detailed
    set of api docs, though authentication was... an experience for me!
    """
    
    URL = "https://api.bybit.com"

    
    def __init__(self, api_key = None, api_secret = None, testnet: bool = False):
    
        self.api_key = api_key
        self.api_secret = api_secret
        self.time_stamp = str(int(time.time() * 1000))
        self.recv_window = str(5000)

        if testnet:
            self.base_url = "https://api-testnet.bybit.com"
        else:
            self.base_url = "https://api.bybit.com"


    def test_connection(self):
        try:
            requests.get(self.base_url+"/v5/market/time")
            return 1
        except Exception:
            print("Could not connect to bybit's servers, try again later")
            exit(0)


    def authenticate_connection(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret


    def _generate_signature(self, params) -> str:
        """
        uses your api to generate a signature to make requests, needed to ensure
        you are making valid requests in terms of time, were they recently made 
        or are they being played back by a hackermans! atleast I think... should 
        probably update this description in the future.
        """

        param_str= self.time_stamp + self.api_key + self.recv_window + params 
        signature= hmac.new(bytes(self.api_secret, "utf-8"), 
                        param_str.encode("utf-8"),
                        hashlib.sha256).hexdigest()

        return signature
      

    def _make_request(self, method, endpoint, params):
        """
        Will take in your request and call generate_signature to send an authenticated
        request to the exchange to do you bidding
        """
        # You gotta update the time every request
        self.time_stamp = str(int(time.time() * 1000))

        signature = self._generate_signature(params)


        headers = {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': self.time_stamp,
            'X-BAPI-RECV-WINDOW': self.recv_window,
            'Content-Type': 'application/json'
        }

        if method == "GET":
            response = requests.get(self.base_url + endpoint + "?" + params,
                                    headers=headers)
        elif method == "POST":
            response = requests.post(self.base_url + endpoint, 
                                     headers=headers, data=params)
        else:
            raise ValueError("Invalid HTTP method: " + method)

        return response

       
    def get_position(self, category = "linear", symbol = "BTCUSDT"):
        """
        Gets current position from exchange 

        Params:
        category - The contract type of your position, i.e 'linear', 'spot'
        symbol - The ticker name of the asset you have a position in i.e 'BTCUSDT',
                default is 'None' so will return all... i believe.

        Returns:
        direction - 
        size - 
        price - 
        query_status - return message from exchange
        """
        
        params=f'category={category}&symbol={symbol}'
        
        result = self._make_request("GET", "/v5/position/list", params)
         
        # TODO - Look into strange bug that crops up every now and then revolving 
        # around bybit timing out, for now a simple try except till further investigation
        try:
            returned_result = result.json()["result"]["list"][0]#["side"]
            direction = returned_result["side"]
            size = returned_result["size"]
            price = returned_result["avgPrice"]
            query_status = result.json()["retMsg"]
        except KeyError:
            print("Trouble retrieving your current position from the exchange, Try again shortly")
            exit(0)
            #return 
            
        return direction, size, price, query_status


    def get_balance(self, account_type: str = "UNIFIED", coin: str = "USDT"):
        """
        Get user balance
        """
        params = f"accountType={account_type}&coin={coin}"

        result = self._make_request("GET", "/v5/account/wallet-balance", params)

        returned_result = result.json()["result"]["list"][0]["coin"][0]["walletBalance"]#["totalWalletBalance"]
        #print(returned_result) 
        return returned_result 


    def get_price(self, category: str = "linear", symbol: str = "BTCUSDT"):
        """
        Get price of provided ticker
        """
        
        params = f"category={category}&symbol={symbol}"

        result = self._make_request("GET", "/v5/market/tickers", params)

        returned_result = result.json()["result"]["list"][0]["lastPrice"]

        return returned_result


    def create_limit_order(self, category, symbol, side, order_type, qty, price, time_in_force="PostOnly"):
        params = json.dumps({
                            "category": category,
                            "symbol": symbol,
                            "side": side,
                            "orderType": order_type,
                            "qty": qty,
                            "price": price,
                            "timeInForce": time_in_force
        })

        response = self._make_request("POST", "/v5/order/create", params)

        return response.json()


    def market_order(self, category, symbol, side, order_type, qty) -> str: 
        params = json.dumps({
                            "category": category,
                            "symbol": symbol,
                            "side": side,
                            "orderType": order_type,
                            "qty": qty,
        })

        response = self._make_request("POST", "/v5/order/create", params)
        # print(response.json())
        # Return the response mostly for testing
        return response.json()


    def cancel_all(self, category = "linear", symbol = "BTCUSDT"):
        params = json.dumps({
                            "category": category,
                            "symbol": symbol
        })

        self._make_request("POST", "/v5/order/cancel-all", params)




