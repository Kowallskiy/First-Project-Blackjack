import random

HANDS = 2
# all_cards variable indicates that we have 5 decks in the game
all_cards = {
    'A': 20,
    'K': 20,
    'Q': 20,
    'J': 20,
    '10': 20,
    '9': 20,
    '8': 20,
    '7': 20,
    '6': 20,
    '5': 20,
    '4': 20,
    '3': 20,
    '2': 20
}
# cards_value helps us to calculate scores of a player and a dealer
cards_value = {
    'A': 11,
    'K': 10,
    'Q': 10,
    'J': 10,
    '10': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2
}


# The deposit function receives how much a player wants to deposit
def deposit():
    while True:
        balance = input('How much money would you like to deposit? $')
        if balance.isdigit() and balance != '0':
            break
        else:
            print('Please, enter a positive number')
    return int(balance)


# get_bet receives how much a player wants to bet
def get_bet():
    while True:
        bet = input('How much would you like to bet on your hand? $')
        if bet.isdigit() and bet != '0' and bet != '':
            print(f'Your bet is ${bet}')
            break
        else:
            print('Enter a positive number')

    return int(bet)


# This function generates random combinations
# The name of the function does not mean what is says
def removes_value_from_combinations(HANDS, amount_of_cards):
    # Amount of hands is player's random combination
    amount_of_hands = []
    # Dealer's amount of hands is dealer's random combination
    dealers_amount_of_hands = []
    # The idea was to make a copy of all cards and remove received by
    # player and dealer cards from the deck
    current_hands = amount_of_cards[:]
    for hand in range(HANDS):
        value = random.choice(current_hands)
        current_hands.remove(value)
        amount_of_hands.append(value)

        value_d = random.choice(current_hands)
        current_hands.remove(value_d)
        dealers_amount_of_hands.append(value_d)

    return amount_of_hands, dealers_amount_of_hands


# I divided the function because I wanted to remove value separately from getting cards combination
# It did not work out. But the code looks fancier
def get_cards_combination(HANDS, all_cards):
    amount_of_cards = []
    for card, card_count in all_cards.items():
        for _ in range(card_count):
            amount_of_cards.append(card)
    removes_value_from_combinations(HANDS, amount_of_cards)

    return removes_value_from_combinations(HANDS, amount_of_cards)


# print_hands simply prints what combination a player and a dealer have.
# I print only the first element because amount_of_hands and dealers_amount_of_hands
# give us two combinations each. That is a serious problem
def print_hands(amount_of_hands, dealers_amount_of_hands):
    print(f'Your hand is: {amount_of_hands[0]}')
    print(f"Dealer's hand is: {dealers_amount_of_hands[0][0]} |X|")

# ace_value_player calculates whether "Ace" should be 11 or 1
def ace_value_player(players_score, new_value):
    if 'A' in new_value and players_score + 11 < 22:
        players_score += 11
    elif 'A' in new_value and players_score + 11 >= 22:
        players_score += 1

    return players_score


def ace_value_dealer(dealers_score, new_dealers_value):
    if 'A' in new_dealers_value and dealers_score + 11 < 22:
        dealers_score += 11
    elif 'A' in new_dealers_value and dealers_score + 11 >= 22:
        dealers_score += 1

    return dealers_score


# The main action is in this function
def game(balance):
    # we receive player's bet from get_bet function
    while True:
        bet = get_bet()
        total_bet = bet
        lost = - total_bet

        if total_bet > balance:
            print(f'You do not have enough money to bet. Your current balance is ${balance}')
        else:
            break
    # we receive combinations of a player and a dealer and print them
    combination = get_cards_combination(HANDS, all_cards)
    dealer_combination = get_cards_combination(HANDS, all_cards)
    print_hands(combination, dealer_combination)

    # Calculate dealer's and player's scores
    players_score = 0
    dealers_score = 0
    for i in combination[0]:
        players_score += cards_value.get(i)
    for a in dealer_combination[0]:
        dealers_score += cards_value.get(a)

    # I did not want to print combinations as arrays and created strings
    string_combination = ''
    dealers_string_combination = ''
    for a in dealer_combination[0]:
        dealers_string_combination += a + ' '
    for i in combination[0]:
        string_combination += i + ' '
    while True:
        answer = input('Press enter to take one more card (q to quit) ')
        if answer != 'q':
            new_value = random.choice(list(cards_value.keys()))
            string_combination += new_value + ' '
            print(f"You received {new_value}. Your current combination is {string_combination}")

            # This is where I checked whether a player received an "A"
            # The problem is if the player received an "A" in the beginning of the game
            # that ace "A" will always be 11
            if 'A' in new_value:
                ace_value_player(players_score, new_value)
            else:
                players_score += cards_value.get(new_value)
            if players_score > 21:
                print(f'You lost your bet. Your score is {players_score}')
                return lost
            else:
                continue

        # This part of code is similar to that one of the player
        elif answer == 'q':
            while dealers_score < 17 or dealers_score < players_score:
                new_dealers_value = random.choice(list(cards_value.keys()))
                dealers_string_combination += new_dealers_value + ' '
                print(f"Dealer's current combination is {dealers_string_combination}")
                if 'A' in new_dealers_value:
                    ace_value_dealer(dealers_score, new_dealers_value)
                else:
                    dealers_score += cards_value.get(new_dealers_value)

            if players_score > dealers_score or dealers_score > 21:
                print(f'You won! Your score is {players_score}. Dealers score is {dealers_score}')
                return total_bet
            elif players_score == dealers_score:
                print(f'It is a draw. Your score is {players_score}. Dealers score is {dealers_score}')
                return 0
            else:
                print(f'You lost! Your score is {players_score}. Dealers score is {dealers_score}')
                return lost
        break


def main():
    balance = deposit()
    while True:
        balance += game(balance)
        print(f"Your balance is {balance}")
        answer = input('Press enter if you want to keep playing (q to quit) ')
        if answer == 'q':
            print(f"You left with ${balance}")
            break


main()
