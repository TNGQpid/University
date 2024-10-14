#!/usr/bin/python
# +
import os, json, math, copy
from collections import namedtuple
from bs4 import BeautifulSoup

HIDDEN_FILE = os.path.join("hidden", "hidden_tests.py")
if os.path.exists(HIDDEN_FILE):
    import hidden.hidden_tests as hidn
# -

MAX_FILE_SIZE = 750 # units - KB
REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats
TOTAL_SCORE = 100 # total score for the project

DF_FILE = 'expected_dfs.html'
PLOT_FILE = 'expected_plots.json'

PASS = "All test cases passed!"

TEXT_FORMAT = "TEXT_FORMAT"  # question type when expected answer is a type, str, int, float, or bool
TEXT_FORMAT_UNORDERED_LIST = "TEXT_FORMAT_UNORDERED_LIST"  # question type when the expected answer is a list or a set where the order does *not* matter
TEXT_FORMAT_ORDERED_LIST = "TEXT_FORMAT_ORDERED_LIST"  # question type when the expected answer is a list or tuple where the order does matter
TEXT_FORMAT_DICT = "TEXT_FORMAT_DICT"  # question type when the expected answer is a dictionary
TEXT_FORMAT_SPECIAL_ORDERED_LIST = "TEXT_FORMAT_SPECIAL_ORDERED_LIST"  # question type when the expected answer is a list where order does matter, but with possible ties. Elements are ordered according to values in special_ordered_json (with ties allowed)
TEXT_FORMAT_NAMEDTUPLE = "TEXT_FORMAT_NAMEDTUPLE"  # question type when expected answer is a namedtuple
PNG_FORMAT_SCATTER = "PNG_FORMAT_SCATTER" # question type when the expected answer is a scatter plot
HTML_FORMAT = "HTML_FORMAT" # question type when the expected answer is a DataFrame
FILE_JSON_FORMAT = "FILE_JSON_FORMAT" # question type when the expected answer is a JSON file
SLASHES = " SLASHES" # question SUFFIX when expected answer contains paths with slashes

def get_expected_format():
    """get_expected_format() returns a dict mapping each question to the format
    of the expected answer."""
    expected_format = {'q1': 'TEXT_FORMAT_DICT',
                       'q2': 'TEXT_FORMAT',
                       'q3': 'TEXT_FORMAT_UNORDERED_LIST',
                       'q4': 'TEXT_FORMAT_UNORDERED_LIST',
                       'q5': 'TEXT_FORMAT_ORDERED_LIST',
                       'q6': 'TEXT_FORMAT',
                       'q7': 'TEXT_FORMAT',
                       'q8': 'TEXT_FORMAT_ORDERED_LIST',
                       'q9': 'TEXT_FORMAT',
                       'q10': 'TEXT_FORMAT',
                       'q11': 'TEXT_FORMAT',
                       'q12': 'TEXT_FORMAT_ORDERED_LIST',
                       'q13': 'TEXT_FORMAT',
                       'q14': 'TEXT_FORMAT_ORDERED_LIST',
                       'q15': 'TEXT_FORMAT_ORDERED_LIST',
                       'q16': 'TEXT_FORMAT',
                       'q17': 'TEXT_FORMAT',
                       'q18': 'TEXT_FORMAT_ORDERED_LIST',
                       'q19': 'TEXT_FORMAT',
                       'q20': 'TEXT_FORMAT_UNORDERED_LIST'}
    return expected_format


def get_expected_json():
    """get_expected_json() returns a dict mapping each question to the expected
    answer (if the format permits it)."""
    expected_json = {'q1': {'tt15398776': 'Oppenheimer',
                            'tt1517268': 'Barbie',
                            'nm0634240': 'Christopher Nolan',
                            'nm0614165': 'Cillian Murphy',
                            'nm1289434': 'Emily Blunt',
                            'nm0000354': 'Matt Damon',
                            'nm0000375': 'Robert Downey Jr.',
                            'nm1950086': 'Greta Gerwig',
                            'nm3053338': 'Margot Robbie',
                            'nm0331516': 'Ryan Gosling',
                            'nm4793987': 'Issa Rae',
                            'nm0571952': 'Kate McKinnon'},
                     'q2': 'Emily Blunt',
                     'q3': ['Christopher Nolan',
                            'Cillian Murphy',
                            'Emily Blunt',
                            'Matt Damon',
                            'Robert Downey Jr.',
                            'Greta Gerwig',
                            'Margot Robbie',
                            'Ryan Gosling',
                            'Issa Rae',
                            'Kate McKinnon'],
                     'q4': ['nm0614165'],
                     'q5': [{'title': 'tt15398776',
                             'year': 2023,
                             'duration': 180,
                             'genres': ['Biography', 'Drama', 'History'],
                             'rating': 8.7,
                             'directors': ['nm0634240'],
                             'cast': ['nm0614165', 'nm1289434', 'nm0000354', 'nm0000375']},
                            {'title': 'tt1517268',
                             'year': 2023,
                             'duration': 114,
                             'genres': ['Adventure', 'Comedy', 'Fantasy'],
                             'rating': 7.5,
                             'directors': ['nm1950086'],
                             'cast': ['nm3053338', 'nm0331516', 'nm4793987', 'nm0571952']}],
                     'q6': 4,
                     'q7': 'nm0614165',
                     'q8': [{'title': 'Oppenheimer',
                             'year': 2023,
                             'duration': 180,
                             'genres': ['Biography', 'Drama', 'History'],
                             'rating': 8.7,
                             'directors': ['Christopher Nolan'],
                             'cast': ['Cillian Murphy',
                                      'Emily Blunt',
                                      'Matt Damon',
                                      'Robert Downey Jr.']},
                            {'title': 'Barbie',
                             'year': 2023,
                             'duration': 114,
                             'genres': ['Adventure', 'Comedy', 'Fantasy'],
                             'rating': 7.5,
                             'directors': ['Greta Gerwig'],
                             'cast': ['Margot Robbie',
                                      'Ryan Gosling',
                                      'Issa Rae',
                                      'Kate McKinnon']}],
                     'q9': 'Barbie',
                     'q10': ['Margot Robbie', 'Ryan Gosling', 'Issa Rae', 'Kate McKinnon'],
                     'q11': ['Greta Gerwig'],
                     'q12': [{'title': 'Bad Night',
                              'year': 2015,
                              'duration': 92,
                              'genres': ['Adventure', 'Comedy', 'Crime'],
                              'rating': 4.9,
                              'directors': ['Chris Riedell', 'Nick Riedell'],
                              'cast': ['Lauren Elizabeth',
                                       'Jenn McAllister',
                                       'Julianna Guill',
                                       'Judy Marte']},
                             {'title': 'Operation Camel',
                              'year': 1960,
                              'duration': 100,
                              'genres': ['Comedy'],
                              'rating': 5.7,
                              'directors': ['Sven Methling'],
                              'cast': ['Paul Hagen',
                                       'Louis Miehe-Renard',
                                       'Ebbe Langberg',
                                       'Preben Kaas']},
                             {'title': 'True Story',
                              'year': 2015,
                              'duration': 99,
                              'genres': ['Biography', 'Crime', 'Drama'],
                              'rating': 6.3,
                              'directors': ['Rupert Goold'],
                              'cast': ['James Franco',
                                       'Jonah Hill',
                                       'Felicity Jones',
                                       'Maria Dizzia']},
                             {'title': 'The Death of Louis XIV',
                              'year': 2016,
                              'duration': 115,
                              'genres': ['Biography', 'Drama', 'History'],
                              'rating': 6.8,
                              'directors': ['Albert Serra'],
                              'cast': ['Jean-Pierre Léaud',
                                       "Patrick d'Assumçao",
                                       'Marc Susini',
                                       'Bernard Belin']},
                             {'title': 'Olga',
                              'year': 2021,
                              'duration': 85,
                              'genres': ['Drama', 'Sport'],
                              'rating': 6.8,
                              'directors': ['Elie Grappe'],
                              'cast': ['Anastasiia Budiashkina',
                                       'Sabrina Rubtsova',
                                       'Caterina Barloggio',
                                       'Théa Brogli']},
                             {'title': 'Solitary Fragments',
                              'year': 2007,
                              'duration': 135,
                              'genres': ['Drama'],
                              'rating': 6.6,
                              'directors': ['Jaime Rosales'],
                              'cast': ['Sonia Almarcha',
                                       'Petra Martínez',
                                       'Miriam Correa',
                                       'Nuria Mencía']},
                             {'title': 'My Blue Heaven',
                              'year': 1950,
                              'duration': 96,
                              'genres': ['Drama', 'Musical'],
                              'rating': 6.2,
                              'directors': ['Henry Koster'],
                              'cast': ['Betty Grable', 'Dan Dailey', 'David Wayne', 'Jane Wyatt']},
                             {'title': 'The Crocodiles',
                              'year': 2009,
                              'duration': 98,
                              'genres': ['Adventure', 'Family'],
                              'rating': 6.2,
                              'directors': ['Christian Ditter'],
                              'cast': ['Nick Romeo Reimann',
                                       'Fabian Halbig',
                                       'Leonie Tepe',
                                       'Manuel Steitz']},
                             {'title': 'White Wolves: A Cry in the Wild II',
                              'year': 1993,
                              'duration': 90,
                              'genres': ['Action', 'Adventure', 'Family'],
                              'rating': 5.7,
                              'directors': ['Catherine Cyran'],
                              'cast': ['Matt McCoy',
                                       'David Moscow',
                                       'Mark-Paul Gosselaar',
                                       'Ami Dolenz']},
                             {'title': "Devil's Town",
                              'year': 2009,
                              'duration': 82,
                              'genres': ['Comedy', 'Drama'],
                              'rating': 5.7,
                              'directors': ['Vladimir Paskaljevic'],
                              'cast': ['Lazar Ristovski',
                                       'Danica Ristovski',
                                       'Marija Zeljkovic',
                                       'Mina Colic']},
                             {'title': 'Balkan Brothers',
                              'year': 2005,
                              'duration': 87,
                              'genres': ['Comedy', 'Drama'],
                              'rating': 5.9,
                              'directors': ["Bozidar 'Bota' Nikolic"],
                              'cast': ['Isidora Minic',
                                       'Svetozar Cvetkovic',
                                       'Goran Susljik',
                                       'Petar Bozovic']},
                             {'title': 'Shadow Builder',
                              'year': 1998,
                              'duration': 101,
                              'genres': ['Action', 'Horror', 'Thriller'],
                              'rating': 4.8,
                              'directors': ['Jamie Dixon'],
                              'cast': ['Michael Rooker',
                                       'Leslie Hope',
                                       'Shawn Thompson',
                                       'Andrew Jackson']},
                             {'title': 'Gordy',
                              'year': 1994,
                              'duration': 90,
                              'genres': ['Comedy', 'Drama', 'Family'],
                              'rating': 3.7,
                              'directors': ['Mark Lewis'],
                              'cast': ['Kristy Young',
                                       'Doug Stone',
                                       'James Donadio',
                                       'Deborah Hobart']},
                             {'title': 'The Zoo',
                              'year': 1967,
                              'duration': 125,
                              'genres': ['Crime', 'Drama', 'Mystery'],
                              'rating': 7.2,
                              'directors': ['Satyajit Ray'],
                              'cast': ['Uttam Kumar',
                                       'Kalipada Chakraborty',
                                       'Nripati Chatterjee',
                                       'Shekhar Chatterjee']},
                             {'title': 'Miami Heat',
                              'year': 2021,
                              'duration': 87,
                              'genres': ['Action', 'Crime', 'Drama'],
                              'rating': 4.1,
                              'directors': ['Fabio W. Silva', 'Zack Matthews'],
                              'cast': ['Oleg Prudius',
                                       'Shannon Murray',
                                       'Gabriela Wong',
                                       'Olivier Richters']},
                             {'title': 'Nostos: The Return',
                              'year': 1989,
                              'duration': 85,
                              'genres': ['Adventure', 'History'],
                              'rating': 7.8,
                              'directors': ['Franco Piavoli'],
                              'cast': ['Luigi Mezzanotte',
                                       'Branca de Camargo',
                                       'Alex Carozzo',
                                       'Paola Agosti']},
                             {'title': 'Groom',
                              'year': 2016,
                              'duration': 90,
                              'genres': ['Comedy'],
                              'rating': 4.3,
                              'directors': ['Aleksandr Nezlobin'],
                              'cast': ['Sergey Svetlakov',
                                       'Philippe Reinhardt',
                                       'Svetlana Smirnova-Martsinkevich',
                                       'Olga Kartunkova']},
                             {'title': 'The Lookout',
                              'year': 2007,
                              'duration': 99,
                              'genres': ['Crime', 'Drama', 'Thriller'],
                              'rating': 7.0,
                              'directors': ['Scott Frank'],
                              'cast': ['Joseph Gordon-Levitt',
                                       'Jeff Daniels',
                                       'Matthew Goode',
                                       'Isla Fisher']}],
                     'q13': 1179,
                     'q14': [{'title': 'The Wrong Man',
                              'year': 1956,
                              'duration': 105,
                              'genres': ['Drama', 'Film-Noir'],
                              'rating': 7.4,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Henry Fonda',
                                       'Vera Miles',
                                       'Anthony Quayle',
                                       'Harold J. Stone']},
                             {'title': 'Lifeboat',
                              'year': 1944,
                              'duration': 97,
                              'genres': ['Drama', 'War'],
                              'rating': 7.6,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Tallulah Bankhead',
                                       'John Hodiak',
                                       'Walter Slezak',
                                       'William Bendix']},
                             {'title': 'Young and Innocent',
                              'year': 1937,
                              'duration': 80,
                              'genres': ['Crime', 'Mystery', 'Romance'],
                              'rating': 6.8,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Nova Pilbeam',
                                       'Derrick De Marney',
                                       'Percy Marmont',
                                       'Edward Rigby']},
                             {'title': 'Marnie',
                              'year': 1964,
                              'duration': 130,
                              'genres': ['Crime', 'Drama', 'Mystery'],
                              'rating': 7.1,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Tippi Hedren',
                                       'Sean Connery',
                                       'Martin Gabel',
                                       'Louise Latham']},
                             {'title': 'I Confess',
                              'year': 1953,
                              'duration': 95,
                              'genres': ['Crime', 'Drama', 'Thriller'],
                              'rating': 7.2,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Montgomery Clift',
                                       'Anne Baxter',
                                       'Karl Malden',
                                       'Brian Aherne']},
                             {'title': 'Shadow of a Doubt',
                              'year': 1943,
                              'duration': 108,
                              'genres': ['Film-Noir', 'Thriller'],
                              'rating': 7.8,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Teresa Wright',
                                       'Joseph Cotten',
                                       'Macdonald Carey',
                                       'Henry Travers']},
                             {'title': 'Torn Curtain',
                              'year': 1966,
                              'duration': 128,
                              'genres': ['Drama', 'Romance', 'Thriller'],
                              'rating': 6.6,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Paul Newman',
                                       'Julie Andrews',
                                       'Lila Kedrova',
                                       'Hansjörg Felmy']},
                             {'title': 'East of Shanghai',
                              'year': 1931,
                              'duration': 110,
                              'genres': ['Comedy', 'Drama', 'Romance'],
                              'rating': 5.7,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Henry Kendall',
                                       'Joan Barry',
                                       'Percy Marmont',
                                       'Betty Amann']},
                             {'title': 'Number 17',
                              'year': 1932,
                              'duration': 66,
                              'genres': ['Crime', 'Mystery', 'Thriller'],
                              'rating': 5.7,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Leon M. Lion',
                                       'Anne Grey',
                                       'John Stuart',
                                       'Donald Calthrop']},
                             {'title': 'The Manxman',
                              'year': 1929,
                              'duration': 110,
                              'genres': ['Drama', 'Romance'],
                              'rating': 6.2,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Clare Greet',
                                       'Anny Ondra',
                                       'Carl Brisson',
                                       'Malcolm Keen',
                                       'Randle Ayrton']},
                             {'title': 'To Catch a Thief',
                              'year': 1955,
                              'duration': 106,
                              'genres': ['Mystery', 'Romance', 'Thriller'],
                              'rating': 7.4,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Cary Grant',
                                       'Grace Kelly',
                                       'Jessie Royce Landis',
                                       'John Williams']},
                             {'title': 'Blackmail',
                              'year': 1929,
                              'duration': 85,
                              'genres': ['Crime', 'Drama', 'Thriller'],
                              'rating': 6.9,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Anny Ondra',
                                       'John Longden',
                                       'Sara Allgood',
                                       'Charles Paton']},
                             {'title': 'North by Northwest',
                              'year': 1959,
                              'duration': 136,
                              'genres': ['Action', 'Adventure', 'Mystery'],
                              'rating': 8.3,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Cary Grant',
                                       'Eva Marie Saint',
                                       'James Mason',
                                       'Jessie Royce Landis']},
                             {'title': 'The Trouble with Harry',
                              'year': 1955,
                              'duration': 99,
                              'genres': ['Comedy', 'Mystery'],
                              'rating': 7.0,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['John Forsythe',
                                       'Shirley MacLaine',
                                       'Edmund Gwenn',
                                       'Mildred Natwick']},
                             {'title': 'Topaz',
                              'year': 1969,
                              'duration': 143,
                              'genres': ['Drama', 'Thriller'],
                              'rating': 6.2,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Frederick Stafford',
                                       'Dany Robin',
                                       'John Vernon',
                                       'Karin Dor']},
                             {'title': 'The Pleasure Garden',
                              'year': 1925,
                              'duration': 75,
                              'genres': ['Drama', 'Romance'],
                              'rating': 5.8,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Virginia Valli',
                                       'Carmelita Geraghty',
                                       'Miles Mander',
                                       'John Stuart']},
                             {'title': 'The 39 Steps',
                              'year': 1935,
                              'duration': 86,
                              'genres': ['Crime', 'Mystery', 'Thriller'],
                              'rating': 7.6,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Robert Donat',
                                       'Madeleine Carroll',
                                       'Lucie Mannheim',
                                       'Godfrey Tearle']},
                             {'title': 'Mr. & Mrs. Smith',
                              'year': 1941,
                              'duration': 95,
                              'genres': ['Comedy', 'Romance'],
                              'rating': 6.3,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Philip Merivale',
                                       'Carole Lombard',
                                       'Robert Montgomery',
                                       'Gene Raymond',
                                       'Jack Carson']},
                             {'title': 'Stage Fright',
                              'year': 1950,
                              'duration': 110,
                              'genres': ['Film-Noir', 'Mystery', 'Thriller'],
                              'rating': 7.0,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Marlene Dietrich',
                                       'Jane Wyman',
                                       'Richard Todd',
                                       'Michael Wilding']},
                             {'title': 'The Ring',
                              'year': 1927,
                              'duration': 116,
                              'genres': ['Drama', 'Romance', 'Sport'],
                              'rating': 6.1,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Carl Brisson',
                                       'Lillian Hall-Davis',
                                       'Ian Hunter',
                                       'Forrester Harvey',
                                       'Harry Terry',
                                       'Gordon Harker']},
                             {'title': 'Under Capricorn',
                              'year': 1949,
                              'duration': 117,
                              'genres': ['Crime', 'Drama', 'Romance'],
                              'rating': 6.2,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Ingrid Bergman',
                                       'Joseph Cotten',
                                       'Michael Wilding',
                                       'Margaret Leighton']},
                             {'title': 'Frenzy',
                              'year': 1972,
                              'duration': 116,
                              'genres': ['Thriller'],
                              'rating': 7.4,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Jon Finch',
                                       'Barry Foster',
                                       'Barbara Leigh-Hunt',
                                       'Anna Massey']},
                             {'title': 'Juno and the Paycock',
                              'year': 1929,
                              'duration': 85,
                              'genres': ['Comedy', 'Drama'],
                              'rating': 4.6,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Sara Allgood',
                                       'Edward Chapman',
                                       'Barry Fitzgerald',
                                       "Maire O'Neill"]},
                             {'title': 'Jamaica Inn',
                              'year': 1939,
                              'duration': 108,
                              'genres': ['Adventure', 'Crime'],
                              'rating': 6.3,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ["Maureen O'Hara",
                                       'Robert Newton',
                                       'Charles Laughton',
                                       'Horace Hodges']},
                             {'title': 'Dial M for Murder',
                              'year': 1954,
                              'duration': 105,
                              'genres': ['Crime', 'Thriller'],
                              'rating': 8.2,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Ray Milland',
                                       'Grace Kelly',
                                       'Robert Cummings',
                                       'John Williams']},
                             {'title': 'Foreign Correspondent',
                              'year': 1940,
                              'duration': 120,
                              'genres': ['Action', 'Romance', 'Thriller'],
                              'rating': 7.4,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Joel McCrea',
                                       'Laraine Day',
                                       'Herbert Marshall',
                                       'George Sanders']},
                             {'title': "Strauss' Great Waltz",
                              'year': 1934,
                              'duration': 81,
                              'genres': ['Biography', 'Music', 'Romance'],
                              'rating': 5.8,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Edmund Gwenn',
                                       'Esmond Knight',
                                       'Jessie Matthews',
                                       'Fay Compton']},
                             {'title': 'Saboteur',
                              'year': 1942,
                              'duration': 109,
                              'genres': ['Thriller', 'War'],
                              'rating': 7.1,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Priscilla Lane',
                                       'Robert Cummings',
                                       'Otto Kruger',
                                       'Alan Baxter']},
                             {'title': 'Champagne',
                              'year': 1928,
                              'duration': 86,
                              'genres': ['Comedy'],
                              'rating': 5.4,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Vivian Gibson',
                                       'Betty Balfour',
                                       'Jean Bradin',
                                       'Ferdinand von Alten',
                                       'Gordon Harker',
                                       "Alexander D'Arcy"]},
                             {'title': 'Strangers on a Train',
                              'year': 1951,
                              'duration': 101,
                              'genres': ['Crime', 'Drama', 'Film-Noir'],
                              'rating': 7.9,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Farley Granger',
                                       'Robert Walker',
                                       'Ruth Roman',
                                       'Leo G. Carroll']},
                             {'title': 'The Man Who Knew Too Much',
                              'year': 1934,
                              'duration': 75,
                              'genres': ['Crime', 'Mystery', 'Thriller'],
                              'rating': 6.7,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Leslie Banks', 'Edna Best', 'Peter Lorre', 'Frank Vosper']},
                             {'title': 'The Paradine Case',
                              'year': 1947,
                              'duration': 125,
                              'genres': ['Crime', 'Drama', 'Romance'],
                              'rating': 6.5,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Gregory Peck',
                                       'Ann Todd',
                                       'Charles Laughton',
                                       'Charles Coburn']},
                             {'title': 'Secret Agent',
                              'year': 1936,
                              'duration': 86,
                              'genres': ['Mystery', 'Thriller'],
                              'rating': 6.4,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['John Gielgud',
                                       'Madeleine Carroll',
                                       'Robert Young',
                                       'Peter Lorre']},
                             {'title': 'Psycho',
                              'year': 1960,
                              'duration': 109,
                              'genres': ['Horror', 'Mystery', 'Thriller'],
                              'rating': 8.5,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Anthony Perkins',
                                       'Janet Leigh',
                                       'Vera Miles',
                                       'John Gavin']},
                             {'title': 'Sabotage',
                              'year': 1936,
                              'duration': 76,
                              'genres': ['Crime', 'Thriller'],
                              'rating': 7.0,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Sylvia Sidney',
                                       'Oscar Homolka',
                                       'Desmond Tester',
                                       'John Loder']},
                             {'title': 'Murder!',
                              'year': 1930,
                              'duration': 104,
                              'genres': ['Crime', 'Mystery', 'Thriller'],
                              'rating': 6.3,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Herbert Marshall',
                                       'Norah Baring',
                                       'Phyllis Konstam',
                                       'Edward Chapman']},
                             {'title': 'The Skin Game',
                              'year': 1931,
                              'duration': 85,
                              'genres': ['Drama'],
                              'rating': 5.7,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Edmund Gwenn', 'Jill Esmond', 'C.V. France', 'Helen Haye']},
                             {'title': 'Downhill',
                              'year': 1927,
                              'duration': 80,
                              'genres': ['Adventure', 'Drama', 'Thriller'],
                              'rating': 6.0,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Ivor Novello',
                                       'Ben Webster',
                                       'Norman McKinnel',
                                       'Robin Irvine']},
                             {'title': 'Vertigo',
                              'year': 1958,
                              'duration': 128,
                              'genres': ['Mystery', 'Romance', 'Thriller'],
                              'rating': 8.3,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['James Stewart',
                                       'Kim Novak',
                                       'Barbara Bel Geddes',
                                       'Tom Helmore']},
                             {'title': 'Spellbound',
                              'year': 1945,
                              'duration': 111,
                              'genres': ['Film-Noir', 'Mystery', 'Romance'],
                              'rating': 7.5,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Ingrid Bergman',
                                       'Gregory Peck',
                                       'Michael Chekhov',
                                       'Leo G. Carroll']},
                             {'title': 'Rebecca',
                              'year': 1940,
                              'duration': 130,
                              'genres': ['Drama', 'Film-Noir', 'Mystery'],
                              'rating': 8.1,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Laurence Olivier',
                                       'Joan Fontaine',
                                       'George Sanders',
                                       'Judith Anderson']},
                             {'title': 'Notorious',
                              'year': 1946,
                              'duration': 102,
                              'genres': ['Drama', 'Film-Noir', 'Romance'],
                              'rating': 7.9,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Cary Grant',
                                       'Ingrid Bergman',
                                       'Claude Rains',
                                       'Louis Calhern']},
                             {'title': 'Suspicion',
                              'year': 1941,
                              'duration': 99,
                              'genres': ['Film-Noir', 'Mystery', 'Thriller'],
                              'rating': 7.3,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Cary Grant',
                                       'Joan Fontaine',
                                       'Cedric Hardwicke',
                                       'Nigel Bruce']},
                             {'title': 'Easy Virtue',
                              'year': 1927,
                              'duration': 80,
                              'genres': ['Romance', 'Thriller'],
                              'rating': 5.5,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Violet Farebrother',
                                       'Isabel Jeans',
                                       'Franklin Dyall',
                                       'Eric Bransby Williams',
                                       'Ian Hunter',
                                       'Robin Irvine']},
                             {'title': 'The Lodger: A Story of the London Fog',
                              'year': 1927,
                              'duration': 92,
                              'genres': ['Crime', 'Drama', 'Mystery'],
                              'rating': 7.3,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['June Tripp',
                                       'Ivor Novello',
                                       'Marie Ault',
                                       'Arthur Chesney']},
                             {'title': 'Rear Window',
                              'year': 1954,
                              'duration': 112,
                              'genres': ['Mystery', 'Thriller'],
                              'rating': 8.5,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['James Stewart',
                                       'Grace Kelly',
                                       'Wendell Corey',
                                       'Thelma Ritter']},
                             {'title': 'Mary',
                              'year': 1931,
                              'duration': 78,
                              'genres': ['Mystery', 'Thriller'],
                              'rating': 5.7,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Alfred Abel',
                                       'Olga Tschechowa',
                                       'Paul Graetz',
                                       'Lotte Stein']},
                             {'title': 'Family Plot',
                              'year': 1976,
                              'duration': 120,
                              'genres': ['Comedy', 'Crime', 'Drama'],
                              'rating': 6.8,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Karen Black',
                                       'Bruce Dern',
                                       'Barbara Harris',
                                       'William Devane']},
                             {'title': 'The Man Who Knew Too Much',
                              'year': 1956,
                              'duration': 120,
                              'genres': ['Drama', 'Thriller'],
                              'rating': 7.4,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['James Stewart',
                                       'Doris Day',
                                       'Brenda de Banzie',
                                       'Bernard Miles']},
                             {'title': 'The Lady Vanishes',
                              'year': 1938,
                              'duration': 96,
                              'genres': ['Mystery', 'Thriller'],
                              'rating': 7.7,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Margaret Lockwood',
                                       'Michael Redgrave',
                                       'Paul Lukas',
                                       'May Whitty']},
                             {'title': "The Farmer's Wife",
                              'year': 1928,
                              'duration': 100,
                              'genres': ['Comedy', 'Drama', 'Romance'],
                              'rating': 5.8,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Jameson Thomas',
                                       'Lillian Hall-Davis',
                                       'Gordon Harker',
                                       'Gibb McLaughlin']},
                             {'title': 'Rope',
                              'year': 1948,
                              'duration': 80,
                              'genres': ['Crime', 'Drama', 'Mystery'],
                              'rating': 7.9,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['James Stewart',
                                       'John Dall',
                                       'Farley Granger',
                                       'Dick Hogan']},
                             {'title': 'Elstree Calling',
                              'year': 1930,
                              'duration': 86,
                              'genres': ['Comedy', 'Musical'],
                              'rating': 5.0,
                              'directors': ['André Charlot',
                                            'Jack Hulbert',
                                            'Paul Murray',
                                            'Alfred Hitchcock'],
                              'cast': ['Gordon Begg', 'Helen Burnell']},
                             {'title': 'The Birds',
                              'year': 1963,
                              'duration': 119,
                              'genres': ['Drama', 'Horror', 'Mystery'],
                              'rating': 7.6,
                              'directors': ['Alfred Hitchcock'],
                              'cast': ['Rod Taylor',
                                       'Tippi Hedren',
                                       'Jessica Tandy',
                                       'Suzanne Pleshette']}],
                     'q15': [{'title': 'Once Upon a Time in Mumbaai',
                              'year': 2010,
                              'duration': 134,
                              'genres': ['Action', 'Crime', 'Drama'],
                              'rating': 7.4,
                              'directors': ['Milan Luthria'],
                              'cast': ['Ajay Devgn',
                                       'Emraan Hashmi',
                                       'Kangana Ranaut',
                                       'Prachi Desai']},
                             {'title': 'Once Upon a Time in Deadwood',
                              'year': 2019,
                              'duration': 85,
                              'genres': ['Action', 'Western'],
                              'rating': 3.0,
                              'directors': ['Rene Perez'],
                              'cast': ['Robert Bronzi',
                                       'Michael Paré',
                                       'Karin Brauns',
                                       'Lauren Compton']},
                             {'title': 'Once Upon a Time in China II',
                              'year': 1992,
                              'duration': 113,
                              'genres': ['Action', 'Adventure', 'Biography'],
                              'rating': 7.3,
                              'directors': ['Hark Tsui'],
                              'cast': ['Jet Li', 'Rosamund Kwan', 'Siu Chung Mok', 'David Chiang']},
                             {'title': 'Once Upon a Time in High School: The Spirit of Jeet Kune '
                                       'Do',
                              'year': 2004,
                              'duration': 116,
                              'genres': ['Action', 'Drama', 'History'],
                              'rating': 7.4,
                              'directors': ['Ha Yoo'],
                              'cast': ['Sang-woo Kwon',
                                       'Lee Jung-Jin',
                                       'Ga-in Han',
                                       'Hyo-jun Park']},
                             {'title': 'Once Upon a Time in China III',
                              'year': 1992,
                              'duration': 125,
                              'genres': ['Action', 'Adventure', 'Biography'],
                              'rating': 6.7,
                              'directors': ['Hark Tsui'],
                              'cast': ['Jet Li',
                                       'Rosamund Kwan',
                                       'Siu Chung Mok',
                                       'Xin Xin Xiong']},
                             {'title': 'Once Upon a Time in Hollywood',
                              'year': 2019,
                              'duration': 161,
                              'genres': ['Comedy', 'Drama'],
                              'rating': 7.6,
                              'directors': ['Quentin Tarantino'],
                              'cast': ['Leonardo DiCaprio',
                                       'Brad Pitt',
                                       'Margot Robbie',
                                       'Emile Hirsch']},
                             {'title': 'Once Upon a Time in China and America',
                              'year': 1997,
                              'duration': 102,
                              'genres': ['Action', 'Adventure', 'History'],
                              'rating': 6.3,
                              'directors': ['Sammo Kam-Bo Hung'],
                              'cast': ['Jet Li',
                                       'Rosamund Kwan',
                                       'Xin Xin Xiong',
                                       'Kwok-Pong Chan']},
                             {'title': 'Once Upon a Time in Anatolia',
                              'year': 2011,
                              'duration': 157,
                              'genres': ['Crime', 'Drama', 'Thriller'],
                              'rating': 7.8,
                              'directors': ['Nuri Bilge Ceylan'],
                              'cast': ['Muhammet Uzuner',
                                       'Yilmaz Erdogan',
                                       'Taner Birsel',
                                       'Ahmet Mümtaz Taylan']},
                             {'title': 'Once Upon a Time in China V',
                              'year': 1994,
                              'duration': 101,
                              'genres': ['Action', 'Drama'],
                              'rating': 5.9,
                              'directors': ['Hark Tsui'],
                              'cast': ['Wenzhuo Zhao',
                                       'Rosamund Kwan',
                                       'Siu Chung Mok',
                                       'Kent Cheng']},
                             {'title': 'Once Upon a Time in Mumbaai Dobara',
                              'year': 2013,
                              'duration': 160,
                              'genres': ['Action', 'Crime', 'Drama'],
                              'rating': 4.4,
                              'directors': ['Milan Luthria'],
                              'cast': ['Akshay Kumar',
                                       'Imran Khan',
                                       'Sonakshi Sinha',
                                       'Sonali Bendre']},
                             {'title': 'Once Upon a Time in Brooklyn',
                              'year': 2013,
                              'duration': 116,
                              'genres': ['Action', 'Crime'],
                              'rating': 3.8,
                              'directors': ['Paul Borghese'],
                              'cast': ['Armand Assante',
                                       'William DeMeo',
                                       'Cathy Moriarty',
                                       'Ice-T']},
                             {'title': 'Once Upon a Time in the West',
                              'year': 1968,
                              'duration': 165,
                              'genres': ['Western'],
                              'rating': 8.5,
                              'directors': ['Sergio Leone'],
                              'cast': ['Henry Fonda',
                                       'Charles Bronson',
                                       'Claudia Cardinale',
                                       'Jason Robards']},
                             {'title': 'Once Upon a Time in Phuket',
                              'year': 2011,
                              'duration': 105,
                              'genres': ['Comedy', 'Romance'],
                              'rating': 5.7,
                              'directors': ['Staffan Lindberg'],
                              'cast': ['Peter Magnusson',
                                       'Susanne Thorson',
                                       'Jenny Skavlan',
                                       'David Hellenius']},
                             {'title': 'Once Upon a Time in Mexico',
                              'year': 2003,
                              'duration': 102,
                              'genres': ['Action', 'Crime', 'Thriller'],
                              'rating': 6.3,
                              'directors': ['Robert Rodriguez'],
                              'cast': ['Antonio Banderas',
                                       'Salma Hayek',
                                       'Johnny Depp',
                                       'Willem Dafoe']},
                             {'title': 'Once Upon a Time in the Battlefield',
                              'year': 2003,
                              'duration': 104,
                              'genres': ['Comedy'],
                              'rating': 5.7,
                              'directors': ['Joon-ik Lee'],
                              'cast': ['Joong-Hoon Park',
                                       'Jin-young Jung',
                                       'Ji-myeong Oh',
                                       'Kim Seon-a']},
                             {'title': 'Once Upon a Time in America',
                              'year': 1984,
                              'duration': 229,
                              'genres': ['Crime', 'Drama'],
                              'rating': 8.3,
                              'directors': ['Sergio Leone'],
                              'cast': ['Robert De Niro',
                                       'James Woods',
                                       'Elizabeth McGovern',
                                       'Treat Williams']},
                             {'title': 'Once Upon a Time in Queens',
                              'year': 2013,
                              'duration': 98,
                              'genres': ['Comedy', 'Drama'],
                              'rating': 6.1,
                              'directors': ['David Rodriguez'],
                              'cast': ['Paul Sorvino',
                                       'Michael Rapaport',
                                       'Renee Props',
                                       'Andrea Nittoli Kelly']},
                             {'title': 'Once Upon a Time in London',
                              'year': 2019,
                              'duration': 111,
                              'genres': ['Crime', 'History'],
                              'rating': 5.2,
                              'directors': ['Simon Rumley'],
                              'cast': ['Terry Stone',
                                       'Andy Beckwith',
                                       'Josh Myers',
                                       'Christopher Dunne']},
                             {'title': 'Once Upon a Time in Shanghai',
                              'year': 2014,
                              'duration': 96,
                              'genres': ['Action', 'Crime'],
                              'rating': 6.7,
                              'directors': ['Ching-Po Wong'],
                              'cast': ['Sammo Kam-Bo Hung',
                                       'Andy On',
                                       'Philip Ng',
                                       'Kuan Tai Chen']},
                             {'title': 'Once Upon a Time in the Midlands',
                              'year': 2002,
                              'duration': 104,
                              'genres': ['Comedy', 'Drama', 'Romance'],
                              'rating': 6.1,
                              'directors': ['Shane Meadows'],
                              'cast': ['Robert Carlyle',
                                       'Rhys Ifans',
                                       'Kathy Burke',
                                       'Vanessa Feltz']},
                             {'title': 'Once Upon a Time in Ukraine',
                              'year': 2020,
                              'duration': 90,
                              'genres': ['Action', 'Adventure', 'Comedy'],
                              'rating': 6.9,
                              'directors': ['Roman Perfilyev'],
                              'cast': ['Roman Lutskyi',
                                       'Sergey Strelnikov',
                                       'Kateryna Slyusar',
                                       'Gen Seto']},
                             {'title': 'Once Upon a Time in China IV',
                              'year': 1993,
                              'duration': 101,
                              'genres': ['Action'],
                              'rating': 5.9,
                              'directors': ['Bun Yuen'],
                              'cast': ['Wenzhuo Zhao',
                                       'Jean Wang',
                                       'Siu Chung Mok',
                                       'Xin Xin Xiong']},
                             {'title': 'Once Upon a Time in China',
                              'year': 1991,
                              'duration': 134,
                              'genres': ['Action', 'Adventure', 'Drama'],
                              'rating': 7.2,
                              'directors': ['Hark Tsui'],
                              'cast': ['Jet Li', 'Rosamund Kwan', 'Biao Yuen', 'Jacky Cheung']},
                             {'title': 'Once Upon a Time in Venice',
                              'year': 2017,
                              'duration': 94,
                              'genres': ['Action', 'Adventure', 'Comedy'],
                              'rating': 5.3,
                              'directors': ['Mark Cullen'],
                              'cast': ['Bruce Willis',
                                       'John Goodman',
                                       'Jason Momoa',
                                       'Emily Robinson']},
                             {'title': 'Once Upon a Time in Euskadi',
                              'year': 2021,
                              'duration': 100,
                              'genres': ['Drama'],
                              'rating': 6.1,
                              'directors': ['Manu Gómez'],
                              'cast': ['Asier Flores',
                                       'Aitor Calderón',
                                       'Miguel Rivera',
                                       'Hugo García']},
                             {'title': 'Lagaan: Once Upon a Time in India',
                              'year': 2001,
                              'duration': 224,
                              'genres': ['Drama', 'Musical', 'Sport'],
                              'rating': 8.1,
                              'directors': ['Ashutosh Gowariker'],
                              'cast': ['Aamir Khan',
                                       'Raghubir Yadav',
                                       'Gracy Singh',
                                       'Rachel Shelley']},
                             {'title': 'Once Upon a Time in the North',
                              'year': 2012,
                              'duration': 128,
                              'genres': ['Drama', 'History'],
                              'rating': 6.1,
                              'directors': ['Jukka-Pekka Siili'],
                              'cast': ['Lauri Tilkanen',
                                       'Mikko Leppilampi',
                                       'Pamela Tola',
                                       'Aku Hirviniemi']},
                             {'title': 'Once Upon a Time in Hong Kong',
                              'year': 2021,
                              'duration': 105,
                              'genres': ['Action', 'Crime', 'History'],
                              'rating': 5.5,
                              'directors': ['Woody Hui Yan', 'Jing Wong'],
                              'cast': ['Louis Koo',
                                       'Tony Ka Fai Leung',
                                       'Francis Ng',
                                       'Ka-Tung Lam']}],
                     'q16': 24,
                     'q17': 1011,
                     'q18': ['The Hour of the Furnaces',
                             'September 11: The New Pearl Harbor',
                             'The Cure for Insomnia',
                             'At Berkeley',
                             '16 Days of Glory',
                             'Route One USA'],
                     'q19': 'Drama',
                     'q20': ['Srini Hanumantharaju', 'Srini', 'Chris Delforce']}
    return expected_json


def get_special_json():
    """get_special_json() returns a dict mapping each question to the expected
    answer stored in a special format as a list of tuples. Each tuple contains
    the element expected in the list, and its corresponding value. Any two
    elements with the same value can appear in any order in the actual list,
    but if two elements have different values, then they must appear in the
    same order as in the expected list of tuples."""
    special_json = {}
    return special_json


def compare(expected, actual, q_format=TEXT_FORMAT):
    """compare(expected, actual) is used to compare when the format of
    the expected answer is known for certain."""
    try:
        if q_format == TEXT_FORMAT:
            return simple_compare(expected, actual)
        elif q_format == TEXT_FORMAT_UNORDERED_LIST:
            return list_compare_unordered(expected, actual)
        elif q_format == TEXT_FORMAT_ORDERED_LIST:
            return list_compare_ordered(expected, actual)
        elif q_format == TEXT_FORMAT_DICT:
            return dict_compare(expected, actual)
        elif q_format == TEXT_FORMAT_SPECIAL_ORDERED_LIST:
            return list_compare_special(expected, actual)
        elif q_format == TEXT_FORMAT_NAMEDTUPLE:
            return namedtuple_compare(expected, actual)
        elif q_format == PNG_FORMAT_SCATTER:
            return compare_flip_dicts(expected, actual)
        elif q_format == HTML_FORMAT:
            return compare_cell_html(expected, actual)
        elif q_format == FILE_JSON_FORMAT:
            return compare_json(expected, actual)
        else:
            if expected != actual:
                return "expected %s but found %s " % (repr(expected), repr(actual))
    except:
        if expected != actual:
            return "expected %s" % (repr(expected))
    return PASS


def print_message(expected, actual, complete_msg=True):
    """print_message(expected, actual) displays a simple error message."""
    msg = "expected %s" % (repr(expected))
    if complete_msg:
        msg = msg + " but found %s" % (repr(actual))
    return msg


def simple_compare(expected, actual, complete_msg=True):
    """simple_compare(expected, actual) is used to compare when the expected answer
    is a type/Nones/str/int/float/bool. When the expected answer is a float,
    the actual answer is allowed to be within the tolerance limit. Otherwise,
    the values must match exactly, or a very simple error message is displayed."""
    msg = PASS
    if 'numpy' in repr(type((actual))):
        actual = actual.item()
    if isinstance(expected, type):
        if expected != actual:
            if isinstance(actual, type):
                msg = "expected %s but found %s" % (expected.__name__, actual.__name__)
            else:
                msg = "expected %s but found %s" % (expected.__name__, repr(actual))
    elif not isinstance(actual, type(expected)) and not (isinstance(expected, (float, int)) and isinstance(actual, (float, int))):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
    elif isinstance(expected, float):
        if not math.isclose(actual, expected, rel_tol=REL_TOL, abs_tol=ABS_TOL):
            msg = print_message(expected, actual, complete_msg)
    elif isinstance(expected, (list, tuple)) or is_namedtuple(expected):
        new_msg = print_message(expected, actual, complete_msg)
        if len(expected) != len(actual):
            return new_msg
        for i in range(len(expected)):
            val = simple_compare(expected[i], actual[i])
            if val != PASS:
                return new_msg
    elif isinstance(expected, dict):
        new_msg = print_message(expected, actual, complete_msg)
        if len(expected) != len(actual):
            return new_msg
        val = simple_compare(list(expected.keys()), list(actual.keys()))
        if val != PASS:
            return new_msg
        for key in expected:
            val = simple_compare(expected[key], actual[key])
            if val != PASS:
                return new_msg
    else:
        if expected != actual:
            msg = print_message(expected, actual, complete_msg)
    return msg


def intelligent_compare(expected, actual, obj=None):
    """intelligent_compare(expected, actual) is used to compare when the
    data type of the expected answer is not known for certain, and default
    assumptions  need to be made."""
    if obj == None:
        obj = type(expected).__name__
    if is_namedtuple(expected):
        msg = namedtuple_compare(expected, actual)
    elif isinstance(expected, (list, tuple)):
        msg = list_compare_ordered(expected, actual, obj)
    elif isinstance(expected, set):
        msg = list_compare_unordered(expected, actual, obj)
    elif isinstance(expected, (dict)):
        msg = dict_compare(expected, actual)
    else:
        msg = simple_compare(expected, actual)
    msg = msg.replace("CompDict", "dict").replace("CompSet", "set").replace("NewNone", "None")
    return msg


def is_namedtuple(obj, init_check=True):
    """is_namedtuple(obj) returns True if `obj` is a namedtuple object
    defined in the test file."""
    bases = type(obj).__bases__
    if len(bases) != 1 or bases[0] != tuple:
        return False
    fields = getattr(type(obj), '_fields', None)
    if not isinstance(fields, tuple):
        return False
    if init_check and not type(obj).__name__ in [nt.__name__ for nt in _expected_namedtuples]:
        return False
    return True


def list_compare_ordered(expected, actual, obj=None):
    """list_compare_ordered(expected, actual) is used to compare when the
    expected answer is a list/tuple, where the order of the elements matters."""
    msg = PASS
    if not isinstance(actual, type(expected)):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    if obj == None:
        obj = type(expected).__name__
    for i in range(len(expected)):
        if i >= len(actual):
            msg = "at index %d of the %s, expected missing %s" % (i, obj, repr(expected[i]))
            break
        val = intelligent_compare(expected[i], actual[i], "sub" + obj)
        if val != PASS:
            msg = "at index %d of the %s, " % (i, obj) + val
            break
    if len(actual) > len(expected) and msg == PASS:
        msg = "at index %d of the %s, found unexpected %s" % (len(expected), obj, repr(actual[len(expected)]))
    if len(expected) != len(actual):
        msg = msg + " (found %d entries in %s, but expected %d)" % (len(actual), obj, len(expected))

    if len(expected) > 0:
        try:
            if msg != PASS and list_compare_unordered(expected, actual, obj) == PASS:
                msg = msg + " (%s may not be ordered as required)" % (obj)
        except:
            pass
    return msg


def list_compare_helper(larger, smaller):
    """list_compare_helper(larger, smaller) is a helper function which takes in
    two lists of possibly unequal sizes and finds the item that is not present
    in the smaller list, if there is such an element."""
    msg = PASS
    j = 0
    for i in range(len(larger)):
        if i == len(smaller):
            msg = "expected %s" % (repr(larger[i]))
            break
        found = False
        while not found:
            if j == len(smaller):
                val = simple_compare(larger[i], smaller[j - 1], complete_msg=False)
                break
            val = simple_compare(larger[i], smaller[j], complete_msg=False)
            j += 1
            if val == PASS:
                found = True
                break
        if not found:
            msg = val
            break
    return msg

class NewNone():
    """alternate class in place of None, which allows for comparison with
    all other data types."""
    def __str__(self):
        return 'None'
    def __repr__(self):
        return 'None'
    def __lt__(self, other):
        return True
    def __le__(self, other):
        return True
    def __gt__(self, other):
        return False
    def __ge__(self, other):
        return other == None
    def __eq__(self, other):
        return other == None
    def __ne__(self, other):
        return other != None

class CompDict(dict):
    """subclass of dict, which allows for comparison with other dicts."""
    def __init__(self, vals):
        super(self.__class__, self).__init__(vals)
        if type(vals) == CompDict:
            self.val = vals.val
        elif isinstance(vals, dict):
            self.val = self.get_equiv(vals)
        else:
            raise TypeError("'%s' object cannot be type casted to CompDict class" % type(vals).__name__)

    def get_equiv(self, vals):
        val = []
        for key in sorted(list(vals.keys())):
            val.append((key, vals[key]))
        return val

    def __str__(self):
        return str(dict(self.val))
    def __repr__(self):
        return repr(dict(self.val))
    def __lt__(self, other):
        return self.val < CompDict(other).val
    def __le__(self, other):
        return self.val <= CompDict(other).val
    def __gt__(self, other):
        return self.val > CompDict(other).val
    def __ge__(self, other):
        return self.val >= CompDict(other).val
    def __eq__(self, other):
        return self.val == CompDict(other).val
    def __ne__(self, other):
        return self.val != CompDict(other).val

class CompSet(set):
    """subclass of set, which allows for comparison with other sets."""
    def __init__(self, vals):
        super(self.__class__, self).__init__(vals)
        if type(vals) == CompSet:
            self.val = vals.val
        elif isinstance(vals, set):
            self.val = self.get_equiv(vals)
        else:
            raise TypeError("'%s' object cannot be type casted to CompSet class" % type(vals).__name__)

    def get_equiv(self, vals):
        return sorted(list(vals))

    def __str__(self):
        return str(set(self.val))
    def __repr__(self):
        return repr(set(self.val))
    def __getitem__(self, index):
        return self.val[index]
    def __lt__(self, other):
        return self.val < CompSet(other).val
    def __le__(self, other):
        return self.val <= CompSet(other).val
    def __gt__(self, other):
        return self.val > CompSet(other).val
    def __ge__(self, other):
        return self.val >= CompSet(other).val
    def __eq__(self, other):
        return self.val == CompSet(other).val
    def __ne__(self, other):
        return self.val != CompSet(other).val

def make_sortable(item):
    """make_sortable(item) replaces all Nones in `item` with an alternate
    class that allows for comparison with str/int/float/bool/list/set/tuple/dict.
    It also replaces all dicts (and sets) with a subclass that allows for
    comparison with other dicts (and sets)."""
    if item == None:
        return NewNone()
    elif isinstance(item, (type, str, int, float, bool)):
        return item
    elif isinstance(item, (list, set, tuple)):
        new_item = []
        for subitem in item:
            new_item.append(make_sortable(subitem))
        if is_namedtuple(item):
            return type(item)(*new_item)
        elif isinstance(item, set):
            return CompSet(new_item)
        else:
            return type(item)(new_item)
    elif isinstance(item, dict):
        new_item = {}
        for key in item:
            new_item[key] = make_sortable(item[key])
        return CompDict(new_item)
    return item

def list_compare_unordered(expected, actual, obj=None):
    """list_compare_unordered(expected, actual) is used to compare when the
    expected answer is a list/set where the order of the elements does not matter."""
    msg = PASS
    if not isinstance(actual, type(expected)):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    if obj == None:
        obj = type(expected).__name__

    try:
        sort_expected = sorted(make_sortable(expected))
        sort_actual = sorted(make_sortable(actual))
    except:
        return "unexpected datatype found in %s; expected entries of type %s" % (obj, obj, type(expected[0]).__name__)

    if len(actual) == 0 and len(expected) > 0:
        msg = "in the %s, missing " % (obj) + sort_expected[0]
    elif len(actual) > 0 and len(expected) > 0:
        val = intelligent_compare(sort_expected[0], sort_actual[0])
        if val.startswith("expected to find type"):
            msg = "in the %s, " % (obj) + simple_compare(sort_expected[0], sort_actual[0])
        else:
            if len(expected) > len(actual):
                msg = "in the %s, missing " % (obj) + list_compare_helper(sort_expected, sort_actual)
            elif len(expected) < len(actual):
                msg = "in the %s, found un" % (obj) + list_compare_helper(sort_actual, sort_expected)
            if len(expected) != len(actual):
                msg = msg + " (found %d entries in %s, but expected %d)" % (len(actual), obj, len(expected))
                return msg
            else:
                val = list_compare_helper(sort_expected, sort_actual)
                if val != PASS:
                    msg = "in the %s, missing " % (obj) + val + ", but found un" + list_compare_helper(sort_actual,
                                                                                               sort_expected)
    return msg


def namedtuple_compare(expected, actual):
    """namedtuple_compare(expected, actual) is used to compare when the
    expected answer is a namedtuple defined in the test file."""
    msg = PASS
    if is_namedtuple(actual, False):
        msg = "expected namedtuple but found %s" % (type(actual).__name__)
        return msg
    if type(expected).__name__ != type(actual).__name__:
        return "expected namedtuple %s but found namedtuple %s" % (type(expected).__name__, type(actual).__name__)
    expected_fields = expected._fields
    actual_fields = actual._fields
    msg = list_compare_ordered(list(expected_fields), list(actual_fields), "namedtuple attributes")
    if msg != PASS:
        return msg
    for field in expected_fields:
        val = intelligent_compare(getattr(expected, field), getattr(actual, field))
        if val != PASS:
            msg = "at attribute %s of namedtuple %s, " % (field, type(expected).__name__) + val
            return msg
    return msg


def clean_slashes(item):
    """clean_slashes()"""
    if isinstance(item, str):
        return item.replace("\\", "/").replace("/", os.path.sep)
    elif item == None or isinstance(item, (type, int, float, bool)):
        return item
    elif isinstance(item, (list, tuple, set)) or is_namedtuple(item):
        new_item = []
        for subitem in item:
            new_item.append(clean_slashes(subitem))
        if is_namedtuple(item):
            return type(item)(*new_item)
        else:
            return type(item)(new_item)
    elif isinstance(item, dict):
        new_item = {}
        for key in item:
            new_item[clean_slashes(key)] = clean_slashes(item[key])
        return item


def list_compare_special_initialize(special_expected):
    """list_compare_special_initialize(special_expected) takes in the special
    ordering stored as a sorted list of items, and returns a list of lists
    where the ordering among the inner lists does not matter."""
    latest_val = None
    clean_special = []
    for row in special_expected:
        if latest_val == None or row[1] != latest_val:
            clean_special.append([])
            latest_val = row[1]
        clean_special[-1].append(row[0])
    return clean_special


def list_compare_special(special_expected, actual):
    """list_compare_special(special_expected, actual) is used to compare when the
    expected answer is a list with special ordering defined in `special_expected`."""
    msg = PASS
    expected_list = []
    special_order = list_compare_special_initialize(special_expected)
    for expected_item in special_order:
        expected_list.extend(expected_item)
    val = list_compare_unordered(expected_list, actual)
    if val != PASS:
        return val
    i = 0
    for expected_item in special_order:
        j = len(expected_item)
        actual_item = actual[i: i + j]
        val = list_compare_unordered(expected_item, actual_item)
        if val != PASS:
            if j == 1:
                msg = "at index %d " % (i) + val
            else:
                msg = "between indices %d and %d " % (i, i + j - 1) + val
            msg = msg + " (list may not be ordered as required)"
            break
        i += j
    return msg


def dict_compare(expected, actual, obj=None):
    """dict_compare(expected, actual) is used to compare when the expected answer
    is a dict."""
    msg = PASS
    if not isinstance(actual, type(expected)):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    if obj == None:
        obj = type(expected).__name__

    expected_keys = list(expected.keys())
    actual_keys = list(actual.keys())
    val = list_compare_unordered(expected_keys, actual_keys, obj)

    if val != PASS:
        msg = "bad keys in %s: " % (obj) + val
    if msg == PASS:
        for key in expected:
            new_obj = None
            if isinstance(expected[key], (list, tuple, set)):
                new_obj = 'value'
            elif isinstance(expected[key], dict):
                new_obj = 'sub' + obj
            val = intelligent_compare(expected[key], actual[key], new_obj)
            if val != PASS:
                msg = "incorrect value for key %s in %s: " % (repr(key), obj) + val
    return msg


def is_flippable(item):
    """is_flippable(item) determines if the given dict of lists has lists of the
    same length and is therefore flippable."""
    item_lens = set(([str(len(item[key])) for key in item]))
    if len(item_lens) == 1:
        return PASS
    else:
        return "found lists of lengths %s" % (", ".join(list(item_lens)))

def flip_dict_of_lists(item):
    """flip_dict_of_lists(item) flips a dict of lists into a list of dicts if the
    lists are of same length."""
    new_item = []
    length = len(list(item.values())[0])
    for i in range(length):
        new_dict = {}
        for key in item:
            new_dict[key] = item[key][i]
        new_item.append(new_dict)
    return new_item

def compare_flip_dicts(expected, actual, obj="lists"):
    """compare_flip_dicts(expected, actual) flips a dict of lists (or dicts) into
    a list of dicts (or dict of dicts) and then compares the list ignoring order."""
    msg = PASS
    example_item = list(expected.values())[0]
    if isinstance(example_item, (list, tuple)):
        val = is_flippable(actual)
        if val != PASS:
            msg = "expected to find lists of length %d, but " % (len(example_item)) + val
            return msg
        msg = list_compare_unordered(flip_dict_of_lists(expected), flip_dict_of_lists(actual), "lists")
    elif isinstance(example_item, dict):
        expected_keys = list(example_item.keys())
        for key in actual:
            val = list_compare_unordered(expected_keys, list(actual[key].keys()), "dictionary %s" % key)
            if val != PASS:
                return val
        for cat_key in expected_keys:
            expected_category = {}
            actual_category = {}
            for key in expected:
                expected_category[key] = expected[key][cat_key]
                actual_category[key] = actual[key][cat_key]
            val = list_compare_unordered(flip_dict_of_lists(expected), flip_dict_of_lists(actual), "category " + repr(cat_key))
            if val != PASS:
                return val
    return msg


def get_expected_tables():
    """get_expected_tables() reads the html file with the expected DataFrames
    and returns a dict mapping each question to a html table."""
    if not os.path.exists(DF_FILE):
        return None

    expected_tables = {}
    f = open(DF_FILE, encoding='utf-8')
    soup = BeautifulSoup(f.read(), 'html.parser')
    f.close()

    tables = soup.find_all('table')
    for table in tables:
        expected_tables[table.get("data-question")] = table

    return expected_tables

def parse_df_html_table(table):
    """parse_df_html_table(table) takes in a table as a html string and returns
    a dict mapping each row and column index to the value at that position."""
    rows = []
    for tr in table.find_all('tr'):
        rows.append([])
        for cell in tr.find_all(['td', 'th']):
            rows[-1].append(cell.get_text().strip("\n "))

    cells = {}
    for r in range(1, len(rows)):
        for c in range(1, len(rows[0])):
            rname = rows[r][0]
            cname = rows[0][c]
            cells[(rname,cname)] = rows[r][c]
    return cells


def get_expected_namedtuples():
    """get_expected_namedtuples() defines the required namedtuple objects
    globally. It also returns a tuple of the classes."""
    expected_namedtuples = []
    
    return tuple(expected_namedtuples)

_expected_namedtuples = get_expected_namedtuples()


def compare_cell_html(expected, actual):
    """compare_cell_html(expected, actual) is used to compare when the
    expected answer is a DataFrame stored in the `expected_dfs` html file."""
    expected_cells = parse_df_html_table(expected)
    try:
        actual_cells = parse_df_html_table(BeautifulSoup(actual, 'html.parser').find('table'))
    except Exception as e:
        return "expected to find type DataFrame but found type %s instead" % type(actual).__name__

    expected_cols = list(set(["column %s" % (loc[1]) for loc in expected_cells]))
    actual_cols = list(set(["column %s" % (loc[1]) for loc in actual_cells]))
    msg = list_compare_unordered(expected_cols, actual_cols, "DataFrame")
    if msg != PASS:
        return msg

    expected_rows = list(set(["row index %s" % (loc[0]) for loc in expected_cells]))
    actual_rows = list(set(["row index %s" % (loc[0]) for loc in actual_cells]))
    msg = list_compare_unordered(expected_rows, actual_rows, "DataFrame")
    if msg != PASS:
        return msg

    for location, expected in expected_cells.items():
        location_name = "column {} at index {}".format(location[1], location[0])
        actual = actual_cells.get(location, None)
        if actual == None:
            return "in %s, expected to find %s" % (location_name, repr(expected))
        try:
            actual_ans = float(actual)
            expected_ans = float(expected)
            if math.isnan(actual_ans) and math.isnan(expected_ans):
                continue
        except Exception as e:
            actual_ans, expected_ans = actual, expected
        msg = simple_compare(expected_ans, actual_ans)
        if msg != PASS:
            return "in %s, " % location_name + msg
    return PASS


def get_expected_plots():
    """get_expected_plots() reads the json file with the expected plot data
    and returns a dict mapping each question to a dictionary with the plots data."""
    if not os.path.exists(PLOT_FILE):
        return None

    f = open(PLOT_FILE, encoding='utf-8')
    expected_plots = json.load(f)
    f.close()
    return expected_plots


def compare_file_json(expected, actual):
    """compare_file_json(expected, actual) is used to compare when the
    expected answer is a JSON file."""
    msg = PASS
    if not os.path.isfile(expected):
        return "file %s not found; make sure it is downloaded and stored in the correct directory" % (expected)
    elif not os.path.isfile(actual):
        return "file %s not found; make sure that you have created the file with the correct name" % (actual)
    try:
        e = open(expected, encoding='utf-8')
        expected_data = json.load(e)
        e.close()
    except json.JSONDecodeError:
        return "file %s is broken and cannot be parsed; please delete and redownload the file correctly" % (expected)
    try:
        a = open(actual, encoding='utf-8')
        actual_data = json.load(a)
        a.close()
    except json.JSONDecodeError:
        return "file %s is broken and cannot be parsed" % (actual)
    if type(expected_data) == list:
        msg = list_compare_ordered(expected_data, actual_data, 'file ' + actual)
    elif type(expected_data) == dict:
        msg = dict_compare(expected_data, actual_data)
    return msg


_expected_json = get_expected_json()
_special_json = get_special_json()
_expected_plots = get_expected_plots()
_expected_tables = get_expected_tables()
_expected_format = get_expected_format()

def check(qnum, actual):
    """check(qnum, actual) is used to check if the answer in the notebook is
    the correct answer, and provide useful feedback if the answer is incorrect."""
    msg = PASS
    error_msg = "<b style='color: red;'>ERROR:</b> "
    q_format = _expected_format[qnum]

    if q_format == TEXT_FORMAT_SPECIAL_ORDERED_LIST:
        expected = _special_json[qnum]
    elif q_format == PNG_FORMAT_SCATTER:
        if _expected_plots == None:
            msg = error_msg + "file %s not parsed; make sure it is downloaded and stored in the correct directory" % (PLOT_FILE)
        else:
            expected = _expected_plots[qnum]
    elif q_format == HTML_FORMAT:
        if _expected_tables == None:
            msg = error_msg + "file %s not parsed; make sure it is downloaded and stored in the correct directory" % (DF_FILE)
        else:
            expected = _expected_tables[qnum]
    else:
        expected = _expected_json[qnum]

    if SLASHES in q_format:
        q_format = q_format.replace(SLASHES, "")
        expected = clean_slashes(expected)
        actual = clean_slashes(actual)

    if msg != PASS:
        print(msg)
    else:
        msg = compare(expected, actual, q_format)
        if msg != PASS:
            msg = error_msg + msg
        print(msg)


def check_file_size(path):
    """check_file_size(path) throws an error if the file is too big to display
    on Gradescope."""
    size = os.path.getsize(path)
    assert size < MAX_FILE_SIZE * 10**3, "Your file is too big to be displayed by Gradescope; please delete unnecessary output cells so your file size is < %s KB" % MAX_FILE_SIZE


def reset_hidden_tests():
    """reset_hidden_tests() resets all hidden tests on the Gradescope autograder where the hidden test file exists"""
    if not os.path.exists(HIDDEN_FILE):
        return
    hidn.reset_hidden_tests()

def rubric_check(rubric_point, ignore_past_errors=True):
    """rubric_check(rubric_point) uses the hidden test file on the Gradescope autograder to grade the `rubric_point`"""
    if not os.path.exists(HIDDEN_FILE):
        print(PASS)
        return
    error_msg_1 = "ERROR: "
    error_msg_2 = "TEST DETAILS: "
    try:
        msg = hidn.rubric_check(rubric_point, ignore_past_errors)
    except:
        msg = "hidden tests crashed before execution"
    if msg != PASS:
        hidn.make_deductions(rubric_point)
        if msg == "public tests failed":
            comment = "The public tests have failed, so you will not receive any points for this question."
            comment += "\nPlease confirm that the public tests pass locally before submitting."
        elif msg == "answer is hardcoded":
            comment = "In the datasets for testing hardcoding, all numbers are replaced with random values."
            comment += "\nIf the answer is the same as in the original dataset for all these datasets"
            comment += "\ndespite this, that implies that the answer in the notebook is hardcoded."
            comment += "\nYou will not receive any points for this question."
        else:
            comment = hidn.get_comment(rubric_point)
        msg = error_msg_1 + msg
        if comment != "":
            msg = msg + "\n" + error_msg_2 + comment
    print(msg)

def get_summary():
    """get_summary() returns the summary of the notebook using the hidden test file on the Gradescope autograder"""
    if not os.path.exists(HIDDEN_FILE):
        print("Total Score: %d/%d" % (TOTAL_SCORE, TOTAL_SCORE))
        return
    score = min(TOTAL_SCORE, hidn.get_score(TOTAL_SCORE))
    display_msg = "Total Score: %d/%d" % (score, TOTAL_SCORE)
    if score != TOTAL_SCORE:
        display_msg += "\n" + hidn.get_deduction_string()
    print(display_msg)

def get_score_digit(digit):
    """get_score_digit(digit) returns the `digit` of the score using the hidden test file on the Gradescope autograder"""
    if not os.path.exists(HIDDEN_FILE):
        score = TOTAL_SCORE
    else:
        score = hidn.get_score(TOTAL_SCORE)
    digits = bin(score)[2:]
    digits = "0"*(7 - len(digits)) + digits
    return int(digits[6 - digit])
