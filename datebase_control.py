import sqlite3




class DatabaseControl:
    def __init__(self):
        # connect to the database
        self.connection = sqlite3.connect("festival_database.db")
        # create a cursor
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS festivals (
                date TEXT,
                name TEXT,
                location TEXT,
                bands TEXT
            )
        ''')
        self.connection.commit()




    def add_festivals_to_database(self, festival_list):
        """Add the new festivals to the database"""

        # TODO: Bands is a list, so we need to convert it to a string, or something else.
        for festival in festival_list:
            self.cursor.execute("INSERT INTO festivals (date, name, location) VALUES (?, ?, ?)",
                                (festival['date'], festival['name'], festival['location']))
            self.connection.commit()
        self.connection.close()
    def get_festivals_from_database(self):
        """Get the festivals from the database"""
        self.cursor.execute("SELECT * FROM festivals")
        festivals = self.cursor.fetchall()
        self.connection.close()
        return festivals


