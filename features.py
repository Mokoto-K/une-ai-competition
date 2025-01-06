# TODO - This needs to be reworked more modular so that any indices passed in 
# can have its own set of features? or perhaps once I train le algo I will know
# how to contruct the right set of features correctly? come back to this.

# TODO - Actually figure out what features you need to not lose your house in the
# market(i suspect this is incredibly difficult and unsolvable, edge is hard to, 
# find) for now hardcorde basic things, rework once solution is up and running.

import pandas as pd
from pandas._libs.tslibs.fields import month_position_check # "standing on the shoulders of giants - Issac Newton"
from mykitlearn import split_test_train, encode_labeler # Screw the giants!

# Location of our Database file
db_path: str = "./BTCUSDT_D_Data.csv"

# Load our database as a df 
market_data: pd.DataFrame = pd.read_csv(db_path)

# Assign quick refs to our main data points in the dataframe
price_open = market_data.open
price_high= market_data.high
price_low= market_data.low
price_close= market_data.close
price_volume= market_data.volume


# TODO - All these features can be rolled into one for loop....do that pls

# Feature "engineering" (like im building bridges out here!)-------------------

# Creating labels for our NN to use for training, if market close is higher then
# open, it was a buy, otherwise it was a sell.
def create_labels() -> list:
    target = ["long" if price_close[i] > price_open[i] else "short" 
        for i in range(len(price_open))]

    return target


market_data["target"] = create_labels()


# Create day and month features------------------------------------------------
def process_dates() -> tuple:
    dates = market_data.date
    day_list: list = []
    month_list: list = []

    for row in dates:
        # working the date string from the db, separating days and months in the df
        day: str = row.split("-")[0]
        month: str = row.split("-")[2]

        day_list.append(day)
        month_list.append(month)

    return day_list, month_list


market_data["day"], market_data["month"] = process_dates() 

# Don't need the old date or time, just the new day & month for these features
market_data = market_data.drop(["date", "time"], axis = 1)


# Creating daily open change-------------------nvim---------------btw----------
def calc_daily_change() -> list:
    daily_change: list = [0] # explanation below

    for row in range(len(price_open)):

        # Skipping the first element initialzed to 0, this is due to the offset of
        # calculating one days open to the next, we end up one short in the list
        if row == 0:
            continue
    
        # percentage change for the timeframe
        change: float = (price_open[row] - price_open[row - 1]) / price_open[row -1] * 100
        daily_change.append(round(change,8))

    return daily_change


market_data["daily_change"] = calc_daily_change() 


# Creating volitility----------------arch-user-btw---------not-a-furry---------

# TODO - Consider an offset to help predict current day
def calc_volitility() -> list:
    volitility: list = [0]

    for row in range(len(price_high)):

        if row == 0:
            continue

        vol: float = (price_high[row - 1] - price_low[row - 1]) / 100
        volitility.append(vol)

    return volitility

market_data["volitility"] = calc_volitility()


# Create volume col------------------------------------------------------------
def calc_volume() -> list:
    volume: list = [0]

    for row in range(len(price_volume)):

        if row == 0:
            continue

        volume.append(price_volume[row - 1] / 100000000)


    return volume


market_data["volume"] = calc_volume() 

# TODO - All these features can be rolled into one for loop....do that pls
# TODO - MOAR FEATURES, such as:
# TODO - Price moving average
# TODO - % change moving average
# TODO - volitility Moving average
# TODO - Price to standard dev distance

# Prep the dataframe for training----------------------------------------------

# Encode all str features + the labels
    # TODO - should move this dict out of this function
encoders = {"day" : encode_labeler(),
                "month": encode_labeler(),
                "target": encode_labeler()
                }

for feature, encoder in encoders.items():
    market_data[feature] = encoder.fit_transform(market_data[feature])


# Scale the features
# Coming soon

# Feature selection
def prep_data() -> tuple:
    selected_features: list =["day", "month", "daily_change", "volitility", 
                              "volume", "target"] 

    X: pd.DataFrame = market_data.filter(selected_features)

    X_full, X_test, y_full, y_test = split_test_train(X.drop("target", axis = 1), 
                                                  X.target,
                                                  test_size = 0.2, 
                                                  random_state = 42)

    # The datasets used to train and test the NN
    X_val, X_train = X_full[:100], X_full[100:]
    y_val, y_train = y_full[:100], y_full[100:]
    
    return X_val, X_train, X_test, y_val, y_train, y_test


def get_latest_values():
    # The set of values to predict the current market decision, slicing out the 
    # target from the selected_features
    selected_features: list =["day", "month", "daily_change", "volitility", 
                              "volume"]
    return market_data[-1:].filter(selected_features)


if __name__ == "__main__":
    pass
