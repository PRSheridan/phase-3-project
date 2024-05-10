from models.__init__ import CURSOR, CONN

class User:
    all = {}

    def __init__(self, name, id = None):
        self.id = id
        self.name = name

    def __repr__(self):
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    #Methods
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of User instances """
        sql = """
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists User instances """
        sql = """
            DROP TABLE IF EXISTS users;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, job title, and department id values of the current User object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO users (name)
                VALUES (?)
        """

        CURSOR.execute(sql, (self.name,))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current User instance."""
        sql = """
            UPDATE users
            SET name = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current User instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM users
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, name):
        """ Initialize a new User instance and save the object to the database """
        user = cls(name)
        user.save()
        return user

    @classmethod
    def instance_from_db(cls, row):
        """Return an User object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        user = cls.all.get(row[0])
        if user:
            # ensure attributes match row values in case local instance was modified
            user.name = row[1]
        else:
            # not in dictionary, create new instance and add to dictionary
            user = cls(row[1])
            user.id = row[0]
            cls.all[user.id] = user
        return user

    @classmethod
    def get_all(cls):
        """Return a list containing one User object per table row"""
        sql = """
            SELECT *
            FROM users
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return User object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM users
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return User object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM users
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def tests(self):
        """Return all instances of test for the current user instance"""
        from models.test import Test
        sql = """
            SELECT *
            FROM tests
            WHERE user_id_ is ?
        """

        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Test.instance_from_db(row) for row in rows]

    def avg_time(self):
        """Return the average time for all tests of the current user instance"""
        average = 0
        user_times = [test.time for test in self.tests()]
        for time in user_times:
            average = average + time
        return average/len(user_times)

    def avg_accuracy(self):
        """Return the average accuracy for all tests of the current user instance"""
        average = 0
        user_accuracies = [test.accuracy for test in self.tests()]
        for accuracy in user_accuracies:
            average = average + accuracy
        return average/len(user_accuracies)

    def avg_wpm(self):
        """Return the average wpm for all tests of the current user instance"""
        average = 0
        user_wpms = [test.wpm for test in self.tests()]
        for wpm in user_wpms:
            average = average + wpm
        return average/len(user_wpms)
    
    def record_wpm(self):
        """Return the highest wpm for all tests of the current user instance"""
        record = 0
        user_wpms = [test.wpm for test in self.tests()]
        for wpm in user_wpms:
            if wpm > record:
                record = wpm
        return record