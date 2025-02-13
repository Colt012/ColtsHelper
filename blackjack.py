import random

card_type_str = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
card_suit_str = ['heart', 'club', 'spade', 'diamond']

def pick_a_card(existing_cards):

    while True:
        card_type = random.choice(card_type_str)
        card_suit = random.choice(card_suit_str)

        #assign a value to the cards 10 for face cards, 11 for ace
        if card_type == 'ace':
            card_value = 11
        elif card_type in ['jack', 'queen', 'king']:
            card_value = 10
        else: 
            card_value = int(card_type)

        new_card = (card_type, card_suit, card_value) #assigns all 3 needed values to new_card 

        if new_card not in existing_cards: #check to see if the new card has been drawn before
            return new_card #if it is new, unique card, return the 3 values assigned
            

def dealer_hand():
    dealer_cards = [] #list the cards the dealer has in hand

    #initial 2 card draw
    dealer_cards.append(pick_a_card(dealer_cards))
    dealer_cards.append(pick_a_card(dealer_cards))

    #check for blackjack - end the game
    total_score = sum(card[2] for card in dealer_cards)
    if total_score == 21:
        print('Dealer has blackjack!')
        return
    
    #draw new cards until the dealer is over 15
    while total_score < 15:
        potential_card = pick_a_card(dealer_cards)
        potential_score = total_score + potential_card[2]

        if potential_score > 22 and total_score > 15:
            break

        dealer_cards.append(potential_card)
        total_score = sum(card[2] for card in dealer_cards)

    print("\nDealer's final hand:")
    for card in dealer_cards:
        print(f"  {card[0].capitalize()} of {card[1].capitalize()}s")

    if total_score > 21:
        print(f'\nDealer busts ({total_score})\n')
    else:
        print(f"\nDealer's final score: {total_score}\n")


dealer_hand()