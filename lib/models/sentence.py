from models.__init__ import CURSOR, CONN

class Sentence:
    all = {}

    def __init__(self, string, id = None):
        self.id = id
        self.string = string

    def __repr__(self):
        pass

    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, string):
        if isinstance(string, str) and len(string):
            if(not any(index.isdigit() for index in string)):
                self._string = string
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    #Methods
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Sentence instances """
        sql = """
            CREATE TABLE IF NOT EXISTS sentences (
            id INTEGER PRIMARY KEY,
            string TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Sentence instances """
        sql = """
            DROP TABLE IF EXISTS sentences;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the string, job title, and department id values of the current Sentence object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO sentences (string)
                VALUES (?)
        """

        CURSOR.execute(sql, (self.string,))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Sentence instance."""
        sql = """
            UPDATE sentences
            SET string = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.string, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Sentence instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM sentences
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, string):
        """ Initialize a new Sentence instance and save the object to the database """
        user = cls(string)
        user.save()
        return user

    @classmethod
    def instance_from_db(cls, row):
        """Return an Sentence object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        user = cls.all.get(row[0])
        if user:
            # ensure attributes match row values in case local instance was modified
            user.string = row[1]
        else:
            # not in dictionary, create new instance and add to dictionary
            user = cls(row[1])
            user.id = row[0]
            cls.all[user.id] = user
        return user

    @classmethod
    def get_all(cls):
        """Return a list containing one Sentence object per table row"""
        sql = """
            SELECT *
            FROM sentences
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return Sentence object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM sentences
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
