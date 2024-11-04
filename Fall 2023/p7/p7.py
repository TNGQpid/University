# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# + [code] deletable=false editable=false
# import and initialize otter
import otter
grader = otter.Notebook("p7.ipynb")

# + editable=false
import public_tests

# +
# PLEASE FILL IN THE DETAILS
# enter none if you don't have a project partner
# you will have to add your partner as a group member on Gradescope even after you fill this

# project: p7
# submitter: sheberlein
# partner: sheberlein
# hours: 3

# + [markdown] deletable=false editable=false
# # Project 7: Soccer Stars

# + [markdown] deletable=false editable=false
# ## Learning Objectives:
#
# In this project you will demonstrate how to:
#
# - Write programs to interpret data present in csv files,
# - Use lists and dictionaries effectively to manage data,

# + [markdown] deletable=false editable=false
# ## Testing your code:
#
# Along with this notebook, you must have downloaded the file `public_tests.py`. If you are curious about how we test your code, you can explore this file, and specifically the function `get_expected_json`, to understand the expected answers to the questions.

# + [markdown] deletable=false editable=false
# <h2 style="color:red">Warning (Note on Academic Misconduct):</h2>
#
# Under any circumstances, **no more than two students are allowed to work together on a project** as mentioned in the course policies. If your code is flagged by our code similarity detection tools, **both partners will be responsible** for sharing/copying the code, even if the code is shared/copied by one of the partners with/from other non-partner student(s). Note that each case of plagiarism will be reported to the Dean of Students with a zero grade on the project. **If you think that someone cannot be your project partner then don’t make that student your lab partner.**
#
# **<font color = "red">Project partners must submit only one copy of their project on Gradescope, but they must include the names of both partners.</font>**

# + [markdown] deletable=false editable=false
# ## Project Description:
#
# In this project, we will analyze data in [`soccer_stars.csv`](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/blob/main/p7/soccer_stars.csv). This dataset has some data on nearly 20,000 soccer stars who play in the top soccer leagues across the world. The statistics in this dataset are obained from the video game [FC'24](https://www.ea.com/games/ea-sports-fc/fc-24) (formerly the FIFA series) and was collected from the website [https://sofifa.com/](https://sofifa.com/). We will look at various statistics about your favorite players and teams, and identify their strengths and weaknesses.

# + [markdown] deletable=false editable=false
# ## Dataset:
#
# A small portion of the dataset `soccer_stars.csv` is reproduced here:
#
# ID|Name|Age|Nationality|Team|League|Value|Wage|Attacking|Movement|Defending|Goalkeeping|Overall rating|Position|Height|Preferred foot
# --|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--
# 239085|E. Haaland|22|Norway|Manchester City|Premier League (England)|€185M|€340K|78.6|83.6|38.0|10.4|91|ST|195cm|Left
# 231747|K. Mbappé|24|France|Paris Saint Germain|Ligue 1 (France)|€181.5M|€230K|83.0|92.4|30.7|8.4|91|ST|182cm|Right
# 192985|K. De Bruyne|32|Belgium|Manchester City|Premier League (England)|€103M|€350K|82.4|77.6|63.0|11.2|91|CM|181cm|Right
# 202126|H. Kane|29|England|FC Bayern München|Bundesliga (Germany)|€119.5M|€170K|88.0|74.0|43.3|10.8|90|ST|188cm|Right
# 192119|T. Courtois|31|Belgium|Real Madrid|La Liga (Spain)|€63M|€250K|17.2|58.0|18.0|86.6|90|GK|199cm|Left

# + [markdown] deletable=false editable=false
# The dataset contains the following information about each player:
# - `ID` : the **unique ID** used by FC'24 for identifying each player,
# - `Name` : the **name** of the player,
# - `Age` : the **age** of the player,
# - `Nationality` : the **national team** the player represents,
# - `Team` : the **football club** that the player represents,
# - `League`: the **football league** that the player's club is a part of,
# - `Value` : the **value** of the player in the transfer market (in **Euros**),
# - `Wage` : the **weekly wages** earned by the player as per their contract (in **Euros**),
# - `Attacking` : the **total attacking stats** of the player (out of **100.0**),
# - `Movement` : the **total movement stats** of the player (out of **100.0**),
# - `Defending` : the **total defending stats** of the player (out of **100.0**),
# - `Goalkeeping` : the **total goalkeeping stats** of the player (out of **100.0**),
# - `Overall rating` : the **overall rating** of the player (out of **100**),
# - `Position` : the player's **favored position** on the soccer field,
# - `Height` : the **height** of the player (in **centimeters**),
# - `Preferred foot` : the player's **favored foot**.
#
# **Please go through [Lab-P7](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/tree/main/lab-p7) before starting this project.** The lab introduces some useful techniques necessary for parsing the dataset and for answering questions in this project.

# + [markdown] deletable=false editable=false
# ## Project Requirements:
#
# You **may not** hardcode indices in your code unless specified in the question. If you are not sure what hardcoding is, here is a simple test you can use to determine whether you have hardcoded:
#
# *If we were to change the data (e.g. add more soccer players, remove some players, change their statistics, or swap some columns or rows), would your code still find the correct answer to the question as it is asked?*
#
# If your answer to that question is *No*, then you have likely hardcoded something. Please reach out to TAs/PMs during office hours to find out how you can **avoid hardcoding**.
#
# In general, all your functions and code must be **case sensitive** unless the function or question description **explicitly** says otherwise.
#
# **Store** your final answer for each question in the **variable specified for each question**. This step is important because Otter grades your work by comparing the value of this variable against the correct answer.
#
# For some of the questions, we'll ask you to write (then use) a function to compute the answer.  If you compute the answer **without** creating the function we ask you to write, the Gradescope autograder will **deduct** points, even if the way you did it produced the correct answer.
#
# #### Required Functions:
#
# - `format_euros`
# - `cell`
# - `average_stat_by_position`
# - `best_player_of_team_at_position`
# - `best_starting_players_of`
#
#
# In this project, you will also be required to define certain **data structures**. If you do not create these data structures exactly as specified, the Gradescope autograder will **deduct** points, even if the way you did it produced the correct answer.
#
# #### Required Data Structures:
#
# - `players` 
#     
# Students are only allowed to use Python commands and concepts that have been taught in the course prior to the release of P7. Therefore, **you should not use the pandas module**. The Gradescope autograder will **deduct** points otherwise.
#
# For more details on what will cause you to lose points during code review and specific requirements, please take a look at the [Grading rubric](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/blob/main/p7/rubric.md).

# + [markdown] deletable=false editable=false
# ## Incremental Coding and Testing:
#
# You should always strive to do incremental coding. **Incremental coding enables you to avoid challenging bugs.** Always write a few lines of code and then test those lines of code, before proceeding to write further code. You can call the `print` function to test intermediate step outputs.
#
# We also recommend you do incremental testing: make sure to run the local tests as soon as you are done with a question. This will ensure that you haven't made a big mistake that might potentially impact the rest of your project solution. Please refrain from making multiple submissions on Gradescope for testing individual questions' answers. Instead use the local tests, to test your solution on your laptop.
#
# That said, it is **important** that you check the Gradescope test results as soon as you submit your project on Gradescope. Test results on Gradescope are typically available somewhere between 15 to 30 minutes after the submission.
#
# Also, remember to check with the [P7 rubric](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/blob/main/p7/rubric.md) to verify that you will not be losing any points during manual review.

# + [markdown] deletable=false editable=false
# ## Project Questions and Functions:
# -

# it is considered a good coding practice to place all import statements at the top of the notebook
# please place all your import statements in this cell if you need to import any more modules for this project
import csv


# + [markdown] deletable=false editable=false
# First, read the data stored in `soccer_stars.csv`. You **must** read the csv file and then get the header and rows (and store them into `csv_header` and `csv_rows` variables). You will **lose points** if you use any other names to store these variables.
#
# **Note**: It is recommended that you just copy/paste the code from your Lab-P7 notebook. However, instead of reading data from `small_soccer_stars.csv`, this time, you **must** read the data from `soccer_stars.csv`.
# -

# copy/paste the definition of `process_csv` here
def process_csv(filename):
    example_file = open(filename, encoding="utf-8")
    example_reader = csv.reader(example_file)
    example_data = list(example_reader)
    example_file.close()
    return example_data


# +
# use process_csv to read 'soccer_stars.csv'
csv_data = process_csv("soccer_stars.csv")

# split the header and other rows into appropriate variables
csv_header = csv_data[0]
csv_rows = csv_data[1:]

print(csv_header)
print(csv_rows[0:2])


# + [markdown] deletable=false editable=false
# We will now copy/paste some function and data structure definitions from Lab-P7 to get us started with the project.

# + [markdown] deletable=false editable=false
# ### Function 1: `format_euros(euros)` 
#
# You **must** write a helper function that takes in a **string** representing the `Wage` or `Value` (such as `"€250K"` or `"€158.5M"`), and converts it into an **int**.
#
# For example, `"€250K"` should be converted to `250000`, and `"€158.5M"` should be converted to `158500000`.
#
# You can **assume** that the first character of the input string `euros` always starts with the Euro symbol (€), and that **if** the last character is either `"K"` or `"M"`, it represents the preceeding number in thousands or millions, respectively. Note that the last character **need not** be `"K"` or `"M"` in all inputs. If the last character is not one of these letters, then the entire input string (except the starting €) can be **assumed** to be an **integer**.
#
# **Note:** You may copy/paste your definition of `format_euros` from Lab-P7 here.
# -

# define the `format_euros` function here
def format_euros(euros):
    euros = euros[1:]
    if euros[-1] == "K":
        euros = float(euros[0:-1])*1000
    elif euros[-1] == "M":
        euros = float(euros[0:-1]) * 1000000
    else:
        euros = float(euros)
    return int(euros)


# + deletable=false editable=false
grader.check("format_euros")


# + [markdown] deletable=false editable=false
# ### Function 2: `cell(row_idx, col_name)` 
#
# This function must take in a row index, `row_idx` and a column name, `col_name` as its inputs, and return the value in `soccer_stars.csv` stored there. There is **no missing data** in this dataset, so you do **not** have to worry about returning `None` for **missing data**.
#
# Your `cell` function **must** also typecast the values based on column names. These are the expected data types for each of the columns:
#
# - `ID` : **int**,
# - `Name` : **str**,
# - `Age` : **int**,
# - `Nationality` : **str**,
# - `Team` : **str**,
# - `League` : **str**,
# - `Value` : **int**,
# - `Wage` : **int**,
# - `Attacking` : **float**,
# - `Movement` : **float**,
# - `Defending` : **float**,
# - `Goalkeeping` : **float**,
# - `Overall rating` : **int**,
# - `Position` : **str**,
# - `Height` : **int**,
# - `Preferred foot` : **str**.
#
# Make special care to convert the `Height` into an **int** by slicing off the units, and to convert the `Wage` and `Value` into **ints** using the `format_euros` helper function.
#
# **Note:** You may copy/paste your definition of `cell` from Lab-P7 here. Since the variables `csv_header` and `csv_rows` are defined in this notebook to be data in `soccer_stars.csv`, the same function from Lab-P7 will now read the data from `soccer_stars.csv` instead of `small_soccer_stars.csv`.

# +
# define the `cell` function here

def cell(row_idx, col_name):
    col_idx = csv_header.index(col_name) # extract the `col_idx` from the `col_name`
    val = csv_rows[row_idx][col_idx]
    data = None
    if col_name == "ID" or col_name == "Age" or col_name == "Overall rating":
        data=int(val)
    elif col_name  == "Attacking" or col_name == "Movement" or col_name == "Defending" or col_name == "Goalkeeping":
        data = float(val)
    elif col_name == "Name" or col_name == "Nationality" or col_name == "Team" or col_name == "League" or col_name == "Preferred foot" or col_name == "Position":
        data = str(val)
    elif col_name == "Value" or col_name == "Wage":
        data = format_euros(val)
    elif col_name == "Height":
        data = int(val[:-2])
    return data


# + deletable=false editable=false
grader.check("cell")

# + [markdown] deletable=false editable=false
# ### Data Structure 1: `players` 
#
# You **must** now define a data structure `players` that stores all the data in `soccer_stars.csv` after processing the values. This data structure **must** be a **dictionary** of **dictionaries**. The **outer dictionary** must map each player `ID` to another **dictionary** which contains all the data about the player with that `ID`. Each **inner dictionary** corresponding to each player must map the **column names** to their **values** for that player.
#
# #### For the rest of the project, you MUST access data from `soccer_stars.csv` ONLY using this data structure `players`.
#
# The first few elements of `players` **must** look like this:
#
# ```python
# {239085: {'ID': 239085,
#           'Name': 'E. Haaland',
#           'Age': 22,
#           'Nationality': 'Norway',
#           'Team': 'Manchester City',
#           'League': 'Premier League (England)',
#           'Value': 185000000,
#           'Wage': 340000,
#           'Attacking': 78.6,
#           'Movement': 83.6,
#           'Defending': 38.0,
#           'Goalkeeping': 10.4,
#           'Overall rating': 91,
#           'Position': 'ST',
#           'Height': 195,
#           'Preferred foot': 'Left'},
#  231747: {'ID': 231747,
#           'Name': 'K. Mbappé',
#           'Age': 24,
#           'Nationality': 'France',
#           'Team': 'Paris Saint Germain',
#           'League': 'Ligue 1 (France)',
#           'Value': 181500000,
#           'Wage': 230000,
#           'Attacking': 83.0,
#           'Movement': 92.4,
#           'Defending': 30.7,
#           'Goalkeeping': 8.4,
#           'Overall rating': 91,
#           'Position': 'ST',
#           'Height': 182,
#           'Preferred foot': 'Right'},
#  192985: {'ID': 192985,
#           'Name': 'K. De Bruyne',
#           'Age': 32,
#           'Nationality': 'Belgium',
#           'Team': 'Manchester City',
#           'League': 'Premier League (England)',
#           'Value': 103000000,
#           'Wage': 350000,
#           'Attacking': 82.4,
#           'Movement': 77.6,
#           'Defending': 63.0,
#           'Goalkeeping': 11.2,
#           'Overall rating': 91,
#           'Position': 'CM',
#           'Height': 181,
#           'Preferred foot': 'Right'},
#  ...
# }
# ```
#
# **Note:** You may copy/paste your definition of `players` from Lab-P7 here. Since the variables `csv_header` and `csv_rows` are defined in this notebook to be data in `soccer_stars.csv`, the same code from Lab-P7 will now use the data from `soccer_stars.csv` instead of `small_soccer_stars.csv` to define `players`.

# +
# define the `players` data structure here
# but do NOT display it as it is very large
players = {}

for row_idx in range(len(csv_rows)):
    player = {} # initialize a new empty dictionary for the player at `row_idx`
    # TODO: loop through the `csv_header` and add each column to `player`
    #       *Hint*: Take a look at Question 17 and Question 18
    for header in csv_header:
        player[header] = cell(row_idx, header)
    player_id = cell(row_idx, "ID") # extract the `ID` of the `player`
    players[player_id] = player # add the `player_id`-`player` key-value pair to the dict `players` 

# + deletable=false editable=false
grader.check("players")

# + [markdown] deletable=false editable=false
# You are all set! You are now ready to start solving the questions.

# + [markdown] deletable=false editable=false
# **Question 1:** What are the **all** the statistics of the player with the `ID` *158023*?
#
# Your output **must** be a **dict** whose keys are **all** the **column names** in the dataset, and the corresponding values are the values under that column for the player with the given `ID`.

# +
# compute and store the answer in the variable 'stats_player_158023', then display it
stats_player_158023 = players[158023]


stats_player_158023

# + deletable=false editable=false
grader.check("q1")

# + [markdown] deletable=false editable=false
# **Question 2:** Find **all** the statistics of the **highest** valued (`Value`) player.
#
# Your output **must** be a **dict** whose keys are **all** the **column names** in the dataset, and the corresponding values are the values under that column for the player with the **highest** `Value`.
#
# You do **not** have to worry about any ties. There is a **unique** player in the dataset with the highest `Value`.

# +
# compute and store the answer in the variable 'highest_valued_stats', then display it
bestp = None
highest_valued_stats = {}
for player in players:
    if bestp == None or players[player]["Value"] > players[bestp]["Value"]:
        bestp = player
        highest_valued_stats = players[player]


highest_valued_stats

# + deletable=false editable=false
grader.check("q2")

# + [markdown] deletable=false editable=false
# **Question 3:** What is the `Nationality` of the player with the **highest** `Wage`?
#
# You do **not** have to worry about any ties. There is a **unique** player in the dataset with the highest `Wage`.

# +
# compute and store the answer in the variable 'highest_wage_nationality', then display it
highest_wage_nationality = None
wageb = None
wagep = None
for player in players:
    if wageb == None or players[player]["Wage"] > players[wagep]["Wage"]:
        wagep = player
        wageb = players[player]["Wage"]

highest_wage_nationality = players[wagep]["Nationality"]
highest_wage_nationality

# + deletable=false editable=false
grader.check("q3")

# + [markdown] deletable=false editable=false
# **Question 4:** What is the favored `Position` of the player with the **highest** `Wage`?
#
# You **must** not recompute the player with the highest `Wage`. Instead, you can use the `ID` you found in your answer to **Question 3**, and just find the `Position` of that player. If you did not store the `ID` of that player in **Question 3**, go back and **modify** your answer there, so you can directly use it here.

# +
# compute and store the answer in the variable 'highest_wage_position', then display it
highest_wage_position = players[wagep]["Position"]


highest_wage_position

# + deletable=false editable=false
grader.check("q4")

# + [markdown] deletable=false editable=false
# **Question 5:** Find all the teams (`Team`) that belong to the `League` *Premier League (England)*.
#
# Your output **must** be a **list** of **strings** with **no duplicates**. The order does **not** matter.

# +
# compute and store the answer in the variable 'premier_league_teams', then display it
premier_league_teams = []
for player in players:
    if players[player]["League"] == "Premier League (England)":
        premier_league_teams.append(players[player]["Team"])

premier_league_teams = list(set(premier_league_teams))    
premier_league_teams

# + deletable=false editable=false
grader.check("q5")

# + [markdown] deletable=false editable=false
# **Question 6:** Find the **number** of players with each `Preferred foot`. 
#
# Your output **must** be a **dictionary** that maps each `Preferred Foot` (i.e., *Right* and *Left*) to the **number** of players with that `Preferred foot`. Your output **must** look like this:
#
# ```python
# {'Left': 4585, 'Right': 15082}
# ```
#
# You **must** not **hardcode** the feet (i.e., *Right* and *Left*) in your answer. Instead, you must extract that information from the dictionary `players`.  Remember that you **must** extract all the information from the csv file only using the data structure `players`.

# +
# compute and store the answer in the variable 'preferred_foot_count', then display it
preferred_foot_count = {}

# loop over each player in `players`
for player in players:
    preferred_foot = players[player]["Preferred foot"] # find the `Preferred foot` of the player
    # if the `preferred_foot` doesn't already exist in the new dict,
    # add it and set the initial value to 1
    if preferred_foot not in preferred_foot_count:
        preferred_foot_count[preferred_foot] = 1
    # if the `preferred_foot` already exists in the new dict,
    # just update the value
    else:
        preferred_foot_count[preferred_foot] += 1

preferred_foot_count

# + deletable=false editable=false
grader.check("q6")

# + [markdown] deletable=false editable=false
# **Question 7:** What is the **average** `Overall rating` of *Right* vs *Left* footed players (`Preferred foot`)?
#
# Your output **must** be a **dict** that looks as follows:
#
# ```python
# {'Left': 64.3494002181025, 'Right': 63.14427794722185}
# ```
#
# You **must** not **hardcode** the feet (i.e., *Right* and *Left*) in your answer. Instead, you must extract that information from the dictionary `players`.
#
# **Hint**: You should first compute a dictionary that computes the **total** `Overall rating` of *Left* and *Right* footed players, then divide the values in this dictionary by the corresponding values in the dictionary you computed in **Question 6** to find the **average**.

# +
# compute and store the answer in the variable 'preferred_foot_avg_overall', then display it
preferred_foot_dict = {}
preferred_foot_avg_overall = {}

for player in players:
    preferred_foot = players[player]["Preferred foot"]
    if preferred_foot == players[player]["Preferred foot"] not in preferred_foot_dict:
        preferred_foot_dict[preferred_foot] = players[player]["Overall rating"]
    else:
        preferred_foot_dict[preferred_foot] += players[player]["Overall rating"]
        
for i in preferred_foot_dict:
    preferred_foot_avg_overall[i] = preferred_foot_dict[i] / preferred_foot_count[i]

preferred_foot_avg_overall

# + deletable=false editable=false
grader.check("q7")

# + [markdown] deletable=false editable=false
# **Food for thought:** We notice that Left-footed players have a slightly higher `Overall rating` on **average** than Right-footed players. Can you explain what is going on here?
# -

# Food for thought is an entirely OPTIONAL exercise
# you may leave your thoughts here as a comment if you wish to


# + [markdown] deletable=false editable=false
# ### Soccer Positions
#
# We will now analyze the various **positions** on the soccer field. Before we get started, it will be helpful to have at least a rough idea as to what the different **positions** are. Here is an image that explains where each **position** is expected to play on the soccer field:
# -

# <div><img src="attachment:positions.jpg" style="height: 400px;"/></div>

# + [markdown] deletable=false editable=false
# The **bottom** of the image is the team's goalpost, and the **top** is the opposite team's goalpost. The positions closer to the **bottom** of the image are broadly tasked with **protecting** their team's goal, while the positions closer to the **top** of the image are tasked with **scoring** goals against the opposition.
#
# Apart from the *Goalkeeper* (**GK**), the **five** players closest to their own goalpost (**LWB**, **LB**, **CB**, **RB**, **RWB**) are called *Defenders*. The **five** players in the middle of the field (**CDM**, **LM**, **CM**, **RM**, **CAM**) are called *Midfielders*, and the **four** players closest to the oppposite team's goalpost (**LW**, **CF**, **RW**, **ST**) are called the *Forwards*.
#
# With this brief explanation, you are ready to tackle more questions in this project!

# + [markdown] deletable=false editable=false
# **Question 8:** For **each** `Position`, find the **number** of players who play in that `Position`.
#
# Your output **must** be a **dict** that looks as follows:
#
# ```python
# {'ST': 3126,
#  'CM': 1076,
#  'GK': 2084,
#  'CF': 62,
#  'CAM': 2911,
#  ...
# }
# ```
#
# You **must** not **hardcode** the positions in your answer. Instead, you must extract that information from the dictionary `players`.

# +
# compute and store the answer in the variable 'positions_count', then display it
positions_count = {}
for player in players:
    if players[player]["Position"] not in positions_count:
        positions_count[players[player]["Position"]] = 1
    else:
        positions_count[players[player]["Position"]] += 1


positions_count

# + deletable=false editable=false
grader.check("q8")

# + [markdown] deletable=false editable=false
# **Question 9:** Find the **average** `Age` of players in **each** `Position`.
#
# Your output **must** be a **dict** that looks as follows:
#
# ```python
# {'ST': 23.2552783109405,
#  'CM': 24.481412639405203,
#  'GK': 23.379078694817657,
#  'CF': 28.822580645161292,
#  'CAM': 22.032291308828583,
#  ...
# }
# ```
#
# You **must** not **hardcode** the positions in your answer. Instead, you must extract that information from the dictionary `players`.

# +
# compute and store the answer in the variable 'positions_avg_age', then display it
positions_avg_age = {}
for player in players:
    if players[player]["Position"] not in positions_avg_age:
        positions_avg_age[players[player]["Position"]] = players[player]["Age"]
    else:
        positions_avg_age[players[player]["Position"]] += players[player]["Age"]

for i in positions_avg_age:
    positions_avg_age[i] = positions_avg_age[i] / positions_count[i]



positions_avg_age

# + deletable=false editable=false
grader.check("q9")

# + [markdown] deletable=false editable=false
# **Food for thought:** Notice that players at the position **CF** (Center Forward) are significantly older on average than players who play at other positions. Similarly, players at positions **LW** (Left Wing Forward), and **RW** (Right Wing Forward) are also older on average than players at other positions. Can you explain this phenomenon? On average do you notice any patterns in the ages of the players as we move up the field from the *Defenders* to the *Forwards*?
# -

# Food for thought is an entirely OPTIONAL exercise
# you may leave your thoughts here as a comment if you wish to


# + [markdown] deletable=false editable=false
# **Question 10:** Find the **average** `Height` of players in **each** `Position`.
#
# Your output **must** be a **dict** that looks as follows:
#
# ```python
# {'ST': 182.81222008957133,
#  'CM': 179.23234200743494,
#  'GK': 188.366122840691,
#  'CF': 178.24193548387098,
#  'CAM': 176.6496049467537,
#  ...
# }
# ```
#
# You **must** not **hardcode** the positions in your answer. Instead, you must extract that information from the dictionary `players`.

# +
# compute and store the answer in the variable 'positions_avg_height', then display it
positions_avg_height = {}
for player in players:
    if players[player]["Position"] not in positions_avg_height:
        positions_avg_height[players[player]["Position"]] = players[player]["Height"]
    else:
        positions_avg_height[players[player]["Position"]] += players[player]["Height"]

for i in positions_avg_height:
    positions_avg_height[i] = positions_avg_height[i] / positions_count[i]

positions_avg_height

# + deletable=false editable=false
grader.check("q10")

# + [markdown] deletable=false editable=false
# **Food for thought:** Notice that players at the position **GK** (Goalkeeper) tend to be the tallest by far, followed by players at the position **CB** (Center Back). Can you explain why this is the case? Also, notice that although the positions **CF** (Center Forward) and **ST** (Striker) appear very close to each other in the Position map, there is a significant difference in their average heights (and average ages). What does that tell you about the roles of the players at these positions?
# -

# Food for thought is an entirely OPTIONAL exercise
# you may leave your thoughts here as a comment if you wish to


# + [markdown] deletable=false editable=false
# ### Function 3: `average_stat_by_position(col_name)` 
#
# This function must take in a `col_name` of a **numerical** column (such as `"Age"`, `"Overall rating"`, `"Value"`, `"Wage"`, `"Attacking"`, `"Movement"`, `"Defending"`, `"Goalkeeping"`, or `"Height"`), and then return a **dict** that maps **each** `Position` in the dataset to the **average** value under the `col_name` of all the players at that `Position`.
#
# You may assume that the values under the given `col_name` are always **numerical** (i.e., **int** or **float**).
#
# **Hint**: Recall that the dictionary `players` represents each player as a **dict**. So, if you wanted to extract a particular `stat` of a player, you can **index** directly **without looping** through the **dict**.
# -

# define the `average_stat_by_position` function here
def average_stat_by_position(col_name):
    position_avg_value = {}
    count = {}
    for player in players:
        if players[player]["Position"] not in position_avg_value:
            position_avg_value[players[player]["Position"]] = players[player][col_name]
        else:
            position_avg_value[players[player]["Position"]] += players[player][col_name]
        if players[player]["Position"] not in count:
            count[players[player]["Position"]] = 1
        else:
            count[players[player]["Position"]] += 1
    for i in position_avg_value:
        position_avg_value[i] = position_avg_value[i] / count[i]
    return position_avg_value


# + deletable=false editable=false
grader.check("average_stat_by_position")

# + [markdown] deletable=false editable=false
# **Question 11:** Find the **average** `Attacking` stat of players in **each** `Position`.
#
# Your output **must** be a **dict** that looks as follows:
#
# ```python
# {'ST': 56.65591810620609,
#  'CM': 57.14814126394047,
#  'GK': 14.351439539347414,
#  'CF': 64.66774193548387,
#  'CAM': 55.027825489522414,
#  ...
# }
# ```
#
# You **must** use the `average_stat_by_position` function to answer this question.

# +
# compute and store the answer in the variable 'positions_avg_attacking', then display it
positions_avg_attacking = average_stat_by_position("Attacking")


positions_avg_attacking

# + deletable=false editable=false
grader.check("q11")

# + [markdown] deletable=false editable=false
# **Food for thought:** Which positions have the highest average `Attacking` stat? Do you notice any anomalies? Notice that among the *Defenders*, the position **CB** (Center Back) has a significantly **lower** `Attacking` stat than other positions such as **LB** (Left Back), **RB** (Right Back), **LWB** (Left Wing Back), and **RWB** (Right Wing Back). Similarly, note that the **Midfield** position **CM** (Center Midfield) has a higher average than more offensive positions such as **CAM** (Center Attacking Midfield) and **ST** (Striker). Can you explain this?
# -

# Food for thought is an entirely OPTIONAL exercise
# you may leave your thoughts here as a comment if you wish to


# + [markdown] deletable=false editable=false
# **Question 12:** Find the **average** `Movement` stat of players in **each** `Position`.
#
# Your output **must** be a **dict** that looks as follows:
#
# ```python
# {'ST': 64.60620601407543,
#  'CM': 65.4442379182156,
#  'GK': 38.34232245681379,
#  'CF': 67.86129032258067,
#  'CAM': 68.510958433528,
#  ...
# }
# ```
#
# You **must** use the `average_stat_by_position` function to answer this question.

# +
# compute and store the answer in the variable 'positions_avg_movement', then display it
positions_avg_movement = average_stat_by_position("Movement")

positions_avg_movement

# + deletable=false editable=false
grader.check("q12")

# + [markdown] deletable=false editable=false
# **Food for thought:** Which positions have the highest average `Movement` stat? Notice that the players on the wings have higher `Movement` on average than players in the center of the field. Can you explain this? Do you notice any **correlations** between the `Movement` and another statistic that we have already looked at? If so, can you explain why that **correlation** exists?
# -

# Food for thought is an entirely OPTIONAL exercise
# you may leave your thoughts here as a comment if you wish to


# + [markdown] deletable=false editable=false
# **Question 13:** **Which** `Position` has the **highest** `Defending` stat on **average**?
#
# Your output **must** be a **string** that represents the `Position` with the **highest** `Defending` stat. You do **not** have to worry about breaking any ties. There is a **unique** `Position` with the **highest** `Defending` stat.
#
# You **must** use the `average_stat_by_position` function to answer this question.
# -

# compute and store the answer in the variable 'best_defending_position', then display it
best_defending_positio = average_stat_by_position("Defending")
b = None
for position in best_defending_positio:
    if b == None or best_defending_positio[position] > best_defending_positio[b]:
        b = position
best_defending_position = b
best_defending_position

# + deletable=false editable=false
grader.check("q13")


# + [markdown] deletable=false editable=false
# ### Forming Teams
#
# For the rest of this project, we will attempt to construct **teams** for the various teams in our dataset.
#
# To start with, it would be useful to identify the **best** player at any given `Position` for a `Team`. We could get more fancy here, by using a stat such as `Defending`, or perhaps a combination of stats such as `Defending`, `Movement`, and `Height` to identify the **best** *CB*, and use stats such as `Attacking` to identify the **best** *CF*.
#
# However, we will keep it **simple** here, and just use the `Overall rating` to determine the **best** players.

# + [markdown] deletable=false editable=false
# ### Function 4: `best_player_of_team_at_position(position, team)` 
#
# This function must take in a `position` as well as a `team` and then return the `ID` of the player who plays for the given `team`, and has the **highest** `Overall rating` among **all other players** who play at that `position` for the same `team`.
#
# In case two players are **tied** with the **same** `Overall rating`, the ties **must** be broken in favor of the player with the **smaller** `ID`.
#
# In case there are **no** players who play at the given `position` for the given `team`, then the function **must** return `None`.
#
# **Note**: It is important to find the `ID` of the best player, and **not** something like their `Name`. This is because if we have the `ID`, we can then use the `players` **dict** to extract **all** statistics about the player.
# -

# define the `best_player_of_team_at_position` function here
def best_player_of_team_at_position(team, position):
    highest_rating = 0
    highest_id = None
    for player in players:
        if players[player]["Team"] == team and players[player]["Position"] == position:
            if players[player]["Overall rating"] == highest_rating:
                if highest_id > player:
                    highest_rating = players[player]["Overall rating"]
                    highest_id = player
            elif highest_id == None or players[player]["Overall rating"] > highest_rating:
                highest_rating = players[player]["Overall rating"]
                highest_id = player
    return highest_id


# + deletable=false editable=false
grader.check("best_player_of_team_at_position")

# + [markdown] deletable=false editable=false
# **Question 14:** **What** is the `ID` of the **best** (highest `Overall rating`) player at `Position` *CDM* for the `team` *Manchester United*?
#
# You **must** use the `best_player_of_team_at_position` function to answer this question.
# -

# compute and store the answer in the variable 'best_cdm_man_utd_id', then display it
best_cdm_man_utd_id = best_player_of_team_at_position("Manchester United", "CDM")
best_cdm_man_utd_id

# + deletable=false editable=false
grader.check("q14")

# + [markdown] deletable=false editable=false
# **Question 15:** **What** are the statistics of the **best** (highest `Overall rating`) player at `Position` *RW* for the `team` *Liverpool*?
#
# You **must** use the `best_player_of_team_at_position` function to answer this question.

# +
# compute and store the answer in the variable 'best_rw_liverpool', then display it
p = best_player_of_team_at_position("Liverpool", "RW")
best_rw_liverpool = players[p]

best_rw_liverpool

# + deletable=false editable=false
grader.check("q15")


# + [markdown] deletable=false editable=false
# ### Forming Teams
#
# Every team would like to **start** their games with their **best** players on the field at each position. Now that we have a function for finding the **best** player at any `Position`, we can use it identify the **best** player at **each** `Position` for any `Team`.
#
# There are a few problems with this approach. For a start, *most* teams will **not** have players for **each** `Position`. For example, a team which uses a *Striker* (**ST**) might not need a *Center Forward* (**CF**) as well. Alternately, a team might play **two** *Center Midfielders* (**CM**) and **not** use any *Right Midfielders* (**RM**) or *Left Midfielders* (**LM**) at all.
#
# For now, we will not deal with these complexities. We will simply pick the **best** player for **each** `Position`, to form a team. We also won't concern ourselves with **how many** players are picked in total.

# + [markdown] deletable=false editable=false
# ### Function 5: `best_starting_players_of(team)` 
#
# This function must take in a `team` and return a **dict** mapping each `Position` to the `ID` of the **best player** (i.e., player with the **highest** `Overall`) at that `Position` for the given `team`.
#
# In the case where two players are **tied** with the **same** `Overall rating`, the ties **must** be broken in favor of the player with the **smaller** `ID`.
#
# In the case where there are **no** players who play at a particular `Position` for the given `team`, the `Position` must **not** appear as a **key** in the **dictionary**.
# -

# define the `best_starting_players_of` function here
def best_starting_players_of(team):
    pos_dict = {}
    for position in positions_count:
        if position not in pos_dict:
            if best_player_of_team_at_position(team, position):
                pos_dict[position] = best_player_of_team_at_position(team, position)
    return pos_dict


# + deletable=false editable=false
grader.check("best_starting_players_of")

# + [markdown] deletable=false editable=false
# **Question 16:** **Who** are the **best starting players** of the `Team` *Paris Saint Germain*?
#
# Your output **must** be a **dict** that maps each `Position` for which *Paris Saint Germain* has a player to the `ID` of the **best** player (i.e., **highest** `Overall rating`) they have at that position.
#
# Your output **must** be a **dict** that looks as follows:
#
# ```python
# {'CDM': 200888,
#  'GK': 230621,
#  'LW': 202166,
#  'RW': 231443,
#  'RB': 235212,
#  'CAM': 255253,
#  'CB': 207865,
#  'RM': 264652,
#  'CM': 199556,
#  'LB': 252145,
#  'ST': 231747}
# ```
#
# You **must** use the `best_starting_players_of` function to answer this question.

# +
# compute and store the answer in the variable 'best_starters_of_psg', then display it
best_starters_of_psg = best_starting_players_of("Paris Saint Germain")

best_starters_of_psg

# + deletable=false editable=false
grader.check("q16")

# + [markdown] deletable=false editable=false
# **Question 17:** **What** are the names (`Name`) of the **best starting players** of the `Team` *FC Bayern München*?
#
# Your output **must** be a **dict** that maps each `Position` for which *FC Bayern München* has a player to the `Name` of the **best** player (i.e., **highest** `Overall rating`) they have at that position.
#
# Your output **must** be a **dict** that looks as follows:
#
# ```python
# {'CDM': 'J. Kimmich',
#  'LM': 'K. Coman',
#  'GK': 'O. Kahn',
#  'RW': 'B. Sarr',
#  'RWB': 'P. Lahm',
#  'LWB': 'F. Krätzig',
#  'CAM': 'J. Musiala',
#  'CB': 'M. de Ligt',
#  'RM': 'S. Gnabry',
#  'CM': 'L. Goretzka',
#  'ST': 'H. Kane'}
# ```
#
# You **must** use the `best_starting_players_of` function to answer this question.
#
# **Note**: If you cannot type the characters of the team's name using your keyboard, you can just copy/paste it from the question above.

# +
# compute and store the answer in the variable 'best_starters_of_bayern', then display it
best_starters_of_bayern = best_starting_players_of("FC Bayern München")
for position in best_starters_of_bayern:
    best_starters_of_bayern[players[best_starters_of_bayern[position]]["Position"]] = players[best_starters_of_bayern[position]]["Name"]
    

best_starters_of_bayern

# + deletable=false editable=false
grader.check("q17")

# + [markdown] deletable=false editable=false
# **Question 18:** What is the **cumulative** `Value` of the **bench** of the `Team` *FC Barcelona*?
#
# The **bench** refers to the players in the squad of the team (i.e., players whose `Team` is *FC Barcelona*), who are **not** one of the **best starting players**. The **cumulative** `Value` refers to the **sum** of the `Value` of **all** the players on the **bench**.
#
# **Hint**: You can use the `best_starting_players_of` function to identify the **best starting players** of *FC Barcelona*, and then identify all the players from that team, who are **not** among its best starting players.

# +
# compute and store the answer in the variable 'bench_value_barcelona', then display it
best_starting_players = []
best_players_with_pos = best_starting_players_of("FC Barcelona")
for position in best_players_with_pos:
    best_starting_players.append(best_players_with_pos[position])

bench_value_barcelona = 0
for player in players:
    if (players[player]["Team"] == "FC Barcelona") and (player not in best_starting_players):
        bench_value_barcelona += players[player]["Value"]
    
bench_value_barcelona

# + deletable=false editable=false
grader.check("q18")

# + [markdown] deletable=false editable=false
# **Question 19:** **Find** the **average** `Attacking` stat of the **best starting players** for **each** `Team` in the `League` *Premier League (England)*.
#
# Your output **must** be a **dict** that maps **each** `Team` in the `League` *Premier League (England)* to the **sum** of `Attacking` stats of all the **best starting players** of that `Team` **divided** by the **number** of **best starting players** of that `Team`.
#
# Recall that you already made a **list** of all the teams in *Premier League (England)* to answer **Question 5**. You can loop through that **list** instead of computing the teams in *Premier League (England)* again, or looping unnecessarily over a larger data structure.
#
# **Hint**: You can loop through all the teams in the given league, find the **best starting players** of **each** team, then have a nested loop to find the **average** of the `Attacking` stat of all the **best starting players** of that team.

# +
# compute and store the answer in the variable 'avg_attacking_prem_league', then display it
playerd = {}
counter = 0
for team in premier_league_teams:
    best_starting_players = []
    best_players_with_pos = best_starting_players_of(team)
    
    for position in best_players_with_pos:
        best_starting_players.append(best_players_with_pos[position])
        
    for player in best_starting_players:
        if team not in playerd:
            playerd[team] = players[player]["Attacking"]
        else:
            playerd[team] += players[player]["Attacking"]
        counter += 1
    playerd[team] = playerd[team] / counter
    counter = 0
        

avg_attacking_prem_league = playerd

# + deletable=false editable=false
grader.check("q19")

# + [markdown] deletable=false editable=false
# **Question 20:** **Which** `Team` in the `League` *Premier League (England)*  has the **highest** **average** `Attacking` stat among its **best starting players**?
#
# You do **not** have to worry about breaking any ties. There is a **unique** `Team` whose **best starting players** have the **highest** **average** `Attacking` stat.
#
# You **must** **not** recompute the **average** `Attacking` stat of the **best starting players** of all teams in the *Premier League (England)*. Instead, use the dictionary that you have already computed to answer this question.

# +
# compute and store the answer in the variable 'best_attackers_prem_league', then display it
best_attackers_prem_league = None
bestattacking = 0
for team in avg_attacking_prem_league:
    if best_attackers_prem_league == None or avg_attacking_prem_league[team] > bestattacking:
        best_attackers_prem_league = team
        bestattacking = avg_attacking_prem_league[team]


best_attackers_prem_league

# + deletable=false editable=false
grader.check("q20")

# + deletable=false editable=false
grader.check("general_deductions")

# + deletable=false editable=false
grader.check("summary")

# + [markdown] deletable=false editable=false
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

# + [code] deletable=false editable=false
# running this cell will create a new save checkpoint for your notebook
from IPython.display import display, Javascript
display(Javascript('IPython.notebook.save_checkpoint();'))

# + [code] deletable=false editable=false
# !jupytext --to py p7.ipynb

# + [code] deletable=false editable=false
public_tests.check_file_size("p7.ipynb")
grader.export(pdf=False, run_tests=False, files=["p7.py"])

# + [markdown] deletable=false editable=false
#  
