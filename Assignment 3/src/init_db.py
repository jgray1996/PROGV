import sqlite3
import sys

class DBCreater:

    def __init__(self, db_name, sql_script):
        self.db_name = db_name
        self.sql_script = sql_script

    def _read_script(self):
        """
        Takes scriptfile and reads it into memory
        """
        script = """"""

        with open(self.sql_script, 'r') as f_in:
            for command in f_in:
                script += command
        return script
    
    def _run_commands(self):
        """
        Creates local database and executes script to it.
        """
        connector = sqlite3.connect(self.db_name)
        cursor = connector.cursor()
        cursor.executescript(
            self._read_script()
        )

    def execute(self):
        """
        Run this to initialize database with new tables
        """
        self._run_commands()

if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        d = DBCreater(args[0], args[1])
        d.execute()
    except:
        print("python3 init_db.py [database_name.db] [table_creation_script.sql]")