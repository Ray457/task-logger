import view
import model
import argparse
import time


class Controller:
    m = None  # model object
    v = None  # view object

    def main(self):
        args = self.init()

        if args.gui_mode:
            self.v = view.ViewQt()
        else:
            self.v = view.ViewCMDLine()

        self.m = model.ModelSQLite()
        self.m.connect()
        mode = self.v.get_mode()
        if mode == '1':
            self.mode_1()
        elif mode == '2':
            self.mode_2()
        elif mode == '3':
            self.mode_3()

    def mode_1(self):
        # create a new log entry
        log = model.TaskLog()
        log.project = self.v.get_project()

        while True:
            log.task = self.v.get_task()

            log.start_time = self.v.wait_for_start()
            log.stop_time = self.v.wait_for_stop(log.start_time)
            log.comment = self.v.get_comments()
            self.m.save_log(log)

            if self.v.confirm_exit():
                break

    def mode_2(self):
        # view logs
        pass

    def mode_3(self):
        # modify logs
        pass

    def init(self):  # set up argparse
        parser = argparse.ArgumentParser(description='A simple utility that logs tasks.')
        parser.add_argument('-g', dest='gui_mode', action='store_const',
                            const=True, default=False,
                            help='start the program with GUI (default: No)')
        return parser.parse_args()


controller = Controller()
controller.main()
