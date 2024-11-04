# Fall 2023 Projects

This repository contains various projects completed during the Fall 2023 semester as part of my **Data Science** studies at the University of Wisconsin-Madison.

## Overview

The projects in this repository showcase the starting steps for a career in Data Science, and highlights usage of SQL, Pandas, Matplotlib and others to accomplish various data anaylsis. 

## Projects

### 1. P5
- **Description**: Hurricanes often count among the worst natural disasters, both in terms of monetary costs, and more importantly, human life. Data Science can help us better understand these storms. In this project we will use Python to answer questions about past hurricanes.
- **Key Techniques**: Fundemental loops, breaking
- **Files**: `p5.ipynb`, `hurricanes.csv`

### 2. P6
- **Description**: In this project, we will use Python to analyze Electric Power Generation within the state of Wisconsin. The data used in this project has been adapted from this dataset maintained by the US Energy Information Administration. Information includes the capacities, locations, and the technologies used by the generators.
- **Key Techniques**: Accessing elements, get to know Python's data structures
- **Files**: `p6.ipynb`, `power_generators.csv`

### 3. P7
- **Description**: In this project, we will analyze data in soccer_stars.csv. This dataset has some data on nearly 20,000 soccer stars who play in the top soccer leagues across the world. The statistics in this dataset are obained from the video game FC'24 (formerly the FIFA series) and was collected from the website https://sofifa.com/. We will look at various statistics about your favorite players and teams, and identify their strengths and weaknesses.
- **Key Techniques**: csv operations, looping, mutability
- **Files**: `p7.ipynb`, `soccor_stars.csv`

### 4. P8
- **Description**: In this project and the next, we will be working on the IMDb Movies Dataset. We will use Python to discover some cool facts about our favorite movies, cast, and directors. In this project, we will combine the data from the movie and mapping files into a more useful format.
- **Key Techniques**: Splitting, slicing, hashing, bucketizing
- **Files**: `p8.ipynb`, `mapping.csv`, `movies.csv`

### 4. P9
- **Description**: In P8, we created very useful helper functions to parse the raw IMDb dataset. We also created useful data structures to store the data. In this project, we will be building on the work you did in P8 to analyze your favorite movies.
- **Key Techniques**: Hashing, bucketizing, Matplotlib, Lambda functions
- **Files**: `p9.ipynb`, `mapping.csv`, `movies.csv`

### 4. P10
- **Description**: Cleaning data is an important part of a data scientist's work cycle. As you have already seen, the data we will be analyzing in P10 and P11 has been split up into 15 different files of different formats. Even worse, as you shall see later in this project, some of these files have been corrupted, and lots of data is missing. Unfortunately, in the real world, a lot of data that you will come across will be in rough shape, and it is your job to clean it up before you can analyze it. In P10, you will combine the data in these different files to create a few manageable data structures, which can be easily analyzed. In the process, you will also have to deal with broken CSV files (by skipping rows with broken data), and broken JSON files (by skipping the files entirely).
After you create these data structures, in P11, you will dive deeper by analyzing this data and arrive at some exciting conclusions about various planets and stars outside our Solar System.
- **Key Techniques**: Files, file structure, broken data, namedtuple, json, os module
- **Files**: `p10.ipynb`, `data/`

### 4. P11
- **Description**: You have already parsed the data in the data directory in P10. You will now dive deeper by analyzing this data and arrive at some exciting conclusions about various planets and stars outside our Solar System. You will also use recursion to retrieve data from the broken JSON file in the data directory, and ask some interesting questions about the data.
- **Key Techniques**: Matplotlib, namedtuple, json, os module, recursion
- **Files**: `p11.ipynb`, `data/`, `broken_data/`

### 4. P12
- **Description**: For this project, you're going to analyze World University Rankings! Specifically, you're going to use Pandas to analyze various statistics of the top ranked universities across the world, over the last three years.
- **Key Techniques**: Pandas, json, html, requests module, web scraping, dataframes
- **Files**: `p12.ipynb`, `data/`, `broken_data/`

### 4. P13
- **Description**: For your final CS220 project, you're going to continue analyzing world university rankings. However, we will be using a different dataset this time. The data for this project has been extracted from here. Unlike the CWUR rankings we used in P12, the QS rankings dataset has various scores for the universities, and not just the rankings. This makes the QS rankings dataset more suitable for plotting (which you will be doing a lot of!). In this project, you'll have to dump your DataFrame to a SQLite database. You'll answer questions by doing queries on that database. Often, your answers will be in the form of a plot. Check these carefully, as the tests only verify that a plot has been created, not that it looks correct (the Gradescope autograder will manually deduct points for plotting mistakes).
- **Key Techniques**: SQL, Pandas, Requests + web scraping, Matplotlib, OS module, NumPy, dataframes, SQL querying
- **Files**: `p13.ipynb`, `mapping.csv`, `movies.csv`

## Technologies Used
- **Languages**: Python, html, SQL
- **Libraries**: 
  - Data Science: Pandas, Requests, Sqlite3, NumPy, os, math, csv
  - Visualization: Matplotlib
