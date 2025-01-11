# TODO - I dont know if this should be a class or just a method... i dunno, ponder
# on it once everything is built and running
def write_log_file(strategy: str = "D - Low Risk", direction: str = "None", 
                   price: str = "None", acct_size: str = "None", last_pnl: str = "None", 
                   total_pnl: str = "None", start_bal: str = "None"):
    
    
    log = (f"Current Strategy: {strategy}\nCurrent Position: {direction}\n"
            f"Open_price: {price}\nAccount Balance: {acct_size}\n"
            f"Last trade PNL: {last_pnl}\nTotal PNL: {total_pnl}\n"
            f"Starting Bal: {start_bal}")
    
    with open("user_log.txt", "w") as file:
        file.writelines(log)
    
            
def read_log_file():
    
    log_vars = []
    
    with open("user_log.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            log_vars.append(line.split(":")[1].strip(" ").strip("\n"))

    return log_vars
   

# Needed to then print the logs..so much duplicate code to refactor
def print_log():
    vars = read_log_file()
    log = (f"Current Strategy: {vars[0]}\nCurrent Position: {vars[1]}\n"
            f"Open_price: {vars[2]}\nAccount Balance: {vars[3]}\n"
            f"Last trade PNL: {vars[4]}\nTotal PNL: {vars[5]}\n"
            f"Starting Bal: {vars[6]}")
    
    print(f"{'-'*55}\n{log}\n{'-'*55}\n")
