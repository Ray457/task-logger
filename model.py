import sqlite3
import datetime


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

    def load_today(self):
        """
        Returns all records saved today
        :return: list of TaskLog objects
        """
        date_today = datetime.date.today()
        start_timestamp_today = int(datetime.datetime(date_today.year,
                                                      date_today.month,
                                                      date_today.day,
                                                      0, 0).timestamp())
        date_tmrw = date_today + datetime.timedelta(days=1)
        end_timestamp_today = int(datetime.datetime(date_tmrw.year,
                                                    date_tmrw.month,
                                                    date_tmrw.day,
                                                    0, 0).timestamp())
        self.cur.execute("SELECT * FROM logs WHERE (startTime BETWEEN ? AND ?)",
                         (start_timestamp_today, end_timestamp_today))
        logs = self.cur.fetchall()
        out = []
        for log in logs:
            out.append(TaskLog(log[0], log[1], log[2], log[3], log[4]))

        return out


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
    task = ''
    project = ''
    stop_time = 0
    comment = ''

    def __init__(self, start_time=0, task='', project='', stop_time=0, comment=''):
        self.start_time = start_time
        self.stop_time = stop_time
        self.task = task
        self.project = project
        self.comment = comment
