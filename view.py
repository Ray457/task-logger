from PyQt5.QtWidgets import QApplication
import time
import datetime
from collections import OrderedDict
import re


def format_time(log):
    """
    Format the times in a log entry into a list of strings to print
    :param log: a TaskLog object
    :return: a list of strings representing start time, stop time and time taken
    """
    return [str(datetime.datetime.fromtimestamp(log.start_time)),
            str(datetime.datetime.fromtimestamp(log.stop_time)),
            str(datetime.datetime.fromtimestamp(log.stop_time)
                - datetime.datetime.fromtimestamp(log.start_time))]


def calc_time(logs):
    """
    Calculate the time difference and sum them up
    :param logs: a list of TaskLog objects
    :return: total time difference in seconds
    """
    sum_time = 0
    for log in logs:
        sum_time += (log.stop_time - log.start_time)
    return sum_time


def parse_datetime(datetime_str):
    """
    Parses a string representing date and/or time into datetime.datetime objects
    :param datetime_str: a string with the format yyyy-mm-dd hh:mm:ss
    :return: a datetime.datetime object the string corresponds to
    """
    datetime_fmt_str = "%Y-%m-%d %H:%M:%S"
    date_fmt_str = "%Y-%m-%d"
    date_match_str = "\d\d\d\d-\d\d-\d\d"
    time_match_str = "\d\d:\d\d:\d\d"
    datetime_match_str = date_match_str + ' ' + time_match_str

    if re.match(time_match_str, datetime_str):  # time only, using today as the date
        today_date = datetime.date.today()
        times = datetime_str.split(':')
        return datetime.datetime(year=today_date.year,
                                 month=today_date.month,
                                 day=today_date.day,
                                 hour=int(times[0]),
                                 minute=int(times[1]),
                                 second=int(times[2]))

    elif re.match(date_match_str, datetime_str):  # date only, using 00:00:00 as the time
        return datetime.datetime.strptime(datetime_str, date_fmt_str)

    elif re.match(datetime_match_str, datetime_str):  # both date and time are typed in
        return datetime.datetime.strptime(datetime_str, datetime_fmt_str)

    else:
        raise ValueError("No recognizable pattern found!")


class ViewCMDLine:
    @staticmethod
    def __init__():
        print()
        print('=' * 20 + ' Task  Logger ' + '=' * 20)
        print('=' * 24 + ' V2.0 ' + '=' * 24)
        print('=' * 54 + '\n')

    @staticmethod
    def get_project():
        return input('Project name: ')

    @staticmethod
    def get_task():
        return input('Task name: ')

    @staticmethod
    def get_mode():
        return ViewCMDLine.get_input('Mode=? (1:Create new logs, 2:View logs)', ['1', '2', ''], '1')

    @staticmethod
    def wait_for_start():
        """
        Waits for user confirmation to start timing.
        :return:
        The start time in epoch time
        """
        ViewCMDLine.get_input('Ready to start? y/n ', ['y', 'Y'])
        start_time = int(time.time())
        print('Starting at: ' + str(datetime.datetime.fromtimestamp(start_time)) + '\n')
        return start_time

    @staticmethod
    def wait_for_stop(start_time):
        """
        Waits for user confirmation to stop timing.
        :return:
        The stop time in epoch time
        """
        ViewCMDLine.get_input('Stop? y/n ', ['y', 'Y'])
        stop_time = int(time.time())
        print('Stopped at: ' + str(datetime.datetime.fromtimestamp(stop_time)))
        print('Time taken: '
              + str(datetime.datetime.fromtimestamp(stop_time) - datetime.datetime.fromtimestamp(start_time)))
        return stop_time

    @staticmethod
    def get_comments():
        """
        Gets any user comments after the timing has stopped.
        :return:
        The comment string
        """
        return input('Any comments? ')

    @staticmethod
    def confirm_exit():
        """
        Ask for confirmation to exit
        :return: True if confirmed to exit
        """
        res = ViewCMDLine.get_input('Exit? Answer n to create more records. y/n ', ['y', 'n'])
        if res == 'y':
            return True
        else:
            print()
            return False

    @staticmethod
    def get_input(prompt, expecting, default=None):
        """
        Gets input from user at command line. Will not return until expected answer(s) are given
        :param prompt: Prompt text to be displayed
        :param expecting: list of expected inputs, as strings
        :param default: If the expected inputs contain ''(no input), this value will be used when user provide no input
        :return: the input from user
        """
        while True:
            if default is None:
                got = input(prompt)
            else:
                got = input("{} [{}] ".format(prompt, default))
            if got in expecting:
                break
        if ('' in expecting) and (got == ''):
            got = default
        return got

    @staticmethod
    def get_view_range():
        """
        Gets the view range (list today, list last week) from user
        :return: 2 datetime.datetime or datetime.date objects
        """
        selection = int(ViewCMDLine.get_input("View range? (1: list today, 2: list last 7 days, 3: specify)",
                                              ['', '1', '2', '3'],
                                              '1'))
        if selection == 1:
            return (datetime.date.today(),
                    datetime.date.today() + datetime.timedelta(days=1))
        elif selection == 2:
            return (datetime.date.today() - datetime.timedelta(days=6),
                    datetime.date.today() + datetime.timedelta(days=1))
        elif selection == 3:
            return ViewCMDLine.get_specified_range()
        else:
            return (datetime.date.today(),  # default to "list today"
                    datetime.date.today() + datetime.timedelta(days=1))

    @staticmethod
    def get_specified_range():
        """
        Gets a datetime range specified by user
        :return: 2 datetime.datetime or datetime.date objects
        """
        print("Type in date and/or time in this format: yyyy-mm-dd hh:mm:ss. Use 24-hour clock")
        begin_datetime_raw = input("Begin time: ")
        end_datetime_raw = input("End time: ")

        begin_datetime = parse_datetime(begin_datetime_raw)
        end_datetime = parse_datetime(end_datetime_raw)
        
        return begin_datetime, end_datetime

    @staticmethod
    def get_show_detail():
        """
        Gets the user preference about how detailed the output should be
        :return: True for list and stats, False for list only
        """
        if ViewCMDLine.get_input("Show details? (y: list and show stats, n: list only)", ['', 'y', 'n'], 'y') == 'y':
            return True
        else:
            return False

    @staticmethod
    def show_stats(logs, group_output=False):
        """
        Shows last 7 days' log entries, first sort by time then by projects and tasks
        :param logs: list of TaskLog objects, each represent a log entry
        :param group_output: if True groups the output by projects and tasks
        :return: None
        """
        print()
        if group_output:
            print("Sorted by projects and tasks:")
            print("=" * 54)
            # a dictionary holding the logs which are keyed using the projects they're belonging to
            logs_by_projects = OrderedDict()
            for log in logs:  # sort by project
                if log.project not in logs_by_projects:
                    logs_by_projects[log.project] = [log]
                else:
                    logs_by_projects[log.project].append(log)
            for project in logs_by_projects:  # sort by task and print
                print("Project: " + project)
                logs_by_tasks = OrderedDict()
                for log in logs_by_projects[project]:
                    if log.task not in logs_by_tasks:
                        logs_by_tasks[log.task] = [log]
                    else:
                        logs_by_tasks[log.task].append(log)
                for task in logs_by_tasks:
                    for log in logs_by_tasks[task]:
                        time_formatted = format_time(log)
                        print("\tTask: " + task)
                        print("\tTime: {} to {}".format(time_formatted[0], time_formatted[1]))
                        print("\tTime taken: " + time_formatted[2])
                        print("\tComments: " + log.comment)
                        print()
                    print("\tTotal time for this task: " + str(
                        datetime.timedelta(seconds=calc_time(logs_by_tasks[task]))))
                    print()
                print("Total time for this project: "
                      + str(datetime.timedelta(seconds=calc_time(logs_by_projects[project]))))
                print("-" * 54)

            time_today = calc_time(logs)
            print("Total logged time: " + str(datetime.timedelta(seconds=time_today)))
            print("Out of 24 hours, this is {:.2f}%. Out of 18 hours, this is {:.2f}%".format(
                time_today / 864, time_today / 648))
            print()

        else:
            print("Today's records:")
            print("=" * 54)

            for log in logs:
                time_formatted = format_time(log)
                print("[{}]-[{}]: {} to {}, time taken: {}. Comments: {}".format(
                    log.project,
                    log.task,
                    time_formatted[0],
                    time_formatted[1],
                    time_formatted[2],
                    log.comment))


class ViewQt:
    def start(self):
        pass

    def get_project(self):
        pass

    def get_task(self):
        pass

    def get_mode(self):
        pass

    def show_stats(self):
        pass

