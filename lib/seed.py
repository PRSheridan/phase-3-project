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
    Sentence.create("Learning to code is fun and cool")
    Sentence.create("Flatiron school is a great way to learn")
    Sentence.create("Continuing education is exciting")
    Sentence.create("Python is an object oriented programming language")
    Sentence.create("React uses components to build user interfaces")
    Sentence.create("To speak a language is to take on a world")
    Sentence.create("Words give all things meaning")
    Sentence.create("I do not want to go on the roof")
    Sentence.create("I could watch that man play piano all day")
    Sentence.create("The ability to speak does not make you intelligent")
    Sentence.create("You will never find a more wretched hive of scum and villainy")
    Sentence.create("I am one with the force and the force is with me")
    Sentence.create("I have a bad feeling about this")

seed_database()
print("Seeded database")