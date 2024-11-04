#!/usr/bin/env python
# coding: utf-8
# import and initialize otter
import otter
grader = otter.Notebook("p10.ipynb")

import public_tests

# +
# PLEASE FILL IN THE DETAILS
# Enter none if you don't have a project partner
# You will have to add your partner as a group member on Gradescope even after you fill this

# project: p10
# submitter: sheberlein
# partner: sheberlein
# -

# # Project 10: Stars and Planets

# ## Learning Objectives:
#
# In this project, you will demonstrate how to:
#
# * use `os` module to get information of files in a directory,
# * use `os` module to get paths of files,
# * look up data between JSON and CSV files using unique keys,
# * read JSON and CSV files to store data to `namedTuple` objects,
# * clean up missing values and handle cases when the file is too corrupt to parse,
#
# Please go through [Lab-P10](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/tree/main/lab-p10) before working on this project. The lab introduces some useful techniques related to this project.

# <h2 style="color:red">Warning (Note on Academic Misconduct):</h2>
#
# **IMPORTANT**: **P10 and P11 are two parts of the same data analysis.** You **cannot** switch project partners between these two projects. That is if you partner up with someone for P10, you have to sustain that partnership until the end of P11. Now may be a good time to review [our course policies](https://cs220.cs.wisc.edu/f23/syllabus.html).
#
# Under any circumstances, **no more than two students are allowed to work together on a project** as mentioned in the course policies. If your code is flagged by our code similarity detection tools, **both partners will be responsible** for sharing/copying the code, even if the code is shared/copied by one of the partners with/from other non-partner student(s). Note that each case of plagiarism will be reported to the Dean of Students with a zero grade on the project. **If you think that someone cannot be your project partner then don’t make that student your lab partner.**
#
# **<font color = "red">Project partners must submit only one copy of their project on Gradescope, but they must include the names of both partners.</font>**

# ## Testing your code:
#
# Along with this notebook, you must have downloaded the file `public_tests.py`. If you are curious about how we test your code, you can explore this file, and specifically the output of the function `get_expected_json`, to understand the expected answers to the questions.

# ## Setup:
#
# Before proceeding much further, download `data.zip` and extract it to a directory on your
# computer (using [Mac directions](http://osxdaily.com/2017/11/05/how-open-zip-file-mac/) or
# [Windows directions](https://support.microsoft.com/en-us/help/4028088/windows-zip-and-unzip-files)).
#
# You need to make sure that the project files are stored in the following structure:
#
# ```
# +-- p10.ipynb
# +-- public_tests.py
# +-- data
# |   +-- .DS_Store
# |   +-- .ipynb_checkpoints
# |   +-- mapping_1.json
# |   +-- mapping_2.json
# |   +-- mapping_3.json
# |   +-- mapping_4.json
# |   +-- mapping_5.json
# |   +-- planets_1.csv
# |   +-- planets_2.csv
# |   +-- planets_3.csv
# |   +-- planets_4.csv
# |   +-- planets_5.csv
# |   +-- stars_1.csv
# |   +-- stars_2.csv
# |   +-- stars_3.csv
# |   +-- stars_4.csv
# |   +-- stars_5.csv
# ```
#
# Make sure that the files inside `data.zip` are inside the `data` directory. If you place your files inside some other directory, then your code will **fail on Gradescope** even after passing local tests.

# ## Project Description:
#
# Cleaning data is an important part of a data scientist's work cycle. As you have already seen, the data we will be analyzing in P10 and P11 has been split up into 15 different files of different formats. Even worse, as you shall see later in this project, some of these files have been corrupted, and lots of data is missing. Unfortunately, in the real world, a lot of data that you will come across will be in rough shape, and it is your job to clean it up before you can analyze it. In P10, you will combine the data in these different files to create a few manageable data structures, which can be easily analyzed. In the process, you will also have to deal with broken CSV files (by skipping rows with broken data), and broken JSON files (by skipping the files entirely).
#
# After you create these data structures, in P11, you will dive deeper by analyzing this data and arrive at some exciting conclusions about various planets and stars outside our Solar System.

# ## The Data:
#
# In P10 and P11, you will be studying stars and planets outside our Solar System using this dataset from the [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PSCompPars). You will use Python to ask some interesting questions about the laws of the universe and explore the habitability of other planets in our universe. The raw data from the [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PSCompPars) has been parsed and stored in multiple different files of different formats. You can find these files inside `data.zip`.

# You can open each of these files using Microsoft Excel or some other Spreadsheet viewing software to see how the data is stored. For example, these are the first three rows of the file `stars_1.csv`:
#
# Star Name|Spectral Type|Stellar Effective Temperature [K]|Stellar Radius [Solar Radius]|Stellar Mass [Solar mass]|Stellar Luminosity [log(Solar)]|Stellar Surface Gravity [log10(cm/s**2)]|Stellar Age [Gyr]
# ---|---|---|---|---|---|---|---
# 11 Com|G8III|4874.00|13.76|2.09|1.978|2.45|
# 11 UMi|K4III|4213.00|29.79|2.78|2.430|1.93|1.560
# 14 And|K0III|4888.00|11.55|1.78|1.840|2.55|4.500
#
# As you might have already guessed, this file contains data on a number of *stars* outside our solar system along with some important statistics about these stars. The columns here are as follows:
#
# - `Star Name`: The **name** given to the star by the *International Astronomical Union*,
# - `Spectral Type`: The **Spectral Classification** of the star as per the *Morgan–Keenan (MK) system*,
# - `Stellar Effective Temperature [K]`: The **temperature** of a *black body* (in units of Kelvin) that would emit the *observed radiation* of the star,
# - `Stellar Radius [Solar Radius]`: The **radius** of the star (in units of the radius of the Sun),
# - `Stellar Mass [Solar mass]`: The **mass** of the star (in units of the mass of the Sun),
# - `Stellar Luminosity [log(Solar)]`: The *total* amount of **energy radiated** by the star **each second** (represented by the logarithm of the energy radiated by the Sun in each second),
# - `Stellar Surface Gravity [log10(cm/s**2)]`: The **acceleration due to the gravity** of the Star at its *surface* (represented by the logarithm of the acceleration measured in centimeter per second squared),
# - `Stellar Age [Gyr]`: The total **age** of the star (in units of Giga years, i.e., billions of years).
#
# The four other files `stars_2.csv`, `stars_3.csv`, `stars_4.csv`, and `stars_5.csv` also store similar data in the same format. At this stage of the project, it is alright if you do not understand what these columns mean - they will be explained to you when they become necessary (in P11).

# On the other hand, here are the first three rows of the file `planets_1.csv`:
#
# Planet Name|Discovery Method|Discovery Year|Controversial Flag|Orbital Period [days]|Planet Radius [Earth Radius]|Planet Mass [Earth Mass]|Orbit Semi-Major Axis [au]|Eccentricity|Equilibrium Temperature [K]|Insolation Flux [Earth Flux]
# ---|---|---|---|---|---|---|---|---|---|---
# 11 Com b|Radial Velocity|2007|0|323.21000000|12.200|4914.89849|1.178000|0.238000||
# 11 UMi b|Radial Velocity|2009|0|516.21997000|12.300|4684.81420|1.530000|0.080000||
# 14 And b|Radial Velocity|2008|0|186.76000000|13.100|1131.15130|0.775000|0.000000||
#
# This file contains data on a number of *planets* outside our solar system along with some important statistics about these planets. The columns here are as follows:
#
# - `Planet Name`: The **name** given to the planet by the *International Astronomical Union*,
# - `Discovery Method`: The **method** by which the planet was *discovered*,
# - `Discovery Year`: The **year** in which the planet was *discovered*,
# - `Controversial Flag`: Indicates whether the status of the discovered object as a planet was **disputed** at the time of discovery, 
# - `Orbital Period [days]`: The amount of **time** (in units of days) it takes for the planet to **complete one orbit** around its star,
# - `Planet Radius [Earth Radius]`: The **radius** of the planet (in units of the radius of the Earth),
# - `Planet Mass [Earth Mass]`: The **mass** of the planet (in units of the mass of the Earth),
# - `Orbit Semi-Major Axis [au]`: The **semi-major axis** of the planet's elliptical **orbit** around its host star (in units of Astronomical Units),
# - `Eccentricity`: The **eccentricity** of the planet's orbit around its host star,
# - `Equilibrium Temperature [K]`: The **temperature** of the planet (in units of Kelvin) if it were a *black body* heated only by its host star,
# - `Insolation Flux [Earth Flux]`:  The amount of **radiation** the planet received from its host star **per unit of area** (in units of the Insolation Flux of the Earth from the Sun).
#
# The four other files `planets_2.csv`, `planets_3.csv`, `planets_4.csv`, and `planets_5.csv` also store similar data in the same format. At this stage of the project, it is alright if you do not understand what these columns mean - they will be explained to you when they become necessary (in P11).

# Finally, if you take a look at `mapping_1.json` (you can open json files using any Text Editor), you will see that the first three entries look like this:
#
# ```python
# {"11 Com b":"11 Com","11 UMi b":"11 UMi","14 And b":"14 And", ...}
# ```
#
# This file contains a *mapping* from each *planet* in `planets_1.csv` to the *star* in `stars_1.csv` that the planet orbits. Similarly, `mapping_2.json` contains a *mapping* from each *planet* in `planets_2.csv` to the *star* in `stars_2.csv` that the planet orbits. The pattern also holds true for `mapping_3.json`, `mapping_4.json`, and `mapping_5.json`.

# ## Project Requirements:
#
# You **may not** hardcode indices in your code, unless the question explicitly says to. If you open your `.csv` files with Excel, manually count through the rows and use this number to loop through the dataset, this is also considered as hardcoding. If any instances of hardcoding are found during code review, the Gradescope autograder will **deduct** points from your public score.
#
# **Store** your final answer for each question in the **variable specified for each question**. This step is important because Otter grades your work by comparing the value of this variable against the correct answer.
#
# For some of the questions, we'll ask you to write (then use) a function to compute the answer. If you compute the answer **without** creating the function we ask you to write, the Gradescope autograder will **deduct** points from your public score, even if the way you did it produced the correct answer.
#
# #### Required Functions:
# - `star_cell`
# - `get_stars`
# - `planet_cell`
# - `get_planets`
#
# In this project, you will also be required to define certain **data structures**. If you do not create these data structures exactly as specified, the Gradescope autograder will **deduct** points from your public score, even if the way you did it produced the correct answer.
#
# #### Required Data Structures:
# - `Star` (**namedtuple**)
# - `stars_dict` (**dictionary** mapping **strings** to `Star` objects)
# - `Planet` (**namedtuple**)
# - `planets_list` (**list** of `Planet` objects)
#
# In addition, you are also **required** to follow the requirements below:
#
# * You **must** never use the output of the `os.listdir` function directly. You **must** always first remove all files and directories that start with `"."`, and **explicitly sort** the list before doing anything with it.
# * You are **not** allowed to use **bare** `try/except` blocks. In other words, you can **not** use `try/except` without explicitly specifying the type of exceptions that you want to catch.
# * You are **only** allowed to use Python commands and concepts that have been taught in the course prior to the release of P10. In particular, this means that you are **not** allowed to use **modules** like `pandas` to answer the questions in this project.
# * Please do not display `start_dict` or `planets_list` anywhere in the notebook. Please **remove** such statements before submission.
#
# Otherwise, the Gradescope autograder will **deduct** points from your public score.
#
# For more details on what will cause you to lose points during code review and specific requirements, please take a look at the [Grading rubric](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/blob/main/p10/rubric.md).

# ## Questions and Functions:
#
# Let us start by importing all the modules we will need for this project.
# it is considered a good coding practice to place all import statements at the top of the notebook
# please place all your import statements in this cell if you need to import any more modules for this project
import data
import csv
import os
from collections import namedtuple
import json
# ### File handling:
#
# In the next questions, you will be using functions in the `os` module to make **lists** of files and paths in the `data` directory. All your **lists** **must** satisfy the following conditions:
#
# * Any files with names beginning with `"."` **must** be **excluded**.
# * The list **must** be in **reverse-alphabetical** order.

# **Question 1:** What are the **names** of the files present in the `data` directory
#
# Your output **must** be a **list** of **strings** representing the **names** of the files.

# compute and store the answer in the variable 'files_in_data', then display it
files_in_data = [file for file in os.listdir("data") if not file.startswith(".")]
files_in_data = sorted(files_in_data, reverse = True)
files_in_data
grader.check("q1")

# **Question 2:** What are the **paths** of all the files in the `data` directory?
#
# Your output **must** be a **list** of **strings** representing the **paths** of the files. You **must** use the `files_in_data` variable created in the previous question to answer this.
#
# **Warning:** Please **do not hardcode** `"/"` or `"\"` in your path because doing so will cause your function to **fail** on a computer that's not using the same operating system as yours. This may result in your code failing on Gradescope.

# +
# compute and store the answer in the variable 'file_paths', then display it
file_paths = [os.path.join("data", path) for path in files_in_data]


file_paths
# -
grader.check("q2")

# **Question 3:** What are the **paths** of all the **CSV files** present in `data` directory?
#
# Your output **must** be filtered to **only** include files ending in `'.csv'`. You **must** use either the `files_in_data` or `file_paths` variables created in the previous questions to answer this.
#
# **Warning:** Please **do not hardcode** `"/"` or `"\"` in your path because doing so will cause your function to **fail** on a computer that's not using the same operating system as yours. This may result in your code failing on Gradescope.

# compute and store the answer in the variable 'csv_file_paths', then display it
csv_file_paths = [path for path in file_paths if path.endswith(".csv")]
csv_file_paths
grader.check("q3")

# **Question 4:** What are the **paths** of all the files present in `data` directory, that **begin** with the phrase `'stars'`?
#
# Your output **must** be filtered to **only** include files start with `'stars'`. You **must** use either the `files_in_data` or `file_paths` variables created in the previous questions to answer this.
#
# **Warning:** Please **do not hardcode** `"/"` or `"\"` in your path because doing so will cause your function to **fail** on a computer that's not using the same operating system as yours. This may result in your code failing on Gradescope.

# +
# compute and store the answer in the variable 'stars_paths', then display it
stars_paths = [os.path.join("data", file) for file in files_in_data if file.startswith("stars")]


stars_paths
# -
grader.check("q4")

# ### Data Structure 1: namedtuple `Star`
#
# You will be using named tuples to store the data in the `stars_1.csv`, ..., `stars_5.csv` files. Before you start reading these files however, you **must** create a new `Star` type (using namedtuple). It **must** have the following attributes:
#
# * `spectral_type`,
# * `stellar_effective_temperature`,
# * `stellar_radius`,
# * `stellar_mass`,
# * `stellar_luminosity`,
# * `stellar_surface_gravity`,
# * `stellar_age`.

# +
# define the namedtuple 'Star' here
star_attributes = ['spectral_type',
                  'stellar_effective_temperature',
                  'stellar_radius',
                  'stellar_mass',
                  'stellar_luminosity',
                  'stellar_surface_gravity',
                  'stellar_age']

# create the namedtuple type 'Star' with the correct attributes
Star = namedtuple("Star", star_attributes)
# +
# run this following cell to initialize and test an example Star object
# if this cell fails to execute, you have likely not defined the namedtuple 'Star' correctly

sun = Star('G2 V', 5780.0, 1.0, 1.0, 0.0, 4.44, 4.6)

sun
# -

grader.check("Star")


# ### Creating `Star` objects
#
# Now that we have created the `Star` namedtuple, our next objective will be to read the files `stars_1.csv`, ..., `stars_5.csv` and create `Star` objects out of all the stars in there. In order to process the CSV files, you will first need to copy/paste the `process_csv` function you have been using since P6.

# # copy & paste the process_csv file from previous projects here
# # copy & paste the process_csv file from previous projects here
def process_csv(filename):
    example_file = open(filename, encoding="utf-8")
    example_reader = csv.reader(example_file)
    example_data = list(example_reader)
    example_file.close()
    return example_data


# You are now ready to read the data in `stars_1.csv` using `process_csv` and convert the data into `Star` objects. In the cell below, you **must** read the data in `stars_1.csv` and extract the **header** and the non-header **rows** of the file.

# +
# replace the ... with your code

stars_1_csv = process_csv(os.path.join("data", "stars_1.csv")) # read the data in 'stars_1.csv'
stars_header = stars_1_csv[0]
stars_1_rows = stars_1_csv[1:]


# -

# If you wish to **verify** that you have read the file and defined the variables correctly, you can check that `stars_header` has the value:
#
# ```python
# ['Star Name', 'Spectral Type', 'Stellar Effective Temperature [K]', 'Stellar Radius [Solar Radius]',
#  'Stellar Mass [Solar mass]', 'Stellar Luminosity [log(Solar)]', 
#  'Stellar Surface Gravity [log10(cm/s**2)]', 'Stellar Age [Gyr]']
# ```
#
# and that `stars_1_rows` has **1595** rows of which the **first three** are:
#
# ```python
# [['11 Com', 'G8III', '4874.00', '13.76', '2.09', '1.978', '2.45', ''],
#  ['11 UMi', 'K4III', '4213.00', '29.79', '2.78', '2.430', '1.93', '1.560'],
#  ['14 And', 'K0III', '4888.00', '11.55', '1.78', '1.840', '2.55', '4.500']]
# ```

# ### Function 1: `star_cell(row_idx, col_name, stars_rows, header=stars_header)`
#
# This function **must** read the **list** of **lists** `stars_rows`, and extract the value at **row** index `row_idx` and **column** index `col_idx`. The function **must** typecast the value based on `col_name`. If the value in `stars_rows` is **missing** (i.e., it is `''`), then the value returned **must** be `None`.
#
# The **column** of `stars_rows` where the value should be obtained from, and the correct **data type** for the value are listed in the table below:
#
# |Column of `stars_rows`|Data Type|
# |------|---------|
# |Star Name|**string**|
# |Spectral Type|**string**|
# |Stellar Effective Temperature [K]|**float**|
# |Stellar Radius [Solar Radius]|**float**|
# |Stellar Mass [Solar mass]|**float**|
# |Stellar Luminosity [log(Solar)]|**float**|
# |Stellar Surface Gravity [log10(cm/s**2)]|**float**|
# |Stellar Age [Gyr]|**float**|
#
# You are **allowed** to copy/paste this function from Lab-P10.

# define the 'star_cell' function here
def star_cell(row_idx, col_name, stars_rows, header=stars_header):
    col_idx = header.index(col_name)
    val = stars_rows[row_idx][col_idx]
    # return None if value is missing
    # else typecast 'val' and return it depending on 'col_name'
    if val == "":
        return None
    else:
        if col_name == "Star Name" or col_name == "Spectral Type":
            val = str(val)
        else:
            val = float(val)
    return val


grader.check("star_cell")

# **Question 5:** Create a `Star` object for the **third** star in `"stars_1.csv"`.
#
# You **must** access the values in `stars_1.csv` using the `star_cell` function. Note that the third star would be at **index** 2.
#
# The **attribute** of the `Star` namedtuple object, the corresponding **column** of the `stars_1.csv` file where the value should be obtained from, and the correct **data type** for the value are listed in the table below:
#
# |Attribute of `Star` object|Column of `stars_1.csv`|Data Type|
# |---------|------|---------|
# |`spectral_type`|Spectral Type|**string**|
# |`stellar_effective_temperature`|Stellar Effective Temperature [K]|**float**|
# |`stellar_radius`|Stellar Radius [Solar Radius]|**float**|
# |`stellar_mass`|Stellar Mass [Solar mass]|**float**|
# |`stellar_luminosity`|Stellar Luminosity [log(Solar)]|**float**|
# |`stellar_surface_gravity`|Stellar Surface Gravity [log10(cm/s**2)]|**float**|
# |`stellar_age`|Stellar Age [Gyr]|**float**|

# +
 # compute and store the answer in the variable 'third_star', then display it
row_idx = 2 # the index of the star we want to convert into a Star object

# extract the values from stars_1_rows
spectral_type = stars_1_rows[row_idx][stars_header.index("Spectral Type")]
stellar_effective_temperature = float(stars_1_rows[row_idx][stars_header.index("Stellar Effective Temperature [K]")])
stellar_radius = float(stars_1_rows[row_idx][stars_header.index("Stellar Radius [Solar Radius]")])
stellar_mass = float(stars_1_rows[row_idx][stars_header.index("Stellar Mass [Solar mass]")])
stellar_luminosity = float(stars_1_rows[row_idx][stars_header.index("Stellar Luminosity [log(Solar)]")])
stellar_surface_gravity = float(stars_1_rows[row_idx][stars_header.index("Stellar Surface Gravity [log10(cm/s**2)]")])
stellar_age = float(stars_1_rows[row_idx][stars_header.index("Stellar Age [Gyr]")])

# initialize 'first_star'
third_star = Star(spectral_type, stellar_effective_temperature, stellar_radius, \
                  stellar_mass, stellar_luminosity, \
                  stellar_surface_gravity, stellar_age)

third_star
# -
grader.check("q5")


# ### Function 2:  `get_stars(star_file)`
#
# This function **must** take in as its input, the path of a CSV file `star_file` which contains data on stars in the same format as `stars_1.csv`. It **must** return a **dictionary** mapping the `Name` of each star in `star_file` to a `Star` object containing all the other details of the star.
#
# You **must** access the values in `stars_file` using the `star_cell` function.
#
# You **must not** hardcode the name of the directory `data` into the `get_stars` function. Instead, you must pass it as a part of the argument `star_file`, by including it in the **path** `star_file`.
#
# Once again, as a reminder, the attributes of the `Star` objects should be obtained from the **rows** of `star_file` and stored as follows:
#
# |Attribute of `Star` object|Column of `star_file`|Data Type|
# |---------|------|---------|
# |`spectral_type`|Spectral Type|**string**|
# |`stellar_effective_temperature`|Stellar Effective Temperature [K]|**float**|
# |`stellar_radius`|Stellar Radius [Solar Radius]|**float**|
# |`stellar_mass`|Stellar Mass [Solar mass]|**float**|
# |`stellar_luminosity`|Stellar Luminosity [log(Solar)]|**float**|
# |`stellar_surface_gravity`|Stellar Surface Gravity [log10(cm/s**2)]|**float**|
# |`stellar_age`|Stellar Age [Gyr]|**float**|
#
# In case any data in `star_file` is **missing**, the corresponding value should be `None`.
#
# For example, when this function is called with the file `stars_1.csv` as the input, the **dictionary** returned should look like:
#
# ```python
# {'11 Com': Star(spectral_type='G8III', stellar_effective_temperature=4874.0, 
#                 stellar_radius=13.76, stellar_mass=2.09, stellar_luminosity=1.978, 
#                 stellar_surface_gravity=2.45, stellar_age=None),
#  '11 UMi': Star(spectral_type='K4III', stellar_effective_temperature=4213.0, 
#                 tellar_radius=29.79, stellar_mass=2.78, stellar_luminosity=2.43, 
#                 stellar_surface_gravity=1.93, stellar_age=1.56),
#  '14 And': Star(spectral_type='K0III', stellar_effective_temperature=4888.0, 
#                 stellar_radius=11.55, stellar_mass=1.78, stellar_luminosity=1.84, 
#                 stellar_surface_gravity=2.55, stellar_age=4.5),
#  ...
# }
# ```

# define the function 'get_stars' here
def get_stars(star_file):
    
    data = process_csv(star_file)
    data_header = data[0]
    data_rows = data[1:]
    dict1 = {}
    for rowi in range(len(data_rows)):
        star_name = star_cell(rowi, "Star Name", data_rows)
        spectral_type = star_cell(rowi, "Spectral Type", data_rows)
        stellar_effective_temperature = star_cell(rowi, "Stellar Effective Temperature [K]", data_rows)
        stellar_radius = star_cell(rowi, "Stellar Radius [Solar Radius]", data_rows)
        stellar_mass = star_cell(rowi, "Stellar Mass [Solar mass]", data_rows)
        stellar_luminosity = star_cell(rowi, "Stellar Luminosity [log(Solar)]", data_rows)
        stellar_surface_gravity = star_cell(rowi, "Stellar Surface Gravity [log10(cm/s**2)]", data_rows)
        stellar_age = star_cell(rowi, "Stellar Age [Gyr]", data_rows)
        star = Star(spectral_type, stellar_effective_temperature, stellar_radius, \
                      stellar_mass, stellar_luminosity, \
                      stellar_surface_gravity, stellar_age)
        dict1[star_name] = star
    return dict1


# +
# you can now use 'get_stars' to read the data in 'stars_1.csv'

stars_1_dict = get_stars(os.path.join("data", "stars_1.csv"))
# -

grader.check("get_stars")

# **Question 6:** What is the `Star` object of the star (in `stars_1.csv`) named *DP Leo*?
#
# You **must** access the `Star` object in `stars_1_dict` **dictionary** defined above to answer this question.

# +
# compute and store the answer in the variable 'dp_leo', then display it
dp_leo = stars_1_dict["DP Leo"]


dp_leo
# -
grader.check("q6")

# **Question 7:** What's the **average** `stellar_luminosity` of **all** the stars in the `star_1.csv` file?
#
# You **must** use the `stars_1_dict` **dictionary** defined above to answer this question.
#
# To find the average, you **must** first **add** up the `stellar_luminosity` value of all the stars and **divide** by the total **number** of stars. You **must skip** stars which don't have the `stellar_luminosity` data. Such stars should not contribute to either the sum of `stellar_luminosity` or to the number of stars.

# +
# compute and store the answer in the variable 'avg_lum_stars_1', then display it
stars1 = get_stars(os.path.join("data", "stars_1.csv"))

count = 0
avg_lum_stars_1 = 0
for star in stars1:
    if stars1[star].stellar_luminosity == None:
        continue
    else:
        avg_lum_stars_1 += stars1[star].stellar_luminosity
        count += 1
avg_lum_stars_1 = avg_lum_stars_1/count
avg_lum_stars_1
# -
grader.check("q7")

# **Question 8:** What is the **average** `stellar_age` of **all** the stars in the `stars_2.csv` file?
#
# You **must** use the function `get_stars(csv_file)` to read the data in `stars_2.csv`. Your output **must** be a **float** representing the `stellar_age` in units of *gigayears*. You **must** skip stars which have missing `stellar_age` data.

# +
# compute and store the answer in the variable 'avg_age_stars_2', then display it
stars2 = get_stars(os.path.join("data", "stars_2.csv"))

count = 0
avg_age_stars_2 = 0
for star in stars2:
    if stars2[star].stellar_age == None:
        continue
    else:
        avg_age_stars_2 += stars2[star].stellar_age
        count += 1
avg_age_stars_2 = avg_age_stars_2/count


avg_age_stars_2
# -
grader.check("q8")

# ### Data Structure 2: `stars_dict`
#
# You are now ready to read all the data about the stars stored in the `data` directory. You **must** now create a **dictionary** mapping the `Name` of each star in the `data` directory (inside the files `stars_1.csv`, ..., `stars_5.csv`) to the `Star` object containing all the other details about the star.
#
# You **must not** hardcode the files/paths of the files `stars_1.csv`, ..., `stars_5.csv` to answer this question. Instead, you **must** use the `stars_paths` variable defined earlier in Question 4 to get the list of paths needed for this question. You can use the `update` dictionary **method** to combine two **dictionaries**.
#
# You must use this dictionary to answer the next 3 questions.

# +
# define the variable 'stars_dict' here,
# but do NOT display the variable at the end
stars_dict = {}

for path in stars_paths:
    stars_dict.update(get_stars(path))


# -

grader.check("stars_dict")

# If you wish to **verify** that you have read the files and defined `stars_dict` correctly, you can check that `stars_dict` has **4125** key/value pairs in it.

# **Question 9:** What is the `stellar_effective_temperature` of the star *Kepler-220*?
#
# You **must** access the correct `Star` object in the `stars_dict` **dictionary** defined above to answer this question.

# +
# compute and store the answer in the variable 'kepler_220_temp', then display it
kepler_220_temp = stars_dict["Kepler-220"].stellar_effective_temperature


kepler_220_temp
# -
grader.check("q9")

# **Question 10:** Find the **name** of the **largest** star (in terms of `stellar_radius`) in the `data` directory.
#
# Your output **must** be a **string**. You do **not** need to worry about any ties. You **must** skip any stars with **missing** `stellar_radius` data.

# +
# compute and store the answer in the variable 'biggest_star', then display it
biggest_star = None
maxi = 0
for star in stars_dict:
    if stars_dict[star].stellar_radius != None and stars_dict[star].stellar_radius > maxi:
        maxi = stars_dict[star].stellar_radius
        biggest_star = star

biggest_star
# -

grader.check("q10")

# **Question 11:** What is the **average** `stellar_age` (in gigayears) of **all** the stars in the `data` directory whose names **start with** `"Kepler"`?
#
# Your output **must** be a **float**. You **must** skip all stars with **missing** `stellar_age` data. Such stars should not contribute to either the sum of `stellar_age` or to the number of stars.

# compute and store the answer in the variable 'avg_age_kepler', then display it
avg_age_kepler = 0
count = 0
for star in stars_dict:
    if stars_dict[star].stellar_age == None:
        continue
    elif star.startswith("Kepler"):
        avg_age_kepler += stars_dict[star].stellar_age
        count += 1
avg_age_kepler = avg_age_kepler / count
avg_age_kepler

grader.check("q11")

# ### Data Structure 3: namedtuple `Planet`
#
# Just as you did with the stars, you will be using named tuples to store the data about the planets in the `planets_1.csv`, ..., `planets_5.csv` files. Before you start reading these files however, you **must** create a new `Planet` type (using namedtuple). It **must** have the following attributes:
#
# * `planet_name`,
# * `host_name`,
# * `discovery_method`,
# * `discovery_year`,
# * `controversial_flag`,
# * `orbital_period`,
# * `planet_radius`,
# * `planet_mass`,
# * `semi_major_radius`,
# * `eccentricity`,
# * `equilibrium_temperature`
# * `insolation_flux`.

# +
# define the namedtuple 'Planet' here
planets_attributes = ["planet_name", "host_name", "discovery_method", "discovery_year",\
                      "controversial_flag", "orbital_period", "planet_radius", "planet_mass",\
                      "semi_major_radius", "eccentricity", "equilibrium_temperature", "insolation_flux"] # initialize the list of attributes

# define the namedtuple 'Planet'
Planet = namedtuple("Planet", planets_attributes)
# +
# run this following cell to initialize and test an example Planet object
# if this cell fails to execute, you have likely not defined the namedtuple 'Planet' correctly
jupiter = Planet('Jupiter', 'Sun', 'Imaging', 1610, False, 4333.0, 11.209, 317.828, 5.2038, 0.0489, 110, 0.0345)

jupiter
# -

grader.check("Planet")

# ### Creating `Planet` objects
#
# We are now ready to read the files in the `data` directory and create `Planet` objects. Creating `Planet` objects however, is going to be more difficult than creating `Star` objects, because the data required to create a single `Planet` object is split up into different files.
#
# The `planets_1.csv`, ..., `planets_5.csv` files contain all the data required to create `Planet` objects **except** for the `host_name`. The `host_name` for each planet is to be found in the `mapping_1.json`, ..., `mapping_5.json` files.

# First, let us read the data in `planets_1.csv`. Since this is a CSV file, you can use the `process_csv` function from above to read this file. In the cell below, you **must** read the data in `planets_1.csv` and extract the **header** and the non-header **rows** of the file.

# +
# replace the ... with your code

planets_1_csv = process_csv(os.path.join("data", "planets_1.csv"))
planets_header = planets_1_csv[0]
planets_1_rows = planets_1_csv[1:]


# -

# If you wish to **verify** that you have read the file and defined the variables correctly, you can check that `planets_header` has the value:
#
# ```python
# ['Planet Name', 'Discovery Method', 'Discovery Year', 'Controversial Flag',
#  'Orbital Period [days]', 'Planet Radius [Earth Radius]', 'Planet Mass [Earth Mass]',
#  'Orbit Semi-Major Axis [au]', 'Eccentricity', 'Equilibrium Temperature [K]',
#  'Insolation Flux [Earth Flux]']
# ```
#
# and that `planets_1_rows` has **1595** rows of which the **first three** are:
#
# ```python
# [['11 Com b', 'Radial Velocity', '2007', '0', '323.21000000', '12.200', '4914.89849', '1.178000', '0.238000', '', ''],
#  ['11 UMi b', 'Radial Velocity', '2009', '0', '516.21997000', '12.300', '4684.81420', '1.530000', '0.080000', '', ''],
#  ['14 And b', 'Radial Velocity', '2008', '0', '186.76000000', '13.100', '1131.15130', '0.775000', '0.000000', '', '']]
# ```

# Now, you are ready to read the data in `mapping_1.json`. Since this is a JSON file, you will need to copy/paste the `read_json` function Lab-P10, and use it to read the file.

# # copy & paste the read_json file from Lab-P10
def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# +
# now use the read_json function to read 'mapping_1.json'

mapping_1_json = read_json(os.path.join("data", "mapping_1.json"))


# -

# If you wish to **verify** that you have read the file correctly, you can check that `mapping_1_json` has the value:
#
# ```python
# {'11 Com b': '11 Com',
#  '11 UMi b': '11 UMi',
#  '14 And b': '14 And',
#  ...
#  }
# ```
#
# Now that we have read `planets_1.csv` and `mapping_1.json`, we are now ready to combine these two files to create `Planet` objects.

# ### Function 3: `planet_cell(row_idx, col_name, planets_rows, header=planets_header)`
#
# This function **must** read the **list** of **lists** `planets_rows`, and extract the value at **row** index `row_idx` and **column** index `col_idx`. The function **must** typecast the value based on `col_name`. If the value in `planets_rows` is **missing** (i.e., it is `''`), then the value returned **must** be `None`.
#
# The **column** of `planets_rows` where the value should be obtained from, and the correct **data type** for the value are listed in the table below:
#
# |Column of `planets_rows`|Data Type|
# |------|---------|
# |Planet Name|**string**|
# |Discovery Year|**int**|
# |Discovery Method|**string**|
# |Controversial Flag|**bool**|
# |Orbital Period [days]|**float**|
# |Planet Radius [Earth Radius]|**float**|
# |Planet Mass [Earth Mass]|**float**|
# |Orbit Semi-Major Axis [au]|**float**|
# |Eccentricity|**float**|
# |Equilibrium Temperature [K]|**float**|
# |Insolation Flux [Earth Flux]|**float**|
#
# **Important Hint:** While computing the value of the attribute `controversial_flag`, note that the `Controversial Flag` column of `planets_1.csv` represents `True` with `'1'` and `False` with `'0'`. You **must** be careful with typecasting **strings** to **booleans**.

# +
# define the function 'planet_cell' here

def planet_cell(row_idx, col_name, planets_rows, header=planets_header):
    col_idx = planets_header.index(col_name) # extract col_idx from col_name and header
    val = planets_rows[row_idx][col_idx] # extract the value at row_idx and col_idx
    if val == '':
        return None
    if col_name in ["Controversial Flag"]:
        if val == "1":
            return True
        else:
            return False
    else: 
        if col_name == "Planet Name" or col_name == "Discovery Method":
            val = str(val)
        elif col_name == "Discovery Year":
            val = int(val)
        else:
            val = float(val)
    return val


# -

grader.check("planet_cell")

# **Question 12:** Create a `Planet` object for the **fifth** planet in the `planets_1.csv` file.
#
# You **must** access the values in `planets_1.csv` using the `planet_cell` function. Note that the fifth planet would be at **index** 4.
#
# The **attribute** of the `Planet` namedtuple object, the corresponding **column** of the `planets_1.csv` file where the value should be obtained from, and the correct **data type** for the value are listed in the table below:
#
# |Attribute of `Planet` object|Column of `planets_1.csv`|Data Type|
# |---------|------|---------|
# |`planet_name`|Planet Name|**string**|
# |`host_name`| - |**string**|
# |`discovery_method`|Discovery Method|**string**|
# |`discovery_year`|Discovery Year|**int**|
# |`controversial_flag`|Controversial Flag|**bool**|
# |`orbital_period`|Orbital Period [days]|**float**|
# |`planet_radius`|Planet Radius [Earth Radius]|**float**|
# |`planet_mass`|Planet Mass [Earth Mass]|**float**|
# |`semi_major_radius`|Orbit Semi-Major Axis [au]|**float**|
# |`eccentricity`|Eccentricity|**float**|
# |`equilibrium_temperature`|Equilibrium Temperature [K]|**float**|
# |`insolation_flux`|Insolation Flux [Earth Flux]|**float**|
#
#
# The value of the `host_name` attribute is found in `mapping_1.json`.

# +
# compute and store the answer in the variable 'fifth_planet', then display it

row_idx = 4 # the index of the planet we want to convert into a Planet object

# extract the values from planets_1_rows
planet_name = planet_cell(row_idx, 'Planet Name', planets_1_rows)
host_name = mapping_1_json[planet_name]
discovery_method = planet_cell(row_idx, 'Discovery Method', planets_1_rows)
discovery_year = planet_cell(row_idx, 'Discovery Year', planets_1_rows)
controversial_flag = planet_cell(row_idx, 'Controversial Flag', planets_1_rows)
orbital_period = planet_cell(row_idx, 'Orbital Period [days]', planets_1_rows)
planet_radius = planet_cell(row_idx, 'Planet Radius [Earth Radius]', planets_1_rows)
planet_mass = planet_cell(row_idx, 'Planet Mass [Earth Mass]', planets_1_rows)
semi_major_radius = planet_cell(row_idx, 'Orbit Semi-Major Axis [au]', planets_1_rows)
eccentricity = planet_cell(row_idx, 'Eccentricity', planets_1_rows)
equilibrium_temperature = planet_cell(row_idx, 'Equilibrium Temperature [K]', planets_1_rows)
insolation_flux = planet_cell(row_idx, 'Insolation Flux [Earth Flux]', planets_1_rows)

# initialize 'first_planet'
fifth_planet = Planet(planet_name, host_name, discovery_method, discovery_year,\
                  controversial_flag, orbital_period, planet_radius, planet_mass,\
                  semi_major_radius, eccentricity, equilibrium_temperature, insolation_flux)
fifth_planet
# -

grader.check("q12")


# ### Function 4: `get_planets(planet_file, mapping_file)`: 
#
# This function **must** take in as its input, a CSV file `planet_file` which contains data on planets in the same format as `planets_1.csv`, as well as a JSON file `mapping_file` which maps planets in `planet_file` to their host star in the same format as `mapping_1.json`. This function **must** return a **list** of `Planet` objects by combining the data in these two files. The `Planet` objects **must** appear in the same order as they do in `planet_file`.
#
# You **must** access the values in `planets_file` using the `planet_cell` function.
#
# You **must not** hardcode the name of the directory `data` into the `get_planets` function. Instead, you must pass it as a part of the arguments `planet_file` and `mapping_file`.
#
# Once again, as a reminder, the attributes of the `Planet` objects should be obtained from the **rows** of `planet_file` and from `mapping_file` and stored as follows:
#
# |Attribute of `Planet` object|Column of `planets_1.csv`|Data Type|
# |---------|------|---------|
# |`planet_name`|Planet Name|**string**|
# |`host_name`| - |**string**|
# |`discovery_method`|Discovery Method|**string**|
# |`discovery_year`|Discovery Year|**int**|
# |`controversial_flag`|Controversial Flag|**bool**|
# |`orbital_period`|Orbital Period [days]|**float**|
# |`planet_radius`|Planet Radius [Earth Radius]|**float**|
# |`planet_mass`|Planet Mass [Earth Mass]|**float**|
# |`semi_major_radius`|Orbit Semi-Major Axis [au]|**float**|
# |`eccentricity`|Eccentricity|**float**|
# |`equilibrium_temperature`|Equilibrium Temperature [K]|**float**|
# |`insolation_flux`|Insolation Flux [Earth Flux]|**float**|
#
# The value of the `host_name` attribute is found in `mapping_file`.
#
# In case any data in `planet_file` is **missing**, the corresponding value should be `None`.
#
# For example, when this function is called with the file `planets_1.csv` and `mapping_1.json` as the input, the **list** returned should look like:
#
# ```python
# [ Planet(planet_name='11 Com b', host_name='11 Com', discovery_method='Radial Velocity', discovery_year=2007, controversial_flag=False, orbital_period=323.21, planet_radius=12.2, planet_mass=4914.89849, semi_major_radius=1.178, eccentricity=0.238, equilibrium_temperature=None, insolation_flux=None),
#  Planet(planet_name='11 UMi b', host_name='11 UMi', discovery_method='Radial Velocity', discovery_year=2009, controversial_flag=False, orbital_period=516.21997, planet_radius=12.3, planet_mass=4684.8142, semi_major_radius=1.53, eccentricity=0.08, equilibrium_temperature=None, insolation_flux=None),
#  ...]
# ```

def get_planets(planet_file, mapping_file):
    # TODO: read planet_file to a list of lists
    data = process_csv(planet_file)
    # TODO: extract the header and rows from planet_file
    dataheader = data[0]
    datarows = data[1:]
    # TODO: read mapping_file to a dictionary
    try:
        mapping = read_json(mapping_file)
    except json.decoder.JSONDecodeError:
        return []
    # TODO: loop through each row in planet_file with indices
    list2 = []
    for row_idx in range(len(datarows)):
    # TODO: create a Planet object (namedTuple) for each row
        try:
            planet_name = planet_cell(row_idx, 'Planet Name', datarows, header = dataheader)
            host_name = mapping[planet_name]
            discovery_method = planet_cell(row_idx, 'Discovery Method', datarows, header = dataheader)
            discovery_year = planet_cell(row_idx, 'Discovery Year', datarows, header = dataheader)
            controversial_flag = planet_cell(row_idx, 'Controversial Flag', datarows, header = dataheader)
            orbital_period = planet_cell(row_idx, 'Orbital Period [days]', datarows, header = dataheader)
            planet_radius = planet_cell(row_idx, 'Planet Radius [Earth Radius]', datarows, header = dataheader)
            planet_mass = planet_cell(row_idx, 'Planet Mass [Earth Mass]', datarows, header = dataheader)
            semi_major_radius = planet_cell(row_idx, 'Orbit Semi-Major Axis [au]', datarows, header = dataheader)
            eccentricity = planet_cell(row_idx, 'Eccentricity', datarows, header = dataheader)
            equilibrium_temperature = planet_cell(row_idx, 'Equilibrium Temperature [K]', datarows, header = dataheader)
            insolation_flux = planet_cell(row_idx, 'Insolation Flux [Earth Flux]', datarows, header = dataheader)
            # TODO: add each Planet objet to a list
            currplan = Planet(planet_name, host_name, discovery_method, discovery_year,\
                          controversial_flag, orbital_period, planet_radius, planet_mass,\
                          semi_major_radius, eccentricity, equilibrium_temperature, insolation_flux)
        # TODO: return the list after the end of the loop
            list2.append(currplan)
        except (ValueError, IndexError, KeyError):
            continue
    return list2
grader.check("get_planets")

# **Question 13:** What are the **last five** `Planet` objects in the **list** returned by `get_planets` when `planet_file` is `planets_1.csv` and `mapping_file` is `mapping_1.json`?
#
# Your output **must** be a **list** of `Planet` objects.
#
# **Hint:** First, you **must** use the `get_planets` function to parse the data in `planets_1.csv` and `mapping_1.json` and create a **list** of `Planet` objects. Then, you may slice this **list** to get the last five `Planet` objects.

# +
# compute and store the answer in the variable 'last_five_planets_1', then display it
last_five_planets_1 = get_planets(os.path.join("data", "planets_1.csv"), os.path.join("data", "mapping_1.json"))[-5:]



last_five_planets_1
# -

grader.check("q13")

# **Question 14:** What are the `Planet` objects whose `controversial_flag` attribute is `True` in the **list** returned by `get_planets` when `planet_file` is `planets_2.csv` and `mapping_file` is `mapping_2.json`?
#
# Your output **must** be a **list** of `Planet` objects.

# +
# compute and store the answer in the variable 'controversial_planets', then display it 
listys = get_planets(os.path.join("data", "planets_2.csv"), os.path.join("data", "mapping_2.json"))
controversial_planets = [planet for planet in listys if planet.controversial_flag == True]



controversial_planets
# -
grader.check("q14")

# ### Data Cleaning 1: Broken CSV rows
#
# Our function `get_planets` works very well so far. However, it is likely that it will not work on all the files in the `data` directory. For example, if you use the function `get_planets` to read the data in `planets_4.csv` and `mapping_4.json`, you will most likely run into an error. **Try it yourself to verify!**
#
# The reason your code likely crashed is because there the file `planets_4.csv` is **broken**. For some reason, several rows in `planets_4.csv` have their data jumbled up. For example, in the **seventh** row of `planets_4.csv`, we come across this row:
#
# |Planet Name|Discovery Method|Discovery Year|Controversial Flag|Orbital Period [days]|Planet Radius [Earth Radius]|Planet Mass [Earth Mass]|Orbit Semi-Major Axis [au]|Eccentricity|Equilibrium Temperature [K]|Insolation Flux [Earth Flux]|
# |-----------|----------------|--------------|------------------|---------------------|----------------------------|------------------------|---------------------------|------------|---------------------------|----------------------------|
# 123.01000000|Radial Velocity|2009|0|61 Vir d|5.110|22.90000|0.476000|0.350000||
#
# We can see that for some reason, the value under the column `Planet Name` is a **number** while the value under the column `Orbital Period [days]` is a **string**. It is possible that these two columns of data got *swapped* here, but we cannot be sure about this.
#
# We will call such a **row** in a CSV file where the values under a column do not match the expected format to be a **broken row**. While it is possible to sometimes extract useful data from broken rows, in this project, we will simply **skip** broken rows.
#
# You **must** now go back to your definition of `get_planets` and edit it, so that any **broken rows get skipped**.
#
# **Hints:**
#
# 1. The simplest way to recognize if a row is broken is if you run into any **RunTime Errors** when you call the `get_planets` function. So, one simple way to skip bad rows would be to use `try/except` blocks to avoid processing any rows that cause the code to crash; remember **not** to use *bare* `try/except` blocks.
# 2. There are only **10** broken rows in `planets_4.csv`, and they are all **bunched up** at the very beginning and the very end of the dataset. You can manually **inspect** the **first 10 and last 10** rows, and figure out which of these rows are broken and why.
#
# **Important Warning:** You are **not** allowed to **hardcode** the indices of the broken rows. You may inspect `planets_4.csv` to identify how to tell a **broken row** apart. Therefore, to use the example of the **broken row** above, you **may not** hardcode to skip the **seventh** row of `planets_4.csv`. However, it is **acceptable** to make your function **skip** any row for which the value under the `Planet Name` is not numeric, by observing that this is the reason why the row is broken.

# **Question 15:** What are the **last five** `Planet` objects produced by `get_planets` when `planet_file` is `planets_4.csv` and `mapping_file` is `mapping_4.json`?
#
# Your output **must** be a **list** of `Planet` objects.

# +
# compute and store the answer in the variable 'last_five_planets_4', then display it
last_five_planets_4 = get_planets(os.path.join("data", "planets_4.csv"), os.path.join("data", "mapping_4.json"))[-5:]




last_five_planets_4
# -
grader.check("q15")

# ### Data Cleaning 2: Broken JSON files
#
# We are now ready to read **all** the files in the `data` directory and create a **list** of `Planet` objects for all the planets in the directory. However, if you try to use `get_planets` on all the planet CSV files and mapping JSON files, you will likely run into another error. **Try it for yourself by calling `get_planets` on all the files in `data`!**
#
# It is likely that your code crashed when you tried to read the data in `planets_5.csv` and `mapping_5.json`. This is because the file `mapping_5.json` is **broken**. Unlike **broken** CSV files, where we only had to skip the **broken rows**, it is much harder to parse **broken JSON files**. When a JSON file is **broken**, we often have no choice but to **skip the file entirely**.
#
# You **must** now go back to your definition of `get_planets` and edit it, so that if the JSON file is **broken**, then the file is completely skipped, and only an **empty list** is returned.
#
# **Important Warning:** You are **not** allowed to **hardcode** the name of the files to be skipped. You **must** use `try/except` blocks to determine whether the JSON file is **broken** and skip the file if it is.
#
# **Hint:** You might also want to review the **Project Requirements** at the start of this project, before you use `try/except`.

# ### Data Structure 4: `planets_list`
#
# You are now ready to read all the data about the planets stored in the `data` directory. You **must** now create a **list** containing `Planet` objects by parsing the data inside the files `planets_1.csv`, ..., `planets_5.csv` and `mapping_1.json`, ..., `mapping_5.json`.
#
# You **must** skip any **broken rows** in the CSV file, and also completely skip any **broken JSON files**. However, you are **not** allowed to **hardcode** the file you need to skip. You **must** call `get_planet` on **all** 5 pairs of files to answer this question.
#
# You **must** use the `get_planets` function on each of the five pairs of files in the `data` directory to create `planets_list`.
#
# **Warning:** Recall that the ordering of the files returned by the `os.listdir` function **depends on the operating system**. So, you need to be careful if your code relies on the ordering of the **list** returned by this function. One way to avoid any issues here would be to **sort** the **list** first, so that the ordering is identical across all operating systems.

# +
# define the variable 'planets_list' here,
# but do NOT display the variable at the end
planetslist = [os.path.join("data", file) for file in files_in_data if file.startswith("planets")]
planetslist = sorted(planetslist)
jsonlist = [os.path.join("data", path) for path in files_in_data if path.endswith(".json")]
jsonlist = sorted(jsonlist)
oop = []

for i in range(len(planetslist)):
    oop.extend(get_planets(planetslist[i], jsonlist[i]))
planets_list = oop
# -

grader.check("planets_list")

# If you wish to **verify** that you have read the files and defined `planets_list` correctly, you can check that `planets_list` has **5026** `Planet` objects in it. If it contains fewer or a greater number of planets, it is possible that you have accidentally parsed a broken CSV row in `planets_4.csv`, or accidentally parsed data from the broken JSON file `mapping_5.json`.

# **Question 16:** What is the output of `planets_list[5020:5025]`?
#
# Your output **must** be a **list** of `Planet` objects.
#
# **Hint:** If you did not get the right answer here, it is possible that you did not read the files in the correct **order**. In `planets_list`, the planets from `planets_1.csv` should appear first (in the order that they appear in the dataset), followed by the planets from `planets_2.csv`, `planets_3.csv`, `planets_4.csv`, and `planets_5.csv`.

# +
# compute and store the answer in the variable 'planets_5020_5025', then display it
planets_5020_5025 = planets_list[5020:5025]


planets_5020_5025
# -
grader.check("q16")

# **Question 17:** How many planets in `planets_list` were discovered in the year *2023*?
#
# Your output **must** be an **integer**.

# compute and store the answer in the variable 'planets_disc_2023', then display it
planets_disc_2023_list = [planet for planet in planets_list if planet.discovery_year == 2023]
planets_disc_2023 = len(planets_disc_2023_list)
planets_disc_2023
grader.check("q17")

# **Question 18:** Find the `Star` object around which the `Planet` named *TOI-2202 c* orbits.
#
# Your output **must** be a `Star` object.
#
# **Hint:** You **must** first find the `Planet` object with the `planet_name` *TOI-2202 c* and then use the `host_name` attribute to identify the name of the star around which the planet orbits. Then, you can get the `Star` object using the `stars_dict` **dictionary** defined above.
#
# You **must** exit the loop once you find the first planet with the target name.

# +
# compute and store the answer in the variable 'toi_2022_c_star', then display it
keyplan = None
for planet in planets_list:
    if planet.planet_name == "TOI-2202 c":
        keyplan = planet

hostname = keyplan.host_name
toi_2022_c_star = stars_dict[hostname]

toi_2022_c_star
# -
grader.check("q18")

# **Question 19:** Find the **average** `planet_radius` (in units of the radius of the Earth) of the planets that orbit stars with `stellar_radius` more than *10* (i.e. more than *10* times the radius of the Sun).
#
# Your output **must** be a **float**. You **must** skip any `Planet` objects with **missing** `planet_radius` data and any `Star` objects with **missing** `stellar_radius` data.

# +
# compute and store the answer in the variable 'avg_planet_radius_big_stars', then display it

it = 0
counter =0
for planet in planets_list:
    if planet.planet_radius != None:
        hostname1 = planet.host_name
        if stars_dict[hostname1].stellar_radius != None and stars_dict[hostname1].stellar_radius > 10:
            counter += 1
            it += planet.planet_radius

avg_planet_radius_big_stars = it/counter
avg_planet_radius_big_stars
# -
grader.check("q19")

# **Question 20:** Find all the `Planet` objects that orbit the **youngest** `Star` object.
#
# Your output **must** be a **list** of `Planet` objects (even if there is **only one** `Planet` in the list). The age of a `Star` can be found from its `stellar_age` column. You do **not** have to worry about any ties. There is a **unique** `Star` in the dataset which is the youngest star.

# +
# compute and store the answer in the variable 'youngest_star_planets', then display it
youngest_star_planets = []

starry = None
mini = None
for star in stars_dict:
    if (stars_dict[star].stellar_age != None) and (starry == None or stars_dict[star].stellar_age < mini):
        mini = stars_dict[star].stellar_age
        starry = star

for planet in planets_list:
    if starry == planet.host_name:
        youngest_star_planets.append(starry)

youngest_star_planets
# -
grader.check("q20")

grader.check("general_deductions")

grader.check("summary")

# ## Submission
# It is recommended that at this stage, you Restart and Run all Cells in your notebook.
# That will automatically save your work and generate a zip file for you to submit.
#
# **SUBMISSION INSTRUCTIONS**:
# 1. **Upload** the zipfile to Gradescope.
# 2. If you completed the project with a **partner**, make sure to **add their name** by clicking "Add Group Member"
# in Gradescope when uploading the zip file.
# 3. Check **Gradescope** results as soon as the auto-grader execution gets completed.
# 4. Your **final score** for this project is the score that you see on **Gradescope**.
# 5. You are **allowed** to resubmit on Gradescope as many times as you want to.
# 6. **Contact** a TA/PM if you lose any points on Gradescope for any **unclear reasons**.

# running this cell will create a new save checkpoint for your notebook
from IPython.display import display, Javascript
display(Javascript('IPython.notebook.save_checkpoint();'))

# !jupytext --to py p10.ipynb

public_tests.check_file_size("p10.ipynb")
grader.export(pdf=False, run_tests=False, files=["p10.py"])

#  


