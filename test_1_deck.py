import pytest
import OneGames as og
import copy


def test_1_count_cart():
    deck = og.Deck()
    print("Кол-во карт ", deck.count_card)
    assert deck.count_card == 36


def test_2_mix_deck():
    deck = og.Deck()
    lsdeck0 = copy.deepcopy(list(deck.deck.keys()))
    ls = deck.mix_deck()
    assert lsdeck0 != ls

def test_3_read_card():
    deck = og.Deck()
    deck.mix_deck()
    dd = deck.read_carf(3)
    assert len(dd) == 3

def test_4_read_card():
    deck = og.Deck()
    deck.mix_deck()
    dd1 = deck.read_carf(3)
    dd2 = deck.read_carf(3)
    assert  list(dd1.keys()) != list(dd2.keys())

def test_5_one_card():
    deck = og.Deck()
    deck.mix_deck()
    dd1 = list(deck.read_carf(1))
    assert dd1[0]  != 0

