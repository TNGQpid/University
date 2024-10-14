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
grader = otter.Notebook("p9.ipynb")

# + editable=false
import public_tests

# +
# PLEASE FILL IN THE DETAILS
# enter none if you don't have a project partner
# you will have to add your partner as a group member on Gradescope even after you fill this

# project: p9
# submitter: sheberlein
# partner: sheberlein

# + [markdown] deletable=false editable=false
# # Project 9: Analyzing the Movies

# + [markdown] deletable=false editable=false
# ## Learning Objectives:
#
# In this project, you will demonstrate your ability to:
# - use `matplotlib` to plot bar graphs and visualize statistics
# - process data using dictionaries and lists that you build
# - implement binning by writing algorithms that create dictionaries
# - custom sort a list using the keyword parameter `key`'s argument.
#
# Please go through [Lab-P9](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/tree/main/lab-p9) before starting this project. The lab introduces some useful techniques necessary for this project.

# + [markdown] deletable=false editable=false
# ## Testing your code:
#
# Along with this notebook, you must have downloaded the file `public_tests.py`. If you are curious about how we test your code, you can explore this file, and specifically the value of the variable `expected_json`, to understand the expected answers to the questions.
#
# **Important:** `public_tests.py` **cannot** verify your answers when the output is an image. Your **plots** will be **checked** by the Gradescope autograder, so you must **manually** confirm that your plots look correct by comparing with the images provided in the notebook.

# + [markdown] deletable=false editable=false
# <h2 style="color:red">Warning (Note on Academic Misconduct):</h2>
#
# **IMPORTANT**: **P8 and P9 are two parts of the same data analysis.** You **cannot** switch project partners between these two projects. That is if you partnered up with someone for P8, you have to sustain that partnership until the end of P9. Now may be a good time to review [our course policies](https://cs220.cs.wisc.edu/f23/syllabus.html).
#
# Under any circumstances, **no more than two students are allowed to work together on a project** as mentioned in the course policies. If your code is flagged by our code similarity detection tools, **both partners will be responsible** for sharing/copying the code, even if the code is shared/copied by one of the partners with/from other non-partner student(s). Note that each case of plagiarism will be reported to the Dean of Students with a zero grade on the project. **If you think that someone cannot be your project partner then don’t make that student your lab partner.**
#
# **<font color = "red">Project partners must submit only one copy of their project on Gradescope, but they must include the names of both partners.</font>**

# + [markdown] deletable=false editable=false
# ## Introduction:
#
# In P8, you created very useful helper functions to parse the raw IMDb dataset. You also created useful data structures to store the data. In this project, you will be building on the work you did in P8 to analyze your favorite movies. This is a shorter project than usual, and **P9 will only have 10 questions for you to solve**.

# + [markdown] deletable=false editable=false
# ## Data:
#
# In P9, you will be analyzing the same dataset that you worked with in P8. You may download the files fresh, or just copy/paste the datasets from your P8 directory.

# + [markdown] deletable=false editable=false
# ## Project Requirements:
#
# You **may not** hardcode indices in your code, unless the question explicitly asks you to do so. If you open your `.csv` files with Excel, manually count through the rows and use this number to loop through the dataset, this is also considered as hardcoding. If any instances of hardcoding are found during code review, the Gradescope autograder will **deduct** points from your public score.
#
# **Store** your final answer for each question in the **variable specified for each question**. This step is important because Otter grades your work by comparing the value of this variable against the correct answer.
#
# For some of the questions, we'll ask you to write (then use) a function to compute the answer. If you compute the answer **without** creating the function we ask you to write, the Gradescope autograder will **deduct** points from your public score, even if the way you did it produced the correct answer.
#
# Required Functions:
# - `bucketize`
#
# In this project, you will also be required to define certain **data structures**. If you do not create these data structures exactly as specified, the Gradescope autograder will **deduct** points from your public score, even if the way you did it produced the correct answer.
#
# Required Data Structures:
# - `movies`
# - `cast_buckets`
# - `director_buckets`
# - `genre_buckets`
# - `year_buckets`
#
# You are only allowed to define these data structures **once** and we'll **deduct** points from your public score on Gradescope if you redefine the values of these variables.
#
# In this project (and the next), you will be asked to create **lists** of movies. For all such questions, **unless it is explicitly mentioned otherwise**, the movies should be in the **same order** as in the `movies.csv` (or `small_movies.csv`) file. Similarly, for each movie, the **list** of `genres`, `directors`, and `cast` members should always be in the **same order** as in the `movies.csv` (or `small_movies.csv`) file.
#
# Students are only allowed to use Python commands and concepts that have been taught in the course prior to the release of P9. Therefore, you should not use the `pandas` module. The Gradescope autograder will **deduct** points from your public score otherwise.
#
# For more details on what will cause you to lose points during code review and specific requirements, please take a look at the [Grading rubric](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f23-projects/-/blob/main/p9/rubric.md).

# + [markdown] deletable=false editable=false
# ## Project Questions and Functions:
# -

# it is considered a good coding practice to place all import statements at the top of the notebook
# please place all your import statements in this cell if you need to import any more modules for this project
import csv
import matplotlib
import pandas


# + [markdown] deletable=false editable=false
# ## Loading the Movies Data
#
# For all these questions, we will be looking at the movies in `mapping.csv` and `movies.csv`. You can load the list of movies using the functions you wrote in the last project.

# + [markdown] deletable=false editable=false
# Copy the functions you wrote in `p8.ipynb` to `p9.ipynb` to read the movies data. The functions you should include are `process_csv`, `get_mapping`, `get_raw_movies`, and `get_movies` along with any helper functions you used to write these. Do **not** copy/paste `find_specific_movies` here. Later in P9, we will provide you with a simpler version of that function, which does not require the use of the `copy` module.

# +
# copy/paste the definition of process_csv from previous projects (p6 or p7)
# copy/paste the definitions of get_mapping, get_raw_movies, get_movies from p8.ipynb
# as well as any helper functions used by these functions here
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


# + [markdown] deletable=false editable=false
# Now, you can use `get_movies` to read the data in `movies.csv` and `mapping.csv` as you did in P8.

# +
# create a list of dictionaries named 'movies' to store the data in 'movies.csv' and 'mapping.csv' as in p8
# do NOT display the value of this variable anywhere in this notebook

movies = get_movies("movies.csv", "mapping.csv")


# + [markdown] deletable=false editable=false
# There should be *73075* **dictionaries** in the **list** `movies` and the first entry of `movies` should be a **dictionary** that looks as follows:
#
# ```python
# {'title': 'A Grande Arte',
#  'year': 1991,
#  'duration': 104,
#  'genres': ['Drama', 'Thriller'],
#  'rating': 6.1,
#  'directors': ['Walter Salles'],
#  'cast': ['Peter Coyote', 'Tchéky Karyo', 'Amanda Pays', 'Raul Cortez']}
# ```
#
# **Warning:** At this stage, it is expected that the function `get_movies` works correctly, and that `movies` is defined as it was in P8. If not, your code will run into issues in P9. So, make sure that this function works properly before you start P9. You can do that by **inserting a new cell** in Jupyter below this cell and verifying that the size of your variable `movies`, and that the first **dictionary** in `movies` is as it should be.
#
# Also, just like in P8, delete any cells displaying the whole of `movies` data structure before turning in `p9.ipynb`.

# + [markdown] deletable=false editable=false
# Now, copy over the functions `plot_dict`, `median` and `year_to_decade` from Lab-P9.

# +
# copy/paste the definitions of plot_dict, median, year_to_decade from "Lab-P9
# as well as any helper functions used by these functions here
def plot_dict(d, label="Please Label Me!"):
    """plot_dict(d, label) creates a bar plot using the 
    dictionary 'd' and labels the y-axis as 'label'"""
    ax = pandas.Series(d).sort_index().plot.bar(color="black", fontsize=16, figsize=(4 + len(d)//4, 4))
    ax.set_ylabel(label, fontsize=16)

def median(items):
    """
    median(items) returns the median of the list `items`
    """
    # sort the list
    sorted_list = sorted(items)
    # determine the length of the list
    list_len = len(sorted_list)
    if list_len % 2 == 1: # determine whether length of the list is odd
        # return item in the middle using indexing
        return sorted_list[list_len//2]
    else:
        first_middle = sorted_list[list_len//2] # use appropriate indexing
        second_middle = sorted_list[list_len//2 - 1] # use appropriate indexing
        return (first_middle + second_middle) / 2

def year_to_decade(year):
    if year % 10 == 0:
        decade = str(year-9) + ' to ' + str(year)
    else:
        # TODO: first find the year in which the decade starts
        #       when year % 10 != 0
        # TODO: define the variable 'decade'
        decade = (year - (year%10) + 1)
        decade =  str(decade) + " to " + str(decade + 9)
    return decade



# + [markdown] deletable=false editable=false
# In P8, you were provided with a function `find_specific_movies` which functioned as some sort of a 'search bar' for the movies dataset. However, in order to use that function properly, you had to use the `copy` module to pass a *copy* of your list of movies to `find_specific_movies`. Making copies frequently is **not** a good coding practice. For this project, we will provide **a new version** of `find_specific_movies` that does **not** require using `copy`. Please go through the following function:
# -

# modified find_specific_movies (doesn't require using copy module)
def find_specific_movies(movies, keyword):
    """
    find_specific_movies(movies, keyword) takes a list of movie dictionaries 
    and a keyword; it returns a list of movies that contain the keyword
    in either its title, genre, cast or directors.
    """
    movies_with_keyword = []
    for movie in movies:
        if (keyword in movie['title']) or (keyword in movie['genres']) \
            or (keyword in movie['directors']) or (keyword in movie['cast']):
            movies_with_keyword.append(movie)
    return movies_with_keyword


# + [markdown] deletable=false editable=false
# **Important:** **Even when you are not explicitly prompted to do so, using the `find_specific_movies` function cleverly can simplify your code significantly. Keep an eye out for how you can simplify your code by making use of `find_specific_movies`.**

# + [markdown] deletable=false editable=false
# ### Analyzing the Movies data

# + [markdown] deletable=false editable=false
# **Question 1:** What is the **median** `rating` of the movies that **involve** both *Clint Eastwood* and *Sergio Leone*?
#
# You **must** make multiple calls to the `find_specific_movies` function to identify the movies which involve both *Clint Eastwood* and *Sergio Leone*.

# +
# compute and store the answer in the variable 'median_eastwood_leone_rating', then display it
clint = find_specific_movies(movies, "Clint Eastwood")
sergio = find_specific_movies(movies, "Sergio Leone")
both =[]
for movie in clint:
    if movie in sergio:
        both.append(movie)

median_rating = median([movie['rating'] for movie in both])

median_eastwood_leone_rating = median_rating
median_eastwood_leone_rating

# + deletable=false editable=false
grader.check("q1")

# + [markdown] deletable=false editable=false
# **Question 2:** Among all the *Toy Story* movies, which ones are the **highest** rated?
#
# Your output **must** be a **list** of **dictionaries**. You **must** use `find_specific_movies` to identify all movies which have *Toy Story* as a substring of their `title`.
#
# **Hint:** You could first find the **highest** `rating` that any *Toy Story* movie received, and then find all the *Toy Story* movies that received that `rating`.
# -

# compute and store the answer in the variable 'highest_rated_toy_story_movies', then display it
highest_rated_toy_story_movies = []
mov = find_specific_movies(movies, "Toy Story")
listy = [movie["rating"] for movie in mov]
maxi = max(listy)
for movie in mov:
    if movie["rating"] == maxi:
        highest_rated_toy_story_movies.append(movie)
highest_rated_toy_story_movies

# + deletable=false editable=false
grader.check("q2")


# + [markdown] deletable=false editable=false
# ### Function 1: `bucketize(movies_list, category)` 
#
# This function should take in a **list** of movie **dictionaries** as well as a **category** (i.e. `title`, `year`, `duration`, `genres`, `rating`, `directors`, or `cast`), and *bucketize* the **list** of movie **dictionaries** by this **category**.
#
# For example, the output of `bucketize(movies, 'rating')` should be a **dictionary** so that all the unique values of `rating` of the movies in `movies` are the **keys** and the correspoding **values** would be a **list** of all movie **dictionaries** with that rating (e.g., the value of the key *6.4* should be the **list** of movie dictionaries with `rating` of *6.4*).
#
# The output of `bucketize(movies, 'rating')` should look like this:
#
# ```python
# {6.1: [{'title': 'A Grande Arte',
#         'year': 1991,
#         'duration': 104,
#         'genres': ['Drama', 'Thriller'],
#         'rating': 6.1,
#         'directors': ['Walter Salles'],
#         'cast': ['Peter Coyote', 'Tchéky Karyo', 'Amanda Pays', 'Raul Cortez']},
#        {'title': 'Elena Undone',
#         'year': 2010,
#         'duration': 111,
#         'genres': ['Drama', 'Romance'],
#         'rating': 6.1,
#         'directors': ['Nicole Conn'],
#         'cast': ['Necar Zadegan', 'Thunderbird Dinwiddie', 'Gary Weeks', 'Sam Harris']},
#        ...
#       ],
#  4.1: [{'title': 'Enemy Gold',
#         'year': 1993,
#         'duration': 92,
#         'genres': ['Action', 'Crime'],
#         'rating': 4.1,
#         'directors': ['Christian Drew Sidaris'],
#         'cast': ['Bruce Penhall', 'Mark Barriere', 'Suzi Simpson', 'Tanquil Lisa Collins']},
#        {'title': "Dead Men Don't Die",
#         'year': 1990,
#         'duration': 94,
#         'genres': ['Comedy', 'Crime', 'Horror'],
#         'rating': 4.1,
#         'directors': ['Malcolm Marmorstein'],
#         'cast': ['Elliott Gould', 'Melissa Sue Anderson', 'Mark Moses', 'Mabel King']},
#        ...
#       ],
#  ...
# }
# ```
#
# Similarly, the output of `bucketize(movies, 'cast')` should be a **dictionary** so that all the unique `cast` members of the movies in `movies` are the **keys** and the correspoding **values** would be a **list** of all movie **dictionaries** with that cast member as one of their `cast` (e.g., the value of the key *Kate Winslet* should be the **list** of movie dictionaries with *Kate Winslet* as one of their `cast` members).
#
# The output of `bucketize(movies, 'cast')` should look like this:
#
# ```python
# {{'Peter Coyote': [{'title': 'A Grande Arte',
#                     'year': 1991,
#                     'duration': 104,
#                     'genres': ['Drama', 'Thriller'],
#                     'rating': 6.1,
#                     'directors': ['Walter Salles'],
#                     'cast': ['Peter Coyote', 'Tchéky Karyo', 'Amanda Pays', 'Raul Cortez']},
#                    {'title': 'No Deposit',
#                     'year': 2015,
#                     'duration': 80,
#                     'genres': ['Drama'],
#                     'rating': 5.6,
#                     'directors': ["Frank D'Angelo"],
#                     'cast': ['Paul Amato', 'Daniel Baldwin', 'Jason Blicker', 'Peter Coyote']},
#                    ...
#                   ],
#  'Tchéky Karyo': [{'title': 'A Grande Arte',
#                    'year': 1991,
#                    'duration': 104,
#                    'genres': ['Drama', 'Thriller'],
#                    'rating': 6.1,
#                    'directors': ['Walter Salles'],
#                    'cast': ['Peter Coyote', 'Tchéky Karyo', 'Amanda Pays', 'Raul Cortez']},
#                   {'title': 'Wing Commander',
#                    'year': 1999,
#                    'duration': 100,
#                    'genres': ['Action', 'Adventure', 'Sci-Fi'],
#                    'rating': 4.3,
#                    'directors': ['Chris Roberts'],
#                    'cast': ['Freddie Prinze Jr.', 'Matthew Lillard', 'Saffron Burrows', 'Tchéky Karyo']},
#                    ...
#                   ]
#  ...
# } 
# ```
#
# **Hints:** Note that depending on whether or not the `category` represents a **list** or not, your function will have to behave differently. In P8, you created a function `bucketize_by_genre` that *bucketized* the list of movies by their genre. Take a moment to find that function; it will help you here. Also, take a moment to look at the buckets you made in Lab-P9.

# +
# replace the ... with your code to finish the definition of bucketize

def bucketize(movie_list, category):
    buckets = {}
    for movie in movie_list:
        category_value = movie[category] #TODO: access the category value from a movie
        # TODO: bucketize depending on the type of `category_value`
        if isinstance(category_value, list):
            for cat in movie[category]:
                if cat not in buckets:
                    buckets[cat] = []
                buckets[cat].append(movie)
        else:
            if category_value not in buckets:
                buckets[category_value] = [movie]
            else:
                buckets[category_value].append(movie)
    return buckets


# + deletable=false editable=false
grader.check("bucketize")

# + [markdown] deletable=false editable=false
# **Important:** Just like `get_movies`, `bucketize` is quite a time-consuming function to run. Hence, you do **not** want to call `bucketize` on the same list of movies and category **more than once**. Throughout the project, we will frequently use bucketized lists of movies organized by their `cast`, `directors`, `genre`, and `year`. Rather than calling `bucketize` several times, we will store the bucketized lists in the following variables:

# +
# define buckets for categories mentioned below, but do NOT display any of them

# bucketize the full list of movies by their cast.
cast_buckets = bucketize(movies, "cast")
# bucketize the full list of movies by their directors.
director_buckets = bucketize(movies, "directors")
# bucketize the full list of movies by their genre.
genre_buckets = bucketize(movies, "genres")
# bucketize the full list of movies by their year.
year_buckets = bucketize(movies, "year")


# + deletable=false editable=false
grader.check("cast_buckets")

# + deletable=false editable=false
grader.check("director_buckets")

# + deletable=false editable=false
grader.check("genre_buckets")

# + deletable=false editable=false
grader.check("year_buckets")

# + [markdown] deletable=false editable=false
# Even when you are not explicitly prompted to do so, using these data structures and the `bucketize` function cleverly can simplify your code significantly. Keep an eye out for how you can simplify your code by making use of these data structures and the `bucketize` function.
#
# Remember, you can still use the `bucketize` function on a subset of the `movies` data structure (i.e. not the whole `movies` dataset). You are **not** limited to only using the variables defined above.

# + [markdown] deletable=false editable=false
# **Question 3:** List the movies that *Margot Robbie* was `cast` in.
#
# Your output **must** be a **list** of **dictionaries**. You **must** answer this question by accessing the **value** of the correct **key** from the correct **bucket** defined in the previous cell.

# +
# compute and store the answer in the variable 'robbie_movies', then display it
robbie_movies = cast_buckets["Margot Robbie"]

robbie_movies

# + deletable=false editable=false
grader.check("q3")

# + [markdown] deletable=false editable=false
# **Question 4:** **Plot** the **number** of movies in each *genre* as a **bar graph**.
#
# You **must** first compute a **dictionary** which maps each **genre** to the **number** of movies in that **genre**.

# +
# first compute and store the dictionary in the variable 'genre_num', then display it
# do NOT plot just yet
genre_num = {genre:len(genre_buckets[genre]) for genre in genre_buckets}

genre_num

# + deletable=false editable=false
grader.check("q4")

# + [markdown] deletable=false editable=false
# Now, **plot** `genre_num` as a **bar graph**.
#
# **Important Warning:** `public_tests.py` can only check that the **dictionary** has the correct key/value pairs, but it **cannot** check if your plot appears on the screen, or whether the axes are correctly labelled. The Gradescope autograder will deduct points if your plot is not visible in the **cell below**, or if it is not properly labelled.
#
# **Hint:** If the `grader.export` cell fails to run because the file size is too large, you can delete the plot below to reduce the size of your notebook. Make sure your plot matches the plot below, before you do so.
#
# Your plot should look like this:

# + [markdown] deletable=false editable=false
# <div><img src="attachment:q4.jpg" style="height: 300px;"/></div>

# +
# plot 'genre_num' with the y-axis labelled 'number of movies'

plot_dict(genre_num, "number of movies")

# + [markdown] deletable=false editable=false
# **Food for thought:** Can you tell what the most popular **genres** are from the plot? Do you see anything surprising in this plot?
# -

# Food for thought is an entirely OPTIONAL exercise
# you may leave your thoughts here as a comment if you wish to


# + [markdown] deletable=false editable=false
# **Question 5:** **Plot** the **number** of movies **directed** by *Stanley Kubrick* in each *genre* as a **bar graph**.
#
# You **must** only include those `genres` in which *Stanley Kubrick* has directed **at least** one movie, in your plot.
#
# You **must** first compute a **dictionary** which maps each **genre** to the **number** of movies in that **genre** directed by *Stanley Kubrick*.
#
# **Hint:** Think about how you can use functions such as `bucketize` on a subset of movies for the category that you are interested in.

# +
# first compute and store the dictionary in the variable 'kubrick_genres', then display it
# do NOT plot just yet
kubrick_genres = {genre:len(bucketize(find_specific_movies(movies, "Stanley Kubrick"), "genres")[genre]) \
                  for genre in bucketize(find_specific_movies(movies, "Stanley Kubrick"), "genres")}


kubrick_genres

# + deletable=false editable=false
grader.check("q5")

# + [markdown] deletable=false editable=false
# Now, **plot** `kubrick_genres` as a **bar graph**.
#
# **Important Warning:** `public_tests.py` can only check that the **dictionary** has the correct key/value pairs, but it **cannot** check if your plot appears on the screen, or whether the axes are correctly labelled. The Gradescope autograder will deduct points if your plot is not visible in the **cell below**, or if it is not properly labelled.
#
# **Hint:** If the `grader.export` cell fails to run because the file size is too large, you can delete the plot below to reduce the size of your notebook. Make sure your plot matches the plot below, before you do so.
#
# Your plot should look like this:

# + [markdown] deletable=false editable=false
# <div><img src="attachment:q5.jpg" style="height: 300px;"/></div>
# -

# now plot 'kubrick_genres' with the y-axis labelled 'number of movies'
plot_dict(kubrick_genres, "number of movies")

# + [markdown] deletable=false editable=false
# **Food for thought:** Can you similarly **plot** the **number** of films directed by your favorite director or starring your favorite cast member in each **genre**?
# -

# Food for thought is an entirely OPTIONAL exercise
# you may leave your thoughts here as a comment if you wish to


# + [markdown] deletable=false editable=false
# **Question 6:** **Plot** the **number** of **Sci-Fi** movies released in each *decade* as a **bar graph**.
#
# You **must** first compute a **dictionary** which maps each **decade** to the **number** of movies in released in that **decade**. This dictionary should look like this:
#
# ```python
# {'2011 to 2020': 1100,
#  '1961 to 1970': 201,
#  '1911 to 1920': 6,
#  '1981 to 1990': 383,
#  '1951 to 1960': 198,
#  '1941 to 1950': 24,
#  '1991 to 2000': 389,
#  '2021 to 2030': 242,
#  '2001 to 2010': 517,
#  '1971 to 1980': 243,
#  '1931 to 1940': 28,
#  '1921 to 1930': 5}
# ```
#
# **Hint:** You should use `year_to_decade` function to get the decade for a movie's year

# +
# first compute and store the dictionary in the variable 'sci_fi_decade_mapping', then display it
# do NOT plot just yet

#year_buckers maps year to list of movies

sci_fi_decade_mapping = {}
for year in year_buckets:
    for movie in year_buckets[year]:
        if "Sci-Fi" in movie["genres"]:
            if year_to_decade(year) not in sci_fi_decade_mapping:
                sci_fi_decade_mapping[year_to_decade(year)] = 1
            else:
                sci_fi_decade_mapping[year_to_decade(year)] += 1


sci_fi_decade_mapping

# + deletable=false editable=false
grader.check("q6")

# + [markdown] deletable=false editable=false
# Now, **plot** `sci_fi_decade_mapping` as a **bar graph**.
#
# **Important Warning:** `public_tests.py` can only check that the **dictionary** has the correct key/value pairs, but it **cannot** check if your plot appears on the screen, or whether the axes are correctly labelled. The Gradescope autograder will deduct points if your plot is not visible in the **cell below**, or if it is not properly labelled.
#
# **Hint:** If the `grader.export` cell fails to run because the file size is too large, you can delete the plot below to reduce the size of your notebook. Make sure your plot matches the plot below, before you do so.
#
# Your plot should look like this:

# + [markdown] deletable=false editable=false
# <div><img src="attachment:q6.jpg" style="height: 300px;"/></div>
# -

# now plot 'sci_fi_decade_mapping' with the y-axis labelled 'Sci-Fi movies released'
plot_dict(sci_fi_decade_mapping, "Sci-Fi movies released")

# + [markdown] deletable=false editable=false
# **Food for thought:** Can you explain the shape of this plot? Why do you think the number of Sci-Fi movies increased so rapidly over the last decade? If you want, you could compare this plot against plots of other genres (such as `Western` or `Horror`).
# -

# Food for thought is an entirely OPTIONAL exercise
# you may leave your thoughts here as a comment if you wish to


# + [markdown] deletable=false editable=false
# **Question 7:** **Plot** the **median** `rating` of movies in each `genre` directed by *James Cameron* as a **bar graph**.
#
# You **must** first compute a **dictionary** which maps each **genre** of movies directed by *James Cameron* to the **median** `rating` of all movies in that **genre**. Note that your dictionary **must not** contain any genres in which *James Cameron* has not directed any movie.

# +
# first compute and store the dictionary in the variable 'cameron_median_genres', then display it
# do NOT plot just yet
cameron_median_genres = {}
mos = []
for movie in movies:
    if "James Cameron" in movie["directors"]:
        mos.append(movie)

dicty = bucketize(mos, "genres")

for genre in dicty:    
    listy1 = []
    for movie in dicty[genre]:
        listy1.append(movie["rating"])
    cameron_median_genres[genre] = median(listy1)


cameron_median_genres

# + deletable=false editable=false
grader.check("q7")

# + [markdown] deletable=false editable=false
# Now, **plot** `cameron_median_genres` as a **bar graph**.
#
# **Important Warning:** `public_tests.py` can only check that the **dictionary** has the correct key/value pairs, but it **cannot** check if your plot appears on the screen, or whether the axes are correctly labelled. The Gradescope autograder will deduct points if your plot is not visible in the **cell below**, or if it is not properly labelled.
#
# **Hint:** If the `grader.export` cell fails to run because the file size is too large, you can delete the plot below to reduce the size of your notebook. Make sure your plot matches the plot below, before you do so.
#
# Your plot should look like this:

# + [markdown] deletable=false editable=false
# <div><img src="attachment:q7.jpg" style="height: 300px;"/></div>
# -

# now plot 'cameron_median_genres' with the y-axis labelled 'median rating'
plot_dict(cameron_median_genres, 'median rating')

# + [markdown] deletable=false editable=false
# **Food for thought:** *James Cameron* has directed many critically acclaimed movies such as *Aliens*, *The Terminator*, *Avatar*, and *Titanic*. Nevertheless, median ratings of his work in the *Thriller*, and especially *Horror* genres are surprisingly lackluster. Can you explain this inconsistency?
#
# Hint: Take a look at the years of release of the films in these genres. 
# -

# Food for thought is an entirely OPTIONAL exercise
# you may leave your thoughts here as a comment if you wish to


# + [markdown] deletable=false editable=false
# The visualization in Question 7 immediately tells us that the **median** *Fantasy* movie directed by *James Cameron* is rated higher than the **median** *Horror* movie. However, it is a little hard to tell how the **median** *Romance* movie fares against the **median** *Adventure* movie. In order to compare the `genres`, it would be useful to **sort** the `genres` by their **median** `rating`.
#
# Refer [Mike's](???), [Gurmail's](???) or [Cole's](???) lecture notes on using function references to sort a collection by value(s) related to that collection's elements.

# + [markdown] deletable=false editable=false
# **Question 8:** Produce a **list** of `genres` of films directed by *James Cameron* sorted in **decreasing order** of their **median** `rating`.
#
# **Hint:** Refer to Task 4.2 in Lab-P9 to understand how to sort a collection using the `key` parameter.

# +
# compute and store the answer in the variable 'cameron_genres_desc', then display it
hit = sorted(cameron_median_genres.items(), key = lambda item: item[1], reverse = True)


cameron_genres_desc = [key for key, value in hit]
cameron_genres_desc

# + deletable=false editable=false
grader.check("q8")

# + [markdown] deletable=false editable=false
# **Question 9:** Produce a **list** of movies directed by *Martin Scorsese* and starring *Robert De Niro* sorted in **increasing** order of their `year` of release.
#
# Your output **must** be a **list** of **dictionaries** of movies having *Martin Scorsese* as one of the `directors`, and *Robert De Niro* as one of the `cast` members, that are **sorted** in **increasing** order of their `year`.

# +
# compute and store the answer in the variable 'scorsese_de_niro_movies', then display it
scorsese_de_niro_movies = []
for movie in movies:
    if "Martin Scorsese" in movie["directors"] and "Robert De Niro" in movie["cast"]:
        scorsese_de_niro_movies.append(movie)

scorsese_de_niro_movies = sorted(scorsese_de_niro_movies, key = lambda item:item["year"])

scorsese_de_niro_movies

# + deletable=false editable=false
grader.check("q9")

# + [markdown] deletable=false editable=false
# **Food for thought:** Can you think of other famous director-actor combinations? Can you find a combination with more movies than *Scorsese* and *De Niro*?
# -

# Food for thought is an entirely OPTIONAL exercise
# you may leave your thoughts here as a comment if you wish to


all_m = [(movie['title'], movie['year']) for movie in sorted(movies, key=lambda movie: movie['rating'], reverse=True)][:100]
len([a for a in all_m if a[1] > 2020])

# + [markdown] deletable=false editable=false
# ### Finding the best `directors`
#
# Notice that the movie with the **highest** `rating` in the dataset is
#
# ```python
# {'title': 'Red Sandal Wood',
#   'year': 2023,
#   'duration': 94,
#   'genres': ['Action', 'Thriller'],
#   'rating': 9.9,
#   'directors': ['Guru Ramaanujam'],
#   'cast': ['Vetri', 'Diya Mayuri', 'Ramachandra Raju', 'Abhi']}
# ```
#
# This movie is the **only** movie directed by this `director`. So, it is hardly appropriate to use this one movie to hail this director as one of the best ever. Moreover, **nine out of the top ten** highest rated movies in the dataset happen to be from just the `year` **2023**, while **over half of the top hundred** highest rated movies were released after the `year` *2020*. This is explained by the fact that IMDb `ratings` tend to be **inflated** soon after release, and *settle* down after a while.
#
# Therefore, if we want to identify who the **best** directors are, it would be a good idea to ignore the movies that were released **after** the `year` *2020*, and to restrict our attention to `directors` who have directed a **decent number** of movies. 

# + [markdown] deletable=false editable=false
# **Question 10:** Produce a **list** of `directors` who have directed **at least** *10* movies, have a **median** `rating` of **at least** *7.5*, and have a **minimum** `rating` of **at least** *5.0*. You **must** **exclude** all movies released **after** the `year` *2020*.
#
# Your output **must** be a **list** of the names of the `directors`. The order does **not** matter.
#
# **Hint**: You must first create a **list** of movies **excluding** the movies released **after** the `year` *2020*. Then, among these movies, you must find the `directors` who have directed `>= 10` movies, and whose movies have a **median** `rating` of `>= 7.5`, as well as a **minimum** `rating` of `>= 5.0`.

# +
# compute and store the answer in the variable 'best_directors', then display it
best_directors = []
movs = [movie for movie in movies if movie["year"] <= 2020]
potedict = bucketize(movs, "directors") # directors to list of movies
directors1 = [director for director in potedict if len(potedict[director]) >= 10]

mediansdirs = []

for director in potedict:
    list11= []
    for movie in potedict[director]:
        list11.append(movie["rating"])
    if median(list11) >= 7.5 and min(list11) >=5.0:
        mediansdirs.append(director)

for director in directors1:
    if director in mediansdirs:
        best_directors.append(director)

best_directors

# + deletable=false editable=false
grader.check("q10")

# + [markdown] deletable=false editable=false
# **Food for thought:** How many of these directors can you recognize? Do you spot your favorite director in that list? Can you come up with better criteria for deciding who the best directors are?
# -

# Food for thought is an entirely OPTIONAL exercise
# you may leave your thoughts here as a comment if you wish to


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
# !jupytext --to py p9.ipynb

# + [code] deletable=false editable=false
public_tests.check_file_size("p9.ipynb")
grader.export(pdf=False, run_tests=False, files=["p9.py"])

# + [markdown] deletable=false editable=false
#  
