   # -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 18:10:53 2022

@author: lovaa
"""

## need to get in the habit of commenting pretty much everything that i do 
## 
## poker 

## notice here that the aces and face cards have been assigned numbers 
## king is 13, queen is 12 

## in general i think it would be more clear to have 11 == J and 12 = Q and 13= K and then 1 = A 

import random 

suits = ['C','D','H','S']
ranks = [1,2,3,4,5,6,7,8,9,10,11,12,13]
deck = [[rank,suit] for suit in suits for rank in ranks]

card_sorting_key = {str(rank) + suit:0 for rank in ranks for suit in suits}
### it makes more sense for cards to be string objects because lists are not hashable,
### (drawbacks of strings used to denote cards)

for key in card_sorting_key:
    print(key)
    rank = 0
    digit = 0 
    for i in key:
        if i.isdigit() == True :
            digit += 1 
    if digit == 1: 
        index = int(key[0])*4 - 4
        
    else:
        index = int(key[0:2])*4 - 4
    if key[digit] == 'C':
        index += 0
    elif key[digit] == 'D':
        index += 1
    elif key[digit] == 'H':
        index += 2
    else:
        index += 3
    card_sorting_key[key] = index

poker_hands = ['High Card','One Pair','Two Pair','Three of a Kind','Straight','Flush','Full House','Four of a Kind','Straight Flush']
poker_hand_dict = {poker_hand:index for index,poker_hand in enumerate(poker_hands)}
poker_hand_with_card = [[poker_hand,rank] for poker_hand in poker_hands for rank in ranks]
poker_hand_with_card_num = [[poker_hand_dict[poker_hand],rank] for poker_hand in poker_hands for rank in ranks]

def poker_hand_val(X):
    for i in X:
        if X[1] < 10:
            return X[0] + X[1]/100
        else: 
            mod = X[1] % 10 
            return round(X[0] + .1 + mod/100,3)
## not sure what this is for yet         
poker_hand_with_card_dict = {poker_hand_val(poker_hand):0 for poker_hand in poker_hand_with_card_num}
        
## create a program that shuffles the deck 

def shuffler(X):
    random.shuffle(X)
    return X 


def deal_five(X): 
    ''' deal  five cards from the top of deck which would be the high 
        end of the index for conventions sake 
    '''
    deal = []
    for i in range(len(X)-5,len(X)):
        if len(X) >= 5:
            deal.append(X.pop())
        else:
            print("only 4 cards left in deck")
            deal = []
    return deal

def deal_five2(deck):
    deal = []
    for i in range(5):
        deal.append(deck.pop())
    return deal, deck 

        

def deal_n(X,N):
    ''' deals N many cards unless there is less than N many cards in the deck)
    '''
    deal = []
    for i in range(len(X)-N,len(X)):
        if len(X) >= N:
            deal.append(X.pop())
        else:
            print("only 4 cards left in deck")
            deal = []
    return deal
        
#♥♦♣♠
def symbolic_suits(X):
    for i in range(len(X)):
        if X[i][1] == 'S':
            X[i][1] = '♠'
        if X[i][1] == 'C':
            X[i][1] = '♣'
        if X[i][1] == 'H':
            X[i][1] = '♥'    
        if X[i][1] == 'D':
            X[i][1] = '♦'
        '''if X[i][1] == 13:
            X[i][1] = 'King'
        if X[i][1] == 12:
            X[i][1] = 'Queen'
        if X[i][1] == 11:
            X[i][1] = 'Jack'''    
    return X

def max_len_hand(hands):
    return max([len(hand) for hand in hands])

def as_strings(cards, onetwo = 1):
    new_deck = []
    string_deck = ''
    for card in cards: 
        delimeter = ''
        new_deck.append(str(card[0]) + card[1])
    if onetwo == 1:
        return new_deck
    else:
        delimeter = ''
        string_deck = delimeter.join(new_deck)
        return string_deck
        

def card_sort(hand):
    hand = as_strings(hand)
    return sorted(hand, key = lambda carded: card_sorting_key[carded])


def flush_finder(hand,search_len = 5):
    suit_dict = {card[1]:0 for card in hand}
    flushes = [] 
    for card in hand:
        suit_dict[card[1]] += 1 
    ''''print(suit_dict)'''
    for key in suit_dict:
        if suit_dict[key] >= search_len:
            flush = [card for card in hand if card[1] == key] 
            flushes.append(flush)
            max_rank_card = max_rank_card = max([card[0] for card in flush])
            hand_val = poker_hand_val([5,max_rank_card])
    if len(flushes) != 0:
        return flushes[0],hand_val 
    else:
        return None 







hand2 = [[4, 'C'],
 [9, 'D'],
 [5, 'C'],
 [8, 'C'],
 [10, 'C'],
 [4, 'H'],
 [4, 'D'],
 [7, 'D'],
 [6, 'H'],
 [5, 'H']]

'''
hand2 = as_strings(hand2)
print(sorted(hand2,key = lambda carded: card_sorting_key[carded] ))

print(flush_finder(hand2)) 
'''    
    
def straightflush_finder(hand):
    if flush_finder(hand) != None and straight_finder(hand) != None:
        max_card = max([card[0] for card in hand])
        hand_val = poker_hand_val([8,max_card])
        return hand,hand_val 

def pair_finder(hand):
    rank_dict = {card[0]:0 for card in hand}
    suit_dict = {card[1]:0 for card in hand}
    pairs = [] ## realy pairs or more  
    flushes = []
    fullhouse = [] 
    straight = []
    for card in hand:
        rank_dict[card[0]] += 1 
        suit_dict[card[1]] += 1 
    for key in rank_dict:
        if rank_dict[key] >= 2:
            pair = [card for card in hand if card[0] == key] 
            pairs.append(pair)
    num_pairs = len(pairs)
    if num_pairs != 0:    
        max_pair_len = max([len(pair) for pair in pairs])
        for pair in pairs:
            if len(pair) == max_pair_len:
                max_len_pair = pair 
        if len(pairs) == 2 and len(pairs[0]) == len(pairs[1]):
            max_rank = max([pair[0][0] for pair in pairs])
            hand_val = poker_hand_val([2,max_rank])
            pairs = pairs[0] + pairs[1]
        elif len(pairs) == 1 :
            if max_pair_len == 4:
                hand_val = poker_hand_val([7,pairs[0][0][0]])
                pairs = pairs[0]
            elif max_pair_len == 2:
                hand_val = poker_hand_val([1,pairs[0][0][0]])
                pairs = pairs[0]
            else:
                hand_val = poker_hand_val([max_pair_len,pairs[0][0][0]])
                pairs = pairs[0]
        else:
            hand_val = poker_hand_val([6,max_len_pair[0][0]])
            pairs = pairs[0] + pairs[1]
        return pairs,hand_val
    else:
        return None 
                                   
print(pair_finder([[8, 'C'], [8, 'C'], [8, 'S'], [6, 'H'], [6, 'H']]))
        
'''
    for key in suit_dict:
        if suit_dict[key] >= 3:
            flush = [card for card in hand if card[1] == key] 
            flushes.append(flush)
            print(flushes)
            dead = []
            for index,pair in enumerate(pairs):
                for card in pair:
                    if card in flush:
                        print(card)
                        dead.append(pairs[index])
            for death in dead:
                pairs.remove(death)
            print(dead)
    '''
'''
print(pair_finder([[10, 'C'], [10, 'C'], [8, 'S'], [12, 'H'], [12, 'H']]))
print(len(pair_finder([[13, 'C'], [13, 'C'], [12, 'S'], [12, 'H'], [12, 'H']])))
'''

def straight_finder(hand,search_len = 5):
    rank_dict = {card[0]:0 for card in hand}
    rank_with_card = {card[0]:card for card in hand}
    straights = []
    for card in hand:
        straight_count_plus = 1
        straight_count_below = 1
        straight = [card]
        while True:
            try:
                if card[0]+straight_count_plus in rank_dict:
                    straight.append(rank_with_card[card[0]+straight_count_plus])
                    straight_count_plus += 1
                else:
                    break
            except:
                break
        while True:
            try:
                if card[0]-straight_count_below in rank_dict:
                    straight.append(rank_with_card[card[0]-straight_count_below])
                    straight_count_below += 1 
                else:
                    break
            except:
                break 
        if straight_count_plus+straight_count_below-1 >= search_len:
            straights.append(straight)
            max_rank_card = max([card[0] for card in straight])
            hand_val = poker_hand_val([4,max_rank_card])
    for straight in straights: 
        if len(straight) == max_len_hand(straight):
            straights.remove(straight)
    if len(straights) != 0:
        return straights[0],hand_val
    else: 
        return None 

        #straights.append(straight_count_plus + straight_count_below-1)
    #if max(straights) >= 5 :
        #return True
    #else:
        #return False 

print(straight_finder([[8, 'C'], [9, 'C'], [7, 'S'], [6, 'H'], [10, 'H']]))
        

def best_hand(hand):
    max_card_rank = max([card[0] for card in hand])
    max_card = [card for card in hand if max_card_rank == card[0]]
    hand_val = poker_hand_val([0,max_card_rank])
    hands = [(max_card,hand_val),pair_finder(hand),flush_finder(hand),straight_finder(hand),straightflush_finder(hand)]
    top_hand = hands[0]
    for indx,hand in enumerate(hands):
        if hand != None and hand[1] > hand_val:
            hand_val = hand[1]
            top_hand = hand
    return top_hand 

print(best_hand([[8, 'C'], [8, 'C'], [8, 'C'], [6, 'H'], [6, 'C']]))       
        
       
'''
deck1 = {13: 1, 12: 1, 11: 1, 10: 1, 9: 1}
print(deck1.values())
'''

'''    
def pair_finder(X):
    #function takes a hand of cards and identifies all pairs
    
    pairs = []
    for i in range(len(X)-1):
        iter = 0
        pairs = []
        while X[i][1] != X[iter+1][1] :
            iter = iter + 1
            if iter+i > len(X):
                break
        if iter != 0:
            pairs.append([i,i+iter])
    print(pairs)

pair_finder(deal1)
'''

class Cards(object):
    
    
    def __init__(self,cards):
        self.data = cards
    
    def shuffler(X):
        random.shuffle(X)
        return X 
        
    def shuffle(self):
        shuffle = shuffler(self.data)
        self.data = shuffle 
        
    def display(self):
        print(self.data)
        
    def suit_symbol(self):
        for i in range(len(self.data)):
            if self.data[i][1] == 'S':
                self.data[i][1] = '♠'
            if self.data[i][1] == 'C':
                self.data[i][1] = '♣'
            if self.data[i][1] == 'H':
                self.data[i][1] = '♥'    
            if self.data[i][1] == 'D':
                self.data[i][1] = '♦'
    def deal(self,n):
        deal = []
        for i in range(n):
            deal.append(self.data.pop())
        return deal 
    
class Card(Cards):
    def __init__(self, card):
        self.data = card 
        if len(card) != 2 :
            print("not a valid card object")
        self.rank = card[0]
        self.suit = card[1]
        
    

print(as_strings(hand2,2))
    


hand1 = Cards([[1,'D'],[2,'H']])


### probably makes it more clear for the class not to have __init__ 

class Cards2():
    def setcards(self,cards):
        self.data = cards 
    def display(self):
        print(self.data)

hand3 = [[4, 'C'],
 [12, 'D'],
 [5, 'C'],
 [8, 'C'],[4, 'C'],
  [9, 'D'],
  [5, 'C'],
  [8, 'C'],
  [4, 'C'],
   [9, 'D'],
   [5, 'C'],
   [8, 'C'],[4, 'C'],
    [9, 'D'],
    [5, 'C'],
    [8, 'C']]

'''or i could try printing multiline strings next to eachother '''        

print(" __  "*len(hand3))
for index,card in enumerate(hand3):
    if index == len(hand3)-1:
        print(f"|{card[0]:<2}|  ")
    else:
        print(f"|{card[0]:<2}| ",end = '')

for index,card in enumerate(hand3):
    if index == len(hand3)-1:
        print(f"|{card[1]:>2}| ")
    else:
        print(f"|{card[1]:>2}| ",end = '')
print("|__| "*len(hand3))

def print_hand(hand):
    print(" __  "*len(hand))
    for index,card in enumerate(hand):
        if index == len(hand)-1:
            print(f"|{card[0]:<2}|")
        else:
            print(f"|{card[0]:<2}| ",end = '')

    for index,card in enumerate(hand):
        if index == len(hand)-1:
            print(f"|{card[1]:>2}| ")
        else:
            print(f"|{card[1]:>2}| ",end = '')
    print("|__| "*len(hand))    

def string_to_listform(cards):
    list_form = []
    for card in cards :
        digits = 0 
        for char in card:
            if char.isdigit() == True:
                digits += 1
        list_form.append([int(card[0:digits]),card[-1]])
    return list_form 

def five_card_draw(num_players):
    suits = ['C','D','H','S']
    ranks = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    deck = [[rank,suit] for suit in suits for rank in ranks]
    deals = []
    deck = Cards(deck)
    deck.shuffle()
    '''deck.suit_symbol()'''
    for i in range(num_players):
        hand = deck.deal(5)
        hand = card_sort(hand)
        hand = string_to_listform(hand)
        hand = Cards(hand)
        hand.suit_symbol()
        hand = hand.data
        
        deals.append(hand)
    for index,player in enumerate(deals):
        print(f"Player {index+1}:")
        print_hand(player)
    top_hands = [best_hand(hand) for hand in deals]
    top_top_hand = top_hands[0][1]
    print(top_top_hand)
    for indx,top_hand in enumerate(top_hands):
        if top_hand[1] >= top_top_hand:
            top_top_hand = top_hand[1]
            top_player = indx + 1
    print(f"Player {top_player} has the best hand")
    ''''print_hand(top_hands[top_player-1][0])'''
    return top_hands
        
def discard_strat(hand):
    discard = []
    hand1 = hand
    hand = card_sort(hand)
    '''print(hand1)'''
    try:
        if len(straight_finder(hand1,4)[0]) == 4:
            for card in hand:
                if card not in as_strings(straight_finder(hand1,4)[0]):
                    discard.append(card)
                    '''print('something')'''
                    break
    except: 
        try:
            if len(flush_finder(hand1,4)[0]) == 4:
                for card in hand:
                    if card not in as_strings(flush_finder(hand1,4)[0]):
                        '''print(card)'''
                        discard.append(card)
                        break
        except:
            if best_hand(hand1)[1] <= 3.5 and len(discard) == 0:
                iter_count = 0
                for card in hand:
                    if card not in as_strings(best_hand(hand1)[0]):
                        discard.append(card)
                    if len(discard) == 3:
                        break
    return discard 

def five_card_draw2(num_players):
    suits = ['C','D','H','S']
    ranks = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    deck = [[rank,suit] for suit in suits for rank in ranks]
    deals = []
    deck = Cards(deck)
    deck.shuffle()
    '''deck.suit_symbol()'''
    for i in range(num_players):
        hand = deck.deal(5)
        hand = card_sort(hand)
        hand = string_to_listform(hand)
        hand = Cards(hand)
        #hand.suit_symbol()
        hand = hand.data
        
        deals.append(hand)
    new_deals = []
    for indx,hand in enumerate(deals):
        discard = string_to_listform(discard_strat(hand))
        new_hand = []
        print(discard)
        for card in hand:
            print(card)
            if card in discard:
                print('something')
                new_hand.append(deck.deal(1)[0])
            else:
                new_hand.append(card)
        new_deals.append(new_hand)
    for indx,player in enumerate(deals):
        print(f"Player {indx+1}:")
        print_hand(player)
        print('')
        print(f"draws {len(discard_strat(player))}")
        print_hand(new_deals[indx])
        print('-'*40)
    deals = new_deals
    top_hands = [best_hand(hand) for hand in deals]
    top_top_hand = top_hands[0][1]
    print(top_top_hand)
    for indx,top_hand in enumerate(top_hands):
        if top_hand[1] >= top_top_hand:
            top_top_hand = top_hand[1]
            top_player = indx + 1
    print(f"Player {top_player} has the best hand")
    ''''print_hand(top_hands[top_player-1][0])'''
    return top_hands
 


## cool application of card printing
## the card printing program should be able to print any number of cards 
