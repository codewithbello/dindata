import csv
from datetime import datetime, timedelta
from time import strftime
import pandas as pd
import numpy as np
import re
from datetime import datetime
from threading import Thread
from kivy.app import App
from tkinter import filedialog
from tkinter import Tk
import os
import ctypes.wintypes


class DINDataCodeRun:
    # class attributes
    # instance attributes
    def __init__(self, start_year, start_month, start_day, end_year, end_month, end_day, cs_score, file_path='',
                 only_path=''):
        self.start_year = start_year
        self.start_month = start_month
        self.start_day = start_day
        self.end_year = end_year
        self.end_month = end_month
        self.end_day = end_day
        self.path = file_path
        self.save_path = only_path
        self.cs_score = cs_score

    # instance methods
    #    -------------------------- Date generator creates the 15min interval date for the period the user enters. ---------
    def dateGenerator(self):
        date = []
        root = App.get_running_app().root
        logger = root.log_to_terminal

        try:
            startDate = datetime(self.start_year, self.start_month, self.start_day, 0, 0)
            endDate = datetime(self.end_year, self.end_month, self.end_day, 23, 59)
            increment = 15
            while startDate <= endDate:
                date.append(startDate.strftime("%Y-%m-%dT%H:%M:%S.%S0Z"))
                startDate = startDate + timedelta(minutes=increment)
        except:
            logger('Error, failed to generate dates', 'error')
            root.ids.spinner.active = False
            exit()

        return date

    # ---------------------------------- Data Reader: Reads the data and formats it ---------------------------------
    def ionogramNumReader(self, comment='# ', comment2='#\n', sep=' '):
        filename = r"{}".format(self.path)
        rawString = '\\'
        filename.replace(rawString, '/')
        raw_data = []
        root = App.get_running_app().root
        logger = root.log_to_terminal

        # Try and except  and show error (Wrong dataset uploaded) in the UI
        try:
            fileID = open(filename, 'r')
            lines = fileID.readlines()
            for line in lines:
                if not (line.startswith(comment) or line.startswith(comment2)):
                    t = "{}".format(line.strip())
                    t = re.sub("\s+", ",", line.strip()).split(',')
                    raw_data.append((t))
            raw_data = pd.DataFrame(raw_data)
        except:
            logger('Wrong dataset uploaded', 'error')
            root.ids.spinner.active = False
            exit()

        # print("DataFrame Created")
        return raw_data

    # Saving File: Browsing location
    def save_file(self):
        Tk().withdraw()
        path_file = filedialog.askdirectory()
        return path_file

    def cleaner(self, launch=True):
        if launch:
            Thread(target=self.cleaner, args=[False], daemon=True).start()
            return

        root = App.get_running_app().root
        logger = root.log_to_terminal

        generatedDates = self.dateGenerator()
        logger('Date generated', 'success')

        raw_data = self.ionogramNumReader()
        logger('Ionogram data successfully read. Dataframe created', 'success')

        logger('Processing...')

        try:
            col_names = list(raw_data.iloc[0])
            col_names[0] = col_names[0].replace("#", '')  # To remove '#' from '#Time'
            raw_data.columns = col_names

            raw_data.drop(labels=0, axis=0, inplace=True)
            raw_data.reset_index(drop=True, inplace=True)
            raw_data.drop('QD', axis=1, inplace=True)

            # Create a DataFrame from the generated date
            complete_data = pd.DataFrame(generatedDates, columns=[col_names[0]])

            # Lookup date fields in raw_data and merge column to completed_data
            df_Data = pd.merge(raw_data, complete_data, how='right')

            # Find '---' and replace with NaN
            df_Data.replace('---', np.nan, inplace=True)

            # Convert CS columns to int
            df_Data['CS'] = pd.to_numeric(df_Data['CS'], errors='coerce')

            # CS Filteration sequence
            heading = df_Data.columns
            df_Data.loc[df_Data['CS'] > 100, heading[2:]] = np.nan
            df_Data.loc[df_Data['CS'] < self.cs_score, heading[2:]] = np.nan
        except:
            logger('Data process failed', 'error')
            root.ids.spinner.active = False
            exit()
        logger('Data cleaning completed successfully', 'success')
        logger('Process completed', 'success')
        logger('Saving file...')

        #     ------------------------- This section handles the saving of the cleaned data to the user specified location ---
        # Get Current Time
        now = datetime.now()
        mytimestamp = now.strftime("%Y%m%d%I%M%S")

        # CISDL_PERSONAL = 5
        # SHGFP_TYPE_CURRENT = 0
        #
        # buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        # ctypes.windll.shell32.SHGetFolderPathW(0, CISDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, buf)
        #
        # # print(buf.value)
        # spath = f'{buf.value}/DINDATA'
        # if not os.path.exists(spath):
        #     os.makedirs(spath)
        spath = root.save_file()
        rawString = '\\'
        # if spath:
        spath.replace(rawString, '/')
        convertedDataFilePath = f'{spath}\\DINData{mytimestamp}.csv'
        df_Data.to_csv(convertedDataFilePath, index=False, encoding='utf-8')
        logger(f'File saved to {convertedDataFilePath}', 'success')

        root.ids.spinner.active = False
        exit()
