# Repository: template.project56
# Term Project 

> Course: **[CS 1656 - Introduction to Data Science](http://cs1656.org)** (CS 2056) -- Fall 2019  
> Instructor: [Alexandros Labrinidis](http://labrinidis.cs.pitt.edu)  
> 
> Term Project  
> Released: November 20, 2019  
> **Due:      December 10, 2019**

### Description
This is the **term project** for the CS 1656 -- Introduction to Data Science (CS 2056) class, for the Fall 2019 semester.

### Goal
The goal of this project is to expose you with a real data science problem, looking at the end-to-end pipeline. 

### What to do 
You are asked to write a Python Jupyter notebook, called `bikeviz.ipynb` that will:
* [Task 1] access historical bike rental data for 2019 from HealthyRidePGH and summarize the rental data  
* [Task 2] create graphs to show the popularity of the different rental stations, given filter conditions  
* [Task 3] create graphs to show the rebalancing issue  
* [Task 4] cluster the data to group similar stations together, using a variety of clustering functions and visualize the results of the clustering.  

We present the details of each task next. You are provided with a skeleton `bikeviz.ipynb` Jupyter notebook file which you should use.

### Task 1 (20 points)
In this task you will need to access historical bike rental data for 2019 from HealthyRidePGH and summarize it.

We will use historical rental data from HealthyRidePGH, available at [https://healthyridepgh.com/data/](https://healthyridepgh.com/data/). 
In particular, we will use data for the first three quarters of 2019: 
* Q1: [http://data.cs1656.org/project/HealthyRideRentals2019-Q1.csv](http://data.cs1656.org/project/HealthyRideRentals2019-Q1.csv)  
* Q2: [http://data.cs1656.org/project/HealthyRideRentals2019-Q2.csv](http://data.cs1656.org/project/HealthyRideRentals2019-Q2.csv)  
* Q3: [http://data.cs1656.org/project/HealthyRideRentals2019-Q3.csv](http://data.cs1656.org/project/HealthyRideRentals2019-Q3.csv)  

Each row in the file shows one rental transaction, indicating the bicycle ID, the source bike station (from station) and the destination bike station (to station). Worth noting:
* if there is no station ID, then this was usually a ``dockless'' bike, e.g., `BIKE 70000`,  
* if a bike was ``magically'' moved from one station to a different one, that means this happened as a result of rebalancing, where HealthyRidePGH staff relocated the bike using a truck to address demand imbalance.   

To make your program run faster, you are asked to donwload the files in the same directory as your Jupyter notebook and read them in your program as local files. You are also asked to not change the filenames. When your assignments are graded, we will make sure the same files are there (i.e., you do not need to upload them with your repo onto github).

For this task, you will need to read in all the CSV data and create appropriate data structures (**HINT: use dataframes**) to record the following information, for every date (_year, month, day_), for every station (_stationID_):
- **fromCNT** = total number of ``from'' bikes at that station for that day (i.e., number of transactions with that _stationID_ in the **from** column)
- **toCNT** = total number of ``to'' bikes at that station for that day (i.e., number of transactions with that _stationID_ in the **to** column)
- **rebalCNT*** = total number of ``rebalanced'' bikes. See the next section for an explanation on how to compute this.  


* **Task 1.1** Print the first 20 rows of the data structure you used to store the above data (i.e, **daily breakdown**).

You should also aggregate the above data at the month level as well, i.e., for every month, station combination record the total fromCNT, total toCNT, and total rebalCNT. 

* **Task 1.2** Print the first 20 rows of the data structure you used to store the above data (i.e., **monthly breakdown**).



### How to compute the rebalancing
For every bikeID we need to figure out cases where when the data is sorted by bikeID trip start time.

Consider the following snipet from the Q2 data:

|Trip id | Starttime | Stoptime | Bikeid | Tripduration | From station id | From station name | To station id | To station name | Usertype |  
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | 
|66669783 | 4/1/19 16:31 | 4/1/19 17:41 | 70000 |4178	| 1047	|S 22nd St & E Carson St	|1046	|S 25th St & E Carson St	|Customer|  
|67181259 | 4/6/19 18:56	| 4/6/19 19:08 | 70000 | 719	| 49301	|Centre Ave & N Craig St	|1024	|S Negley Ave & Baum Blvd	|Subscriber |   
|67425370 | 4/8/19 16:45	| 4/8/19 16:50 | 70000 | 305	| 1024	|S Negley Ave & Baum Blvd	|1026	|Penn Ave & S Whitfield St	|Customer  |  

The first line indicates a rental from stationID = 1047 to stationID = 1046.
The second line indicates a rental from stationID = 49301 to stationID = 1024. This implies rebalancing, as somehow this bike was taken off circulation and put back in circulation in a different station (49301) than what was dropped off by a customer/subscriber earlier (1046).
The third line indicates a rental from stationID = 1024 (where it was left off before) to stationID = 1026.

So in this case you will need to increase by one the rebalancing count for 4/8/19 for stationID = 1024.

Note that you should not consider dockless stations (e.g., BIKE 70000) as stations; only consider as stations those with a proper stationID value.

Finally, note that a simple version, where you just take rebalCNT = fromCNT - toCNT will work as an **approximation**, since it counts as rebalancing bikes that were left at the station and not used. If you have trouble or ran out of time, this is an appropriate shortcut for partial credit (-8 points).


### Task 2 (30 points)
In this task you will need to create graphs to show the popularity of the different rental stations, given filter conditions.

For this task you assume two variables containing input from the user:
* **filter_month** which corresponds to the month of interest (1-9, should have a default value of 4, i.e., April), and  
* **filter_stationID** which corresponds to the stationID of interest (should have a default value of 1046).  

Given the above two variables, you should create the following graphs:
* **Task 2.1** Show a bar chart for the 25 most popular bikestations when considering the number of **fromCNT** per station (for filter_month). Y axis should be the fromCNT per station, X axis should be the stationID. The first stationID corresponds to the most popular station. 

* **Task 2.2** For the filter_month and for the filter_stationID show a graph that shows the distribution of bike rentals throughout the month, for that station only. Y axis should be the fromCNT for that stationID for that day, X axis would be the different days in that month (i.e., 1 - 30 for April). 

* **Task 2.3** Update your data structure to compute the total number of rentals each bike had for each day (regardless of station). In other words, figure out how many times a bike was listed in the input data, for each different date. For the filter_month, show a graph that shows the 25 most popular bikes. Y axis should be the number of times a bike was rented, X axis should be the bikeID. The first bikeID corresponds to the most popular station.

  
### Task 3 (20 points)
In this task you will create graphs to show the rebalancing issue.

* **Task 3.1** Show a bar chart for the 25 most popular bikestations when considering the number of **rebalCNT** per station (for filter_month). Y axis should be the rebalCNT per station, X axis should be the stationID. The first stationID corresponds to the most demanding station in terms of rebalancing. 

* **Task 3.2** For the filter_month and for the filter_stationID show a graph that shows the distribution of bike rebalancing throughout the month, for that station only. Y axis should be the rebalCNT for that stationID for that day, X axis would be the different days in that month (i.e., 1 - 30 for April). 


### Task 4 (30 points)
In this task you will cluster the data to group similar stations together, using a variety of clustering functions and visualize the results of the clustering. 

For this task, you should create a data structure where for each stationID you record the following features:
* 3 variables for the total fromCNT for each station for each of the 3 months of the third quarter (i.e., 7, 8, 9)   
* 3 variables for the total rebalCNT for each station for each of the 3 months of the third quarter (i.e., 7, 8, 9)  

This creates a 6-dimensional space for the different stations. 

* **Task 4.1** You should perform clustering on the above 6-dimensional space using K-means (with at least 3 different values for K) and DBSCAN  (with at least three different value combinations for min_samples and eps) [https://scikit-learn.org/stable/modules/clustering.html#clustering](https://scikit-learn.org/stable/modules/clustering.html#clustering). 

* **Task 4.2** You should generate one bar chart per algorithm option (i.e., 6 different charts) showing the distribution of the number of stations per cluster. Y axis should be the number of stations in that cluster, X axis would be the clusterID. The first clusterID corresponds to the biggest cluster. Make sure each graph is properly labeled with the algorithm name and the parameters used. 

* **Task 4.3** You should provide a brief explanation about your choice of K and the additional clustering algorithm. This should be in the form of plain text inside the Jupyter notebook, under the Task 4.3 heading. You should also mention (a) what is the best value of K and (b) what is the best algorithm out of the three that you tried. For the second question, it is possible the results will be inconclusive. 


### Important notes about grading
It is absolutely imperative that your Jupyter notebook program:  
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
matplotlib
os
pandas
re
requests
sklearn
string
sys
time
xml
```
If you would like to use any other libraries, you must ask permission by Monday, December 2nd, 2019, using [canvas](http://cs1656.org).


### About your github account
It is very important that:  
* Your github account can do **private** repositories. If this is not already enabled, you can do it by visiting <https://education.github.com/>  
* You use the same github account for the duration of the course  
* You use the github account that you specified during the test assignment (i.e., this one)  

### How to submit your assignment
For this assignment, you must use the repository that was created for you after visiting the classroom link. You need to update the repository to include the one Jupyter notebook files `bikeviz.ipynb` as described above, and other files that are needed for running your program. You do not need to supply the bike rental data files. You need to make sure to commit your code to the repository provided. 

We will grade your projects using **Tuesday, December 10th, 2019 at 23:59pm** as the timestamp. We will not accept late submissions, but we will grade the projects even if only some of the tasks are completed (for partial credit).
