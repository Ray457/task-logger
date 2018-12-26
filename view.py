from PyQt5.QtWidgets import QApplication
import time
import datetime
from collections import OrderedDict


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
    def show_today(logs):
        """
        Shows today's log entries, first sort by time then by projects and tasks
        :param logs: list of TaskLog objects, each represent a log entry
        :return: None
        """
        print()
        print("Today's records:")
        print("=" * 54)

        for log in logs:
            time_formatted = format_time(log)
            print("[{}]-[{}]: {} to {}, time taken: {}".format(
                log.project,
                log.task,
                time_formatted[0],
                time_formatted[1],
                time_formatted[2]))

        print()
        print("Sorted by projects and tasks:")
        print("=" * 54)
        # a dictionary holding the logs which are keyed using the projects they're belonging to
        logs_by_projects = OrderedDict()
        for log in logs:  # sort by project
            if log.project not in logs_by_projects:
                logs_by_projects[log.project] = [log]
                # so we have a list of sorted projects sorted by when it was inserted to the database
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
                    print()
            print("-" * 54)


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

