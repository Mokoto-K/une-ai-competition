# TODO - Implement a strategy class/module that selects the assets and timeframe
# automatically for the data module. ie if low risk is selected, choose less volitile
# assets and higher time frames like days and weeks to make decisions on.
# TODO - Switch from a csv to a proper db like sqlite or postgres


import requests as r
import csv
import os 
import datetime as dt
BASE_URL: str = "https://api.bybit.com"
OHLC_URL: str = BASE_URL + "/v5/market/kline"

ASSET_NAME: str = "BTCUSDT"
TIME_FRAME: str = "D"

FILE_NAME: str = f"{ASSET_NAME}_{TIME_FRAME}_Data.csv"


def create_DB() -> None:
    # TODO - Decide if hard coded params is the way to go or more dynamic approach needed
    """
    Creates a database if one does not yet exist
    """

    with open(FILE_NAME, "w") as new_file:

        print("CREATING NEW DATABASE FILE")
        
        # Add the column names to the file 
        new_file.write("date,time,open,high,low,close,volume,utc\n")
    
    params = {"category": "linear",     
          "symbol": ASSET_NAME,      
          "interval": TIME_FRAME,         
          "limit": 1000                 
          }

    write_to_DB(params) 


def write_to_DB(parameters: dict) -> None:
    # TODO - Fix the god damn description! haha

    """
    Queries exchange for market info and writes the info to the DB

    Params:
    parameters - A Dictionary containing the specific.... finish this off later
    """

    # Retrieve market data, put it all in a list
    response = r.get(OHLC_URL, params = parameters)
    market_data: list = [row for row in response.json()["result"]["list"]]

    # Reverse the list so its oldest first, most recent last chronologically
    market_data.reverse() 
    
    # Open our DB file and write the contents of the list to the file
    with open(FILE_NAME, "a", newline = "") as file:
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


    print(f"{parameters["limit"]} line(s) written to Database")


def update_DB():
    """
    Compares todays date and time with the latest record in the database to 
    check if the database is up to date or if it needs to retrieve more records
    """

    # Get todays date in indentical format to the database for comparison
    todays_date = dt.datetime.now().strftime("%a-%d-%b-%y")

    # Get the current days date in unix form using UTC from midnight (matches markets time keeping)
    # This is the most accurate and modular way I can think to measure the difference
    # between the last entry in the database and the current time and this method
    # still doesn't account for intraday timeframes yet.
    utc_todays_date = dt.datetime.strptime(todays_date,"%a-%d-%b-%y")\
                      .replace(tzinfo=dt.timezone.utc).timestamp()

    print(utc_todays_date)

    print("CHECKING IF DATABASE IS UP TO DATE")
    
    # Get the date of the last record in the database
    last_records_date: str = get_last_record()

    if todays_date != last_records_date:
        print(float(utc_todays_date) - float(last_records_date)) 

    with open(FILE_NAME, "a", newline = "") as file:
        pass 


def get_last_record() -> str:
    """
    Queries the database for the last entry and retrieves it's date

    Returns:
    date - The date for the last line in the database
    """
    print(f"RETRIEVEING LAST RECORDS FROM CSV")

    with open(FILE_NAME, "r") as file:
        all_lines = file.readlines()

        # get all lines in the db, slice the last line out and split it at the first comma
        # that will give you the date of the latest record in the db
        date: str = all_lines[-2:][0].split(",")[7].strip("\n")

    return date 


def delete_records():
    pass


def main():
    # TODO - Decide if user decides params or hardcoded for time being

    if not os.path.exists(FILE_NAME):
        create_DB()

    #get_last_record()
    update_DB()
    print(get_last_record())

    # Must contain type of contract, ticker the timeframe and the amount of records
    params = {"category": "linear",     # Contract type
          "symbol": ASSET_NAME,      # Asset ticker or symbol
          "interval": TIME_FRAME,          # Timeframe to retireve data from
          "limit": 1                 # Number of records to retrieve
          }
    # write_to_DB(params)

if __name__ == "__main__":
    main()
