import pyautogui
from datetime import datetime
import os
import csv
import time
from pprint import pprint
import shutil
from playsound import playsound
import keyboard
import statistics
import requests
import glob
from bs4 import BeautifulSoup
import codecs
import pandas as pd
import numpy as np
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv(dotenv_path=f"{os.path.abspath(os.path.dirname(__file__))}/config.env")

num_of_iterations_perAgg=int(os.getenv('num_of_iterations_perAgg'))

tfbutton_x = float(os.getenv('tfbutton_x'))
tfbutton_y =float(os.getenv('tfbutton_y'))
firstclick_x = float(os.getenv('firstclick_x'))
firstclick_y =float(os.getenv('firstclick_y'))
middleof_agg1_x=float(os.getenv('middleof_agg1_x'))
middleof_agg1_y=float(os.getenv('middleof_agg1_y'))
okbutton_x=float(os.getenv('okbutton_x'))
okbutton_y=float(os.getenv('okbutton_y'))
exportFile_x=float(os.getenv('exportFile_x'))
exportFile_y=float(os.getenv('exportFile_y'))
filesofType_x=float(os.getenv('filesofType_x'))
filesofType_y=float(os.getenv('filesofType_y'))
savebutton_x=float(os.getenv('savebutton_x'))
savebutton_y=float(os.getenv('savebutton_y'))
exitstrat_x=float(os.getenv('exitstrat_x'))
exitstrat_y=float(os.getenv('exitstrat_y'))
scrollbar_x=float(os.getenv('scrollbar_x'))
scrollbar_y=float(os.getenv('scrollbar_y'))
scrollbar2_x=float(os.getenv('scrollbar2_x'))
scrollbar2_y=float(os.getenv('scrollbar2_y'))
middleof_agg2_x=float(os.getenv('middleof_agg2_x'))
middleof_agg2_y=float(os.getenv('middleof_agg2_y'))
tradetype_x=float(os.getenv('tradetype_x'))
tradetype_y=float(os.getenv('tradetype_y'))

discord_webhook=(os.getenv('discord_webhook'))


class AutoExport:

    def __init__(self):

        # THIS WILL BE THE AMOUNT OF TIMEFRAMES THAT YOU CYCLE THROUGH
        self.working_tf = []
        self.tradingSide = []

        # ADJUST THIS TO ALLOW FOR SLOWER OR FASTER MOVEMENTS
        # DELAY MAY NEED TO BE INCREASED BASED ON INTERNET SPEED AND AGGREGATION/LENGTH OF CHARTS
        # THIS IS NEEDED BECAUSE SOMETIMES THE CHARTS DO NOT LOAD FAST ENOUGH
        self.delay = float(os.getenv('delay'))  # 0.15
        self.extended_delay = float(os.getenv('extended_delay'))

        # THIS IS THE WATCHLIST FILE FROM TOS, WHICH IS FORMATED WITH THE CURRENT DATE OF WHICH DOWNLOADED
        self.watchlist_file = f"{datetime.now().strftime('%Y-%m-%d')}-watchlist.csv"

        # PATH TO USERS DOCUMENTS FOLDER. THIS IS WHERE TOS DOWNLOADS THE STRATEGY REPORTS
        self.path=(os.getenv('tos_study_path'))
        self.picture_path=((os.getenv('dst_dir')) + str(self.working_tf)+ 'm/pics/')
        self.new_study_path=None

        # ADDED CONDITIONAL FOR THE WHILE LOOP IN START METHOD.
        # IF ERROR, ATTRIBUTE WILL BE SET TO FALSE AND WHILE LOOP WILL STOP
        self.no_error = True

        self.on_start = False


    def throwError(self, error):

        self.no_error = False

        for _ in range(1):

            print(error)

#         # REMOVE ALL EXISTING STRATEGY REPORTS CSV FILES FROM DOCUMENTS FOLDER
#         for file in os.listdir(export.path):
#
#             sep = file.split("_")
#
#             if file.endswith(".html"):
#
#                 try:
#
#                     os.remove(os.path.join(export.path, file))
#
#                 except:
#
#                     pass

    def getWatchlist(self):

        proceed = input("What TFs are you using? (1/2/3): ")
        while proceed != "DONE":
            self.working_tf.append(proceed.upper())
            proceed = input("Any other TFs? Type DONE when finished: ")

#         side = input("What side to you want to trade? (long/short/both): ")
#         while side != "DONE":
#             self.tradingSide.append(side.upper())
#             side = input("Any other side you want to see? Type DONE when finished")

        self.working_tf.sort()
        print("BEGINNING AUTO EXPORTS....")
        time.sleep(2)
        self.start()


    def moveHTMLFile(self, tf):

        # ABSOLUTE PATH TO CSV_FILES DIRECTORY
        self.new_study_path=((os.getenv('dst_dir')) + str(tf)+ 'm/')
        print(f"Moving files to: {self.new_study_path}")

        for file in tqdm(glob.glob(self.path + '*.html')):

            try:

                # MOVES MOST RECENT STRATEGY REPORT FILE FROM DOCUMENTS FOLDER TO CSV_FILES FOLDER

                shutil.move(file, self.new_study_path)

            except shutil.Error as e:

                self.throwError(e)



    def createDATAFRAME(self):
        files = glob.glob(self.new_study_path + '*.html')
        df = pd.DataFrame()

        for f in tqdm(files):
            newdf = pd.read_html(f, header=0)[0].set_index('Id')
            newdf['Strategy'] = os.path.basename(f)
            df = pd.concat([df, newdf])

        df['Trade P/L'] = df['Trade P/L'].str.replace(',', '',regex=False)
        df['Trade P/L'] = df['Trade P/L'].str.replace('$', '',regex=False)
        df['Trade P/L'] = df['Trade P/L'].str.replace('(', '-',regex=False)
        df['Trade P/L'] = df['Trade P/L'].str.replace(')', '',regex=False)
        df['Trade P/L'] = pd.to_numeric(df['Trade P/L'], errors='coerce')

        TotalP_L = df.groupby(['Strategy']).sum()['Trade P/L']

        CountTrades = df.groupby(['Strategy']).size()

        TotalP_Lcommission = TotalP_L - (CountTrades * .65)

        df2 = pd.concat([TotalP_Lcommission, CountTrades], axis=1)
        df2.columns = ['Total P/L minus Commission', 'Number of Trades']
        df2['P/L per Trade'] = round(df2['Total P/L minus Commission'] / df2['Number of Trades'], 2)

        df2 = df2.sort_values('P/L per Trade', ascending=False)
        df3 = df2.head()
        print(df3)

        discord_message_to_push = {"content": df3.to_string()}
        response = requests.post(discord_webhook, json=discord_message_to_push)

    def switchTotalTFs(self, tf):

        if tf == '1':
            return

        elif tf == '2':
            pyautogui.moveTo(tfbutton_x, tfbutton_y) # ABSOLUTE
            time.sleep(self.delay)
            pyautogui.click()
            time.sleep(self.delay)
            pyautogui.move(0,82) #RELATIVE
            time.sleep(self.delay)
            pyautogui.click()
            time.sleep(self.extended_delay)

        elif tf == '3':
             pyautogui.moveTo(tfbutton_x, tfbutton_y) # ABSOLUTE
             time.sleep(self.delay)
             pyautogui.click()
             time.sleep(self.delay)
             pyautogui.move(0,107) #RELATIVE
             time.sleep(self.delay)
             pyautogui.click()
             time.sleep(self.extended_delay)

#     def setTradeSide(self):
#         if self.tradingSide = "LONG":
#             pyautogui.moveTo(tradetype_x, tradetype_y)
#             time.sleep(self.delay)
#             pyautogui.moveTo()

    def switchAgg1(self, agg, agg2, study, tf):
        picture_path = ((os.getenv('dst_dir')) + str(tf) + 'm/pics/' + str(study) + '.png')
        # SHOW SETTINGS BUTTON
        pyautogui.rightClick(firstclick_x, firstclick_y) # ABSOLUTE
        time.sleep(self.delay)
        pyautogui.move(57, 22) # RELATIVE
        time.sleep(self.delay)
        pyautogui.click()
        time.sleep(self.delay)

        # RESET TFS
        if agg == 0:
            pyautogui.moveTo(middleof_agg1_x, middleof_agg1_y)
            pyautogui.click()
            time.sleep(self.delay)
            pyautogui.moveTo(scrollbar_x, scrollbar_y)
            time.sleep(self.delay)
            pyautogui.click()
            pyautogui.click()
            time.sleep(self.delay)
            if tf == '1':
                pyautogui.move(-53, -2)
                time.sleep(self.delay)
                pyautogui.click()
                time.sleep(self.delay)
            elif tf == '2':
                pyautogui.move(-53,21)
                time.sleep(self.delay)
                pyautogui.click()
                time.sleep(self.delay)
            elif tf == '3':
                pyautogui.move(-53,47)
                time.sleep(self.delay)
                pyautogui.click()
                time.sleep(self.delay)
            if study == 0 or (agg==0 and agg2==0):
                pyautogui.moveTo(middleof_agg2_x, middleof_agg2_y)
                time.sleep(self.delay)
                pyautogui.click()
                time.sleep(self.delay)
                pyautogui.moveTo(scrollbar2_x, scrollbar2_y)
                time.sleep(self.delay)
                pyautogui.click()
                pyautogui.click()
                time.sleep(self.delay)
                if tf == '1':
                    pyautogui.move(-53, -2)
                    pyautogui.click()
                    time.sleep(self.delay)
                elif tf == '2':
                    pyautogui.move(-53, 21)
                    pyautogui.click()
                    time.sleep(self.delay)
                elif tf == '3':
                    pyautogui.move(-53, 47)
                    pyautogui.click()
                    time.sleep(self.delay)
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save(picture_path)
            pyautogui.moveTo(okbutton_x, okbutton_y)
            pyautogui.click()
            time.sleep(self.extended_delay)

        # CHANGE THE AGGREGATION
        if agg != 0:
            pyautogui.moveTo(middleof_agg1_x, middleof_agg1_y)
            time.sleep(self.delay)
            pyautogui.click()
            time.sleep(self.delay)
            pyautogui.move(0,58)
            time.sleep(self.delay)
            pyautogui.click()
            time.sleep(self.delay)
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save(picture_path)
            pyautogui.moveTo(okbutton_x, okbutton_y)
            pyautogui.click()
            time.sleep(self.extended_delay)


        # BRING UP REPORT
        pyautogui.rightClick(firstclick_x, firstclick_y) # ABSOLUTE
        time.sleep(self.delay)
        pyautogui.move(19,86)
        pyautogui.click()
        time.sleep(self.delay+5)

        # EXPORT FILE BUTTON
        pyautogui.moveTo(exportFile_x, exportFile_y)
        time.sleep(self.delay)
        pyautogui.click()

        # SWITCH TO HTML
        pyautogui.write(str(study))
        pyautogui.moveTo(filesofType_x, filesofType_y)
        time.sleep(self.delay)
        pyautogui.click()
        pyautogui.move(10, 35) # RELATIVE
        time.sleep(self.delay)
        pyautogui.click()


        # SAVE BUTTON (save strategy report to documents folder)
        pyautogui.moveTo(savebutton_x, savebutton_y) # ABSOLUTE
        time.sleep(self.delay)
        pyautogui.click()
        time.sleep(self.delay)

        # CLOSE BUTTON (close out of the strategy report)
        pyautogui.moveTo(exitstrat_x, exitstrat_y) # ABSOLUTE
        time.sleep(self.delay)
        pyautogui.click()
        time.sleep(self.delay)


    def switchAgg2(self, agg2, study):
        # SHOW SETTINGS BUTTON
        pyautogui.rightClick(firstclick_x, firstclick_y) # ABSOLUTE
        time.sleep(self.delay)
        pyautogui.move(57, 22) # RELATIVE
        time.sleep(self.delay)
        pyautogui.click()
        time.sleep(self.delay)

        # CHANGE SMI AGG2
        pyautogui.moveTo(middleof_agg2_x, middleof_agg2_y)
        time.sleep(self.delay)
        pyautogui.click()
        pyautogui.move(0,60)
        time.sleep(self.delay)
        pyautogui.click()
        time.sleep(self.delay)

        # SAVE SETTINGS
        pyautogui.moveTo(okbutton_x, okbutton_y)
        time.sleep(self.delay)
        pyautogui.click()
        time.sleep(self.delay)



    def start(self):

        study=0

        for tf in tqdm(self.working_tf):
            for agg2 in tqdm(range(num_of_iterations_perAgg),leave=False):
                for agg in tqdm(range(num_of_iterations_perAgg),leave=False):
                    print("starting: agg",agg)
                    print("starting: agg2=",agg2)
                    print("starting: study=",study)

                    self.switchAgg1(agg, agg2, study, tf)
                    study+=1

                # SEND TO DISCORD
                discord_message_to_push = {"content": f"finished first column, changing agg2 by 1"}
                response = requests.post(discord_webhook, json=discord_message_to_push)
                self.switchAgg2(agg2, study)

            self.moveHTMLFile(tf)
            self.createDATAFRAME()
            self.switchTotalTFs(tf)


        print('WE HAVE COMPLETED! CONGRATS!')
        discord_message_to_push = {"content": f"WE HAVE COMPLETED! CONGRATS!"}
        response = requests.post(discord_webhook, json=discord_message_to_push)
        time.sleep(20)

###############



if __name__ == "__main__":

    export = AutoExport()

    time.sleep(2)

    export.getWatchlist()

