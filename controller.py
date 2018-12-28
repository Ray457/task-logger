import view
import model
import argparse
import datetime


class Controller:
    m = None  # model object
    v = None  # view object

    def main(self):
        args = self.get_args()

        if args.gui_mode:
            self.v = view.ViewQt()
        else:
            self.v = view.ViewCMDLine()

        self.m = model.ModelSQLite()
        # set up the model. A filename can be passed in for potential user-specified file name in the future
        self.m.connect()
        mode = self.v.get_mode()
        if mode == '1':
            self.mode_1()
        elif mode == '2':
            self.mode_2()
        elif mode == '3':
            self.mode_3()

        self.m.cleanup()

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
        end_date = datetime.date.today() + datetime.timedelta(days=1)

        view_range = self.v.get_view_range()
        view_detail = self.v.get_show_detail()
        if view_range == 1:  # list today
            begin_date = datetime.date.today()
        elif view_range == 2:  # list last 7 days
            begin_date = datetime.date.today() - datetime.timedelta(days=6)
        else:
            begin_date = datetime.date.today()  # default
        logs = self.m.load_range(begin_date, end_date)
        self.v.show_stats(logs)
        if view_detail:
            self.v.show_stats(logs, True)

    def mode_3(self):
        # modify logs
        pass

    def get_args(self):  # set up argparse
        parser = argparse.ArgumentParser(description='A simple utility that logs tasks.')
        parser.add_argument('-g', dest='gui_mode', action='store_const',
                            const=True, default=False,
                            help='start the program with GUI (default: No)')
        return parser.parse_args()


controller = Controller()
controller.main()
