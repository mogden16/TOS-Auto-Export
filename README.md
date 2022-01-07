# TOS Auto Export

This program was BASED off Trey Thomas's Auto ToS Strategy Exporter which allows you to auto export strategy reports from the TDAmeritrades Thinkorswim desktop platform.

## Getting Started

This program has only been tested on Windows OS and MAC OSX.

You will need the Thinkorswim desktop application, for the program is created for this application specifically.
The program uses pyautogui to automate native keyboard and mouse functionalities.

*This is specific to strategies created by @Mightymorphinchris on useThinkscript but can be adjusted to be used for any strategy.

### Prerequisites

Dependencies: pyautogui, datetime, keyboard, os, csv, time, pprint, shutil, statisics, requests, glob, BeautifulSoup, codecs, pandas, numpy, tqdm, dotenv

Desktop App: TDAmeritrade's ThinkOrSwim

Language: Python 3.8+

### First thing we need to do is setup the Thinkorswim app.

1. Go into your thinkscript editor for the strategy of your choice and plot a SMA or anything that will plot a line, and multiply it by 2 or more. (See image below)
2. Once entered, apply and save.

![Alt text](/img/thinkscript_editor_add_sma.png)

3. Once back at the main screen, go to your chart where you are displaying the strategy that you just added the SMA line to. Notice how high it is above the actual candles. Thats what we want. (See image below)

![Alt text](/img/sma_line.png)

4. Next, double click on the SMA line, and a customizing popup will display. Click on the plots dropdown, then click on the SMA tab. The image below is what should be displayed.

![Alt text](/img/customize_sma_line.png)

5. Next, we need to change the draw as display, which changes how the plot is shown on the chart.
6. We need to change this to a bar graph that covers the entire chart. (See image below)

![Alt text](/img/customize_sma_line_to_cover.png)

7. Click apply, and save.
8. You should now have something like the image below.

![Alt text](/img/basic_chart_cover.png)

9. You will also need to set up your total timeframes to cycle through if you want to do multi-overall timeframes.
10. Click your chart timeframe and click -> customize timeframe.
11. Make sure 30D:1m, 30D:2m, and 30D:3m are at the absolute top of your chart.  Click 30D:1m to make that active (even if you don't want to start with 1m TFs)

![Alt text](/img/chart_tfs.png)


### Getting coordinates for key locations based on your screen size

- There are key locations that you must obtain so the program knows where to send the cursor.
- The images below will show the locations.
- All of these coordinates will need to be set in accordance to where they are needed in the program. All of the locations are in the env file.
- MAKE SURE TO RENAME THE example_config.env AS config.env

1. First, you will need to open the config.env.  Set the delays (delay=a quick delay, min 2 is recommended.  This will be how many seconds it waits to click something else.
extended_delay=how long you want to wait for your strategy to load & do calculations (60-75min recommended).
   num_of_iterations_perAgg=how many aggregations do you want to go thru starting from 1m) (1m/2m/3m/4m/5m/10m/15m/20m/30m/1hr/2hr/4hr/1d)

2. Set the default study location.  You can find this if you try to export a study (what folder does it automatically bring up?).  Make sure there is are quotes around this ('xxxx').

3. Set the new destination directory location (dst_dir).  It will make subfolders in here for 1m/2m/3m.  Where do you want to save your new studies?


    Use Mofiki Coordinate finder to find these coordinates
4. Location of the chart timeframe button
   
![Alt text](/img/tfbutton.png)

5. Location of your first right click on the chart to bring up your settings or report
   (anywhere in that shaded space).

6. Location of the middle of your agg1 setting (red)

7. Location of the middle of your agg2 setting (green)

![Alt text](/img/aggchanges.png)


8. Location of the tradetype setting (not used currently)


9. Specific location used on the scrollbar to scroll up on agg1 (will be clicked twice to scroll to the top) do this for agg2 too.
   
![Alt text](/img/aggslider.png)

10. Location of the OK button on the settings

![Alt text](/img/okaybutton.png)


11. Location of Export file button

![Alt text](/img/exportfile.png)

12. Location of Files of Type button (it will automatically say .csv)

![Alt text](/img/exportfile.png)

13. Location of Save strategy button

![Alt text](/img/savefile.png)

14. Location of Close strategy button


15. Webhook to integrate with Discord (string)
Add your webhook to your discord to have the results posted to there.  You might have an issue if you don't have it.  Make sure it's in quotes.


# How to run it
1. Install all of the packages
2. Run:    python updatedmain.py
3. It will ask you what total timeframes you'll want to run and it will always go smallest to largest.
   1. ex. entering (3, enter, 2, enter, 1, enter, DONE, enter) will run 1/2/3
   2. Please don't enter anything else besides 1,2,3,or DONE