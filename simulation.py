# TODO - Turn this into a readable file instead of a reflection of your brain.... 
# TODO - Pull everything into methods so its not so busy in that loop
from strategy import build_strategy 
from time import sleep

def run_simulation(strategy):
    # Neural network
    nn, data = strategy 

    SIMULATIONS = 500
    sim_data =  data.simulation_data(SIMULATIONS) 
    
    # Market open and closes
    price_opens = data.price_open[-SIMULATIONS:]
    price_dates = data.dates[-SIMULATIONS:] 

    # Account details
    ACCT_START = ACCT_SIZE = 100000
    RISK, POS, SIZE = 0.5, "none", 0
    
    ACCT_MAX, ACCT_LOW = 0, ACCT_START 
    
    predictions = nn.predict(sim_data)
    
    # I too would throw up if i saw this ungodly for loop... 
    print("----------------STARTING UP SIMULATION-------------------")
    for i in range(len(predictions)):
    
        # Used for calculating profits and losses and printing the date
        price_open, price_date = price_opens.iloc[i], price_dates.iloc[i]

        trade_pnl = "-"    
        decision = "long" if predictions[i] > 0.5 else "short"

        print(f"{'-'*55}\nDecision {i + 1}/{SIMULATIONS}\nDate: {price_date}")
        print(f"Account opening bal: ${round(ACCT_SIZE, 2):,.2f}")
        
        c_pos = "Long" if POS == "long" else "Short" if POS == "short" else "None"
        print(f"Current Position: {c_pos}") 

        if POS != "none":
            if POS == decision:
                # Doing literally nothing
                print(f"Decision: Remain {c_pos}")
            else:
                # Closing trade
                print(f"Decision: Closing {POS} @ ${price_open:,.2f}") 
                POS = "none"
                # Adjusts account with profit/loss and calcs visuals
                old_act_size = ACCT_SIZE
                dollar_diff = price_open * RISK - SIZE
                ACCT_SIZE += dollar_diff 
                percent_pnl = (ACCT_SIZE - old_act_size) / old_act_size * 100
                trade_pnl = f"${round(dollar_diff,2 ):,.2f} ({round(percent_pnl, 2)}%)"
        else:
            # Opening a new position
            print(f"Decision: Opening a {decision} @ ${price_open:,.2f}")
            POS = decision

            # TODO - Recalculate size correctly, for now this will do
            SIZE = price_open * RISK
    
        # Print the current bal of account and the pnl for the last trade
        print(f"Account Closing Bal: ${round(ACCT_SIZE, 2):,.2f}") 
        print(f"Trade Profit/Loss: {trade_pnl}")
       
        # Calculate and display the total dollar change and percent for account
        dpnl = ACCT_SIZE - ACCT_START
        ppnl = f"{round((dpnl) / ACCT_START * 100, 2)}%"
        print(f"Total Profit/Loss: ${dpnl:,.2f} ({ppnl})\n{'-'*55}")

        ACCT_MAX = ACCT_SIZE if ACCT_SIZE > ACCT_MAX else ACCT_MAX
        ACCT_LOW = ACCT_SIZE if ACCT_SIZE < ACCT_LOW else ACCT_LOW
        sleep(0.20)

    print(f"\nAccount reach a high of: {ACCT_MAX} and a low of: {ACCT_LOW}\n")
    print("Please note this is only a simulation to show a working product\n"+
          "Results shown here should not be taken seriously.\n")
if __name__ == "__main__":
    run_simulation(build_strategy("1")) 
