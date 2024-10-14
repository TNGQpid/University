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
grader = otter.Notebook("p8.ipynb")

# + editable=false
import public_tests

# +
# PLEASE FILL IN THE DETAILS
# enter none if you don't have a project partner
# you will have to add your partner as a group member on Gradescope even after you fill this

# project: p8
# submitter: sheberlein
# partner: sheberlein
# hours: 3

# + [markdown] deletable=false editable=false
# # Project 8: Going to the Movies

# + [markdown] deletable=false editable=false
# ## Learning Objectives:
#
# In this project, you will demonstrate how to:
#
# * integrate relevant information from various sources (e.g. multiple csv files),
# * build appropriate data structures for organized and informative presentation (e.g. list of dictionaries),
# * practice good coding style.
#
# Please go through [Lab-P8](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/tree/main/lab-p8) before working on this project. The lab introduces some useful techniques related to this project.

# + [markdown] deletable=false editable=false
# ## Testing your code:
#
# Along with this notebook, you must have downloaded the file `public_tests.py`. If you are curious about how we test your code, you can explore this file, and specifically the function `get_expected_json`, to understand the expected answers to the questions.

# + [markdown] deletable=false editable=false
# <h2 style="color:red">Warning (Note on Academic Misconduct):</h2>
#
# **IMPORTANT**: **P8 and P9 are two parts of the same data analysis.** You **cannot** switch project partners between these two projects. That is if you partner up with someone for P8, you have to sustain that partnership until the end of P9. Now may be a good time to review [our course policies](https://cs220.cs.wisc.edu/f23/syllabus.html).
#
# Under any circumstances, **no more than two students are allowed to work together on a project** as mentioned in the course policies. If your code is flagged by our code similarity detection tools, **both partners will be responsible** for sharing/copying the code, even if the code is shared/copied by one of the partners with/from other non-partner student(s). Note that each case of plagiarism will be reported to the Dean of Students with a zero grade on the project. **If you think that someone cannot be your project partner then don’t make that student your lab partner.**
#
# **<font color = "red">Project partners must submit only one copy of their project on Gradescope, but they must include the names of both partners.</font>**

# + [markdown] deletable=false editable=false
# ## Introduction:
#
# In this project and the next, we will be working on the [IMDb Movies Dataset](https://www.imdb.com/interfaces/). We will use Python to discover some cool facts about our favorite movies, cast, and directors.
#
# In this project, you will combine the data from the movie and mapping files into a more useful format.
# Start by downloading the following files: `public_tests.py`, `small_mapping.csv`, `small_movies.csv`, `mapping.csv`, and `movies.csv`.

# + [markdown] deletable=false editable=false
# ## The Data:
#
# Open `movies.csv` and `mapping.csv` in any spreadsheet viewer, and see what the data looks like.
# `movies.csv` has ~75,000 rows and `mapping.csv` has ~220,000 rows. These files store information about **every** movie on the IMDb dataset which was released in the US, and received over **250** reviews on IMDb. These datasets are **very** large when compared to `small_movies.csv` and `small_mapping.csv` from [Lab-P8](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/tree/main/lab-p8), but the data is stored in the **same format**. For a description of the datasets, please refer back to [Lab-P8](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/tree/main/lab-p8).
#
# Before we start working with these very large datasets, let us start with the much smaller datasets, `small_movies.csv` and `small_mapping.csv` from Lab-P8. In the latter half of P8 and in P9, you will be working with `movies.csv` and `mapping.csv`. Since the files `movies.csv` and `mapping.csv` are large, some of the functions you write in P8 and P9 **may take a while to execute**. You do not have to panic if a single cell takes between 5 to 10 seconds to run. If any cell takes significantly longer, follow the recommendations below:
#
# - **Do not** call **slow functions** multiple times within a loop.
# - **Do not** call functions that **iterate over the entire dataset within a loop**; instead, call the function before the loop and store the result in a variable.
# - **Do not** compute quantities **inside a loop** if it can be computed outside the loop; for example, if you want to calculate the average of a list, you should use the loop to find the numerator and denominator but divide **once** after the loop ends instead of inside the loop.

# + [markdown] deletable=false editable=false
# ## Project Requirements:
#
# You **may not** hardcode indices in your code, unless the question explicitly asks you to do so. If you open your `.csv` files with Excel, manually count through the rows and use this number to loop through the dataset, this is also considered as hardcoding. If any instances of hardcoding are found during code review, the Gradescope autograder will **deduct** points from your public score.
#
# **Store** your final answer for each question in the **variable specified for each question**. This step is important because Otter grades your work by comparing the value of this variable against the correct answer.
#
# For some of the questions, we'll ask you to write (then use) a function to compute the answer. If you compute the answer **without** creating the function we ask you to write, the Gradescope autograder will **deduct** points from your public score, even if the way you did it produced the correct answer.
#
# #### Required Functions:
# - `get_mapping`
# - `get_raw_movies`
# - `get_movies`
# - `find_specific_movies`
# - `bucketize_by_genre`
#
# In this project, you will also be required to define certain **data structures**. If you do not create these data structures exactly as specified, the Gradescope autograder will **deduct** points from your public score, even if the way you did it produced the correct answer.
#
# #### Required Data Structures:
# - `small_movies_data`
# - `movies`
# - `genre_dict`
#
# You are only allowed to define these data structures **once** and the Gradescope autograder will **deduct** points from your public score if you redefine the values of these variables.
#
# In this project (and the next), you will be asked to create **lists** of movies. For all such questions, **unless it is explicitly mentioned otherwise**, the movies should be in the **same order** as in the `movies.csv` (or `small_movies.csv`) file. Similarly, for each movie, the **list** of `genres`, `directors`, and `cast` members should always be in the **same order** as in the `movies.csv` (or `small_movies.csv`) file.
#
# Students are only allowed to use Python commands and concepts that have been taught in the course prior to the release of P8. Therefore, you should not use the pandas module. The Gradescope autograder will **deduct** points from your public score otherwise.
#
# In addition, you are also **required** to follow the requirements below:
# - **Do not use the method `csv.DictReader` for P8**. Although the required output can be obtained using this method, one of the learning outcomes of this project is to demonstrate your ability to build dictionaries with your own code.  
# - Additional import statements beyond those that are stated in the directions are not allowed. For this project, we allow you to use `csv` and `copy` packages (that is, you can use the `import csv` and `import copy` statements in your submission). You should not use concepts / modules that are yet to be covered in this course; for example: you should **not** use modules like `pandas`.
#
# The Gradescope autograder will **deduct** points accordingly, if you don't follow the provided directions.
#
# For more details on what will cause you to lose points during code review and specific requirements, please take a look at the [Grading rubric](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/blob/main/p8/rubric.md).

# + [markdown] deletable=false editable=false
# ## Questions and Functions:
#
# Let us start by importing all the modules we will need for this project.
#
#
# -

# it is considered a good coding practice to place all import statements at the top of the notebook
# please place all your import statements in this cell if you need to import any more modules for this project
import csv
import copy


# + [markdown] deletable=false editable=false
# ### Function 1: `get_mapping(path)`
#
# We require you to complete the below function to answer the next several questions (this is a **requirement**, and you will **lose points** if you do not implement this function). You may copy/paste code from your lab-p8 notebook to finish this function.

# +
def process_csv(filename):
    example_file = open(filename, encoding="utf-8")
    example_reader = csv.reader(example_file)
    example_data = list(example_reader)
    example_file.close()
    return example_data

def get_mapping(path):
    """
    get_mapping(path) converts a mapping csv in 'path' 
    into a dict with keys as IDs and values as names
    """
    pass # replace with your code
#     TODO: process path
#     TODO: create a dictionary  
#     TODO: iterate through each row of processed path
#     TODO: map value in first column (ID) to value in second column (name/title)
    processed = process_csv(path)
    dic = {}
    for row in processed:
        dic[row[0]] = row[1]
    return dic


# + deletable=false editable=false
grader.check("get_mapping")

# + [markdown] deletable=false editable=false
# **Question 1:** What is returned by `get_mapping("small_mapping.csv")`?
#
# Your output **must** be a **dictionary** which maps the *IDs* in `small_mapping.csv` to *names*.
# -

# compute and store the answer in the variable 'small_mapping', then display it
small_mapping = get_mapping("small_mapping.csv")
small_mapping

# + deletable=false editable=false
grader.check("q1")

# + [markdown] deletable=false editable=false
# **Question 2:** What is the **value** associated with the **key** *nm1289434*?
#
# Your output **must** be a **string**. You **must** use the variable `small_mapping` defined above to answer this question. You **must** not call the function `get_mapping` again on this dataset.
# -

# access and store the answer in the variable 'nm1289434_value', then display it
nm1289434_value = small_mapping["nm1289434"]
nm1289434_value

# + deletable=false editable=false
grader.check("q2")

# + [markdown] deletable=false editable=false
# **Question 3:** What are the **values** associated with **keys** that **begin** with *nm*?
#
# Your output **must** be a **list** of **strings**. You **must** find **only** the values of the keys that **begin** with *nm*, and **not** the keys that contain *nm*. You **must** use the variable `small_mapping` defined above to answer this question.
# -

# compute and store the answer in the variable 'nm_values', then display it
nm_values = []
for key in small_mapping:
    if key.startswith("nm"):
        nm_values.append(small_mapping[key])
nm_values

# + deletable=false editable=false
grader.check("q3")

# + [markdown] deletable=false editable=false
# **Question 4:** Find the **keys** of the people (keys **beginning** with *nm*) whose **last name** is *Murphy*.
#
# Your output **must** be a **list** of **string(s)**. You **must** use the variable `small_mapping` defined above to answer this question.
#
# **Requirements:** Your **code** must be robust and satisfy all the requirements, even if you were to run this on a larger dataset (such as `mapping.csv`). In particular:
# 1. You will **lose points** if your code would find people whose **first** name or **middle** name is *Murphy* (e.g. *Murphy Patrick Martin*, *Lisa Murphy Collins*).
# 2. You will **lose points** if your code would find people whose **last** name contains *Murphy* as a **substring** (e.g. *Benjamin Harter-Murphy*). The name should be **exactly** *Murphy*. 
# 3. You will **lose points** if your code would find any **movie titles** (e.g. *Sergeant Murphy*).
# -

# compute and store the answer in the variable 'nm_murphy', then display it
nm_murphy = []
for key in small_mapping:
    if key.startswith("nm") and small_mapping[key].endswith("Murphy"):
        nm_murphy.append(key)
nm_murphy

# + deletable=false editable=false
grader.check("q4")


# + [markdown] deletable=false editable=false
# #### Now, let's move on to reading the movie files!

# + [markdown] deletable=false editable=false
# ### Function 2: `get_raw_movies(path)`
#
# We require you to complete the below function to answer the next several questions (this is a **requirement**, and you will **lose points** if you do not implement this function).
#
# This function **must** return a **list** of **dictionaries**, where each **dictionary** is of the following format:
#
# ```python
#    {
#         'title': <title-id>,
#         'year': <the year as an integer>,
#         'duration': <the duration as an integer>,
#         'genres': [<genre1>, <genre2>, ...],
#         'rating': <the rating as a float>,
#         'directors': [<director-id1>, <director-id2>, ...],
#         'cast': [<actor-id1>, <actor-id2>, ....]
#     }
# ```
#
# Here is an example:
#
# ```python
#     {
#         'title': 'tt0033313',
#         'year': 1941,
#         'duration': 59,
#         'genres': ['Western'],
#         'rating': 5.2,
#         'directors': ['nm0496505'],
#         'cast': ['nm0193318', 'nm0254381', 'nm0279961', 'nm0910294', 'nm0852305']
#     }
# ```
#
# You may copy/paste code from your lab-p8 notebook to finish this function.
# -

def get_raw_movies(path):
    """
    get_raw_movies(path) converts a movies csv in 'path' 
    into a list of dicts with column names as keys and
    the corresponding type converted values as the values
    """
    processed = process_csv(path)
    csv_rows = processed[1:]
    csv_header = processed[0]
    raw_movies_list = [] # use this empty list to append your dictionary
    # TODO: loop through all the rows of csv_rows
    # TODO: create a dictionary similar to the one in q7.1 for each movie
    # TODO: add each movie dictionary to raw_movies_list
    for row in csv_rows:
        movie = {} # initialize an empty dictionary
        movie["title"] = row[csv_header.index("title")] # extract the title of the movie
        movie["year"] = int(row[csv_header.index("year")])
        movie["duration"] = int(row[csv_header.index("duration")])
        movie["genres"] = row[csv_header.index("genres")].split(", ")
        movie["rating"] = float(row[csv_header.index("rating")])
        movie["directors"] = row[csv_header.index("directors")].split(", ")
        movie["cast"] = row[csv_header.index("cast")].split(", ")
        raw_movies_list.append(movie)
    return raw_movies_list


# + deletable=false editable=false
grader.check("get_raw_movies")

# + [markdown] deletable=false editable=false
# **Question 5:** What is returned by `get_raw_movies("small_movies.csv")`?
#
# Your output **must** be a **list** of **dictionaries** where each dictionary contains information about a movie.
# -

# compute and store the answer in the variable 'raw_small_movies', then display it
raw_small_movies = get_raw_movies("small_movies.csv")
raw_small_movies

# + deletable=false editable=false
grader.check("q5")

# + [markdown] deletable=false editable=false
# If your answer looks correct, but does not pass `grader.check`, make sure that the **datatypes** are all correct. Also make sure that the **directors** and **cast**  are in the **same order** as in `small_movies.csv`.

# + [markdown] deletable=false editable=false
# **Question 6:** How **many** cast members does the **first** movie have?
#
# Your output **must** be an **int**. You **must** use the variable `raw_small_movies` defined above to answer this question. You **must** not call the function `get_raw_movies` again on this dataset.
# -

# compute and store the answer in the variable 'num_cast_first_movie', then display it
num_cast_first_movie = len(raw_small_movies[0]["cast"])
num_cast_first_movie

# + deletable=false editable=false
grader.check("q6")

# + [markdown] deletable=false editable=false
# **Question 7:** What is the *ID* of the **first** cast member listed for the **first** movie of the dataset?
#
# Your output **must** be a **string**. You **must** use the variable `raw_small_movies` defined above to answer this question.
# -

# compute and store the answer in the variable 'first_actor_id_first_movie', then display it
first_actor_id_first_movie = raw_small_movies[0]["cast"][0]
first_actor_id_first_movie

# + deletable=false editable=false
grader.check("q7")


# + [markdown] deletable=false editable=false
# ### Function 3: `get_movies(movies_path, mapping_path)`
#
# We require you to complete the below function to answer the next several questions (this is a **requirement**, and you will **lose points** if you do not implement this function).
#
#
# This function **must** return a **list** of **dictionaries**, where each **dictionary** is of the following format:
#
# ```python
#    {
#         'title': "the movie name",
#         'year': <the year as an integer>,
#         'duration': <the duration as an integer>,
#         'genres': [<genre1>, <genre2>, ...],
#         'rating': <the rating as a float>,
#         'directors': ["director-name1", "director-name2", ...],
#         'cast': ["actor-name1", "actor-name2", ....]
#     }
# ```
#
# Here is an example:
#
# ```python
#     {
#         'title': 'Across the Sierras',
#         'year': 1941,
#         'duration': 59,
#         'genres': ['Western'],
#         'rating': 5.2,
#         'directors': ['D. Ross Lederman'],
#         'cast': ['Dick Curtis', 'Bill Elliott', 'Richard Fiske', 'Luana Walters', 'Dub Taylor']
#     }
# ```
#
# You may copy/paste code from your Lab-P8 notebook to finish this function.
# -

def get_movies(movies_path, mapping_path):
    """
    get_movies(movies_path, mapping_path) converts a movies csv in 'movies_path' 
    into a list of dicts with column names as keys and the corresponding 
    type converted values as the values; then uses the mapping csv in 'mapping_path'
    to replace the IDs of the titles, cast, and directors into actual names
    """
   
    # you are allowed to call get_mapping and get_raw_movies
    # on movies_path and mapping_path
    raw_movies_list = get_raw_movies(movies_path)
    mappy = get_mapping(mapping_path)
    for movie in raw_movies_list:
        directors = []
        for director in movie["directors"]:
            name = mappy[director]
            directors.append(name)
        movie["directors"] = directors
        members = []
        for member in movie["cast"]:
            name = mappy[member]
            members.append(name)
        movie["cast"] = members
        
        movie["title"] = mappy[movie["title"]]
    return raw_movies_list


# + deletable=false editable=false
grader.check("get_movies")

# + [markdown] deletable=false editable=false
# **Question 8:** What is returned by `get_movies("small_movies.csv", "small_mapping.csv")`?
#
# Your output **must** be a **list** of **dictionaries** where each dictionary contains information about a movie.
# -

# compute and store the answer in the variable 'small_movies', then display it
small_movies = get_movies("small_movies.csv", "small_mapping.csv")
small_movies

# + deletable=false editable=false
grader.check("q8")

# + deletable=false editable=false
grader.check("small_movies")

# + [markdown] deletable=false editable=false
# **Question 9:** What is `title` of the **second** movie in `small_movies`?
#
# Your output **must** be a **string**. You **must** use the variable `small_movies` defined above to answer this question. You **must not** call the function `get_movies` again on this dataset.
# -

# compute and store the answer in the variable 'second_movie_title_small_movies', then display it
second_movie_title_small_movies = small_movies[1]["title"]
second_movie_title_small_movies

# + deletable=false editable=false
grader.check("q9")

# + [markdown] deletable=false editable=false
# **Question 10:** Who are the `cast` members of the **second** movie in `small_movies`?
#
# Your output **must** be a **list** of **string(s)**. You **must** use the variable `small_movies` defined above to answer this question.
# -

# compute and store the answer in the variable 'second_movie_cast_small_movies', then display it
second_movie_cast_small_movies = small_movies[1]["cast"]
second_movie_cast_small_movies

# + deletable=false editable=false
grader.check("q10")

# + [markdown] deletable=false editable=false
# **Question 11:** Who are the `directors` of the **last** movie in `small_movies`?
#
# Your output **must** be a **list** of **string(s)**. You **must** use the variable `small_movies` defined above to answer this question.
# -

# compute and store the answer in the variable 'last_movie_directors_small_movies', then display it
last_movie_directors_small_movies = small_movies[len(small_movies)-1]["directors"]
last_movie_directors_small_movies

# + deletable=false editable=false
grader.check("q11")

# + [markdown] deletable=false editable=false
# #### Now that you’ve made it this far, your functions must be working pretty well with small datasets. Next, let's try a much bigger dataset!
#
# Run the following code to open the full dataset:
# -

movies = get_movies("movies.csv", "mapping.csv")
len(movies)

# + [markdown] deletable=false editable=false
# As the files are very large, this cell is expected to take around five seconds to run. If it takes much longer (say, around thirty seconds), then you will **need** to **optimize** your `get_movies` function so it runs faster.
#
# **Warning**: You are **not** allowed to call `get_movies` more than once on the full dataset (`movies.csv` and `mapping.csv`) in your notebook. Instead, reuse the `movies` variable, which is more efficient. The Gradescope autograder will deduct **points** if you call `get_movies` again on these files.
#
# **Warning:** Do **not** display the value of the variable `movies` **anywhere** in your notebook. It will take up a **lot** of space, and your **Gradescope code will not be displayed** for grading. Instead you should verify `movies` has the correct value by looking at a small *slice* of the **list** as in the question below. 

# + deletable=false editable=false
grader.check("movies")

# + [markdown] deletable=false editable=false
# **Question 12:** What are the movies in `movies[22202:22220]`?
#
# Your answer should be a *list* of *dictionaries* that follows the format below:
#
# ```python
# [{'title': 'Bad Night',
#   'year': 2015,
#   'duration': 92,
#   'genres': ['Adventure', 'Comedy', 'Crime'],
#   'rating': 4.9,
#   'directors': ['Chris Riedell', 'Nick Riedell'],
#   'cast': ['Lauren Elizabeth', 'Jenn McAllister', 'Julianna Guill', 'udy Marte']},
#  {'title': 'Operation Camel',
#   'year': 1960,
#   'duration': 100,
#   'genres': ['Comedy'],
#   'rating': 5.7,
#   'directors': ['Sven Methling'],
#   'cast': ['Paul Hagen', 'Louis Miehe-Renard', 'Ebbe Langberg', 'Preben Kaas']},
#  {'title': 'True Story',
#   'year': 2015,
#   'duration': 99,
#   'genres': ['Biography', 'Crime', 'Drama'],
#   'rating': 6.3,
#   'directors': ['Rupert Goold'],
#   'cast': ['James Franco', 'Jonah Hill', 'Felicity Jones', 'Maria Dizzia']},
#  ...]
# ```
# -

# compute and store the answer in the variable 'movies_22202_22220', then display it
movies_22202_22220 = movies[22202:22220]
movies_22202_22220

# + deletable=false editable=false
grader.check("q12")

# + [markdown] deletable=false editable=false
# **Question 13:** What is the **number** of movies released so far in the `year` *2023*?
#
# Your outuput must be an **int**. You **must** use the variable `movies` defined above to answer this question.
# -

# compute and store the answer in the variable 'num_movies_2023', then display it
num_movies_2023 = 0
for movie in movies:
    if movie["year"] == 2023:
        num_movies_2023 += 1
num_movies_2023

# + deletable=false editable=false
grader.check("q13")


# + [markdown] deletable=false editable=false
# ### Function 4: `find_specific_movies(movies, keyword)`
#
# Now that we have created this data structure `movies`, we can start doing some fun things with the data!
# We will continue working on this data structure for the next project (P9) as well.
#
# Let us now use this data structure `movies` to create a **search bar** like the one in Netflix!
# **Do not change the below function in any way**.
# This function takes in a keyword like a substring of a title, a genre, or the name of a person, and returns a list of relevant movies with that title, genre, or cast member/director.
#
# **Warning:** As `movies` is very large, the function `find_specific_movies` may take five to ten seconds to run. This is normal and you should not panic if it takes a while to run.

# + deletable=false editable=false
# DO NOT EDIT THIS CELL AND DO NOT REDEFINE THIS FUNCTION ELSEWHERE
def find_specific_movies(movies, keyword):
    """
    find_specific_movies(movies, keyword) takes a list of movie dictionaries 
    and a keyword; it returns a list of movies that contain the keyword
    in either its title, genre, cast or directors.
    """
    idx = 0
    while idx < len(movies):
        movie = movies[idx]
        # note: \ enables you split a long line of code into two lines
        if (keyword not in movie['title']) and (keyword not in movie["genres"]) \
        and (keyword not in movie["directors"]) and (keyword not in movie["cast"]):
            movies.pop(idx)
        else:
            idx += 1
    return movies


# + [markdown] deletable=false editable=false
# **Important:** While it might look as if we are making it easy for you by providing `find_specific_movies`, there is a catch! There is a subtle flaw with the way the function is defined, that will cause you issues in the next two questions. If you can spot this flaw by just observing the definition of `find_specific_movies`, congratulations! Since you are **not** allowed to modify the function definition, you will have to be a little clever with your function arguments to sidestep the flaw with the function definition.
#
# If you don't see anything wrong with the function just yet, don't worry about it. Solve Question 14 and Question 15 as you normally would, and see if you notice anything suspicious about your answers.

# + deletable=false editable=false
grader.check("find_specific_movies")

# + [markdown] deletable=false editable=false
# **Question 14:** List all the movies involving *Alfred Hitchcock*.
#
# Your answer **must** be a **list** of **dictionaries**.
#
# You **must** answer this question by calling `find_specific_movies` with the keyword `"Alfred Hitchcock"`.
#
# The `find_specific_movies` function is expected to take around 5 seconds or more to run, so do not panic if it takes so long to run.
#
# Remember that you are **not** allowed to modify the definition of `find_specific_movies`. You will need to cleverly pass arguments to `find_specific_movies` (in both Question 14 and Question 15) to ensure that `movies` does not get modified by the function calls. Take a look at the Lecture Slides from October 25 for more hints. You will have to Restart and Run all your cells to see the correct output after you fix your answer for Question 14 (and Question 15).
# -

# compute and store the answer in the variable 'hitchcock_films', then display it
hitchcock_films = find_specific_movies(copy.deepcopy(movies), "Alfred Hitchcock")
hitchcock_films

# + deletable=false editable=false
grader.check("q14")

# + [markdown] deletable=false editable=false
# **Question 15:** List all the movies that contain the string `"Once Upon a Time in"` in their `title`.
#
# Your answer **must** be a **list** of **dictionaries**.
#
# You **must** answer this question by calling `find_specific_movies` with the keyword `"Once Upon a Time in"`.
#
# **Important Hint:**  If you did not notice the flaw with the definition of `find_specific_movies` before, you are likely to have run into an issue with this question. It is likely that you will see that your output for this question is an empty list. To see why this happened, find the value of `len(movies)` and see if it is equal to the value you found earlier.
# -

# compute and store the answer in the variable 'once_upon_a_time_in_movies', then display it
once_upon_a_time_in_movies = find_specific_movies(copy.deepcopy(movies), "Once Upon a Time in")

# + deletable=false editable=false
grader.check("q15")


# + [markdown] deletable=false editable=false
# ### Function 5: `bucketize_by_genre(movies)`
#
# We require you to complete the below function to answer the next several questions (this is a **requirement**, and you will **lose points** if you do not implement this function).
# -

def bucketize_by_genre(movies):
    """bucketize_by_genre(movies) takes a list of movie dictionaries;
    it returns a dict in which each genre is a key and
    the value is a list of all movies that contain that genre"""
    pass # replace with your code
    # TODO: initialize a dictionary
    # TODO: loop through all movies
    # TODO:     loop through all genres in this movie
    # TODO:         if this genre is not a key in our dictionary, set the value associated with this genre to an empty list
    # TODO:         add the movie to the list associated with this genre
    # TODO: return the dictionary
    dic = {}
    for movie in movies:
        for genre in movie["genres"]:
            if genre not in dic:
                dic[genre] = []
            dic[genre].append(movie)
    return dic


# + deletable=false editable=false
grader.check("bucketize_by_genre")

# + [markdown] deletable=false editable=false
# **Warning:** You are **not** allowed to call `bucketize_by_genre` more than once on the full list of movies (`movies`) in your notebook. The Gradescope autograder will **deduct points** if you call `bucketize_by_genre` again on `movies`.

# +
# call the function bucketize_by_genre on 'movies' and store it in the variable 'genre_dict'
# do NOT display the output directly

genre_dict = bucketize_by_genre(movies)

# + deletable=false editable=false
grader.check("genre_dict")

# + [markdown] deletable=false editable=false
# **Question 16:** How many **unique** movie `genres` are present in the dataset?
# -

# compute and store the answer in the variable 'num_genres', then display it
num_genres = len(genre_dict)
num_genres

# + deletable=false editable=false
grader.check("q16")

# + [markdown] deletable=false editable=false
# **Question 17:** How many *Romance* movies (i.e. movies with *Romance* as one of their `genres`) do we have in the dataset released **after** the `year` *2019*?
#
# Your output **must** be an **int**. You **must** use the `genre_dict` data structure to answer this question.
# -

# compute and store the answer in the variable 'romance_after_2019', then display it
romance_after_2019 = 0
for movie in genre_dict["Romance"]:
    if movie["year"] > 2019:
        romance_after_2019 += 1
romance_after_2019

# + deletable=false editable=false
grader.check("q17")

# + [markdown] deletable=false editable=false
# **Question 18:** List the `title` of all *Documentary* movies (i.e. movies with *Documentary* as one of their `genres`) with `duration` **larger** than *240* in the dataset.
#
# Your output **must** be a **list** of **strings**. You **must** use the `genre_dict` data structure to answer this question.
# -

# compute and store the answer in the variable 'docus_longer_than_240_mins', then display it
docus_longer_than_240_mins = []
for movie in genre_dict["Documentary"]:
    if movie["duration"] > 240:
        docus_longer_than_240_mins.append(movie["title"])
docus_longer_than_240_mins

# + deletable=false editable=false
grader.check("q18")

# + [markdown] deletable=false editable=false
# **Question 19:** Which movie `genre` is *Blake Lively* the most involved with?
#
# We say that *Blake Lively* is involved with a movie if she is **either** a *director* **or** a *cast member* of that movie. You need to find the movie `genre` with the **highest** number of movies that *Blake Lively* is involved with. There is a **unique** `genre` that *Blake Lively* is most involved with. You do **not** have to worry about breaking ties.
#
# You may **assume** that there are **no** movies in the dataset with the string `"Blake Lively"` in their `title`.
#
# **Hint:** You can combine the *two* functions above to bucketize the movies that *Blake Lively* was involved with by their `genres`. Then, you can loop through each genre to find the one with the most number of movies in it.
# -

# compute and store the answer in the variable 'blake_lively_genre', then display it
blake_lively_genre = None
dicty1 = bucketize_by_genre(find_specific_movies(movies, "Blake Lively"))
mostynum = 0
for genre in dicty1:
    if len(dicty1[genre]) > mostynum:
        mostynum = len(dicty1[genre])
        blake_lively_genre = genre
blake_lively_genre

# + deletable=false editable=false
grader.check("q19")

# + [markdown] deletable=false editable=false
# **Question 20:** Who are the `directors` of the *Horror* movies with the **highest** `rating` in the movies dataset?
#
# There are **multiple** *Horror* movies in the dataset with the joint highest rating. You **must** output a **list** of **strings** containing the **names** of **all** the `directors` of **all** these movies.
#
# **Hint:** If you are unsure how to efficiently add the elements of one list to another, please review any of the lecture notes from the October 9 lectures ([Mike](https://canvas.wisc.edu/courses/374263/files/folder/Mikes_Lecture_Notes/Lec14_Lists), [Gurmail](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-lecture-material/-/tree/main/f23/Gurmail_Lecture_Notes/14_Lists), or [Cole](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-lecture-material/-/tree/main/f23/Cole_Lecture_Notes/14_Lists)).
# -

# compute and store the answer in the variable 'max_horror_rating_directors', then display it
max_horror_rating_directors = []
highest_rating = 0
for movie in genre_dict["Horror"]:
    if movie["rating"] >= highest_rating:
        highest_rating = movie["rating"]
for movie in genre_dict["Horror"]:
    if movie["rating"] == highest_rating:
        max_horror_rating_directors.extend(movie["directors"])
max_horror_rating_directors

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
# !jupytext --to py p8.ipynb

# + [code] deletable=false editable=false
public_tests.check_file_size("p8.ipynb")
grader.export(pdf=False, run_tests=False, files=["p8.py"])

# + [markdown] deletable=false editable=false
#  
