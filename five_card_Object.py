# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 22:28:08 2022

@author: lovaa
"""

''' object oriented and document version of my cards program ''' 

''' ||||| CLASSES ||||| '''
''' card object, hand object, and maybe a game object


with regard to the poker hand finding methods within the hand class 
what 
 ''' 

import random 


suits = ('♣','♦','♥','♠')
ranks = [1,2,3,4,5,6,7,8,9,10,11,12,13]
card_sorting_key = {str(rank) + suit:0 for rank in ranks for suit in suits}


for index,key in enumerate(card_sorting_key):
    card_sorting_key[key] = index

def max_len_hand(hands):
    return max([len(hand) for hand in hands])

def poker_hand_val(X):
    '''supposed to take in a list with two element, the first element is an integer 
    representing the first number in my poker hand ranking system, the 
    
    don't think the else statement is nessessary 
    
    '''
    for i in X:
        if X[1] < 10:
            return X[0] + X[1]/100
        else: 
            mod = X[1] % 10 
            return round(X[0] + .1 + mod/100,3)

def poker_hand_val2(X):
    '''supposed to take in a list with two element, the first element is an integer 
    representing the first number in my poker hand ranking system, the 
    
    don't think the else statement is nessessary 
    
    '''
    return X[0] + X[1]/100
    
    
    
class Deck:
    def __init__(self):
        self.suits = ('♠','♣','♥','♦')
        self.ranks = (1,2,3,4,5,6,7,8,9,10,11,12,13)
        self.deck = [[rank,suit] for suit in self.suits for rank in self.ranks]
    def shuffle(self):
        random.shuffle(self.deck)
    def deal(self,n):
        deal = []
        for i in range(n):
            deal.append(self.deck.pop())
        return deal 
    def deal_specific(self, hand):
        deal = []
        for card in hand:
            card_index = self.deck.index(card)
            deal.append(self.deck.pop(card_index))
        return deal

        
class Card:
    ''' not so sure that having cards as object will be helpfull it's probably 
    an unnessesarry abstraction '''
    def __init__(self,list_card):
        self.rank = list_card[0]
        self.suit = list_card[1]
        self.card = list_card
        self.card_str = str(self.rank) + str(self.suit)
        

class Hand:
    ''' functionality 
    - sort hands by rank and suit so they are displayed in a logical manner
    - detect all poker hands
    - determine the highest poker hand 
    - pretty print hand in the interpreter 
    '''
    def __init__(self,card_list,discard = True): 
        self.hand = card_list
        self.str = self.as_string()
        
        self.pairs = self.pair_finder()
        self.straight = self.straight_finder(5)
        self.flushes = self.flush_finder(5)
        self.straight_flush = self.straightflush_finder()
        self.rank_dict = {card[0]:0 for card in self.hand}
        self.best_hand = self.best_hand()  
        if discard == True:
            self.sort()
            self.discard = self.discard_strat() 
 
    def as_string(self):
        string_hand = []
        for card in self.hand:
            string_hand.append(str(card[0])+ card[1])
        return string_hand
    
    def str_to_list(self):
        ''' not so sure i need this functionality yet go back later 
            try doing it my way first then go from their'''
        list_hand = []
        for card in self.hand:
            digits = 0
            for char in card:
                if char.isdigit() == True :
                    digits += 1
            list_hand.append([int(card[0:digits]),card[-1]])
        self.hand = list_hand  
    
    def sort(self):
        sorted_hand = sorted(self.str, key = lambda carded: card_sorting_key[carded]) 
        list_hand = []
        for card in sorted_hand:
            digits = 0
            for char in card:
                if char.isdigit() == True :
                    digits += 1
            list_hand.append([int(card[0:digits]),card[-1]])
        self.hand = list_hand  
    
    def print_hand(self):
        ''' print the cards in the interpretter '''
        
        print(" __  "*len(self.hand))
        for index,card in enumerate(self.hand):
            if index == len(self.hand)-1:
                print(f"|{card[0]:<2}|")
            else:
                print(f"|{card[0]:<2}| ",end = '')

        for index,card in enumerate(self.hand):
            if index == len(self.hand)-1:
                print(f"|{card[1]:>2}| ")
            else:
                print(f"|{card[1]:>2}| ",end = '')
        print("|__| "*len(self.hand))   
    
    def straight_finder(self,search_len):
        
        '''nothing yet '''
                
        rank_dict = {card[0]:0 for card in self.hand}
        rank_with_card = {card[0]:card for card in self.hand}
        straights = []
        for card in self.hand:
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
                hand_val = 4 + max_rank_card/100 
        for straight in straights: 
            if len(straight) == max_len_hand(straight):
                straights.remove(straight)
        if len(straights) != 0:
            return straights[0],hand_val
        else: 
            return []
    
    def flush_finder(self,search_len = 5):
        suit_dict = {card[1]:0 for card in self.hand}
        flushes = [] 
        for card in self.hand:
            suit_dict[card[1]] += 1 
        ''''print(suit_dict)'''
        for key in suit_dict:
            if suit_dict[key] >= search_len:
                flush = [card for card in self.hand if card[1] == key] 
                flushes.append(flush)
                max_rank_card = max_rank_card = max([card[0] for card in flush])
                hand_val = poker_hand_val([5,max_rank_card])
        if len(flushes) != 0:
            return flushes[0],hand_val 
        else:
            return []
    def pair_finder(self):
        rank_dict = {card[0]:0 for card in self.hand}
        suit_dict = {card[1]:0 for card in self.hand}
        pairs = [] ## realy pairs or more  
        for card in self.hand:
            rank_dict[card[0]] += 1 
            suit_dict[card[1]] += 1 
        for key in rank_dict:
            if rank_dict[key] >= 2:
                pair = [card for card in self.hand if card[0] == key] 
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
            return [] 
    def best_hand(self):
        max_card_rank = max([card[0] for card in self.hand])
        max_card = [card for card in self.hand if max_card_rank == card[0]]
        hand_val = 0 + max_card_rank/100
        hands = [(max_card,hand_val),self.pairs,self.flushes,self.straight,self.straight_flush ]
        top_hand = hands[0]
        for indx,hand in enumerate(hands):
            if hand == []:
                None
            else:
                if hand[1] > hand_val:
                    hand_val = hand[1]
                    top_hand = hand
        return top_hand 
    
    def straightflush_finder(self):
        if self.flush_finder() != [] and self.straight_finder(5) != []:
            max_card = max([card[0] for card in self.hand])
            hand_val = 8 + max_card/100
            return self.hand, hand_val 
        else:
            return []
        
    def discard_strat(self,strategy = 1):
        
        
        
        def straight_discard():
            ## we dont want to draw for straight unless it's possible to finish the 
            ## straight by drawing a card on the low or high end of the staight. 
            if self.straight_finder(4) != []:
                discard = [] 
                if len(self.straight_finder(4)[0]) == 4 and 1 not in self.rank_dict and 13 not in self.rank_dict: 
                    for card in self.hand:
                        if card not in self.straight_finder(4)[0]:
                            discard.append(card)
                            return discard 
                        
                        
        def flush_discard():
            if self.flush_finder(4) != []: 
                discard = [] 
                if len(self.flush_finder(4)[0]) == 4:
                    for card in self.hand :
                        if card not in self.flush_finder(4)[0]:
                            discard.append(card)
                            return discard 
                        
        def pair_discard():
            discard = [] 
            if self.pair_finder() != []:
                for card in self.hand:
                    if card not in self.pairs[0] and len(discard) <= 3:
                        discard.append(card)
                return discard 
        
        def low_cards_discard():
            return self.hand[0:3]
        
        def three_card_meld_discard():
            ''' this strategy is meant to identify scenarios where you 
            have three cards of matching rank that form a three card straight,
            and then discard card not in the meld, to burrow a term from gin rummy'''
            discard = []
            try:
                if self.straight_finder(3)[0] == self.flush_finder(3)[0]:
                    for card in self.hand:
                        if card not in self.straight_finder(3)[0]:
                            discard.append(card)
                    return discard
            except: 
                None
            
        # print(three_card_meld_discard())
            
                    
        
        if strategy == 1:
            
            if  int(self.best_hand[1] // 1) in [8,7,6,5,4]: ## anything higher than a straight 
                return [] 
            elif int(self.best_hand[1] // 1) in [3,2,1]:
                return pair_discard() 
            else:
                possible_discards = [flush_discard(),straight_discard(),low_cards_discard()]
                #print(possible_discards)
                for discard in possible_discards:
                    if discard != None:
                        return discard 
           
        
        # if strategy == 1: 
        #     print('read')
        #     if flush_discard() == straight_discard() and flush_discard() != None :
        #         return possible_discards[1]
        #     elif flush_discard() != []:
        #         return possible_discards[1] 
        #     elif straight_discard() != [] :
        #         return possible_discards[0]
        #     elif pair_discard() != []:
        #         return possible_discards[2]
        #     else:
        #         return possible_discards[3]
        # elif strategy == 2:
        #     if pair_discard() != []:
        #         return pair_discard()
        #     else:
        #         return low_card_discard()


class Five_card_draw:
    ''' what needs to happen:
        
        - new hand needs to be evaluated for best hand 
        - best way to do that is for the new hand to be a new hand object
            - it would be nice if new hand object didn't run the discard 
              part of the program ... just as a way to speed things up . 
    
    
    ''' 
    def __init__(self,num_players):
        self.deck = Deck()
        self.deck.shuffle()
        self.players = [ Hand(self.deck.deal(5)) for player in range(num_players)] # might make mor
        ## to call this self.round1_hands. and the self.round2 hands. 
        self.players_post_discard = []
        self.play_game()
    def play_game(self):
        original_hands = [player.hand for player in self.players]
        new_hands = [] 
        self.best_hand = None
        self.winning_index = 1
        for player in self.players: 
            new_hand = [] 
            for index,card in enumerate(player.hand):
                if card in player.discard:
                    new_hand.append(self.deck.deal(1)[0])
                else:
                    new_hand.append(card)
            #print(new_hand)
            self.players_post_discard.append(Hand(new_hand,False))
        for index,player in enumerate(self.players_post_discard):
            if self.best_hand == None:
                self.best_hand = player.best_hand
                self.winning_index = index 
            else:
                if player.best_hand[1] > self.best_hand[1]:
                    self.best_hand = player.best_hand
                    self.winning_index = index 
    def print_game(self):
        index = 0 
        print('='*45)
        for player,player_post_discard in zip(self.players,self.players_post_discard):
            index += 1 
            print(f'Player {index}')
            player.print_hand()
            print(f'\nDraws {len(player.discard)} cards')
            #print(f'\nDiscards {" ".join(Hand(player.discard).str)}')
            player_post_discard.print_hand()
            print('-'*25)
        print('-'*25)
        print(f'Player {self.winning_index + 1} wins!')
    
            
def document_simulation(n):
    ''' what would the rows in a csv be 
    game_num, player_num, hand_ pre discard, best_hand post discard, pre discard hand value, discard strategy, discard, post_discard hand, best_hand post discard, hand rating, winner or not winner. 
    thats a bunch of categories''' 
    title = input("type in csv title")
    title = title + '.csv'
    simulation_csv = open(title,'w')
    header = ('Game_Num, Player_Num, PD_Hand, Best_Hand_PD, Best_Hand_PD_val, AD_Hand, Best_Hand_AD,Best_Hand_AD \n')
    simulation_csv.write(header)
    for i in range(n):
        g = Five_card_draw
        for player in g.players:
            row_info = [str(3),''.join(player.str), player.best_hand]
 
    
 
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
                
            
import time

start = time.time()        
for i in range(1000):
    g = Five_card_draw(3)
    g.print_game()
# print(time.time() - start)
            
    
    
    
                        
                
                    
            
            
        # discard = []
        # hand1 = hand
        # hand = self.hand
        # '''print(hand1)'''
        # try:
        #     ## when you have four of the cards needed for a straight
        #     ## in this strategy you discard and go for the inside straight
            
        #     if len(self.straight_finder(4)[0]) == 4:
        #         for card in self.hand:
        #             if card not in self.straight_finder(4)[0]:
        #                 discard.append(card)
        #                 '''print('something')'''
        #                 break
        # except: 
        #     try:
        #         if len(self.flush_finder(4)[0]) == 4:
        #             for card in self.hand:
        #                 if card not in self.flush_finder[0]:
        #                     '''print(card)'''
        #                     discard.append(card)
        #                     break
        #     except:
        #         if best_hand(hand1)[1] <= 3.5 and len(discard) == 0:
        #             iter_count = 0
        #             for card in hand:
        #                 if card not in as_strings(best_hand(hand1)[0]):
        #                     discard.append(card)
        #                 if len(discard) == 3:
        #                     break
        # return discard
        


        

d1 = Deck()
d1.shuffle()
h1 = d1.deal(5)
h2 = Hand(h1)

g = Five_card_draw(4)
        