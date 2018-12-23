import sqlite3


class ModelSQLite:
    """
    A model that uses SQLite as data storage
    """
    conn = None  # SQLite connection object
    cur = None  # SQLite cursor object

    def connect(self, filename='records.db'):
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()

        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs'")
        res = self.cur.fetchone()
        if res is None:  # no table in the database, create one
            self.cur.execute("CREATE TABLE logs\
                             (startTime INTEGER, task TEXT, project TEXT, stopTime INTEGER, comment TEXT)")
            self.conn.commit()

    def save_log(self, log):
        """
        Saves the log entry into the database
        :param log: TaskLog, object holding the info for a log entry
        :return: None
        """
        self.cur.execute("INSERT INTO logs VALUES(?, ?, ?, ?, ?)",
                         (log.start_time, log.task, log.project, log.stop_time, log.comment))
        self.conn.commit()

    def load_today(self, search):
        pass


class ModelXLS:
    """
    A model that uses Excel sheets as data storage
    """
    def connect(self):
        pass

    def save_record(self):
        pass

    def load_today(self):
        pass


class TaskLog:
    """
    Object representing a log entry
    """
    start_time = 0
    stop_time = 0
    task = ''
    project = ''
    comment = ''
