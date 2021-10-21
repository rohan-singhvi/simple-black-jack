import random
import tkinter


def load_images(card_images):
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']
    if tkinter.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'
# for each suit, retrieve card image
    for suit in suits:
        for card in range(1, 11):
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))

        # now its the face cards
        for card in face_cards:
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image,))


def deal_cards(frame):
    # pop the next card from the top of the deck
    next_card = deck.pop(0)
    # pop takes an item from a list and removes it from the list - ensuring no duplicates
    # Add the image to a label and display the label
    tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
    # return the cards face value
    return next_card


def score_hand(hand):
    # calculate the total score of all cards in the list
    # only one ace can have the value 11, and it will go down to one if the hand is bust
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def deal_dealer():
    dealer_score = score_hand(dealer_hand)
    while 0 < dealer_score < 17:
        dealer_hand.append(deal_cards(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set("Dealer Wins!")
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player wins!")
    elif dealer_score > player_score:
        result_text.set("Dealer Wins!")
    else:
        result_text.set("Draw!")


def deal_player():
    player_hand.append(deal_cards(player_card_frame))
    player_score = score_hand(player_hand)

    player_score_label.set(player_score)
    if player_score > 21:
        result_text.set("Dealer Wins!")

    # global player_score
    # global player_ace
    # card_value = deal_cards(player_card_frame)[0]
    # if card_value == 1 and not player_ace: # IF the player gets a one and does not have an ace then ace becomes 11
    #     player_ace = True
    #     card_value = 11
    # player_score += card_value
    # # Check to see if its bust with an ace as an 11 and subtract 10 to treat ace as a 1
    # if player_score > 21 and player_ace:
    #     player_score -= 10
    #     player_ace = False
    # player_score_label.set(player_score)
    # if player_score > 21:
    #     result_text.set("Dealer Wins")


def initial_deal():
    deal_player()
    dealer_hand.append(deal_cards(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()


def reset_game():
    global dealer_card_frame
    global player_card_frame
    global player_hand
    global dealer_hand
    global cards
    global deck
    # embedded frame to hold the card images
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)
    # embedded frame to hold the card images
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background='green')
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    result_text.set('')
    cards = []
    load_images(cards)

    # Create a new deck of cards and shuffle them
    deck = list(cards)
    # must use list as seen above, otherwise as new games and cards are being dealt the old ones are 'destroyed'
    random.shuffle(deck)
    dealer_hand = []
    player_hand = []

    initial_deal()


def reshuffle():
    random.shuffle(deck)


def play():
    initial_deal()

    main_window.mainloop()


main_window = tkinter.Tk()
main_window.title("Black Jack")
main_window.geometry("640x480")
main_window.configure(background='green')

# setup of the game
result_text = tkinter.StringVar()
result = tkinter.Label(main_window, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

card_frame = tkinter.Frame(main_window, relief='sunken', borderwidth=1, background='green')
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)


# Dealer
dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Dealer", background='green', fg='white').grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background='green', fg='White').grid(row=1, column=0)

# embedded frame to hold card images
dealer_card_frame = tkinter.Frame(card_frame, background='green')
dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)


# Player
player_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Player", background='green', fg='white').grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background='green', fg='White').grid(row=3, column=0)

# text variable used because we are getting the value from a variable
player_card_frame = tkinter.Frame(card_frame, background='green')
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)


# Buttons
button_frame = tkinter.Frame(main_window)
button_frame.grid(row=3, column=0, sticky='w')

# dealer button
dealer_button = tkinter.Button(button_frame, text='Dealer', command=deal_dealer)
dealer_button.grid(row=0, column=0)

# player button
player_button = tkinter.Button(button_frame, text='Player', command=deal_player)
player_button.grid(row=0, column=1)
# Restart button
restart_button = tkinter.Button(button_frame, text="New Game", command=reset_game)
restart_button.grid(row=0, column=2)
#  Shuffle button
shuffle_button = tkinter.Button(button_frame, text="Shuffle", command=reshuffle)
shuffle_button.grid(row=0, column=3)
# Load cards
cards = []
load_images(cards)

# Create a new deck of cards and shuffle them
deck = list(cards)
# must use list as seen above, otherwise as new games and cards are being dealt the old ones are 'destroyed'
reshuffle()
# The list created to store the players and the dealers hands
dealer_hand = []
player_hand = []

if __name__ == "__main__":
    play()
