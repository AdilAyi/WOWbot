Directory of the WOWbot

directory setup in such a way the WOWbot can work well. First of all there are 2 directories under this one:

the WOWbot:
-> "data_extracted": This  is the directory where all the results gets pushed to from the wowbot. These are CSV files with in the name the date and time of the extraction
-> "shapefile": This is the directory with the shapefile of the netherlands. There are 3 different resolutions for the shapefile: [1km, 10km, 100km]. The default is set at 10km for the filtering of stations.


backuo_extraction.csv is the previous file you want to give the bot to only update. This means that the bot will not extract stations you already have data of and only extracts new bots if any.

get_ids.ipynb is a script in which the html files of the wow_nl website can be given to extract the station_ids from.

