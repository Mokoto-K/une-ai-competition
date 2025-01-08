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

    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.time_stamp = str(int(time.time() * 1000))
        self.recv_window = str(5000)

        if testnet:
            self.base_url = "https://api-testnet.bybit.com"
        else:
            self.base_url = "https://api.bybit.com"


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

        if method=="GET":
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
        """
        
        params=f'category={category}&symbol={symbol}'
        
        result = self._make_request("GET", "/v5/position/list", params)

        return result.json()["result"]["list"][0]["side"]


    def create_order(self, category, symbol, side, order_type, qty, price, time_in_force="PostOnly"):
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


    def cancel_all(self, category = "linear", symbol = "BTCUSDT"):
        params = json.dumps({
                            "category": category,
                            "symbol": symbol
        })

        self._make_request("POST", "/v5/order/cancel-all", params)




# endpoint="/v5/order/create"
# method="POST"
# orderLinkId=uuid.uuid4().hex
# params='{"category":"linear","symbol": "BTCUSDT","side": "Buy","positionIdx": 0,"orderType": "Limit","qty": "0.001","price": "10000","timeInForce": "GTC","orderLinkId": "' + orderLinkId + '"}'
# HTTP_Request(endpoint,method,params,"Create")

#Get unfilled Orders




#Cancel Order
# endpoint="/v5/order/cancel"
# method="POST"
# params='{"category":"linear","symbol": "BTCUSDT","orderLinkId": "'+orderLinkId+'"}'
# HTTP_Request(endpoint,method,params,"Cancel")
