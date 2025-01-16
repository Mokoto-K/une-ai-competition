task_map = {"question" : "Please select a task: \n" +
        "Press 's' to run a simulation on the market \n" + 
        "Press 'r' to run a real trade in the market \n\n" + ">> ",
                "answers": {"s": True, "r": False}}

risk_map = {"question": "\nEnter the risk strategy you would like to take:\n" +
        "Press 'h' for high risk\n" + 
        "Press 'l' for low risk\n\n" + ">> ", 
                "answers": {"h": "1 - High risk", "l": "D - Low risk"}}

command_map = {"question": "What would you like to do?\n" + 
        "Press r to Refresh Current or Enter a trade\n" + 
        "Press c to Change strategy\n" + 
        "Press a to Automate trading\n" + 
        "Press f to Force close the current trade\n" + 
        "Press e to Exit\n\n" + ">> ",
                   "answers": {"c": change_strategy, 
                               "e": exit_program}}


