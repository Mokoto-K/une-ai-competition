# TODO - Switch from a csv to a proper db like sqlite or postgres

import requests as r
import csv
import os 
import datetime as dt
from typing import Optional

class Database:
    """
    Manages market data retrieval and storage for our assets.
    """

    def __init__(self, asset_name: str = "BTCUSDT", time_frame: str = "D",
                 contract_type: str = "linear", max_limit: int = 1000):

        self.base_url: str = "https://api.bybit.com"
        self.ohlc_url: str = self.base_url + "/v5/market/kline"
        self.asset_name: str = asset_name 
        self.time_frame: str = time_frame 
        self.contract_type: str = contract_type 
        self.max_limit: int = max_limit 
        self.file_name: str = f"{self.asset_name}_{self.time_frame}_Data.csv"


    # TODO - It appears the internet check isnt working, added temp try/excepts
    # fix this bug asap!!
    def test_connection(self) -> int:
        """
        A test to check for internet connection prior to sending requests
        """
    
        try:
            r.get(self.ohlc_url)
        except Exception:
            print("Trouble retrieving your request, check if the exchange api is up\
            and running, check your internet connection and double check what you are\
            requesting")
            return 0
        
        return 1
    
    
    def query_exchange(self, limit: Optional[int] = None) -> list: 
        """
        Requests exchange to retreieve current market records for given parameters 
    
        Params:
        category - The type of contract to query, (spot, linear, etc)
        symbol - Also known as ticker, the name of the asset you are looking
        interval - The timeframe you want to retrieve records for D(day), M(month)
        60(hourly), etc
        limit - The number of records to get, 1000 being the max
    
        Returns:
        market_data - A list of market records in reverse order such that the oldest
        records are first and the newest records are last.
        """
        
        parameters: dict = {"category": self.contract_type, 
              "symbol": self.asset_name,      
              "interval": self.time_frame,         
              "limit": limit or self.max_limit
              }
    
        response = r.get(self.ohlc_url, params = parameters)
        market_data: list = [row for row in response.json()["result"]["list"]]
    
        # Reversing the list to get chronological order
        market_data.reverse()
        return market_data
    
    
    def create_DB(self) -> None:
        """
        Creates a database if one does not yet exist
    
        Params:
        time_frame - the time frame to query data for, i.e the data for every minute,
                     day, week, month, etc
        """
        
    
        with open(self.file_name, "w") as new_file:
    
            print("CREATING NEW DATABASE FILE")
            
            # Add the column names to the file 
            new_file.write("date,time,open,high,low,close,volume,utc\n")
                
        market_data = self.query_exchange()
        self.write_to_DB(market_data) 
    
    
    def write_to_DB(self, market_data: list) -> None:
        """
        Writes passed in data to the database
    
        Params:
        market_data - A list containing market information to be written to the db
        """
    
        # Open our DB file and write the contents of the list to the file
        with open(self.file_name, "a", newline = "") as file:
            writer = csv.writer(file, delimiter = ",")     
    
            for line in range(len(market_data)):
                # slice out the UTC timestamp and divide it by 1000 as "fromdatestamp"
                # doesn't use the full utc stamp (they might want to change this)
                timestamp: float = int(market_data[line][0]) / 1000
    
                # Format the data and time for the line entry
                date: str = dt.datetime.fromtimestamp(timestamp).strftime("%a-%d-%b-%y")
                time: str = dt.datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
    
                open_price: float = round(float(market_data[line][1]))
                high_price: float = round(float(market_data[line][2]))
                low_price: float = round(float(market_data[line][3]))
                close_price: float = round(float(market_data[line][4]))
    
                # For volume we are choosing to multiply by the open price as it's
                # measured via asset contracts sold and not USD, so we convert to USD
                volume: float = round(float(market_data[line][5])) * open_price
    
                writer.writerow([date, time, open_price, high_price, low_price, close_price, volume, timestamp])
    
    
        print(f"{len(market_data)} line(s) written to Database")
    
    
    def update_DB(self):
        """
        Compares database timestamps to current market timestamps to determine how
        many records are missing from the database that need to be downloaded to 
        update it to the current market information
    
        Params:
        time_frame - the time frame to query data for, i.e the data for every minute,
                     day, week, month, etc
        """
        
        print("CHECKING IF DATABASE IS UP TO DATE")
        records_to_retrieve = 1 
       
        try:
            # Query the exchange to get the lastest data & extract just the unix timestamp
            lastest_ts = float(self.query_exchange(limit = 1)[0][0].split(",")[0]) / 1000
        except Exception:
            print("You seem to have lost connection with the exchange, check your internet "+
                "or visit bybit.com to check their current status")
            exit(0)

        # Get the last three records from the db (3 to be safe)
        recent_utc_timestamps: list = self.get_records(3)
    
        if lastest_ts == recent_utc_timestamps[0]:
            # If the utc ts are the same, update only the latest record to current info
            self.delete_records(1)
    
        else:
            # Calculate the time difference between each entry 
            time_difference = recent_utc_timestamps[1] - recent_utc_timestamps[2]
    
            # Subtract current ts from last db entry ts and divide by the difference
            # between entries this will give us the number of entries missing
            records_to_retrieve = int((lastest_ts - recent_utc_timestamps[0]) / time_difference + 1)
    
            # This is the plus 1 from the above sum we are deleting. This is due to
            # not assuming we recorded the precise close for the current timeframe 
            # in the database and therefore will re-record it now we know its closed
            self.delete_records(1)
    
        market_data: list = self.query_exchange(limit = records_to_retrieve)
        self.write_to_DB(market_data)
    
    
    def get_records(self, count: int = 3) -> list:
        """
        Queries the database for the last entry and retrieves it's date
    
        Returns:
        date - The date for the last line in the database
        """
        print(f"RETRIEVEING LAST RECORDS FROM DATABASE")
    
        date_list = []
    
        with open(self.file_name, "r") as file:
            all_lines = file.readlines()
    
            for i in range(1, count+1):
                # get all lines in the db, slice the requested lines out, split them
                # by "," take the last value, strip the newline, isolate the unix ts
                date_list.append(float(all_lines[-i:][0].split(",")[7].strip("\n")))
    
        return date_list
    
    
    def delete_records(self, count: int) -> None:
        """
        Rewrites the database file with the last x amount of lines excluded
    
        Params:
        records - The number of lines to exclude
        """
    
        print(f"UPDATING {count} RECORD(S) FROM DATABASE")
    
        with open(self.file_name, "r") as read_file:
            database = read_file.readlines()
            with open(self.file_name, "w") as fead_rile: # fead_rile... he chuckles to himself
                fead_rile.writelines(database[: -count])
    
   
    def get_file_name(self) -> str:
        """
        Sneaky little function for name retrieval
        """
        return "./"+self.file_name
        

    def run(self):
        print(f"{'-'*45}\n{'-'*45}")
        if self.test_connection:  
            if not os.path.exists(self.file_name):
                self.create_DB()
            else: 
                self.update_DB()
        else:
            print("Cannot connect to exchange, check your internet connect or"+  
                " visit bybit.com to check for their currect operation status")
        print(f"{'-'*45}\n{'-'*45}")

    
if __name__ == "__main__":
    pass
