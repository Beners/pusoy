from __future__ import division, print_function
input = raw_input
import random
import math

## Pusoy Dos Card Values:
## * Singles: 1 - 52 (3C to 2C)
## * Pairs: 101-152 (100 + higher card value, lowest is 3C3S, highest is 2D2X)
## * Three-of-a-kind: 201-252 (200 + highest card value, lowest is 3C3S3H, highest is 2D2X2Y)
## * Four-of-a-kind: 301-352 (300 + highest card value, lowest is 3C3S3H3D, highest is 2C2S2H2D)
## * Five card hands: 401 up (A is both a low and high card for any straight hands)
##      * Straight: 401-456 (400 + highest card poker value, lowest possible is AC2C3C4C5S, highest possible is 0HJDQDKDAD)
##      * Flush: 501-552 (500 + highest card value, lowest possible is 3C4C5C6C8C, highest possible is 0DQDKDAD2D [A and 2 are high cards])
##      * Full-House: 601-652 (600 + three-of-a-kind value, lowest is 3C3S3HXYXZ, highest possible is 2D2H2SXYXZ [A and 2 are high cards])
##      * Four-of-a-kind-plus-one: 701-752 (700 + four-of-a-kind value, lowest is 3C3S3H3DXY, highest is 2D2H2S2CXY [A and 2 are high cards])
##      * Straight flush: 801-852 (800 + highest card poker value, lowest possible is AC2C3C4C5C, highest possible is 0DJDQDKDAD)

class PusoyDosCard:
    def __init__(self, Rank = 0, Suit = None):
        # Constructor, with optional parameters Rank (integer: 1-13) and Suit (string: C, S, H, or D)
        # If no Suit is provided, Rank may be an integer from 1-52, and sets the value of the card
        if Suit == None and Rank > 0 and Rank < 53:
            self.FromValue(Rank)
        elif Rank > 0 and Rank < 14 and Suit in "CSHD":
            self.Rank = Rank
            self.Suit = Suit
        else:
            # Set default rank and suit
            self.Rank = 0
            self.Suit = "X"

    def Display(self):
        # Returns a two-character combination of rank and suit. Returns "XX" if Rank or Suit is invalid
        if self.Rank > 0 and self.Rank < 14 and self.Suit in "CSHD":
            return "A234567890JQK"[self.Rank - 1] + str(self.Suit)
        else:
            return "XX"

    def Value(self):
        # Returns a number from 1 to 52, equivalent to the "strength" of the card. Returns 0 if Rank or Suit is invalid
        # Set for pusoy dos rules (3C is 1)
        if self.Rank > 0 and self.Rank < 14 and self.Suit in "CSHD":
            return ((self.Rank + 10) % 13) * 4 + "CSHD".index(self.Suit) + 1
        else:
            return 0

    def PokerValue(self, highAce = False):
        # Returns a number from 1 to 56, equivalent to the strength of the card.
        # Returns 0 if Rank or Suit is invalid
        # Set for Poker rules (A < 2 < 3 < 4 < ... < 9 < 0 < J < Q < K < A)
        if self.Rank > 0 and self.Rank < 14 and self.Suit in "CSHD":
            # Check if this is an ace...
            if self.Rank == 1:
                if highAce:
                    # High aces: 53 to 56
                    return 53 + "CSHD".index(self.Suit)
                else:
                    # Low aces: 1 to 4
                    return 1 + "CSHD".index(self.Suit)
            else:
                # Everything else goes here
                return (self.Rank - 1) * 4 + "CSHD".index(self.Suit) + 1
            
        else:
            return 0

    def FromValue(self, value):
        # Sets Rank and Suit depending on the value set (integer, 1-52)
        # Illegal values do not modify the card properties
        if value > 0 and value < 53:
            self.Rank = ((value - 1) // 4 + 2) % 13 + 1
            self.Suit = "CSHD"[(value - 1) % 4]

class Hand:
    def __init__(self):
        # Constructor: starts with an empty Hand list
        self.Hand = []

   
    def Display(self):
        # Returns a string of cards based on the Hand list
        output = ""
        for card in self.Hand:
            output += card.Display() + ", "

        # This removes the trailing ", " from output string
        return output[:-2]

    def GetCards(self, cardsDemanded):
        # Returns a new Hand instance based on a string of cards in cardsDemanded.
        # Removes demanded cards from this Hand.
        H = Hand()
        if len(cardsDemanded) % 2 == 0:
            i = 0

            # "for thisCard in cardDemanded..."
            while i < len(cardsDemanded):
                thisCard = cardsDemanded[i:i + 2]
                
                # Find thisCard in Hand
                notFound = True
                for card in self.Hand:
                    if card.Display() == thisCard:
                        H.Hand.append(card)
                        self.Hand.pop(self.Hand.index(card))
                        notFound = False
                        break

                if notFound:
                    # Return all the cards taken back into the old Hand
                    while len(H.Hand) > 0:
                        self.Hand.append(H.Hand.pop())
                    break

                i += 2

        return H

    def isSingles(self):
        # Checks if this Hand is a valid single card, and returns the value if so.
        # Returns 0 if invalid
        if len(self.Hand) == 1:
            return self.Hand[0].Value()

        return 0

    def isMultiSuitHand(self, count = 2):
        # Checks if this Hand is a pair (count == 2), three-of-a-kind (count == 3), or a four-of-a-kind (count == 4)
        # Returns 0 if invalid
        if len(self.Hand) == count:
            Rank = self.Hand[0].Rank
            ThisHandValue = [self.Hand[0].Value()]
            i = 1
            while i < count:
                if Rank != self.Hand[i].Rank:
                    return 0
                
                ThisHandValue.append(self.Hand[i].Value())
                i += 1

            return max(ThisHandValue) + (count - 1) * 100

        return 0

    def isFlush(self):
        # Checks if this hand is a valid 5-card flush
        # Returns 0 if invalid
        if len(self.Hand) == 5:
            Suit = self.Hand[0].Suit
            ThisHandValue = [self.Hand[0].Value()]

            i = 1
            while i < 5:
                if self.Hand[i].Suit != Suit:
                    return 0

                ThisHandValue.append(self.Hand[i].Value())
                i += 1

            return max(ThisHandValue) + 500
            
    def isStraight(self):
        self.sortByPokerValue(self)
        i=0
        if len(self.Hand)==5:
            ThisHandValue = [self.Hand[0].PokerValue()]
            while i<5:
                if ((self.Hand[i].PokerValue()-1)%4)+1 != self.Hand[i+1].PokerValue():
                    return 0
                else:
                    ThisHandValue.append(self.Hand[i].PokerValue())
                i+=1
            return max(ThisHandValue) + 400
   
    def isStraightFlush(self):
        if len(self.Hand) == 5:
            x=self.isStraight()
            if x!=0:
                y=self.isFlush()
                if y!=0:
                    z= x  + y + 800
                    return z
                else:
                    return 0
            else:
                return 0
        else:
            return 0
                        
    def isFullHouse(self):
        if len(self.Hand)==5:
            self.sortByValue()
            Rank = self.Hand[0].Rank
            ThisHandValue = [self.Hand[4].Value()]
            if self.Hand[0].Rank!=self.Hand[4].Rank:
                if self.Hand[0].Rank ==self.Hand[1].Rank and self.Hand[3].Rank==self.Hand[4].Rank:
                    if self.Hand[1].Rank == self.Hand[2].Rank and self.Hand[2].Rank ==self.Hand[3].Rank:
                        return 0
                    elif self.Hand[1].Rank!=self.Hand[2].Rank and self.Hand[2].Rank==self.Hand[3].Rank:
                        return max(ThisHandValue) + 600
                    elif self.Hand[1].Rank==self.Hand[2].Rank and self.Hand[2].Rank!=self.Hand[3].Rank:
                        return max(ThisHandValue) + 600
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        else:
                return 0
        
    def isFourOfAKind(self):
        if len(self.Hand)==5:
            self.sortByValue()
            Rank = self.Hand[0].Rank
            ThisHandValue = [self.Hand[4].Value()]
            if self.Hand[0].Rank!=self.Hand[4].Rank:
                if self.Hand[0].Rank!=self.Hand[1].Rank and self.Hand[1].Rank==self.Hand[2].Rank and self.Hand[2].Rank==self.Hand[3].Rank and self.Hand[3].Rank==self.Hand[4].Rank:
                    return max(ThisHandValue) + 700
                elif self.Hand[0].Rank==self.Hand[1].Rank and self.Hand[1].Rank==self.Hand[2].Rank and self.Hand[2].Rank==self.Hand[3].Rank and self.Hand[3].Rank!=self.Hand[4].Rank:
                    return max(ThisHandValue) + 700
                else:
                    return 0
            else:
                return 0
        else:
            return 0
        
    def sortByValue(self):
        unsorted=self.Hand
        donesort=[]
        donesort.append(unsorted.pop(0))
        while len(unsorted)>0:
            i=0
            while i<len(unsorted):
                i=0
                if unsorted[0].Value()<=donesort[i].Value():
                    donesort.insert(i, unsorted.pop(0))
                elif unsorted[0].Value()> donesort[i].Value() and len(donesort)==1 or unsorted[0].Value()> donesort[i].Value() and unsorted[0].Value()< donesort[i+1].Value():
                    donesort.insert(i+1, unsorted.pop(0))
                else:
                    if donesort[-1].Value()< unsorted[0].Value():
                        donesort.append(unsorted.pop(0))
                    else:
                        while unsorted[0].Value()>donesort[i].Value() and unsorted[0].Value()>donesort[i+1].Value():
                            i+=1
                        donesort.insert(i+1, unsorted.pop(0))

        self.Hand=donesort
    
    def sortByPokerValue(self, highAce=False):
        for x in self.Hand:
            if x.Rank==2:
                highAce=False
                break
            else:
                highAce=True
            
                
        unsorted=self.Hand
        donesort=[]
        donesort.append(unsorted.pop(0))
        while len(unsorted)>0:
            i=0
            while i<len(unsorted):
                i=0
                if unsorted[0].PokerValue(highAce)<=donesort[i].PokerValue(highAce):
                    donesort.insert(i, unsorted.pop(0))
                elif unsorted[0].PokerValue(highAce)> donesort[i].PokerValue(highAce) and len(donesort)==1 or unsorted[0].PokerValue(highAce)> donesort[i].PokerValue(highAce) and unsorted[0].PokerValue(highAce)< donesort[i+1].PokerValue(highAce):
                    donesort.insert(i+1, unsorted.pop(0))
                else:
                    if donesort[-1].PokerValue(highAce)< unsorted[0].PokerValue(highAce):
                        donesort.append(unsorted.pop(0))
                    else:
                        while unsorted[0].PokerValue(highAce)>donesort[i].PokerValue(highAce) and unsorted[0].PokerValue(highAce)>donesort[i+1].PokerValue(highAce):
                            i+=1
                        donesort.insert(i+1, unsorted.pop(0))

        self.Hand=donesort
    
    def sortByRank(self):
        unsorted=self.Hand
        donesort=[]
        donesort.append(unsorted.pop(0))
        while len(unsorted)>0:
            i=0
            while i<len(unsorted):
                i=0
                if unsorted[0].Rank<=donesort[i].Rank:
                    donesort.insert(i, unsorted.pop(0))
                elif unsorted[0].Rank> donesort[i].Rank and len(donesort)==1 or unsorted[0].Rank> donesort[i].Rank and unsorted[0].Rank< donesort[i+1].Rank:
                    donesort.insert(i+1, unsorted.pop(0))
                else:
                    if donesort[-1].Rank< unsorted[0].Rank:
                        donesort.append(unsorted.pop(0))
                    else:
                        while unsorted[0].Rank>donesort[i].Rank and unsorted[0].Rank>donesort[i+1].Rank:
                            i+=1
                        donesort.insert(i+1, unsorted.pop(0))

    
    def sortBySuit(self):
        unsorted=self.Hand
        donesort=[]
        donesort.append(unsorted.pop(0))
        while len(unsorted)>0:
            i=0
            while i<len(unsorted):
                i=0
                if unsorted[0].Suit<=donesort[i].Suit:
                    donesort.insert(i, unsorted.pop(0))
                elif unsorted[0].Suit> donesort[i].Suit and len(donesort)==1 or unsorted[0].Suit> donesort[i].Suit and unsorted[0].Suit< donesort[i+1].Suit:
                    donesort.insert(i+1, unsorted.pop(0))
                else:
                    if donesort[-1].Suit< unsorted[0].Suit:
                        donesort.append(unsorted.pop(0))
                    else:
                        while unsorted[0].Suit>donesort[i].Suit and unsorted[0].Suit>donesort[i+1].Suit:
                            i+=1
                        donesort.insert(i+1, unsorted.pop(0))

class Deck:
    def __init__(self):
        # Constructor: sets up 52 unique PusoyDosCard instances
        self.Deck = []
        i = 1
        while i < 53:
            self.Deck.append(PusoyDosCard(i))
            i += 1

        # Sets a new random number seed (for more randomness)
        random.seed()
    
    def Shuffle(self):
        # Shuffles the Deck list
        if len(self.Deck) > 0:
            j = random.randint(7, 14)
            while j > 0:
                random.shuffle(self.Deck)
                j -= 1

    def Deal(self):
        # Pops 13 PusoyDosCard instances and stuffs them into a Hand instance
        if len(self.Deck) > 12:
            H = Hand()
            i = 13

            while i > 0:
                H.Hand.append(self.Deck.pop(0))
                i -= 1

            return H

        return None


print("-----")
D = Deck()
D.Shuffle()
H = [D.Deal(), D.Deal(), D.Deal(), D.Deal()]
print("Opponent 1 Cards: " + H[0].Display())
print("Opponent 2 Cards: " + H[1].Display())
print("Opponent 3 Cards: " + H[2].Display())
print("-----")
print("Your Cards: " + H[3].Display())


print("-----")

C = raw_input()
H2 = H[3].GetCards(C)
if H2.isSingles() < 1:
    if H2.isMultiSuitHand < 100:
        if H2.isFourOfAKind < 300:
            if H2.isStraight < 400:
                if H2.isFlush() < 500:
                    if H2.isFullHouse < 600:
                        if H2.isStraightFlush < 800:
                            print("Try Again!")
                        else:
                            print("Straight Flush dealt: " + C)
                    else:
                        print("Full House dealt: " + C)
                else:
                    print("Flush dealt: " + C)
            else:
                print("Straight Hand dealt: " + C)
        else:
            print("Four-of-a-Kind dealt: " + C)
    else:
        print("Multi-suit Hand dealt: " + C)
else:
    print("Singles dealt: " + C)

