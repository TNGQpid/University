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
TOTAL_SCORE = 50 # total score for the project

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
    expected_format = {'q1': 'TEXT_FORMAT',
                       'q2': 'TEXT_FORMAT_UNORDERED_LIST',
                       'q3': 'TEXT_FORMAT_ORDERED_LIST',
                       'q4': 'TEXT_FORMAT_DICT',
                       'q5': 'TEXT_FORMAT_DICT',
                       'q6': 'TEXT_FORMAT_DICT',
                       'q7': 'TEXT_FORMAT_DICT',
                       'q8': 'TEXT_FORMAT_SPECIAL_ORDERED_LIST',
                       'q9': 'TEXT_FORMAT_SPECIAL_ORDERED_LIST',
                       'q10': 'TEXT_FORMAT_UNORDERED_LIST'}
    return expected_format


def get_expected_json():
    """get_expected_json() returns a dict mapping each question to the expected
    answer (if the format permits it)."""
    expected_json = {'q1': 8.2,
                     'q2': [{'title': 'Toy Story',
                             'year': 1995,
                             'duration': 81,
                             'genres': ['Adventure', 'Animation', 'Comedy'],
                             'rating': 8.3,
                             'directors': ['John Lasseter'],
                             'cast': ['Tom Hanks', 'Tim Allen', 'Don Rickles', 'Jim Varney']},
                            {'title': 'Toy Story 3',
                             'year': 2010,
                             'duration': 103,
                             'genres': ['Adventure', 'Animation', 'Comedy'],
                             'rating': 8.3,
                             'directors': ['Lee Unkrich'],
                             'cast': ['Tom Hanks', 'Tim Allen', 'Joan Cusack', 'Ned Beatty']}],
                     'q3': [{'title': 'Goodbye Christopher Robin',
                             'year': 2017,
                             'duration': 107,
                             'genres': ['Biography', 'Drama', 'Family'],
                             'rating': 7.1,
                             'directors': ['Simon Curtis'],
                             'cast': ['Domhnall Gleeson',
                                      'Margot Robbie',
                                      'Kelly Macdonald',
                                      'Vicki Pepperdine']},
                            {'title': 'The Wolf of Wall Street',
                             'year': 2013,
                             'duration': 180,
                             'genres': ['Biography', 'Comedy', 'Crime'],
                             'rating': 8.2,
                             'directors': ['Martin Scorsese'],
                             'cast': ['Leonardo DiCaprio',
                                      'Jonah Hill',
                                      'Margot Robbie',
                                      'Matthew McConaughey']},
                            {'title': 'Suite Française',
                             'year': 2014,
                             'duration': 107,
                             'genres': ['Drama', 'Romance', 'Thriller'],
                             'rating': 7.0,
                             'directors': ['Saul Dibb'],
                             'cast': ['Michelle Williams',
                                      'Kristin Scott Thomas',
                                      'Margot Robbie',
                                      'Eric Godon']},
                            {'title': 'I, Tonya',
                             'year': 2017,
                             'duration': 119,
                             'genres': ['Biography', 'Comedy', 'Drama'],
                             'rating': 7.5,
                             'directors': ['Craig Gillespie'],
                             'cast': ['Margot Robbie',
                                      'Sebastian Stan',
                                      'Allison Janney',
                                      'Julianne Nicholson']},
                            {'title': 'Whiskey Tango Foxtrot',
                             'year': 2016,
                             'duration': 112,
                             'genres': ['Biography', 'Comedy', 'Drama'],
                             'rating': 6.6,
                             'directors': ['Glenn Ficarra', 'John Requa'],
                             'cast': ['Tina Fey',
                                      'Margot Robbie',
                                      'Martin Freeman',
                                      'Alfred Molina']},
                            {'title': 'Focus',
                             'year': 2015,
                             'duration': 105,
                             'genres': ['Comedy', 'Crime', 'Drama'],
                             'rating': 6.6,
                             'directors': ['Glenn Ficarra', 'John Requa'],
                             'cast': ['Will Smith',
                                      'Margot Robbie',
                                      'Rodrigo Santoro',
                                      'Adrian Martinez']},
                            {'title': 'Dreamland',
                             'year': 2019,
                             'duration': 98,
                             'genres': ['Drama', 'Thriller', 'Western'],
                             'rating': 5.9,
                             'directors': ['Miles Joris-Peyrafitte'],
                             'cast': ['Finn Cole',
                                      'Margot Robbie',
                                      'Travis Fimmel',
                                      'Kerry Condon']},
                            {'title': 'Terminal',
                             'year': 2018,
                             'duration': 95,
                             'genres': ['Action', 'Comedy', 'Crime'],
                             'rating': 5.3,
                             'directors': ['Vaughn Stein'],
                             'cast': ['Margot Robbie',
                                      'Simon Pegg',
                                      'Dexter Fletcher',
                                      'Mike Myers']},
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
                            {'title': 'I.C.U.',
                             'year': 2009,
                             'duration': 85,
                             'genres': ['Horror', 'Thriller'],
                             'rating': 2.5,
                             'directors': ['Aash Aaron'],
                             'cast': ['Margot Robbie',
                                      'Christian Radford',
                                      'James Dean',
                                      'Natalie Hoflin']},
                            {'title': 'Babylon',
                             'year': 2022,
                             'duration': 189,
                             'genres': ['Comedy', 'Drama', 'History'],
                             'rating': 7.1,
                             'directors': ['Damien Chazelle'],
                             'cast': ['Brad Pitt', 'Margot Robbie', 'Jean Smart', 'Olivia Wilde']},
                            {'title': 'Suicide Squad',
                             'year': 2016,
                             'duration': 123,
                             'genres': ['Action', 'Adventure', 'Fantasy'],
                             'rating': 5.9,
                             'directors': ['David Ayer'],
                             'cast': ['Will Smith', 'Jared Leto', 'Margot Robbie', 'Viola Davis']},
                            {'title': 'Mary Queen of Scots',
                             'year': 2018,
                             'duration': 124,
                             'genres': ['Biography', 'Drama', 'History'],
                             'rating': 6.3,
                             'directors': ['Josie Rourke'],
                             'cast': ['Saoirse Ronan',
                                      'Margot Robbie',
                                      'Jack Lowden',
                                      'Joe Alwyn']},
                            {'title': 'Z for Zachariah',
                             'year': 2015,
                             'duration': 98,
                             'genres': ['Drama', 'Romance', 'Sci-Fi'],
                             'rating': 6.0,
                             'directors': ['Craig Zobel'],
                             'cast': ['Chiwetel Ejiofor', 'Chris Pine', 'Margot Robbie']},
                            {'title': 'Bombshell',
                             'year': 2019,
                             'duration': 109,
                             'genres': ['Biography', 'Drama'],
                             'rating': 6.8,
                             'directors': ['Jay Roach'],
                             'cast': ['Charlize Theron',
                                      'Nicole Kidman',
                                      'Margot Robbie',
                                      'John Lithgow']},
                            {'title': 'Amsterdam',
                             'year': 2022,
                             'duration': 134,
                             'genres': ['Comedy', 'Drama', 'History'],
                             'rating': 6.1,
                             'directors': ['David O. Russell'],
                             'cast': ['Christian Bale',
                                      'Margot Robbie',
                                      'John David Washington',
                                      'Alessandro Nivola']},
                            {'title': 'The Suicide Squad',
                             'year': 2021,
                             'duration': 132,
                             'genres': ['Action', 'Adventure', 'Comedy'],
                             'rating': 7.2,
                             'directors': ['James Gunn'],
                             'cast': ['Margot Robbie', 'Idris Elba', 'John Cena', 'Joel Kinnaman']},
                            {'title': 'Vigilante',
                             'year': 2008,
                             'duration': 90,
                             'genres': ['Action'],
                             'rating': 2.6,
                             'directors': ['Aash Aaron'],
                             'cast': ['Robert Díaz',
                                      'Kazuya Wright',
                                      'Lexie Symon',
                                      'Margot Robbie']},
                            {'title': 'Barbie',
                             'year': 2023,
                             'duration': 114,
                             'genres': ['Adventure', 'Comedy', 'Fantasy'],
                             'rating': 7.1,
                             'directors': ['Greta Gerwig'],
                             'cast': ['Margot Robbie',
                                      'Ryan Gosling',
                                      'Issa Rae',
                                      'Kate McKinnon']},
                            {'title': 'Birds of Prey',
                             'year': 2020,
                             'duration': 109,
                             'genres': ['Action', 'Comedy', 'Crime'],
                             'rating': 6.1,
                             'directors': ['Cathy Yan'],
                             'cast': ['Margot Robbie',
                                      'Rosie Perez',
                                      'Mary Elizabeth Winstead',
                                      'Jurnee Smollett']}],
                     'q4': {'Drama': 40806,
                            'Thriller': 10749,
                            'Action': 11813,
                            'Crime': 10583,
                            'Comedy': 24336,
                            'Adventure': 7037,
                            'Family': 3443,
                            'Sci-Fi': 3336,
                            'Romance': 12354,
                            'Biography': 2507,
                            'War': 1868,
                            'History': 2238,
                            'Fantasy': 3533,
                            'Horror': 9127,
                            'Mystery': 5413,
                            'Animation': 2067,
                            'Documentary': 1334,
                            'Music': 1627,
                            'Musical': 1537,
                            'Western': 1283,
                            'Film-Noir': 666,
                            'Sport': 1105,
                            'News': 22,
                            'Reality-TV': 2},
                     'q5': {'Crime': 3,
                            'Drama': 9,
                            'Film-Noir': 2,
                            'Horror': 1,
                            'Adventure': 3,
                            'War': 5,
                            'Comedy': 1,
                            'Thriller': 2,
                            'Mystery': 1,
                            'Sci-Fi': 2,
                            'Biography': 1},
                     'q6': {'2011 to 2020': 1100,
                            '1961 to 1970': 201,
                            '1911 to 1920': 6,
                            '1981 to 1990': 383,
                            '1951 to 1960': 198,
                            '1941 to 1950': 24,
                            '1991 to 2000': 389,
                            '2021 to 2030': 242,
                            '2001 to 2010': 517,
                            '1971 to 1980': 243,
                            '1931 to 1940': 28,
                            '1921 to 1930': 5},
                     'q7': {'Action': 8.0,
                            'Sci-Fi': 8.25,
                            'Adventure': 7.75,
                            'Fantasy': 7.75,
                            'Drama': 7.7,
                            'Mystery': 7.5,
                            'Comedy': 7.3,
                            'Thriller': 5.55,
                            'Horror': 3.8,
                            'Romance': 7.9},
                     'q10': ['William Wyler',
                             'P. Padmarajan',
                             'Christopher Nolan',
                             'Masaki Kobayashi',
                             'Satyajit Ray',
                             'Jean-Pierre Melville',
                             'Quentin Tarantino',
                             'Akira Kurosawa',
                             'Singeetam Srinivasa Rao',
                             'Theodoros Angelopoulos',
                             'Martin Scorsese',
                             'Yoshikazu Yasuhiko',
                             'Sibi Malayil',
                             'S.S. Rajamouli',
                             'Ertem Egilmez',
                             'Hayao Miyazaki',
                             'Preston Sturges',
                             'Ingmar Bergman',
                             'Georgiy Daneliya',
                             'Sergiu Nicolaescu',
                             'S. Shankar',
                             'Stanley Kubrick',
                             'Shyam Benegal',
                             'Michael Cacoyannis',
                             'K. Balachander',
                             'Gulzar',
                             'Krzysztof Kieslowski',
                             'Yasujirô Ozu',
                             'Oldrich Lipský',
                             'Mani Ratnam',
                             'Rituparno Ghosh',
                             'Nikita Mikhalkov',
                             'Goran Markovic',
                             'Bahram Beyzaie',
                             'David Fincher']}
    return expected_json


def get_special_json():
    """get_special_json() returns a dict mapping each question to the expected
    answer stored in a special format as a list of tuples. Each tuple contains
    the element expected in the list, and its corresponding value. Any two
    elements with the same value can appear in any order in the actual list,
    but if two elements have different values, then they must appear in the
    same order as in the expected list of tuples."""
    special_json = {'q8': [('Sci-Fi', 8.25),
                           ('Action', 8.0),
                           ('Romance', 7.9),
                           ('Adventure', 7.75),
                           ('Fantasy', 7.75),
                           ('Drama', 7.7),
                           ('Mystery', 7.5),
                           ('Comedy', 7.3),
                           ('Thriller', 5.55),
                           ('Horror', 3.8)],
                    'q9': [({'title': 'Mean Streets',
                             'year': 1973,
                             'duration': 112,
                             'genres': ['Crime', 'Drama', 'Thriller'],
                             'rating': 7.2,
                             'directors': ['Martin Scorsese'],
                             'cast': ['Robert De Niro',
                                      'Harvey Keitel',
                                      'David Proval',
                                      'Amy Robinson']},
                            1973),
                           ({'title': 'Taxi Driver',
                             'year': 1976,
                             'duration': 114,
                             'genres': ['Crime', 'Drama'],
                             'rating': 8.2,
                             'directors': ['Martin Scorsese'],
                             'cast': ['Robert De Niro',
                                      'Jodie Foster',
                                      'Cybill Shepherd',
                                      'Albert Brooks']},
                            1976),
                           ({'title': 'New York, New York',
                             'year': 1977,
                             'duration': 155,
                             'genres': ['Drama', 'Music', 'Musical'],
                             'rating': 6.6,
                             'directors': ['Martin Scorsese'],
                             'cast': ['Liza Minnelli',
                                      'Robert De Niro',
                                      'Lionel Stander',
                                      'Barry Primus']},
                            1977),
                           ({'title': 'Raging Bull',
                             'year': 1980,
                             'duration': 129,
                             'genres': ['Biography', 'Drama', 'Sport'],
                             'rating': 8.1,
                             'directors': ['Martin Scorsese'],
                             'cast': ['Robert De Niro',
                                      'Cathy Moriarty',
                                      'Joe Pesci',
                                      'Frank Vincent']},
                            1980),
                           ({'title': 'The King of Comedy',
                             'year': 1982,
                             'duration': 109,
                             'genres': ['Comedy', 'Crime', 'Drama'],
                             'rating': 7.8,
                             'directors': ['Martin Scorsese'],
                             'cast': ['Robert De Niro',
                                      'Jerry Lewis',
                                      'Diahnne Abbott',
                                      'Sandra Bernhard']},
                            1982),
                           ({'title': 'Goodfellas',
                             'year': 1990,
                             'duration': 145,
                             'genres': ['Biography', 'Crime', 'Drama'],
                             'rating': 8.7,
                             'directors': ['Martin Scorsese'],
                             'cast': ['Robert De Niro',
                                      'Ray Liotta',
                                      'Joe Pesci',
                                      'Lorraine Bracco']},
                            1990),
                           ({'title': 'Cape Fear',
                             'year': 1991,
                             'duration': 128,
                             'genres': ['Crime', 'Thriller'],
                             'rating': 7.3,
                             'directors': ['Martin Scorsese'],
                             'cast': ['Robert De Niro',
                                      'Nick Nolte',
                                      'Jessica Lange',
                                      'Juliette Lewis']},
                            1991),
                           ({'title': 'Casino',
                             'year': 1995,
                             'duration': 178,
                             'genres': ['Crime', 'Drama'],
                             'rating': 8.2,
                             'directors': ['Martin Scorsese'],
                             'cast': ['Robert De Niro',
                                      'Sharon Stone',
                                      'Joe Pesci',
                                      'James Woods']},
                            1995),
                           ({'title': 'The Irishman',
                             'year': 2019,
                             'duration': 209,
                             'genres': ['Biography', 'Crime', 'Drama'],
                             'rating': 7.8,
                             'directors': ['Martin Scorsese'],
                             'cast': ['Robert De Niro',
                                      'Al Pacino',
                                      'Joe Pesci',
                                      'Harvey Keitel']},
                            2019),
                           ({'title': 'Killers of the Flower Moon',
                             'year': 2023,
                             'duration': 206,
                             'genres': ['Crime', 'Drama', 'History'],
                             'rating': 9.0,
                             'directors': ['Martin Scorsese'],
                             'cast': ['Leonardo DiCaprio',
                                      'Robert De Niro',
                                      'Lily Gladstone',
                                      'Jesse Plemons']},
                            2023)]}
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
    elif not isinstance(actual, type(expected)):
        if not (isinstance(expected, (float, int)) and isinstance(actual, (float, int))):
            if not is_namedtuple(expected):
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
        val = list_compare_unordered(list(expected.keys()), list(actual.keys()))
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
    if not is_namedtuple(actual, False):
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
        q_format = q_format.replace(SLASHES, "").strip("_ ")
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
