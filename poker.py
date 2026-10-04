import numbers
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 

possible_deck = []

for i in range(1, 53):
    possible_deck.append(i)


def enter_card(suite, number): # cards 1-13 are diamonds, 14-26 are hearts, 27-39 are spades and 40-52 are clubs
    n = number.strip().lower()
    s = suite.strip().lower()
    if n == 'king':
        n = 13
    elif n == 'ace':
        n = 1
    elif n == 'queen':
        n = 12
    elif n == 'jack':
        n = 11
    
    if s == 'diamonds':
        return(int(n))
    elif s == 'hearts':
        return(int(n) + 13)
    elif s == 'spades':
        return(int(n) + 26)
    elif s == 'clubs':
        return(int(n) + 39)


    # go through each number and find how many there are, then go through and check suits, then individually code flush, straight and royal flush




class hand:
    def __init__(self, card_1, card_2):
        self.card_1 = card_1
        self.card_2 = card_2
    def deck(self):
        possible_deck.remove(self.card_1)
        possible_deck.remove(self.card_2)
        return(possible_deck)
    def river(self, possible_deck):
        rng = np.random.default_rng()
        river = rng.choice(possible_deck, 5, replace = False)
        return(river)




def river_sim(c1, c2):
    sim = hand(c1, c2)
    p_d = sim.deck()
    return(sim.river(p_d))


card_enter_1 = enter_card(suite=input('What suite is your card\n'), number=input('What is the card? (enter number if given on card, else enter name of picture card)\n'))
card_enter_2 = enter_card(suite=input('What suite is your card\n'), number=input('What is the card? (enter number if given on card, else enter name of picture card)\n'))





river = (river_sim(card_enter_1, card_enter_2)) # returns a river 


def find_straight(nums):
    nums = sorted(set(nums))            # remove duplicates
    found = []
    for i in range(len(nums) - 4):
        w = nums[i:i + 5]
        if w[4] - w[0] == 4:            # 5 distinct sorted ints spanning 4 = consecutive
            found = w                   # keep going so we end on the highest straight
    return found


def hi(x): # flips aces to the end of the list for scoring purposes
    return 14 if x == 1 else x

def scorer(river, c1, c2):
    flush = False
    royal_flush = False
    straight_flush = False
    four_of_a_kind = False
    fours = 0
    fours_of_a_kind = []
    full_house = False
    flush = False
    straight = False
    three_of_a_kind = False
    threes_of_a_kind = []
    threes = 0
    pairs = []
    pair_s = 0
    two_pair = False
    one_pair = False
    
    scorable = []
    scorable = list(river)
    scorable.append(int(c1))
    scorable.append(int(c2))
    n_scoreable = []
    for i in scorable:
        i = int(i)
        if i <= 13:
            i = {'diamonds' : i}
        elif i <= 26:
            i = {'hearts': (i-1) % 13 + 1}
        elif i <= 39:
            i = {'spades': (i - 1) % 13 + 1}
        elif i <= 52:
            i = {'clubs' : (i - 1) % 13 + 1}
        else:
            print('What have you done???\n')
        n_scoreable.append(i)
    numbers = []
    for i in n_scoreable:
        numbers.append(list(i.values())[0])
        if list(i.values())[0] == 1:
            numbers.append(14)
    suites = []
    for i in n_scoreable:
        suites.append(list(i.keys())[0])
    highest_card = sorted(numbers)[-1]
    pairs  = []
    for i in range(1, 14):
        pair_count = 0
        for k in numbers:
            if i == k:
                pair_count += 1
        if pair_count >= 2:
            pairs.append({i : pair_count})
    flush_numbers = []                      # numbers of the cards in the flush suit
    for s in ['diamonds', 'hearts', 'spades', 'clubs']:
        if suites.count(s) >= 5:
            flush = True
            flush_numbers = [list(d.values())[0] for d in n_scoreable if list(d.keys())[0] == s]
            if 1 in flush_numbers:          # ace counts high as well as low
                flush_numbers.append(14)
    numbers.sort()
    stright_cards = find_straight(numbers)
    if stright_cards:
        straight = True

    flush_straight_cards = find_straight(flush_numbers)
    if flush_straight_cards:
        straight_flush = True
        if flush_straight_cards[0] == 10:
            royal_flush = True
    fours_of_a_kind  = [list(k)[0] for k in pairs if list(k.values())[0] == 4]
    threes_of_a_kind = [list(k)[0] for k in pairs if list(k.values())[0] == 3]
    real_pairs       = [list(k)[0] for k in pairs if list(k.values())[0] == 2]

    four_of_a_kind  = len(fours_of_a_kind) > 0
    three_of_a_kind = len(threes_of_a_kind) > 0
    two_pair  = len(real_pairs) >= 2
    one_pair  = len(real_pairs) == 1
    full_house = three_of_a_kind and (len(threes_of_a_kind) >= 2 or len(real_pairs) >= 1)
    score = 1
    if royal_flush:
        score = 10
    elif straight_flush:
        score = 9
    elif four_of_a_kind:
        score = 8
    elif full_house:
        score = 7
    elif flush:
        score = 6
    elif straight:
        score = 5
    elif three_of_a_kind:
        score = 4
    elif two_pair:
        score = 3
    elif one_pair:
        score = 2
    else:
        score = 1
    ranks = [x for x in numbers[::-1] if x != 1] # sorts the numbers in descending order, with aces at the end
    q = [hi(x) for x in fours_of_a_kind]
    t = sorted([hi(x) for x in threes_of_a_kind], reverse=True)
    p = sorted([hi(x) for x in real_pairs], reverse=True)
    if score == 9:
        order = [flush_straight_cards[-1]] #top card of the straight flush
    elif score == 8:
        order = [q[0]] + [[r for r in ranks if r != q[0]][:1]] #the four then best kicker
    elif score == 7:
        order = [t[0], max(t[1:] + p)] #    the three then the best pair
    elif score == 6:
        order = sorted({hi(x) for x in flush_numbers}, reverse=True)[:5] #the best five cards of the flush
    elif score == 5 and len(flush_straight_cards) > 0:
        order = [flush_straight_cards[-1]] #top card of the straight
    elif score == 4:
        order = [t[0]] + [r for r in ranks if r != t[0]][:2] #the three then the best two kickers
    elif score == 3:
        order = p[:2] + [r for r in ranks if r not in p[:2]][:1] #the two pairs then the best kicker
    elif score == 2:
        order = [p[0]] + [r for r in ranks if r != p[0]][:3] #the pair then the best three kickers
    elif score == 1:
        order = ranks[:5] #the best five cards
    else:
        order = ranks[:5]
    tiebreak = 0
    for f in order:
        tiebreak = tiebreak * 15 + int(f[0] if isinstance(f, list) else f)
    return({score : tiebreak})


rng = np.random.default_rng()
def run_sim(x):
    # Remove your cards, then deal a fresh board and two cards per opponent.
    deck = [card for card in possible_deck
            if card not in (card_enter_1, card_enter_2)]

    draw = rng.choice(deck, 5 + 2 * x, replace=False)
    board = draw[:5]

    my_score = next(iter(scorer(board, card_enter_1, card_enter_2).values()))

    opponent_scores = []
    for i in range(x):
        c1 = draw[5 + 2 * i]
        c2 = draw[6 + 2 * i]
        score = next(iter(scorer(board, c1, c2).values()))
        opponent_scores.append(score)

    best_opponent = max(opponent_scores)

    if my_score > best_opponent:
        return 2  # win
    elif my_score == best_opponent:
        return 0  # tie
    else:
        return 1  # loss



def simulate(x, n_sims):
    scores = []
    for k in range (1, x + 1):
        wins = 0
        i = 0
        while i < n_sims:
            i += 1
            result = run_sim(k)
            if result == 2:
                wins += 1
        scores.append([wins / n_sims])
    return(scores) # for each batch of simulations, returns the number of wins
    
# Run the simulation once for each opponent count
n_sims = int(input("How many simulations per opponent count? "))
max_opponents = int(input("Maximum number of opponents? "))

win_rates = simulate(max_opponents, n_sims)

n = range(1, max_opponents + 1)

plt.figure(figsize=(8, 5))
plt.plot(n, win_rates, marker="o")
plt.xlabel("Number of opponents (n)")
plt.ylabel("Win rate")
plt.title("Poker win rate vs number of opponents")
plt.xticks(n)
plt.ylim(0, 1)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()