# TODO - Turn this into a presentable file.... 

from features import DataFeatures
from strategy import build_strategy 
from time import sleep

def run_simulation(risk):

    # Neural network
    nn, data = build_strategy(risk)

    SIMULATIONS = 1000
    sim_data =  data.simulation_data(SIMULATIONS) 
    
    # Market open and closes
    price_opens = data.price_open[-SIMULATIONS:]
    price_closes = data.price_close[-SIMULATIONS:]
    daily_change = sim_data["daily_change"]
    # Account details
    ACCOUNT_STARTED = 100000
    ACCOUNT_SIZE = 100000
    RISK = 0.5
    POSITION = "none" 
    OPENING_PRICE = 0 
    CLOSE_PRICE = 0
    SIZE = 0
    
    MAX_ACCOUNT_SIZE = 0 
    LOWEST_ACCOUNT_SIZE = ACCOUNT_SIZE
    
    predictions = nn.predict(sim_data)
    
    
    for i in range(len(predictions)):
    
        # Price related things
        price_open = price_opens.iloc[i]
        price_close = price_closes.iloc[i] 
        difference = price_close - price_open
    
        decision = "long" if predictions[i] > 0.5 else "short"
       
    
        print("-------------------------------------------------------")
        print(f"Day {i + 1}")
    
        if POSITION != "none":
            if POSITION == decision:
                print(f"We are {POSITION} and will remain {decision}")
            else:
                print(f"We are {POSITION} and closing our position @ {price_open}") 
                POSITION = "none"
                # Adjusts account with profit/loss
                ACCOUNT_SIZE += price_open * RISK - SIZE
                print(f"Profit/Loss: {price_open * RISK - SIZE}")
        else:
            print(f"We are opening a {decision} from {price_open}")
            POSITION = decision
            # TODO - Recalculate size correctly, for now this will do
            SIZE = price_open * RISK
    
        print(f"ACCOUNT_SIZE: {round(ACCOUNT_SIZE)}, Total Profit/Loss:\
            {round((ACCOUNT_SIZE - ACCOUNT_STARTED) / ACCOUNT_STARTED * 100, 2)}%")

        if ACCOUNT_SIZE > MAX_ACCOUNT_SIZE:
            MAX_ACCOUNT_SIZE = ACCOUNT_SIZE

        if ACCOUNT_SIZE < LOWEST_ACCOUNT_SIZE:
            LOWEST_ACCOUNT_SIZE = ACCOUNT_SIZE

    print(f"Account reach a high of: {MAX_ACCOUNT_SIZE} and a low of: {LOWEST_ACCOUNT_SIZE}")
        #sleep(1)


if __name__ == "__main__":
    run_simulation() 
