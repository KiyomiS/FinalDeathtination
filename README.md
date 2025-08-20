# CS180project Team Final Deathtination
### By: Victor Omosor, Juvenal Ortega, Kiyomi Sugita, Jimmy Han, and Srikar Voleti

This is a web application that analyzes deaths in the United States from the years 2011 to 2015. The main database used is culled from the CDC's database on kaggle. https://www.kaggle.com/cdc/mortality 

# Languages/tools/libraries/datasets
## Languages
Python\
For most linux based systems, python is already installed. To find out if your computer already has python run "python --version". If your computer does not have python please follow this link: https://www.toolsqa.com/python/install-python/

## Tools
Flask\
Flask is a micro web framework written in Python. We use this for our backend code. 

## Libraries
We used the following libraries: [bootstrap](https://getbootstrap.com/), [canvasjs](https://canvasjs.com/)

## Datasets 
[Death in the United States](https://www.kaggle.com/cdc/mortality)\
For our project, we reduced the number of variables to: race, sex, age, cause of death, and month.

## How to run our project:
1. download and extract our files from git
2. cd into the folder
3. run the command python3 -m venv venv
4. run the command . venv/bin/activate
5. install flask, scipy, matplotlib by running command "pip install flask numpy scipy matplotlib"
6. run python3 communicationLayer.py

Now you should get an output that gives you a link. Copy and paste the link into your url and the website should start.

# Code Structure: 
![Capture](https://user-images.githubusercontent.com/91701128/144170619-2014f206-0d80-4d1e-b348-11fffab92339.PNG)
## The Communication Layer
In this layer, we utilize the Flask module to create routines that allow for server-client communication. This layer is dependent on the operation, analytic, and data layers. All of the flask routes created are in communicationLayer.py

## The Analytic Layer
![Capture2](https://user-images.githubusercontent.com/91701128/144172507-df012c56-e98b-41cf-9147-ece7bf37b838.PNG)

This layer contains all six of our analytic functions. It is dependent on the operational and data layers to calculate desired metrics. It then feeds this information to the communication layer which processes and visualizes the data through HTML files. 

The analytic layer is a python script file with various functions for the analytics. Each analytic uses different functions from the operation layer to perform their tasks.

As for our analytics, the first is the average analytic. It takes 1 to 4 inputs consisting of either sex, race, manner of death, and age to help specify a demographic. It outputs the average amount of deaths per month pertaining to the given inputs.

The second analytic is the ranking analytic. It initially only takes 1 input that can be any of the five data features. It then displays a column chart that shows each sub group of the chosen input. Each column displays the total amount of deaths for the group, and they  are sorted from most deaths to least deaths. From there, the user can further narrow down the demographic by inputing any of the other four inputs.

The third analytic is the prediction analytic. It can take up to and any of the 5 features to specify a demographic. It uses the inputs given to collect data pertaining to that demographic. It then calculates the expected amount of deaths for that demographic for the next month and display the old counts and new expected count in a line chart.

The fourth analytic is the Rates analytic. It takes 1 grouping input parameter to visualize the chosen demographic. It can also take up to 4 more inputs for a more specific demographics. It displays a donut chart showing the distributions for the grouping parameter based on the demographic.

The fifth analytic is the leading cause analytic. It takes a single input that can be either sex, month, age, or race. It displays a bar graph that shows the leading causes of death, sorted from highest to lowest for the chosen group. It also shows some statistics such as mean, medium, and standard deviation.

The last analytic is the month percentage analytic. It takes up to four inputs that can be race, sex, age, or manner of death to help specify a demographic. It displays a donut chart that shows the percentage breakdown for the months pertaining to the demographic created.


## The Operational Layer
This layer contains the basic features of the website such as, search, edit, insert, and delete. These features call functions and dictionaries from the data layer. This layer primarily works on data stored in the respective data structures instead of interacting directly with the database.

Any added functionality that is not an analytic goes here. Any function that modifies the data structures goes here. 

## The Data Layer
This is the lowest and most important level of our code structure. It operates directly with the database and is reponsible for importing data into data structures, removing data, adding new data, and backing up data to the database. 

Any function that interacts with the CSV directly goes here. 


