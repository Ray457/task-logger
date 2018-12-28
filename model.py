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

    def load_range(self, datetime_range):
        """
        Returns all records within the specified range
        :param datetime_range: Two datetime.datetime or datetime.date objects specifying the range
        :return: list of TaskLog objects
        """
        if type(datetime_range[0]) is datetime.datetime:  # begin
            begin_timestamp = int(datetime.datetime(datetime_range[0].year,
                                                    datetime_range[0].month,
                                                    datetime_range[0].day,
                                                    datetime_range[0].hour,
                                                    datetime_range[0].minute,
                                                    datetime_range[0].second).timestamp())
        elif type(datetime_range[0]) is datetime.date:
            begin_timestamp = int(datetime.datetime(datetime_range[0].year,
                                                    datetime_range[0].month,
                                                    datetime_range[0].day).timestamp())
        else:
            raise TypeError("Argument begin_datetime must be either a datetime.datetime or datetime.date object")

        if type(datetime_range[1]) is datetime.datetime:
            end_timestamp = int(datetime.datetime(datetime_range[1].year,
                                                  datetime_range[1].month,
                                                  datetime_range[1].day,
                                                  datetime_range[1].hour,
                                                  datetime_range[1].minute,
                                                  datetime_range[1].second).timestamp())
        elif type(datetime_range[1]) is datetime.date:
            end_timestamp = int(datetime.datetime(datetime_range[1].year,
                                                  datetime_range[1].month,
                                                  datetime_range[1].day).timestamp())
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
