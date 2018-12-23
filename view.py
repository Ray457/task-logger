from PyQt5.QtWidgets import QApplication
import model
import time
from datetime import datetime


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
    def show_stats(stats):
        pass

    @staticmethod
    def wait_for_start():
        """
        Waits for user confirmation to start timing.
        :return:
        The start time in epoch time
        """
        ViewCMDLine.get_input('Ready to start? y/n ', ['y', 'Y'])
        start_time = time.time()
        print('Starting at: ' + str(datetime.fromtimestamp(start_time))[:-7] + '\n')
        return start_time

    @staticmethod
    def wait_for_stop(start_time):
        """
        Waits for user confirmation to stop timing.
        :return:
        The stop time in epoch time
        """
        ViewCMDLine.get_input('Stop? y/n ', ['y', 'Y'])
        stop_time = time.time()
        print('Stopped at: ' + str(datetime.fromtimestamp(stop_time))[:-7])
        print('Time taken: ' + str(datetime.fromtimestamp(stop_time) - datetime.fromtimestamp(start_time))[:-7])
        return stop_time

    @staticmethod
    def get_comments():
        """
        Gets any user comments after the timing has stopped.
        :return:
        The comment string
        """
        return input('Any comments?')

    @staticmethod
    def get_input(prompt, expecting, default=None):
        while True:
            if default is None:
                got = input(prompt)
            else:
                got = input("{} [{}] ".format(prompt, default))
            if got in expecting:
                break
        if ('' in expecting) and (default is not None) and (got == ''):
            got = default
        return got


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

