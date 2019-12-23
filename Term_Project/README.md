# Term Project 

### Goal
The goal of this project is to deal with a real data science problem, looking at the end-to-end pipeline. 

### What to do 
The file `bikeviz.ipynb` will:
* [Task 1] access historical bike rental data for 2019 from HealthyRidePGH and summarize the rental data  
* [Task 2] create graphs to show the popularity of the different rental stations, given filter conditions  
* [Task 3] create graphs to show the rebalancing issue  
* [Task 4] cluster the data to group similar stations together, using a variety of clustering functions and visualize the results of the clustering.  


### Task 1 (20 points)
Access historical bike rental data for 2019 from HealthyRidePGH and summarize it.

We will use historical rental data from HealthyRidePGH, available at [https://healthyridepgh.com/data/](https://healthyridepgh.com/data/). 
In particular, we will use data for the first three quarters of 2019: 
* Q1: [http://data.cs1656.org/project/HealthyRideRentals2019-Q1.csv](http://data.cs1656.org/project/HealthyRideRentals2019-Q1.csv)  
* Q2: [http://data.cs1656.org/project/HealthyRideRentals2019-Q2.csv](http://data.cs1656.org/project/HealthyRideRentals2019-Q2.csv)  
* Q3: [http://data.cs1656.org/project/HealthyRideRentals2019-Q3.csv](http://data.cs1656.org/project/HealthyRideRentals2019-Q3.csv)  

Each row in the file shows one rental transaction, indicating the bicycle ID, the source bike station (from station) and the destination bike station (to station). Worth noting:
* if there is no station ID, then this was usually a ``dockless'' bike, e.g., `BIKE 70000`,  
* if a bike was ``magically'' moved from one station to a different one, that means this happened as a result of rebalancing, where HealthyRidePGH staff relocated the bike using a truck to address demand imbalance.   

- **fromCNT** = total number of ``from'' bikes at that station for that day (i.e., number of transactions with that _stationID_ in the **from** column)
- **toCNT** = total number of ``to'' bikes at that station for that day (i.e., number of transactions with that _stationID_ in the **to** column)
- **rebalCNT*** = total number of ``rebalanced'' bikes. 

Given the information, the tasks:

* **Task 1.1** Print the first 20 rows of the data structure store the above data (i.e, **daily breakdown**).

* **Task 1.2** Print the first 20 rows of the data structure to store the above data (i.e., **monthly breakdown**).

### Task 2 (30 points)

For this task there are two variables containing input from the user:
* **filter_month** which corresponds to the month of interest (1-9, should have a default value of 4, i.e., April), and  
* **filter_stationID** which corresponds to the stationID of interest (should have a default value of 1046).  

Given the above two variables, create the following graphs:
* **Task 2.1** Show a bar chart for the 25 most popular bikestations when considering the number of **fromCNT** per station (for filter_month). Y axis is the fromCNT per station, X axis is the stationID. The first stationID corresponds to the most popular station. 

* **Task 2.2** For the filter_month and for the filter_stationID show a graph that shows the distribution of bike rentals throughout the month, for that station only. Y axis is the fromCNT for that stationID for that day, X axis is the different days in that month (i.e., 1 - 30 for April). 

* **Task 2.3** Compute the total number of rentals each bike had for each day (regardless of station). In other words, figure out how many times a bike was listed in the input data, for each different date. For the filter_month, show a graph that shows the 25 most popular bikes. Y axis is the number of times a bike was rented, X axis is the bikeID. The first bikeID corresponds to the most popular station.

  
### Task 3 (20 points)
Create graphs to show the rebalancing issue.

* **Task 3.1** Show a bar chart for the 25 most popular bikestations when considering the number of **rebalCNT** per station (for filter_month). Y axis is the rebalCNT per station, X axis is the stationID. The first stationID corresponds to the most demanding station in terms of rebalancing. 

* **Task 3.2** For the filter_month and for the filter_stationID show a graph that shows the distribution of bike rebalancing throughout the month, for that station only. Y axis is the rebalCNT for that stationID for that day, X axis is the different days in that month (i.e., 1 - 30 for April). 


### Task 4 (30 points)
Cluster the data to group similar stations together, using a variety of clustering functions and visualize the results of the clustering. 

For this task, create a data structure where for each stationID you record the following features:
* 3 variables for the total fromCNT for each station for each of the 3 months of the third quarter (i.e., 7, 8, 9)   
* 3 variables for the total rebalCNT for each station for each of the 3 months of the third quarter (i.e., 7, 8, 9)  

This creates a 6-dimensional space for the different stations. 

* **Task 4.1** Perform clustering on the above 6-dimensional space using K-means (with at least 3 different values for K) and DBSCAN  (with at least three different value combinations for min_samples and eps) [https://scikit-learn.org/stable/modules/clustering.html#clustering](https://scikit-learn.org/stable/modules/clustering.html#clustering). 

* **Task 4.2** Generate one bar chart per algorithm option (i.e., 6 different charts) showing the distribution of the number of stations per cluster. Y axis is the number of stations in that cluster, X axis is the clusterID. The first clusterID corresponds to the biggest cluster.

* **Task 4.3** Provide a brief explanation about the choice of K and the additional clustering algorithm. This is in the form of plain text inside the Jupyter notebook, under the Task 4.3 heading.

---
