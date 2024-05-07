from models.__init__ import CURSOR, CONN
from models.user import User
from models.sentence import Sentence

class Test:
    all = {}

    def __init__(self, user_input, time, accuracy, user_id_, sentence_id_,):
        self.user_input = user_input
        self.time = time
        self.accuracy = accuracy
        self.user_id_ = user_id_
        self.sentence_id_ = sentence_id_

    def __repr__(self):
        pass

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Test instances """
        sql = """
            CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY,
            user_input TEXT,
            time INTEGER,
            accuracy INTEGER,
            user_id_ INTEGER,
            sentence_id_ INTEGER,
            FOREIGN KEY (user_id_) REFERENCES users(id),
            FOREIGN KEY (sentence_id_) REFERENCES sentences(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Test instances """
        sql = """
            DROP TABLE IF EXISTS tests;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, job title, and department id values of the current Test object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO tests (user_input, time, accuracy, user_id_, sentence_id_)
                VALUES (?, ?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.user_input, self.time, self.accuracy, self.user_id_, self.sentence_id_,))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Test instance."""
        sql = """
            UPDATE tests
            SET user_input = ?, time = ?, accuracy = ?, user_id_ = ?, sentence_id_ = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.user_input, self.time, self.accuracy, self.user_id_, self.sentence_id_,))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Test instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM tests
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, user_input, time, accuracy, user_id_, sentence_id_):
        """ Initialize a new Test instance and save the object to the database """
        test = cls(user_input, time, accuracy, user_id_, sentence_id_)
        test.save()
        return test

    @classmethod
    def instance_from_db(cls, row):
        """Return an Test object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        test = cls.all.get(row[0])
        if test:
            # ensure attributes match row values in case local instance was modified
            test.user_input = row[1]
            test.time = row[2]
            test.accuarcy = row[3]
            test.user_id_ = row[4]
            test.sentence_id_ = row[5]
        else:
            # not in dictionary, create new instance and add to dictionary
            test = cls(row[1], row[2], row[3], row[4], row[5])
            test.id = row[0]
            cls.all[test.id] = test
        return test

    @classmethod
    def get_all(cls):
        """Return a list containing one Test object per table row"""
        sql = """
            SELECT *
            FROM tests
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return Test object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM tests
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_user_id(cls, user_id_):
        """Return Test object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM tests
            WHERE user_id_ = ?
        """

        rows = CURSOR.execute(sql, (user_id_,)).fetchall()
        return [cls.instance_from_db(row) for row in rows]

