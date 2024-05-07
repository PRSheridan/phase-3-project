#!/usr/bin/env python3

from models.__init__ import CONN, CURSOR
from models.sentence import Sentence
from models.test import Test
from models.user import User

def seed_database():
    Sentence.drop_table()
    Test.drop_table()
    User.drop_table()
    Sentence.create_table()
    Test.create_table()
    User.create_table()

    # Create seed data
    Sentence.create("This is a test sentence")       #1
    Sentence.create("This is another test sentence") #2
    Sentence.create("I am a test sentence")          #3
    Sentence.create("Testing a sentence")            #4
    Sentence.create("Sentence tested")               #5

    sheridan = User.create("sheridan")
    sky = User.create("sky")
    christian = User.create("christian")
    charlie = User.create("charlie")
    #sentence, time, accuracy, score, user, sentence
    Test.create("This is a test sentence", 5, 90, 18, 1, 1)
    Test.create("This is another test sentence", 6, 80, 13.3, 2, 2)
    Test.create("I am a test sentence", 4, 80, 20, 2, 3)
    Test.create("Testing a sentence", 5, 70, 14, 3, 4)
    Test.create("Sentence tested", 6, 70, 11.6, 3, 5)
    Test.create("This is a test sentence", 7, 80, 11.4, 3, 1)
    Test.create("This is another test sentence", 5, 80, 16, 1, 2)
    Test.create("I am a test sentence", 4, 90, 22.5, 2, 3)
    Test.create("Testing a sentence", 5, 96, 19.2, 4, 4)
    Test.create("Sentence tested", 5, 87, 17.4, 4, 5)

seed_database()
print("Seeded database")