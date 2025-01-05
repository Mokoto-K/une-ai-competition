# TODO - Implement everything from the cli, add a menu to check for different
# things like the trade you are in, profit?, etc
# TODO - Write the database to retrieve and update market info
# TODO - Build the NN.... no packages around here kids!
# TODO - Create separate module for features, potential different risk strategies
# TODO - Build the api to the exchange
# TODO - Hide keys, also provide example api-key implementation?
# TODO - Cli logic
# TODO - indocrinate the impure to nvim

# I think it takes some kinda base structure as this, maybe split it up into 
# diff modules/classes as needed or when it makes sense.

import data

def get_data():
    pass


def neural_net():
    get_data()
    pass


def get_position():
    pass


def take_action(position, decision):
    if not None:
        if position == decision:
            # maintain
            pass
        else:
            # close_position() 
            pass

def main():
    decision = neural_net()
    position = get_position()

    take_action(decision, position)


if __name__ == "__main__":
    main()
