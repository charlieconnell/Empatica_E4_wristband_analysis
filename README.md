# Empatica_E4_wristband_analysis
Python scripts that can be used to organize multiple participant files collected via the Empatica E4 wristband

The file structure and their associated functions are outlined below:

bin —————--------- directory that stores the source code for analysis
	|- organize_data.py ---> script will prompt you to pick the unzipped participant folder you want to analyze.
|- tag_data.py ———->  script prompts you to pick the participant excel file (from the ‘raw’ folder) to tag and sync            and saves it as a pickled file in the ‘interim’ folder.
|- grab_pickle.py------->  script grabs all the pickles in the ‘interim’ folder and combines them together into summary data sets for acc, eda, bvp, ibi and heart rate and saves them to the ‘processed’ folder. 
data —————------- directory that contains folders where data at different stages of processing reside
	|—dump—————> .csv files stored in long format with all data stored here.
	|—interim—————> pickled participant files stored here
	|—processed———> .csv files with columns time(s) and participants for each measure. All tags 						synchronized at the 60s time point
	|—raw——————> individual participant excel files from the organize data script are saved here
	|—unzipped-folders-> store unzipped participant folders here
visualization——------where scripts to produce data visualizations can go (at 25/09/2017 this folder is empty)

Steps for analysis

1. Organize acc, eda, bvp, ibi, tags and heart rate files within unzipped participant folders into a single, uniquely labeled excel file:

•	After data collection, move unzipped participant folders to the ‘unzipped-folders’ folder within the ‘data’ directory
•	Open Spyder application to run python scripts in.
•	Open ‘organize_data.py’ script in Spyder application.
•	‘Run’ the ‘organize_data.py’ script in Spyder by pressing the green play button on the toolbar located at the top of the application.
•	A file dialog box with pop-up – use this to navigate to the ‘unzipped-folders’ folder within the data directory and select the participant folder you would like to organize. 
NOTE: The script will take a variable amount of time to execute, depending on the size of the participant files. You can tell the stage of script execution by looking at the Ipython console embedded within Spyder (the Ipython console is usually located in the lower right quadrant of the application). If the script is still executing, the square in the top right of the Ipython console (the ‘stop’ button) will be filled in red, and the cursor will be absent from the console, preventing you from executing any code while the script is running. If for some reason you wish to stop the script in the middle of execution, select the ‘stop’ button. When the script has been executed, the cursor will reappear in the Ipython console, and the variables created by the script will be visible in the ‘Variable explorer’ in the top right quadrant of the Spyder application. 
•	Check that a participant file has been successfully added as an Excel document to the ‘raw’ folder within the ‘data’ directory.

2. Locate tags within an organized participant data excel file and add a normalized time series relative to the tag and the sampling rate of the outcome measure.

•	Within the Spyder application, open and run the ‘tag_data.py’ script.
•	A file dialog box with pop-up – use this to navigate to the ‘raw’ folder within the data directory and select the participant file you would like to normalize relative to the tags.
NOTE: the duration of time (in seconds) that you want to have before the tag, i.e. the time set as ‘zero’ on the normalized time series, can be altered within the ‘grab_pickle_data.py’ script on line 35.
•	Check that a new participant file has been successfully saved as an ‘pickled’ file (file extension: .p) to the ‘interim’ folder within the ‘data’ directory.

3. Collect all the ‘pickled’ data files in the ‘interim’ folder and combine them into summary files with the format:
Column 1: Normalized time; Column 2: Participant 2#### ….. Column n: Participant n#####.

•	Once you have a collection of pickled files in the ‘interim’ folder within the ‘data’ directory, open and run the python script ‘grab_pickle.py’ in the Spyder application.
•	No file dialog box will pop up – the script will simply collect all the pickled files in the ‘interim’ folder automatically.
•	There are two types of data files that are exported as a result of this script:
o	‘acc’, ‘ibi’, ‘bvp’, ‘eda’ and ‘hr’ .csv files are exported to the ‘processed’ folder within the data directory. These files contain a normalized time series in column one, and one participant per column. The time that the tags occur for each participant are synchronized to the time that the user has input into line 35 of the ‘grab_pickle.py’ script (‘time_pre_tag’ variable; default value is 60 seconds).
o	‘acc’, ‘ibi’, ‘bvp’, ‘eda’ and ‘hr’ .csv files are exported to the ‘dump’ folder within the data directory. These data are provided in ‘long’ format. While difficult to read and understand at a glance, data files in this format are easier to manipulate for further data analysis in excel, python, R etc. if needed. For more information on data files in ‘long format’ please review Hadley Wickham’s paper on ‘Tidy Data’ (http://vita.had.co.nz/papers/tidy-data.html).

