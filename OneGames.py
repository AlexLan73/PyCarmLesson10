import random
import copy

# Class - описание карты, можно добавить поле визуализации карты
class PlayingCard: 
    def __init__(self, *args, **kwargs):
        if args.__len__()>0:
            self.suit = args[0]     # масть "ch"-черви, "bu"-буби, "kr"-крести, "pi"-пики
            self.card = args[1]     # карта "6", "7".. "J","Q","K","A"
            self.weight = args[2]  # веса "6"-6; "7"-7;.. "J"-11; "Q"-12; "K"-13; "A"-14
            self.id = args[3]       # id 
        if kwargs.__len__()>0:
            x=kwargs['dd']
            key=list(x.keys())[0]
            self.suit = x[key].suit
            self.card = x[key].card
            self.weight = x[key].weight
            self.id = x[key].id

    def __lt__(self, other):
         return self.suit==other.suit and self.weight < other.weight

# Class - сравнения карт одна-одна
class ComparCard():
    def __init__(self, **kwargs):
        self.card0 : PlayingCard
        ComparCard.set(self, **kwargs)

    def set(self, **kwargs):
        self.card0=kwargs['d0']

    def __eq_suit_card(self, other):
        key0=list(self.card0.keys())[0]
        key1=list(other.card0.keys())[0]
        eq=self.card0[key0].suit==other.card0[key1].suit
        return eq, key0, key1

    def __eq__(self, other):
        eq, key0, key1= ComparCard.__eq_suit_card(self, other)
        return eq  and self.card0[key0].weight == other.card0[key1].weight

    def __gt__(self, other):
        eq, key0, key1= ComparCard.__eq_suit_card(self, other)
        return eq  and self.card0[key0].weight > other.card0[key1].weight

    def __lt__(self, other):
        eq, key0, key1= ComparCard.__eq_suit_card(self, other)
        return eq  and self.card0[key0].weight < other.card0[key1].weight

# Class - для битья одна карта и все карты противника
#         если заход с нескольких карт и все карты противника
class ComparCards(ComparCard):
    def __init__(self, **kwargs):
        self.comp_card:ComparCard

    def set(self, **kwargs):
        self.card0=kwargs['d0']
        self.card1=kwargs['d1']
        
    def better(self, **kwargs):
        if kwargs.__len__()>0:
            self.card0=kwargs['d0']
            self.card1=kwargs['d1']
        key0= list(self.card0.keys())[0]
        key1= list(self.card0.keys())
        suit= self.card0[key0].suit
        weight=self.card0[key0].weight
        x=[]
        try:
            xx=[val for kye, val in self.card1.items()  
                if val.suit==suit and val.weight>weight]
            xx.sort()
            x=xx[0]
        except IndexError:
            return False, []
        return True, x

    def betters(self, **kwargs):
        cards0={}
        cards1={}

        if kwargs.__len__()>0:
            cards0=copy.deepcopy(kwargs['d0'])
            cards1=copy.deepcopy(kwargs['d1'])
            self.card0=kwargs['d0']
            self.card1=kwargs['d1']
        else:
            return False, cards1
        b_count=True

        for key, val in self.card0.items():
           b, card_=ComparCards.better(self, d0= {key:val}, d1= self.card1)
           b_count=b_count and b
           if b_count:
               del self.card1[card_.id]
           else:
               break

        if b_count:
            return True, self.card1
        else:
            return False, cards1
        return False, cards1

    def __gt__(self, other):
        eq, key0, key1= ComparCard.__eq_suit_card(self, other)
        return eq  and self.card0[key0].weight > other.card0[key1].weight

    def __lt__(self, other):
        eq, key0, key1= ComparCard.__eq_suit_card(self, other)
        return eq  and self.card0[key0].weight < other.card0[key1].weight

# Class - Описание карт находящихся в одной руке
class OneGrunt():
    def __init__(self, *args, **kwargs):
        self.deck={}
        self.mast={}
        self.duplicate={}

    def add(self, *args, **kwargs):
        x=kwargs['dd']
        for kye, val in x.items():
            self.deck[kye]=val
        OneGrunt.form_dict(self)

    def sub(self, *args, **kwargs):
        i=args[0]
        try:
            del self.deck[i]
        except KeyError:
            pass
        OneGrunt.form_dict(self)

    def form_dict(self):
        # dx=onegrunt1.deck
        self.mast={}
        self.duplicate={}
        z=list({val.suit for kye, val in self.deck.items()})
        for it in z:
            xx=[val for kye, val in self.deck.items()if val.suit==it]
            xx.sort()
            self.mast[it]=xx

        z1=list({val.weight for kye, val in self.deck.items()})
        z1.sort()
        for it in z1:
            xx=[val for kye, val in self.deck.items()if val.weight==it]
            xx.sort()
            self.duplicate[it]=xx
    
    def print_card(self):
        for key, val in self.mast.items():
            z1=list({val1.card+"-"+str(val1.id) for val1 in val})
            z1.sort()
            print(" масть - {} :  карты: {}".format(key, z1))

# Планировался Класс - одной игры зайти, отбиться, поддать            
class OneGames:
    human: OneGrunt
    comp: OneGrunt
    type_step = False  # False - human, True-comp
    def __init__(self, *args):
        OneGames.set_one_play(self, *args)

    def set_one_play(self, *args):
        self.type_step=args[0]
        self.human=args[1]
        self.comp=args[2]
        OneGames.run(self)

    def ___select_human(self): # хотел построить функцию с проверками 
                               # большой код и нет смысла
        if self.human.deck.__len__() <=0:
            return {}
        print("Нужно выбрать карту id или несколько (одинаковых) через пробел")
        self.human.print_card()
        mas_id=list(input("Вводите: ").split(" "))
        mas_id =[int(item) for item in mas_id]

        dcard={}
        for it in mas_id:
            try:
                 dcard[it]= dhuman= self.human.deck[it]
                 dhuman= self.human.sub(it)
            except KeyError:
                return dcard
        return dcard
    
    def ___beat(self, dcart0, dcart1):
        for key, val in dcart0.items():
            try:
                x= dcart1.mast[val.suit]
                for it in x:
                   if it.weight > val.weight:
                       dcart1.sub(it.id)
                       continue
                dcart1.add(dcart0)
            except KeyError:
                return dcart1.add(dd = dcart0)
        return dcart1

    def run(self):
        if self.type_step:   #сомп
            pass
        else:   # Человек
            card_human= OneGames.___select_human(self)
            if card_human !={}:
                self.comp=OneGames.___beat(self, card_human, self.comp)

    def run1(self):
        pass

# Планировался Класс - всей игры раздача и контроль карт, отслеживание ходов
#  вызов одной игры с последующим принятием решением отбился не отбился.
class ALLGames:
    def __init__(self, *args, **kwargs):
        pass

# Колода
class DeckBasa:
    __suits = ["ch", "bu", "kr", "pi"]
    __cards = ["6", "7", "8", "9", "10", "J", "Q", "K", "A"] 
    __weights = [6, 7, 8, 9, 10, 11, 12, 13, 14]
    deck={}
    _ls_mix_deck=[]
    def __init__(self):  
        id=0
        for it__suits in self.__suits:
            for it in range(self.__cards.__len__()):
                id+=1;
                xx=PlayingCard(it__suits, self.__cards[it], self.__weights[it], id)
                self.deck[id]=xx

    def mix_deck(self):
        self._ls_mix_deck=list(self.deck.keys())
        random.shuffle(self._ls_mix_deck)

    @property
    def count_card(self):
        return self.deck.__len__()


# Работа с Колодой    
class Deck(DeckBasa):
    __takeACard=[]
    def __init__(self):  
        super().__init__()

    def take_a_card(self):
        for it in self._ls_mix_deck:
            yield self.deck[it]

    def print_deck(self):
         print(self.deck)

    def read_carf(self, n):
        if self.__takeACard == []:
            self.__takeACard = Deck.take_a_card(self)
        rez={}

        for it in range(n):
            try:
                z=next(self.__takeACard)
                rez[z.id]=z
            except StopIteration:
                return rez
        return rez
