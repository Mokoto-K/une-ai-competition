# TODO - add another log file and process that keeps track of all trades 
# TODO - I dont know if this should be a class or just a method... i dunno, ponder
# on it once everything is built and running
def write_log_file(strategy: str = "D - Low Risk", direction: str = "None", 
                   open_price: str = "None", c_pnl = "None", last_pnl: str = "None", 
                   total_pnl: str = "None", acct_size = "None", start_bal: str = "None"):
    
    log = (f"Current Strategy: {strategy}\nCurrent Position: {direction}\n"
            f"Open_price: {open_price}\nCurrent PNL: {c_pnl}\n"
            f"Last trade PNL: {last_pnl}\nTotal PNL: {total_pnl}\n"
            f"Account Bal: {acct_size}\nStarting Bal: {start_bal}")

    with open("user_log.txt", "w") as file:
        file.writelines(log)
         
            
def read_log_file():
    
    log_vars = []
         
    try:
        with open("user_log.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                log_vars.append(line.split(":")[1].strip(" ").strip("\n"))

        return log_vars
    except FileNotFoundError:
        print("Your user log file appears to have dissappeared, reopen the program to start again")
        exit(0)


# Needed to then print the logs..so much duplicate code to refactor
def print_log():
    vars = read_log_file()

    log = (f"Current Strategy: {vars[0]}\nCurrent Position: {vars[1]}\n"
           f"Open Price: {vars[2]}\nCurrent Profit/Loss: {vars[3]}\n\n"
           f"Last trade Profit/Loss: {vars[4]}\n\nTotal Profit/Loss: {vars[5]}\n"
        f"Account Bal: {vars[6]}\nStarting Bal: {vars[7]}\n")
            # f"Starting Bal: {vars[6]}")
    
    print(f"{'-'*45}\n{log}\n{'-'*45}\n")


# Painfully obvious this needs to be class, bandaids for the moment, big fixes coming!!!
def update_strategy_log(strategy):
    log = read_log_file()
    write_log_file(strategy, log[1], log[2], log[3], log[4], log[5], log[6], log[7])
