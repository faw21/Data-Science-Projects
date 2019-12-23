# Repository: template.project1
# Assignment #1: Python 

> Course: **[CS 1656 - Introduction to Data Science](http://cs1656.org)** (CS 2056) -- Fall 2019  
> Instructor: [Alexandros Labrinidis](http://labrinidis.cs.pitt.edu)  
> 
> Assignment: #1.  
> Released: September 12, 2019  
> **Due:      September 26, 2019**

### Description
This is the **first assignment** for the CS 1656 -- Introduction to Data Science (CS 2056) class, for the Fall 2019 semester.

### Goal
The goal of this assignment is to familiarize you with the Python programming language and also expose you to real data.

### What to do -- mybikes.py
You are asked to write a Python program, called `mybikes.py` that will access live data from the [HealthyRidePGH website](https://healthyridepgh.com/) and provide answers to specific queries about shared bike availability in the Pittsburgh region.

You program should be invoked as:
```
python3 mybikes.py baseURL command [parameters]  
```
where baseURL is the prefix URL of the source of the data, and it is typically https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/, although we will modify that during testing, in order to evaluate your submitted programs with static data. It is important for your program to work with ANY proper baseURL.


### Data Feeds
Assume the baseURL parameter is stored in variable $baseURL. We will use two data feeds from the HealthyRidePGH General Bikeshare Feed Specification (GBFS) data feed, as follows:
* **Station Information**: $station_infoURL = $baseURL+'/station_information.json', which provides for each docking station: station_id, name, latitude 
 and longtitude, and the total capacity (e.g., [https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/station_information.json](https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/station_information.json)).   

* **Station Status**: $station_statusURL = $baseURL+'/station_status.json', which provides for each station_id how many bikes and how many docks are available at any given time (e.g., [https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/station_status.json](https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/station_status.json)).


You can find additional information about the GBFS specification at [https://github.com/NABSA/gbfs](https://github.com/NABSA/gbfs) and about all the available data feeds from HealthyRidePGH at [https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/gbfs.json](https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/gbfs.json).


### Command #1: Total bikes available
The command `total_bikes` will compute how many bikes are currently available over all stations in the entire HealthRidePGH network. 

Sample invocation:
```
python3 mybikes.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ total_bikes
```

Sample output of your script (meant to illustrate format only):
```
Command=total_bikes 
Parameters=
Output=123
```

### Command #2: Total docks available
The command `total_docks` will compute how many docks are currently available over all stations in the entire HealthRidePGH network. 

Sample invocation:
```
python3 mybikes.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ total_docks
```

Sample output of your script (meant to illustrate format only):
```
Command=total_docks
Parameters=
Output=168
```

### Command #3: Percentage of docks available in a specific station
The command `percent_avail` will compute how many docks are currently available for the specified station as a percentage over the total number of bikes and docks available. In this case, the station_id is given as a parameter.

Sample invocation:
```
python3 mybikes.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ percent_avail 342885
```

Sample output of your script (meant to illustrate format only):
```
Command=percent_avail
Parameters=342885
Output=76%
```
In our example, the num_bikes_available was 4, the num_docks_available was 13, so the percent available was 13/(4+13), i.e., 76%. You should appropriately round the percentage to be an integer. To simplify things, always round down (floor), i.e., return the highest integer that is not greater than the number you try to round.

### Command #4: Names of three closest HealthyRidePGH stations.
The command `closest_stations` will return the station_ids and the names of the three closest HealthyRidePGH stations based just on latitude and longtitude (of the stations and of the specified location). The first parameter is the latitude and the second parameter is the longtitude. 

Sample invocation:
```
python3 mybikes.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ closest_stations 40.444618 -79.954707
```

Sample output of your script (meant to illustrate format only):
```
Command=closest_stations
Parameters=40.444618 -79.954707
Output=
342885, Schenley Dr at Schenley Plaza (Carnegie Library Main) 
342887, Fifth Ave & S Dithridge St
342882, Fifth Ave & S Bouquet St
```
Note that the output starts on a new line and that the station_id is separated by the name of the station using a comma and a space. You should return one station per line, sorted in increasing distance from the provided lat/long coordinates (i.e., first one is the closest).

In order to compute the distance, you can use the following function:

```
from math import cos, asin, sqrt

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))
```

### Command #5: Name of the closest HealthyRidePGH station with available bikes
The command `closest_bike` will return the station_id and the name of the closest HealthyRidePGH station that has available bikes, given a specific latitude and longtitude. The first parameter is the latitude and the second parameter is the longtitude. 

Sample invocation:
```
python3 mybikes.py https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en/ closest_bike 40.444618 -79.954707
```

Sample output of your script (meant to illustrate format only):
```
Command=closest_bike
Parameters=40.444618 -79.954707
Output=342887, Fifth Ave & S Dithridge St
```





### Important notes about grading
It is absolutely imperative that your python program:  
* runs without any syntax or other errors (using Python 3)  
* strictly adheres to the format specifications for input and output, as explained above.     

Failure in any of the above will result in **severe** point loss. 


### Allowed Python Libraries (Updated)
You are allowed to use the following Python libraries (although a fraction of these will actually be needed):
```
argparse
collections
csv
json
glob
math 
os
pandas
re
requests
string
sys
time
xml
```
If you would like to use any other libraries, you must ask permission by Thursday, September 19, 2019, using [canvas](http://cs1656.org).


### About your github account
It is very important that:  
* Your github account can do **private** repositories. If this is not already enabled, you can do it by visiting <https://education.github.com/>  
* You use the same github account for the duration of the course  
* You use the github account that you specified during the test assignment (i.e., this one)  

### How to submit your assignment
For this assignment, you must use the repository that was created for you after visiting the classroom link. You need to update the repository to include file `mybikes.py` as described above, and other files that are needed for running your program. You need to make sure to commit your code to the repository provided. We will clone all repositories shortly after midnight (23:59pm):  
* the day of the deadline **Thursday, September 26th, 2019 (i.e., by 12:15am, Friday, September 27, 2019)**  
* 24 hours later (for submissions that are one day late / -5 points), and  
* 48 hours after the first deadline (for submissions that are two days late / -15 points). 

**You need to make sure you remember to submit your .py files. We will not grade IDE files (such as .classpath).**

Our assumption is that everybody will submit on the first deadline. If you want us to consider a late submission, you need to email us at `cs1656-staff@cs.pitt.edu`

