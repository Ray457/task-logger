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

    def load_range(self, begin_datetime, end_datetime):
        """
        Returns all records within the specified range
        :param begin_datetime: A datetime.datetime or datetime.date object
        :param end_datetime: A datetime.datetime or datetime.date object
        :return: list of TaskLog objects
        """
        if type(begin_datetime) is datetime.datetime:
            begin_timestamp = int(datetime.datetime(begin_datetime.year,
                                                    begin_datetime.month,
                                                    begin_datetime.day,
                                                    begin_datetime.hour,
                                                    begin_datetime.minute,
                                                    begin_datetime.second).timestamp())
        elif type(begin_datetime) is datetime.date:
            begin_timestamp = int(datetime.datetime(begin_datetime.year,
                                                    begin_datetime.month,
                                                    begin_datetime.day).timestamp())
        else:
            raise TypeError("Argument begin_datetime must be either a datetime.datetime or datetime.date object")

        if type(end_datetime) is datetime.datetime:
            end_timestamp = int(datetime.datetime(end_datetime.year,
                                                  end_datetime.month,
                                                  end_datetime.day,
                                                  end_datetime.hour,
                                                  end_datetime.minute,
                                                  end_datetime.second).timestamp())
        elif type(end_datetime) is datetime.date:
            end_timestamp = int(datetime.datetime(end_datetime.year,
                                                  end_datetime.month,
                                                  end_datetime.day).timestamp())
        else:
            raise TypeError("Argument begin_datetime must be either a datetime.datetime or datetime.date object")

        self.cur.execute("SELECT * FROM logs WHERE (startTime BETWEEN ? AND ?)",
                         (begin_timestamp, end_timestamp))
        logs = self.cur.fetchall()
        out = []
        for log in logs:
            out.append(TaskLog(log[0], log[1], log[2], log[3], log[4]))

        return out

    def cleanup(self):
        """
        Closes database connection. Any other clean up jobs also go here
        :return: None
        """
        self.conn.close()


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
