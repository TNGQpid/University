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

# + [code]
# import and initialize otter
import otter
grader = otter.Notebook("p12.ipynb")
# -

import public_tests

# +
# PLEASE FILL IN THE DETAILS
# Enter none if you don't have a project partner
# You will have to add your partner as a group member on Gradescope even after you fill this

# project: p12
# submitter: sheberlein
# partner: sheberlein

# + [markdown] deletable=false editable=false
# # Project 12: World University Rankings

# + [markdown] deletable=false editable=false
# ## Learning Objectives:
#
# In this project, you will demonstrate your ability to
#
# * read and write files,
# * create and use `Pandas DataFrames`,
# * use `BeautifulSoup` to parse web pages.
#
# Please go through [Lab-P12](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/tree/main/lab-p12) before working on this project. The lab introduces some useful techniques related to this project.

# + [markdown] deletable=false editable=false
# <h2 style="color:red">Warning (Note on Academic Misconduct):</h2>
#
# **IMPORTANT**: **P12 and P13 are two parts of the same data analysis.** You **cannot** switch project partners between these two projects. That is if you partner up with someone for P12, you have to sustain that partnership until the end of P13. Now may be a good time to review [our course policies](https://cs220.cs.wisc.edu/f23/syllabus.html).
#
# Under any circumstances, **no more than two students are allowed to work together on a project** as mentioned in the course policies. If your code is flagged by our code similarity detection tools, **both partners will be responsible** for sharing/copying the code, even if the code is shared/copied by one of the partners with/from other non-partner student(s). Note that each case of plagiarism will be reported to the Dean of Students with a zero grade on the project. **If you think that someone cannot be your project partner then don’t make that student your lab partner.**
#
# **<font color = "red">Project partners must submit only one copy of their project on Gradescope, but they must include the names of both partners.</font>**

# + [markdown] deletable=false editable=false
# ## Testing your code:
#
# Along with this notebook, you must have downloaded the files `public_tests.py` and `expected_dfs.html`. If you are curious about how we test your code, you can explore this file, and specifically the output of the function `get_expected_json`, to understand the expected answers to the questions.
#
# For answers involving DataFrames, `public_tests.py` compares your tables to those in `expected_dfs.html`, so take a moment to open that file on a web browser (from Finder/Explorer). `public_tests.py` doesn't care if you have extra rows or columns, and it doesn't care about the order of the rows or columns. However, you must have the correct values at each index/column location shown in `expected_dfs.html`.

# + [markdown] deletable=false editable=false
# ## Introduction:
#
# For this project, you're going to analyze World University Rankings!
#
# Specifically, you're going to use Pandas to analyze various statistics of the top ranked universities across the world, over the last three years.
#
# Start by downloading the files `public_tests.py`, and `expected_dfs.html`.
#
# **Important Warning:** Do **not** download any of the other `json` or `html` files manually (you **must** write Python code to download these automatically, as in Lab-P12). When we run the autograder, the other files such as `rankings.json`, `2021.html`, `2022.html`, `2023.html` will **not** be in the directory. So, unless your `p12.ipynb` downloads these files, the Gradescope autograder will **deduct** points from your public score. More details can be found in the **Setup** section of the project.

# + [markdown] deletable=false editable=false
# ## Data:
#
# For this project, we will be analyzing statistics about world university rankings adapted from [here](https://cwur.org/). These are the specific webpages that we extracted the data from:
#
# * https://cwur.org/2020-21.php
# * https://cwur.org/2021-22.php
# * https://cwur.org/2023.php
#
# Later in the project, you will be scraping these webpages and extracting the data yourself. Since we don't want all of you bombarding these webpages with requests, we have made snapshots of these webpages, and hosted them on GitLab. You can find the snapshots here:
#
# * https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/tree/main/p12/2021.html
# * https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/tree/main/p12/2022.html
# * https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/tree/main/p12/2023.html
#
# We have also tweaked the snapshots a little, to streamline the process of data extraction for you. You will be extracting the data from these three html pages and analyzing them. However, to make the start of the project a little easier, we have already parsed the files for you! We have gathered the data from these html files, and collected them in a single json file, which can be found here:
#
# * https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/raw/main/p12/rankings.json
#
# You will work with this json file for most of this project. At the end of this project, you will generate an identical json file by parsing the html files yourself.

# + [markdown] deletable=false editable=false
# ## Project Requirements:
#
# You **may not** hardcode indices in your code. You **may not** manually download **any** files for this project, unless you are **explicitly** told to do so. For all other files, you **must** use the `download` function to download the files.
#
# **Store** your final answer for each question in the **variable specified for each question**. This step is important because Otter grades your work by comparing the value of this variable against the correct answer.
#
# For some of the questions, we'll ask you to write (then use) a function to compute the answer. If you compute the answer **without** creating the function we ask you to write, the Gradescope autograder will **deduct** points from your public score, even if the way you did it produced the correct answer.
#
# #### Required Functions:
# - `download`
# - `parse_html`
#
# In this project, you will also be required to define certain **data structures**. If you do not create these data structures exactly as specified, the Gradescope autograder will **deduct** points from your public score, even if the way you did it produced the correct answer.
#
# #### Required Data Structures:
# - `rankings`
# - `year_2021_ranking_df`
# - `year_2022_ranking_df`
# - `year_2023_ranking_df`
# - `institutions_df`
#
# In addition, you are also **required** to follow the requirements below:
# * **Avoid using loops to iterate over pandas dataframes and instead use boolean indexing.**
# * Do **not** use `loc` to look up data in **DataFrames** or **Series**, unless you are explicitly told to do so. You are **allowed** to use `iloc`.
# * Do **not** use **absolute** paths such as `C://mdoescher//cs220//p12`. You may **only** use **relative paths**.
# * Do **not** leave irrelevant output or test code that we didn't ask for.
# * **Avoid** calling **slow** functions multiple times within a loop.
# * Do **not** define multiple functions with the same name or define multiple versions of one function with different names. Just keep the best version.
#
# For more details on what will cause you to lose points during code review and specific requirements, please take a look at the [Grading rubric](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/blob/main/p12/rubric.md).

# + [markdown] deletable=false editable=false
# # Questions and Functions:
#
# Let us start by importing all the modules we will need for this project.
# -

# it is considered a good coding practice to place all import statements at the top of the notebook
# please place all your import statements in this cell if you need to import any more modules for this project
import requests
import os
import json
import pandas as pd
from bs4 import BeautifulSoup as bs


# + [markdown] deletable=false editable=false
# ### Function 1: `download(page, filename)`
#
# You **must** now copy/paste the `download` function from Lab-P12. This function **must** extract the data in the webpage `page` and store it in `filename`. If the `filename` already exists, it **must not** download the file again.
# -

# copy/paste the 'download' function from Lab-P12
def download(url, filename):
    if os.path.exists(filename):
        return filename + " already exists!"
    # TODO: make the request
    r = requests.get(url)
    # TODO: raise an HTTPError if status code is not 200
    r.raise_for_status
    # TODO: get the text
    text = r.text
    # TODO: open the file (with 'utf-8' encoding)
    f = open(filename, "w", encoding = "utf-8")
    # TODO: write to the file
    f.write(text)
    # TODO: close the file
    f.close()
    return (str(filename) + " created!")


grader.check("download")

# + [markdown] deletable=false editable=false
# Now, use `download` to pull the data from here (**do not manually download**): https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/raw/main/p12/rankings.json and store it in the file `rankings.json`. Once you have created the file, create a Dataframe `rankings` from this file.
#
# **Warning:** Make sure your `download` function meets the specifications mentioned in Lab-P12 and does **not** download the file if it already exists. The TAs will **manually deduct** points otherwise. Make sure you use the `download` function to pull the data instead of manually downloading the files. Otherwise you will get a zero.
# -

# use the 'download' function to download the data from the webpage
# 'https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/raw/main/p12/rankings.json'
# to the file 'rankings.json'
download("https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/raw/main/p12/rankings.json", "rankings.json")

# open 'rankings.json' with pd.read_json('rankings.json') and store in the variable 'rankings'
rankings = pd.read_json("rankings.json")

grader.check("rankings")

# + [markdown] deletable=false editable=false
# **Question 1:** How **many** countries do we have in our dataset?
#
# Your output **must** be an **int** representing the number of *unique* countries in the dataset.
# -

# compute and store the answer in the variable 'num_countries', then display it
num_countries = len(list(set(rankings["Country"])))
num_countries

grader.check("q1")

# + [markdown] deletable=false editable=false
# **Question 2:** Generate a `pandas` **DataFrame** containing **all** the statistics of the **highest-ranked** institution based on `World Rank` across all the years.
#
# Your output **must** be a pandas **DataFrame** with 3 rows and 10 columns. It **must** contain all the data for the institutions with `World Rank` of *1*. It **must** look like this:
#
# ||**Year**|**World Rank**|**Institution**|**Country**|**National Rank**|**Education Rank**|**Employability Rank**|**Faculty Rank**|**Research Rank**|**Score**|
# |---|---|---|---|---|---|---|---|---|---|---|
# |**0**|2021|1|Harvard University|USA|1|1.0|1.0|1.0|1.0|100.0|
# |**2000**|2022|1|Harvard University|USA|1|1.0|1.0|1.0|1.0|100.0|
# |**4000**|2023|1|Harvard University|USA|1|1.0|1.0|1.0|1.0|100.0|
# -

# compute and store the answer in the variable 'highest_ranked', then display it
highest_ranked = rankings[rankings["World Rank"] == 1]
highest_ranked


grader.check("q2")

# + [markdown] deletable=false editable=false
# **Question 3:** Generate a `pandas` **DataFrame** containing **all** the statistics of *University of Wisconsin–Madison*.
#
# **Hint**: The `–` symbol in the text above is not the regular hyphen (`-`) symbol. It is recommended that you just *copy/paste* the string `'University of Wisconsin–Madison'` into your code instead of typing it yourself.
#
# Your output **must** be a pandas **DataFrame** with 3 rows and 10 columns. It **must** look like this:
#
# ||**Year**|**World Rank**|**Institution**|**Country**|**National Rank**|**Education Rank**|**Employability Rank**|**Faculty Rank**|**Research Rank**|**Score**|
# |---|---|---|---|---|---|---|---|---|---|---|
# |**24**|2021|25|University of Wisconsin–Madison|USA|19|33.0|97.0|29.0|32.0|87.3|
# |**2026**|2022|27|University of Wisconsin–Madison|USA|20|34.0|100.0|30.0|35.0|87.0|
# |**4027**|2023|28|University of Wisconsin–Madison|USA|20|36.0|102.0|30.0|41.0|87.0|
# -

# compute and store the answer in the variable 'uw_madison', then display it
uw_madison = rankings[rankings["Institution"] == 'University of Wisconsin–Madison']
uw_madison

grader.check("q3")

# + [markdown] deletable=false editable=false
# **Question 4:** What is the `National Rank` of the *University of Wisconsin–Madison* in the `Year` *2023*?
#
# Your output **must** be an **int**. You **must** use **Boolean indexing** on the variable `uw_madison` (from the previous question) to answer this question.
#
# **Hint:** Use Boolean indexing on the DataFrame `uw_madison` to find the data for the year *2023*. You may then extract the `National Rank` column from the subset DataFrame. Finally, use `iloc` to lookup the value in the DataFrame which contains only one row and one column.
# -

# compute and store the answer in the variable 'uw_madison_nat_rank', then display it
uw_madison_nat_rank = uw_madison[uw_madison["Year"] == 2023]["National Rank"].iloc[0]
uw_madison_nat_rank

grader.check("q4")

# + [markdown] deletable=false editable=false
# **Question 5:** What is the **average** `Score` of the *University of Wisconsin–Madison*?
#
# Your output **must** be a **float**. You **must** use the variable `uw_madison` to answer this question.
#
# **Hint:** You **must** extract the `Score` column of the **DataFrame** `uw_madison` as a **Series**. You can find the **average** of  all the scores in a **Series** with the `Series.mean` function.
# -

# compute and store the answer in the variable 'uw_madison_avg_score', then display it
uw_madison_avg_score = uw_madison["Score"].mean()
uw_madison_avg_score

grader.check("q5")

# + [markdown] deletable=false editable=false
# **Question 6:** Generate a `pandas` **DataFrame** containing **all** the statistics of universities from the `Country` *Singapore* in the `Year` *2021*.
#
# Your output **must** be a pandas **DataFrame** with 4 rows and 10 columns. It **must** look like this:
#
# ||**Year**|**World Rank**|**Institution**|**Country**|**National Rank**|**Education Rank**|**Employability Rank**|**Faculty Rank**|**Research Rank**|**Score**|
# |---|---|---|---|---|---|---|---|---|---|---|
# |**88**|2021|89|National University of Singapore|Singapore|1|322.0|155.0|NaN|41.0|82.2|
# |**135**|2021|136|Nanyang Technological University|Singapore|2|NaN|909.0|NaN|68.0|80.4|
# |**1070**|2021|1071|Singapore University of Technology and Design|Singapore|3|NaN|NaN|NaN|1026.0|69.8|
# |**1362**|2021|1363|Singapore Management University|Singapore|4|NaN|NaN|NaN|1305.0|68.3|
#

# + [markdown] deletable=false editable=false
# **Hint:** When there are **multiple** conditions to filter a **DataFrame**, you can combine all the conditions with `&` as a logical operator between them. For example, you can extract the data for all the institutions with `Education Rank <= 10` and `Faculty Rank <= 10` with:
#
# ```python
# rankings[(rankings["Education Rank"] <= 10) & (rankings["Faculty Rank"] <= 10)]
# ```

# +
# compute and store the answer in the variable 'singapore_inst', then display it
singapore_inst = rankings[(rankings["Country"] == "Singapore") & (rankings["Year"] == 2021)]


singapore_inst
# -

grader.check("q6")

# + [markdown] deletable=false editable=false
# **Question 7:** In the `Year` *2022*, what was the **highest-ranked** institution in the `Country` *Germany*?
#
# Your output **must** be a **string** representing the **name** of this institution.
#
# **Hint:** The highest-ranked institution in *Germany* is the institution from Germany with a `National Rank` of *1*.

# +
# compute and store the answer in the variable 'german_best_name', then display it
german_best_name = rankings[(rankings["Country"] == "Germany") & (rankings["National Rank"] ==1) & (rankings["Year"] == 2022)]["Institution"].iloc[0]


german_best_name
# -

grader.check("q7")

# + [markdown] deletable=false editable=false
# **Question 8:** In the `Year` *2022*, list **all** the institutions in the *USA* that were ranked **better** than the highest-ranked institution in *Germany*.
#
# Your output **must** be a **list** containing the **names** of all universities from *USA* with a **better** `World Rank` than the institution `german_best_name` in the `Year` *2022*. By **better** ranked, we refer to institutions with a **lower** value under the `World Rank` column.
#
# **Hint:** You could store the entire row of the highest ranked institution from Germany in a different variable in Question 7, and use it to extract its `World Rank`. You could go back to your answer for Question 7, and edit it slightly to do this.

# +
# compute and store the answer in the variable 'us_better_than_german_best', then display it
munich = rankings[(rankings["Country"] == "Germany") & (rankings["National Rank"] ==1) & (rankings["Year"] == 2022)]
rank = munich["World Rank"].iloc[0]

df = rankings[(rankings["Country"] == "USA") & (rankings["Year"] == 2022) & (rankings["World Rank"] < rank)]
us_better_than_german_best = list(set(df["Institution"]))

us_better_than_german_best
# -

grader.check("q8")

# + [markdown] deletable=false editable=false
# **Question 9:** What is the **highest-ranked** institution based on `Education Rank` in *China* for the `Year` *2023*?
#
# Your output **must** be a **string** representing the **name** of this institution. You may **assume** there is only one institution satisfying these requirements. By the **highest-ranked** institution, we refer to the institution with the **least** value under the `Education Rank` column.
#
# **Hint:** You can find the **minimum** value in a **Series** with the `Series.min` method. You can find the documentation [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.min.html) or by executing the line `help(pd.Series.min)` in a separate cell below.

# +
# compute and store the answer in the variable 'china_highest_qoe', then display it
rank = rankings[(rankings["Country"] == "China") & (rankings["Year"] ==2023)]["Education Rank"].min()
china_highest_qoe = rankings[(rankings["Education Rank" ] == rank) & (rankings["Country"] == "China") & (rankings["Year"] ==2023)]["Institution"].iloc[0]

china_highest_qoe
# -

grader.check("q9")

# + [markdown] deletable=false editable=false
# **Question 10:** What are the **top** *five* **highest-ranked** institutions based on `Research Rank` in *India* for the `Year` *2022*?
#
# Your output **must** be a **list** of institutions **sorted** in *increasing* order of their `Research Rank`.
#
# **Hint:** For sorting a DataFrame based on the values of a particular column, you can use the `DataFrame.sort_values(by="column_name")` method (where `column_name` is the column on which you want to sort). You can find the documentation [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html) or by executing the line `help(pd.Series.sort_values)` in a separate cell below.

# +
# compute and store the answer in the variable 'india_highest_research', then display it

yuh = rankings[(rankings["Country"] == "India") & (rankings["Year"] == 2022)]
item = yuh.sort_values(by="Research Rank")[:5]

india_highest_research = list(item["Institution"])


india_highest_research
# -

grader.check("q10")

# + [markdown] deletable=false editable=false
# For the next few questions, we will be analyzing how the rankings of the institutions change across the three years in the dataset. As you might have already noticed, the list of institutions in each year's rankings are different. As a result, for several institutions in the dataset, we do not have the rankings for all three years. Since it will be more challenging to analyze such institutions, we will simply skip them.

# + [markdown] deletable=false editable=false
# **Question 11:** How **many** institutions have rankings for **all** three years?
#
# Your output **must** be an **integer**. To get started, you have been provided with a code snippet below.
#
# **Hint:** You could make **sets** of the institutions that appear in each **DataFrame**, and find their **intersection**. Look up how to find the intersection of two or more sets in Python, on the internet!

# +
# compute and store the answer in the variable 'num_institutions_2021_2022_2023', then display it
# replace the ... with your code

year_2021_ranking_df = rankings[rankings["Year"] == 2021]
year_2022_ranking_df = rankings[rankings["Year"] == 2022]
year_2023_ranking_df = rankings[rankings["Year"] == 2023]

# TODO: make sets of the institutions in each of the three years
institutions_2021 = set(year_2021_ranking_df["Institution"])
institutions_2022 = set(year_2022_ranking_df["Institution"])
institutions_2023 = set(year_2023_ranking_df["Institution"])
# TODO: find the intersection of the three sets
institutions_2021_2022_2023 = institutions_2021 & institutions_2022 & institutions_2023
# TODO: find the length of the intersection
num_institutions_2021_2022_2023 = len(institutions_2021_2022_2023)

num_institutions_2021_2022_2023
# -

grader.check("q11")

grader.check("year_2021_ranking_df")

grader.check("year_2022_ranking_df")

grader.check("year_2023_ranking_df")

# + [markdown] deletable=false editable=false
# ### Data Structure 1: `institutions_df`
#
# You are now going to create a new **DataFrame** with a **unique** list of institutions which have featured in the rankings for **all** three years, along with their `World Rank` across the three years. Specifically, the **DataFrame** **must** have the following four columns - `'Institution'`, `'2021 ranking'`, `'2022 ranking'`, and `'2023 ranking'`.

# +
# define the variable 'institutions_df', but do NOT display it here

# TODO: initalize an empty list to store the list of institutions
inlist = []
# TODO: loop through the variable 'institutions_2021_2022_2023' defined above
for item in institutions_2021_2022_2023:
    # TODO: create a new dictionary with the necessary key/value pairs
    indict = {}
    indict["Institution"] = item
    indict["2021 ranking"] = rankings[(rankings["Institution"] == item) & (rankings["Year"] == 2021)]["World Rank"].iloc[0]
    indict["2022 ranking"] = rankings[(rankings["Institution"] == item) & (rankings["Year"] == 2022)]["World Rank"].iloc[0]
    indict["2023 ranking"] = rankings[(rankings["Institution"] == item) & (rankings["Year"] == 2023)]["World Rank"].iloc[0]
    # TODO: append the dictionary to the list
    inlist.append(indict)
# TODO: create the DataFrame from the list of dictionaries
institutions_df = pd.DataFrame(inlist)
# -

grader.check("institutions_df")

# + [markdown] deletable=false editable=false
# **Question 12:** Between the years *2022* and *2023*, **list** the institutions which have seen an **improvement** in their `World Rank` by **more than** *200* ranks.
#
# Your output **must** be a **list** of institution names. The **order** does **not** matter. You **must** use the DataFrame `institutions_df` to answer this question.
#
# **Hints:**
#
# 1. In pandas, subtraction of two columns can be simply done using subtraction(`-`) operator. For example,
# ``` python
# df["difference"] = df["column1"] - df["column2"]
# ```
# will create a *new column* `difference` with the difference of the values from the columns `column1` and `column2`.
# 2. Note that an *improved* ranking means that the `World Rank` has *decreased*.

# +
# compute and store the answer in the variable 'improved_institutions', then display it
newdf = institutions_df
newdf["difference"] = newdf["2023 ranking"] - newdf["2022 ranking"]

improved_institutions = list(newdf[newdf["difference"] <= -200]["Institution"])
improved_institutions
# -

grader.check("q12")

# + [markdown] deletable=false editable=false
# **Question 13:** Between the years *2021* and *2023*, which institution had the **third largest** change in its `World Rank`?
#
# Your output **must** be a **string** representing the name of the institution with the **third greatest absolute difference** between its `World Rank` in 2021 and 2023. You **must** use the DataFrame `institutions_df` to answer this question.

# +
# compute and store the answer in the variable 'third_most_change_inst', then display it
newdf2 = institutions_df

newdf2["absolute difference"] = abs(newdf2["2023 ranking"] - newdf2["2021 ranking"])
newdf2.sort_values(by = "absolute difference")
third_most_change_inst = newdf2.sort_values(by = "absolute difference")["Institution"].iloc[-3]


third_most_change_inst
# -

grader.check("q13")

# + [markdown] deletable=false editable=false
# **Question 14:** For all the three years, find the **number** of institutions that **improved** their `World Rank` between **each year** by **at least** 5 ranks.
#
# Your output **must** be an **integer** representing the number of institutions whose `World Rank` **increased** each year by **at least** 5 ranks. You **must** use the DataFrame `institutions_df` to answer this question.

# +
# compute and store the answer in the variable 'five_improved', then display it
newdf1 = institutions_df
newdf1["difference"] = newdf1["2023 ranking"] - newdf1["2022 ranking"]


one = set(newdf1[newdf1["difference"] <= -5]["Institution"])
newdf1["difference2"] = (newdf1["2022 ranking"] - newdf1["2021 ranking"])
two = set(newdf1[newdf1["difference2"] <= -5]["Institution"])

five_improved = len(list(one & two))


five_improved
# -

grader.check("q14")

# + [markdown] deletable=false editable=false
# **Question 15:** In the `Year` *2021*, **list** the institutions which do **not** feature in the **top** *50* in the world based on `World Ranking`, but have a `Employability Rank` **less than or equal** to *25*.
#
# Your output **must** be a **list** of institutions. The **order** does **not** matter. You **must** use the `year_2021_ranking_df` DataFrame that you created in Question 11 to answer this question.

# +
# compute and store the answer in the variable 'only_top_employability', then display it


only_top_employability = list(year_2021_ranking_df[(year_2021_ranking_df["World Rank"] >50) & (year_2021_ranking_df["Employability Rank"] <= 25)]["Institution"])



only_top_employability
# -

grader.check("q15")

# + [markdown] deletable=false editable=false
# **Question 16:** **List** the universities which ranked in the **top** 50 of world rankings (`World Rank`) in the `Year` *2021* but **failed** to do so in the `Year` *2023*.
#
# Your output **must** be a **list** of institutions. The **order** does **not** matter. You **must** use the `year_2021_ranking_df` and `year_2023_ranking_df` DataFrames that you created in Question 11 to answer this question.
#
# **Hints:**
# 1. There could be institutions that are ranked in the **top** 50 in *2021* but do not feature in *2023* at all; you still want to include them in your list.
# 2. You can use `sort_values` and `iloc` to identify the **top** 50 institutions.
# 3. Given two *sets* `A` and `B`, you can find the elements which are in `A` but not in `B` using `A - B`. For example,
# ```python
# set_A = {10, 20, 30, 40, 50}
# set_B = {20, 40, 70}
# set_A - set_B == {10, 30, 50} # elements which are in set_A but not in set_B
# ```

# +
# compute and store the answer in the variable 'top_50_only_2021', then display it
a = set(year_2021_ranking_df.sort_values(by = "World Rank")["Institution"].iloc[0:50])

b = set(year_2023_ranking_df.sort_values(by = "World Rank")["Institution"].iloc[0:50])

top_50_only_2021 = list(a-b)


top_50_only_2021
# -

grader.check("q16")

# + [markdown] deletable=false editable=false
# **Question 17:** **List** the countries which have **at least** *5* and **at most** *10* institutions featuring in the **top** *100* of world rankings (`World Rank`) in the `Year` *2023*.
#
# Your output **must** be a **list**.
#
# **Hints:**
#
# 1. In a **DataFrame**, to find the **number** of times each unique value in a column repeats, you can use the `DataFrame.value_counts` method. For example,
# ``` python
# rankings["Country"].value_counts()
# ```
# would output a `pandas` **Series** with the **indices** being the unique values of `Country` and the **values** being the **number** of times each country has featured in the `rankings` **DataFrame**. You can find the documentation [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.value_counts.html) or by using the `help` function in a separate cell. You can adapt this code to find the number of institutions from each country that features in the `Year` *2023*.
# 2. Just like with **DataFrames**, you can use Boolean indexing on **Series**. For example, try something like this in a separate cell below:
# ```python
# a = pd.Series([100, 200, 300])
# a[a > 100]
# ```
# 3. You can extract the **indices** of a **Series**, `s` with `s.index`.

# +
# compute and store the answer in the variable 'almost_top_countries', then display it
frame = year_2023_ranking_df[year_2023_ranking_df["World Rank"] <= 100]

fr = frame["Country"].value_counts()
almost_top_countries = list((fr[(fr >= 5) & (fr <= 10)]).index)



almost_top_countries
# -

grader.check("q17")

# + [markdown] deletable=false editable=false
# ## Beautiful Soup

# + [markdown] deletable=false editable=false
# ## Setup
#
# In real life, you don't often have data in nice JSON format like `rankings.json`. Instead, data needs to be *scraped* from multiple webpages and requires some cleanup before it can be used.
#
# Most of the projects in CS220 have used data obtained via web scraping, including this one. For p12, as explained above, we obtained the data by scraping the following websites:
#
# * https://cwur.org/2020-21.php
# * https://cwur.org/2021-22.php
# * https://cwur.org/2023.php
#
# Our `rankings.json` file was created using data from these webpages. For the rest of this project, you will write the code to **recreate** `rankings.json` file from the tables in these html pages yourself! We also do **not** want all students in this class to be making multiple requests to the webpages above, as that could be very costly for the people managing the webpages. Instead, we have made **copies** of the webpages above, which can be found here:
#
# * https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/raw/main/p12/2021.html
# * https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/raw/main/p12/2022.html
# * https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/raw/main/p12/2023.html
#
# Before you can parse these html files, you must first *download* them. You **must** use your `download` function to download these files.
# -

# use the 'download' function to download the data from the webpage
# 'https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/raw/main/p12/2021.html'
# to the file '2021.html'
download('https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/raw/main/p12/2021.html', "2021.html")

# use the 'download' function to download the data from the webpage
# 'https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/raw/main/p12/2022.html'
# to the file '2022.html'
download("https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/raw/main/p12/2022.html", "2022.html")

# use the 'download' function to download the data from the webpage
# 'https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/raw/main/p12/2023.html'
# to the file '2023.html'
download('https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/raw/main/p12/2023.html', "2023.html")

# + [markdown] deletable=false editable=false
# **Question 18:** Use `BeautifulSoup` to **parse** `2021.html`, and find the **table** containing the ranking data. Extract the **column names** of this table and the first row of the table to create a **dictionary** where the column headers are the keys and the corresponding values are extracted from the **first** row.
#
# You do **not** have to perform any typecasting of the data **yet**. Your output **must** be a **dictionary** having the format as given below:
# ```python
# {
#     'World Rank': '1',
#     'Institution': 'Harvard University',
#     'Country': 'USA',
#     'National Rank': '1',
#     'Education Rank': '1',
#     'Employability Rank': '1',
#     'Faculty Rank': '1',
#     'Research Rank': '1',
#     'Score': '100'
# }
# ```
#
# **Hint:** You **must** use the `find` or `find_all` **methods** to identify the table and its header.

# +
# compute and store the answer in the variable 'first_dict', then display it
f = open("2021.html", encoding = "utf-8")
text = f.read()
f.close()

soup = bs(text, "html.parser")

table = soup.find("table")

header = [th.get_text() for th in table.find_all('th')]
    
elements = table.find_all('tr')
secondrow = elements[1]
l = secondrow.find_all("td")
first_dict = {"World Rank": str(l[0].get_text()), "Institution": str(l[1].get_text()), "Country": str(l[2].get_text()), "National Rank": str(l[3].get_text()),\
                              "Education Rank": str(l[4].get_text()), "Employability Rank": str(l[5].get_text()), "Faculty Rank": str(l[6].get_text()), \
                                "Research Rank": str(l[7].get_text()), "Score": str(l[8].get_text())}
first_dict
                                                    
# -

grader.check("q18")


# + [markdown] deletable=false editable=false
# ### Function 2: `parse_html(filename)`
#
# You **must** write this function which takes in a HTML file `filename` as its input, parses it, and returns a **list** of **dictionaries** containing all the data in the **table** stored in `filename`.
#
# Note that the data in all these files is **not** stored in the same format. In particular, the `World Rank` column in `2023.html` contains some additional data that we do not need for this dataset. Similarly, the `Institution` column in `2022.html` and `2023.html` contains some additional data for the first twelve rows that we do not need. Your function **must** deal with all these different cases, and return a **dictionary** in the same format as below.
#
# There are **no** restrictions on **hardcoding** for this function. You may tailor your function to work for only these three html files. However, this same function **must** work on **all three** of these html files.
#
# For example, the output of the function call `parse_html("2023.html")` **must** look like this:
#
# ```python
# [
#     {'Year': 2023,
#       'World Rank': 1,
#       'Institution': 'Harvard University',
#       'Country': 'USA',
#       'National Rank': 1,
#       'Education Rank': 1,
#       'Employability Rank': 1,
#       'Faculty Rank': 1,
#       'Research Rank': 1,
#       'Score': 100.0},
#      {'Year': 2023,
#       'World Rank': 2,
#       'Institution': 'Massachusetts Institute of Technology',
#       'Country': 'USA',
#       'National Rank': 2,
#       'Education Rank': 4,
#       'Employability Rank': 12,
#       'Faculty Rank': 3,
#       'Research Rank': 9,
#       'Score': 96.7},
#     ...
# ]
# ```
#
# You can copy/paste this function from Lab-P12 if you have already defined it there.
# -

# define the function 'parse_html' here
def parse_html(filename):
    '''parse_html(filename) parses an HTML file and 
    returns a list of dictionaries containing the tabular data'''
    f = open(filename, encoding="utf-8")
    text = f.read()
    f.close()
    bs_obj = bs(text, "html.parser")
    
    table = bs_obj.find("table")
    header = [th.get_text() for th in table.find_all('th')]
    
    tr_elements = table.find_all('tr')
    
    my = []
    
    for tr in tr_elements[1:]:
        c = tr.find_all("td")
        dictyy = {}
        if c[0].get_text() == "-":
            dictyy["World Rank"] = None
        else:
            dictyy["World Rank"] = int(c[0].get_text().split("T")[0])
        if c[1].get_text() == "-":
            dictyy["Institution"] = None
        else:
            dictyy["Institution"] = str(c[1].get_text().split("\n")[0])
        if c[2].get_text() == "-":
            dictyy["Country"] = None
        else:
            dictyy["Country"] = str(c[2].get_text())
        if c[3].get_text() == "-":
            dictyy["National Rank"] = None
        else:
            dictyy["National Rank"] = int(c[3].get_text())
        if c[4].get_text() == "-":
            dictyy["Education Rank"] = None
        else:
            dictyy["Education Rank"] = int(c[4].get_text())
        if c[5].get_text() == "-":
            dictyy["Employability Rank"] = None
        else:
            dictyy["Employability Rank"] = int(c[5].get_text())
        if c[6].get_text() == "-":
            dictyy["Faculty Rank"] = None
        else:
            dictyy["Faculty Rank"] = int(c[6].get_text())
        if c[7].get_text() == "-":
            dictyy["Research Rank"] = None
        else:
            dictyy["Research Rank"] = int(c[7].get_text())
        if c[8].get_text() == "-":
            dictyy["Score"] = None
        else:
            dictyy["Score"] = float(c[8].get_text())
        
        year = filename[0:4]
        dictyy["Year"] = int(year)
        my.append(dictyy)
    return my


grader.check("parse_html")

# + [markdown] deletable=false editable=false
# **Question 19:** Calculate the **average** score of the **first** 5 institutions in the file `2021.html`.
#
# Your output **must** be a **float** calculated by averaging the scores from the first 5 dictionaries in the file. You **must** use the `parse_html` function to parse the file, and **slice** the list such that you would only loop through the **first five** institutions. For each **dictionary** in the **list** you must use the `Score` key to get the score for that particular institution.

# +
# compute and store the answer in the variable 'avg_top_5', then display it

file1 = parse_html("2021.html")
avg_top_5 = 0
counter = 0
for item in file1[0:5]:
    avg_top_5 += item["Score"]
    counter += 1
avg_top_5 = avg_top_5/counter

avg_top_5
# -

grader.check("q19")


# + [markdown] deletable=false editable=false
# **Question 20:** Parse the contents of the **three** files `2021.html`, `2022.html`, and `2023.html` and combine them to create a **single** file named `my_rankings.json`.
#
# You **must** create a **file** named `my_rankings.json` in your current directory. The contents of this file **must** be **identical** to `rankings.json`.
#
# **Hints:**
# 1. Using the logic from the question above, combine the data from these three files into a single list of dicts, and write it into the file `"my_rankings.json"`.
# 2. You can use the `write_json` function that was introduced in lecture.

# +
# the 'write_json' function from lecture has been provided for you here

def write_json(path, data):
    with open(path, 'w', encoding = "utf-8") as f:
        json.dump(data, f, indent = 2)


# -

# parse the three files and write the contents into 'my_rankings.json'
fileone = parse_html("2021.html")
filetwo = parse_html("2022.html")
filethree = parse_html("2023.html")
fileone.extend(filetwo)
fileone.extend(filethree)
write_json("my_rankings.json", fileone)

grader.check("q20")

grader.check("general_deductions")

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
# !jupytext --to py p12.ipynb

# + [code] deletable=false editable=false
public_tests.check_file_size("p12.ipynb")
grader.export(pdf=False, run_tests=False, files=["p12.py"])

# + [markdown] deletable=false editable=false
#  
