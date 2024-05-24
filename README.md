# Youtube Data Harvesting And Warehousing

## Overview
* This project is focused on harvesting data from YouTube channels using the YouTube API, processing the data, and warehousing it. The harvested data is stored in a SQL records for in-depth data analysis. The project's core functionality relies on the Extract, Transform, Load (ETL) process features.

## Approach 

  - Harvest YouTube channel data using the YouTube API by providing a 'Channel ID'.
    
  - Through channel id  all the channel details and video and comment details are collected.
    
  - After Collecting the data ,the data was pushed to mysql.
    
  - Then got all the information of the 10 quaries by using sql query method
   ```
   Execute data analysis using SQL queries and Python integration.
   ```
  - Implement Streamlit to present code and data in a user-friendly UI.
    
  
##  Necessary Libraries
```
googleapiclient.discovery
pandas as pd
json
datetime
isodate 
re
streamlit
from streamlit import set_option
from datetime import datetime
from sqlalchemy import create_engine
Plotly.express as px
pymysql
```
## Technical Steps to Execute the Project

### Step 1: Install/Import Modules

   - Ensure the required Python modules are installed: Streamlit, Pandas,datetime,json,re,plotly,sqlalchemy,pymysql, Googleapiclient and Isodate.

### Step 2: Utilize the "YT2SQL" Class

   - By many function methods retrive the data of youtube channels and insert the details into mysql.

### Step 3: Run the Project with Streamlit

   - Open the command prompt in the directory where "sai.py" is located.
   - Execute the command: streamlit run sai.py. This will open a web browser, such as Google Chrome, displaying the project's user interface.

### Step 4: Configure Databases

   - Ensure that you are connected to python and MySQL.
   
## Methods

   - Get YouTube Channel Data: Fetches YouTube channel data using a Channel ID and creates channel details in dataframe format.
     
   - Get Playlist Videos: Retrieves all video IDs for a provided playlist ID.
     
   - Get Video and Comment Details: Returns video and comment details for the given video IDs.
     
   
  -  Connection: By using mysql connecter(pymysql) create the data base and tables of channel,video,comments.
     
   - Insert Data: Inserts channel data into Mysql if the data does not exists.
  
     
   - Data Analysis: Conducts data analysis using SQL queries and Python integration.
     

     
## Tools Expertise 

   - Python (Scripting)
     
   - Data Collection
     
   - SQL
     
   - API Integration
     
   - Data Management Mysql
     
   - IDE: VsCode
   
   - Streamlit
   


## Result :

   - This project focuses on harvesting YouTube data using the YouTube API, storing it in MySQL for analysis. Utilizes Streamlit, Python, and various methods for ETL. Expertise includes Python, MySQL, API integration, and data management tools. This project maily reduces 85% percentage of manually data processing and data storing work effectively.

