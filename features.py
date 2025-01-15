# TODO - Implement with no pandas, just numpy
# TODO - figure out what features you need to not lose your house in the
# market(i suspect this is incredibly difficult and unsolvable, edge is hard to, 
# find) for now hardcorde basic things, rework once solution is up and running.

# TODO - Build cross validation, probably in the mykitlearn lib actually.

from shutil import move
from numpy import append
import pandas as pd         #""standing on the shoulders of giants - Issac Newton"... for now" - me
from mykitlearn import NonStandardScaler, split_test_train, encode_labeler # Screw the giants!

# Feature "engineering" (like im building bridges out here!)-------------------
class DataFeatures:
    def __init__(self, db_path: str) -> None:
        """
        Initialize the MarketFeatures class for data loading and preprocessing
        
        Params:
        db_path - a file path that leads to the data you with to process
        """
        self.db_path = db_path
        self.market_data = pd.read_csv(db_path)
        self.encoders = {"day" : encode_labeler(),
                        "month": encode_labeler(),
                        "target": encode_labeler()
                        }
        self.unstandardScaler = NonStandardScaler()

        # Assign quick refs to our main data points in the dataframe
        self.price_open = self.market_data.open
        self.price_high = self.market_data.high
        self.price_low = self.market_data.low
        self.price_close = self.market_data.close
        self.price_volume = self.market_data.volume
        self.dates = self.market_data.date
        self.time = self.market_data.time

        # To hold features that need scaling and filter list for training
        self.selected_features = []
        self.scale_features = []

    def create_target_labels(self) -> None:
        """
        Creates binary labels for the dataset to be used in training
        """
        target: list = []

        for i in range(len(self.price_open)):
            # If market close was higher than open, it was a buy, otherwise a sell.
            target.append("long" if self.price_close[i] > self.price_open[i] else "short") 
    
        self.market_data["target"] = target 
        self.selected_features.append("target")


    def process_dates(self) -> None:
        """
        Strips out the date str from the data and splits it into day and month
        """
        day_list: list = []
        month_list: list = []
    
        for row in self.dates:
            # working the date string from the db, separating days and months in the df
            day: str = row.split("-")[0]
            month: str = row.split("-")[2]
    
            day_list.append(day)
            month_list.append(month)
    
        self.market_data["day"], self.market_data["month"] = day_list, month_list 
        self.selected_features.append("day")
        self.selected_features.append("month")


    def process_time(self) -> None:
        
        hours_list = []
        minutes_list = []

        for row in self.time:
            hour: int = int(row.split(":")[0]) 
            minutes: int = int(row.split(":")[1])
            
            hours_list.append(hour)
            minutes_list.append(minutes)
        
        self.market_data["hour"], self.market_data['minute'] = hours_list, minutes_list

        # Remove the old time data
        # self.market_data.drop(["time"], axis = 1, inplace = True)


    def calc_daily_change(self) -> None:
        """ 
        Calculate the percentage change between each time gap 
        """
    
        daily_change: list = [0] # open to open is two data entries, offset by 1
    
        for row in range(1, len(self.price_open)):
    
            # percentage change for the timeframe
            change: float = (self.price_open[row] - self.price_open[row - 1]) / self.price_open[row -1] * 100
            daily_change.append(round(change,8))
    
        self.market_data["daily_change"] = daily_change
        self.selected_features.append("daily_change")
        self.scale_features.append("daily_change")



    # TODO - Consider an offset to help predict current day
    def calc_volitility(self) -> None:
        """
        Calculates the volitity of the each data entry
        """

        volitility: list = [0]
    
        for row in range(1, len(self.price_high)):
    
            vol: float = (self.price_high[row - 1] - self.price_low[row - 1]) / 100
            volitility.append(vol)
    
    
        self.market_data["volitility"] = volitility 
        self.selected_features.append("volitility")
        self.scale_features.append("volitility")


    # TODO - Change what's being diveded by and use a standard scaling technique
    def calc_volume(self) -> None:
        """
        Rationalizes the volume for each data entry
        """

        volume: list = [0]
    
        for row in range(1, len(self.price_volume)):
    
            volume.append(self.price_volume[row - 1] / 100000000)

        self.market_data["volume"] = volume 
        self.selected_features.append("volume")
        self.scale_features.append("volume")

    def moving_average(self):
        moving_avg = []

        sum = 0
        for row in range(len(self.price_close)):
            sum += self.price_close[row]
            
            if row >=30:
                sum -= self.price_close[row - 30]

            if row >= 30 -1:
                moving_avg.append(sum / 30)
            else:
                moving_avg.append(sum / (row + 1)) 
            
        self.market_data["moving_average"] = moving_avg
        self.selected_features.append("moving_average")
        self.scale_features.append("moving_average")
# TODO - MOAR FEATURES, such as:
# TODO - Price moving average
# TODO - % change moving average
# TODO - volitility Moving average
# TODO - Price to standard dev distance

# ----------------------------------Data prepping-------------------------------

    def encode_features(self) -> None:
        """
        Handles encoding of all categorical features
        """

        for feature, encoder in self.encoders.items():
            self.market_data[feature] = encoder.fit_transform(self.market_data[feature])


    # Feature selection
    def prep_data(self, test_size: float = 0.2, random_state: int = 42) -> tuple:
        """
        Prepares the data for training by selecting features to train on as well
        as splitting the data into different sets for training, testing and validation

        Params:
        test_size - The proportion of the data segmented away for testing only
        random_state - Set the random seed for the shuffling process when splitting
                       the data, set to ensure consistent results.
        """
        X = self.market_data.filter(self.selected_features)
    
        X_full, X_test, y_full, y_test = split_test_train(X.drop("target", axis = 1), 
                                                      X.target,
                                                      test_size = test_size, 
                                                      random_state = random_state)
    
        # The datasets used to train and test the NN
        X_val, X_train = X_full[:100], X_full[100:]
        y_val, y_train = y_full[:100], y_full[100:]
        
        # Implement our originally thought of and created scalling strategy
        self.unstandardScaler.fit(X_train[self.scale_features])

        # THIS WAS NOT WORTH IT, HOLY SHIT IMPLEMENTING MY OWN SCALING WAS A NIGHTMARE
        X_train.loc[:, self.scale_features] = self.unstandardScaler.transform(X_train[self.scale_features])
        X_val.loc[:, self.scale_features] = self.unstandardScaler.transform(X_val[self.scale_features])
        X_test.loc[:, self.scale_features] = self.unstandardScaler.transform(X_test[self.scale_features])
                

        return X_train, X_test, X_val, y_train, y_test, y_val

    
    def simulation_data(self, simulations: int = 10):
        """
        Used to run a simulation of the market if i choose to implement it...
        """
        # Filter which features we want minus the target vals [1:]
        sim_data = self.market_data[-simulations:].filter(self.selected_features[1:])

        sim_data[self.scale_features] = self.unstandardScaler.transform(sim_data[self.scale_features])
        return sim_data


    def get_latest_values(self):

        # self.selected_features[1:] cuts the target labels out of the filtered vals
        latest_vals = self.market_data[-1:].filter(self.selected_features[1:])
        latest_vals[self.scale_features] = self.unstandardScaler.transform(latest_vals[self.scale_features])
        return latest_vals

    def process_all_features(self) -> None:
        """
        Applied all features and database maniuplations at once
        """

        self.create_target_labels()
        self.process_dates()
        #        self.process_time()  # Currently breaks the nn when used as a feature.:
        self.calc_daily_change()
        self.calc_volitility()
        self.calc_volume()
        self.moving_average()
        self.encode_features()


if __name__ == "__main__":
    # feat = DataFeatures("./BTCUSDT_1_Data.csv")
    # feat.process_all_features()
    # print(feat)
    pass
