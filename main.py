from kivy import logger
from kivy.config import Config

Config.set('graphics', 'resizable', 0)
from kivymd.app import MDApp
from kivymd.uix.floatlayout import FloatLayout
# from kivymd.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.config import Config
from tkinter import Tk
from tkinter import filedialog
import datetime
from plyer import filechooser
from kivy.uix.boxlayout import BoxLayout
from DINDataCode import DINDataCodeRun
import re

Window.size = (600, 500)
Window.set_title('DINData')


class UI_layout(FloatLayout):
    log_index = 0

    def choose_file(self):
        # file = filechooser.open_file(title="Choose a file to upload")
        # file = filechooser.choose_dir(title=
        #                              "Select DIDBASE numerical ionogram file")
        # file = filechooser.save_file(title=
        #                               "Select DIDBASE numerical ionogram file")
        file = filechooser.open_file(title=
                                       "Select DIDBASE numerical ionogram file")
        self.file_path = ''
        self.path = ''

        if file:
            self.filename = file[0].split('\\')[-1]  # Filename
            self.file_path = file[0]
            # print(self.file_path)
            self.ids.file_path.text = self.filename
            self.path = '//'.join(file[0].split('\\')[0:-1])

    @staticmethod
    def save_file():
        Tk().withdraw()
        path_file = filedialog.askdirectory()
        return path_file

    @staticmethod
    def formatSpecChecker(date):
        match = re.search(r'(\d+-\d+-\d+)', date)
        try:
            match.group(1)
            return True
        except AttributeError:
            return False

    def validateTextInput(self):
        self.start_date = self.ids.Start_Date.text
        self.end_date = self.ids.End_Date.text
        self.CS = self.ids.CS_input.text or 0

        if self.start_date == '' or self.end_date == '' or self.CS == '':
            self.log_to_terminal('All text inputs must be correctly field', 'error')
            return False
        else:
            self.ids.Terminal_Line_1.text = ''

        isValidDate_start = self.formatSpecChecker(self.start_date)
        isValidDate_end = self.formatSpecChecker(self.end_date)

        if not isValidDate_start or not isValidDate_end:
            self.log_to_terminal('Enter the correct date', 'error')
            return False

        self.start_year, self.start_month, self.start_day = self.start_date.split('-')
        self.end_year, self.end_month, self.end_day = self.end_date.split('-')

        try:
            self.StartDate = datetime.datetime(int(self.start_year),
                                               int(self.start_month), int(self.start_day))

            self.EndDate = datetime.datetime(int(self.end_year),
                                             int(self.end_month), int(self.end_day))
        except ValueError:
            return False

        # Check if startDate is less than endDate
        if self.StartDate > self.EndDate:
            self.log_to_terminal('Starts date can not be greater than end date', 'error')
            return False

        if (int(self.CS) < 0) or (int(self.CS) > 100):
            self.log_to_terminalger('CS value should be between 0 and 100', 'error')
            return False

        return True

    def log_to_terminal(self, log, entry='info'):
        if entry == 'info':
            color = '[color=#ffffff]'
        elif entry == 'success':
            color = '[color=#00FF00]'
        else:
            color = '[color=#ff0000]'

        self.ids.Terminal_Line_1.text = f'{self.ids.Terminal_Line_1.text} {color}[{self.log_index}] {log}[/color]\n'

        self.log_index += 1

    def run_code(self):
        self.ids.spinner.active = True

        if self.validateTextInput():
            # self.ids.Terminal_Line_1.text = 'Program is running.... Do not interrupt'
            data = DINDataCodeRun(int(self.start_year), int(self.start_month), int(self.start_day),
                                  int(self.end_year), int(self.end_month),
                                  int(self.end_day), int(self.CS), self.file_path, self.path)
            data.cleaner()
            # self.log_to_terminal('Data cleaning completed successfully', 'success')
            self.clear('run')

        else:
            # print('invalid Date')
            self.log_to_terminal('Enter the correct data fields', 'error')
            self.ids.spinner.active = False

    def clear(self, ctgory ='main'):
        if ctgory == 'main':
            self.ids.Terminal_Line_1.text = ''
            self.ids.Start_Date.text = ''
            self.ids.End_Date.text = ''
            self.ids.file_path.text = ''
            self.ids.CS_input.text = ''
            self.log_index = 0
        else:
            # elf.ids.Terminal_Line_1.text = ''
            self.ids.Start_Date.text = ''
            self.ids.End_Date.text = ''
            self.ids.file_path.text = ''
            self.ids.CS_input.text = ''
            self.log_index = 0

    @staticmethod
    def open_info():
        Window.add_widget(InfoCard())


class InfoCard(FloatLayout):
    pass


class DINDataApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.icon = 'Dindata_logo.ico'
        self.root = UI_layout()


DINDataApp().run()
