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
SLASHES = "SLASHES" # question SUFFIX when expected answer contains paths with slashes

def get_expected_format():
    """get_expected_format() returns a dict mapping each question to the format
    of the expected answer."""
    expected_format = {'q1': 'TEXT_FORMAT_ORDERED_LIST',
                       'q2': 'TEXT_FORMAT_ORDERED_LIST_SLASHES',
                       'q3': 'TEXT_FORMAT_ORDERED_LIST_SLASHES',
                       'q4': 'TEXT_FORMAT_ORDERED_LIST_SLASHES',
                       'Star': 'TEXT_FORMAT_NAMEDTUPLE',
                       'q5': 'TEXT_FORMAT_NAMEDTUPLE',
                       'q6': 'TEXT_FORMAT_NAMEDTUPLE',
                       'q7': 'TEXT_FORMAT',
                       'q8': 'TEXT_FORMAT',
                       'q9': 'TEXT_FORMAT',
                       'q10': 'TEXT_FORMAT',
                       'q11': 'TEXT_FORMAT',
                       'Planet': 'TEXT_FORMAT_NAMEDTUPLE',
                       'q12': 'TEXT_FORMAT_NAMEDTUPLE',
                       'q13': 'TEXT_FORMAT_ORDERED_LIST',
                       'q14': 'TEXT_FORMAT_ORDERED_LIST',
                       'q15': 'TEXT_FORMAT_ORDERED_LIST',
                       'q16': 'TEXT_FORMAT_ORDERED_LIST',
                       'q17': 'TEXT_FORMAT',
                       'q18': 'TEXT_FORMAT_NAMEDTUPLE',
                       'q19': 'TEXT_FORMAT',
                       'q20': 'TEXT_FORMAT_UNORDERED_LIST'}
    return expected_format


def get_expected_json():
    """get_expected_json() returns a dict mapping each question to the expected
    answer (if the format permits it)."""
    expected_json = {'q1': ['stars_5.csv',
                            'stars_4.csv',
                            'stars_3.csv',
                            'stars_2.csv',
                            'stars_1.csv',
                            'planets_5.csv',
                            'planets_4.csv',
                            'planets_3.csv',
                            'planets_2.csv',
                            'planets_1.csv',
                            'mapping_5.json',
                            'mapping_4.json',
                            'mapping_3.json',
                            'mapping_2.json',
                            'mapping_1.json'],
                     'q2': ['data\\stars_5.csv',
                            'data\\stars_4.csv',
                            'data\\stars_3.csv',
                            'data\\stars_2.csv',
                            'data\\stars_1.csv',
                            'data\\planets_5.csv',
                            'data\\planets_4.csv',
                            'data\\planets_3.csv',
                            'data\\planets_2.csv',
                            'data\\planets_1.csv',
                            'data\\mapping_5.json',
                            'data\\mapping_4.json',
                            'data\\mapping_3.json',
                            'data\\mapping_2.json',
                            'data\\mapping_1.json'],
                     'q3': ['data\\stars_5.csv',
                            'data\\stars_4.csv',
                            'data\\stars_3.csv',
                            'data\\stars_2.csv',
                            'data\\stars_1.csv',
                            'data\\planets_5.csv',
                            'data\\planets_4.csv',
                            'data\\planets_3.csv',
                            'data\\planets_2.csv',
                            'data\\planets_1.csv'],
                     'q4': ['data\\stars_5.csv',
                            'data\\stars_4.csv',
                            'data\\stars_3.csv',
                            'data\\stars_2.csv',
                            'data\\stars_1.csv'],
                     'Star': Star(spectral_type='G2 V', stellar_effective_temperature=5780.0, stellar_radius=1.0, stellar_mass=1.0, stellar_luminosity=0.0, stellar_surface_gravity=4.44, stellar_age=4.6),
                     'q5': Star(spectral_type='K0III', stellar_effective_temperature=4888.0, stellar_radius=11.55, stellar_mass=1.78, stellar_luminosity=1.84, stellar_surface_gravity=2.55, stellar_age=4.5),
                     'q6': Star(spectral_type=None, stellar_effective_temperature=13500.0, stellar_radius=0.01, stellar_mass=0.69, stellar_luminosity=-2.4, stellar_surface_gravity=None, stellar_age=None),
                     'q7': 0.01624010554089703,
                     'q8': 4.3255604996096775,
                     'q9': 4632.0,
                     'q10': 'HD 81817',
                     'q11': 4.245366288492731,
                     'Planet': Planet(planet_name='Jupiter', host_name='Sun', discovery_method='Imaging', discovery_year=1610, controversial_flag=False, orbital_period=4333.0, planet_radius=11.209, planet_mass=317.828, semi_major_radius=5.2038, eccentricity=0.0489, equilibrium_temperature=110, insolation_flux=0.0345),
                     'q12': Planet(planet_name='17 Sco b', host_name='17 Sco', discovery_method='Radial Velocity', discovery_year=2020, controversial_flag=False, orbital_period=578.38, planet_radius=12.9, planet_mass=1373.01872, semi_major_radius=1.45, eccentricity=0.06, equilibrium_temperature=None, insolation_flux=None),
                     'q13': [Planet(planet_name='Kepler-1494 b', host_name='Kepler-1494', discovery_method='Transit', discovery_year=2016, controversial_flag=False, orbital_period=91.080482, planet_radius=3.07, planet_mass=9.64, semi_major_radius=0.3982, eccentricity=0.0, equilibrium_temperature=415.0, insolation_flux=9.11),
                             Planet(planet_name='Kepler-1495 b', host_name='Kepler-1495', discovery_method='Transit', discovery_year=2016, controversial_flag=False, orbital_period=85.273256, planet_radius=2.94, planet_mass=8.96, semi_major_radius=0.3677, eccentricity=0.0, equilibrium_temperature=443.0, insolation_flux=9.1),
                             Planet(planet_name='Kepler-1496 b', host_name='Kepler-1496', discovery_method='Transit', discovery_year=2016, controversial_flag=False, orbital_period=64.6588017, planet_radius=2.22, planet_mass=5.56, semi_major_radius=0.3211, eccentricity=0.0, equilibrium_temperature=535.0, insolation_flux=18.38),
                             Planet(planet_name='Kepler-1497 b', host_name='Kepler-1497', discovery_method='Transit', discovery_year=2016, controversial_flag=False, orbital_period=8.74199772, planet_radius=1.66, planet_mass=3.39, semi_major_radius=0.0817, eccentricity=0.0, equilibrium_temperature=924.0, insolation_flux=172.38),
                             Planet(planet_name='TOI-784 b', host_name='HD 307842', discovery_method='Transit', discovery_year=2023, controversial_flag=False, orbital_period=2.7970365, planet_radius=1.93, planet_mass=9.67, semi_major_radius=0.038, eccentricity=0.0, equilibrium_temperature=1256.0, insolation_flux=413.89)],
                     'q14': [Planet(planet_name='Kepler-452 b', host_name='Kepler-452', discovery_method='Transit', discovery_year=2015, controversial_flag=True, orbital_period=384.843, planet_radius=1.63, planet_mass=3.29, semi_major_radius=1.046, eccentricity=0.0, equilibrium_temperature=265.0, insolation_flux=1.1),
                             Planet(planet_name='Kepler-747 b', host_name='Kepler-747', discovery_method='Transit', discovery_year=2016, controversial_flag=True, orbital_period=35.61760587, planet_radius=5.27, planet_mass=24.1, semi_major_radius=0.1916, eccentricity=0.0, equilibrium_temperature=456.0, insolation_flux=10.19),
                             Planet(planet_name='V830 Tau b', host_name='V830 Tau', discovery_method='Radial Velocity', discovery_year=2016, controversial_flag=True, orbital_period=4.927, planet_radius=14.0, planet_mass=222.481, semi_major_radius=0.057, eccentricity=0.0, equilibrium_temperature=None, insolation_flux=None),
                             Planet(planet_name='nu Oct A b', host_name='nu Oct A', discovery_method='Radial Velocity', discovery_year=2016, controversial_flag=True, orbital_period=417.0, planet_radius=13.3, planet_mass=762.78818, semi_major_radius=1.25, eccentricity=0.11, equilibrium_temperature=None, insolation_flux=None)],
                     'q15': [Planet(planet_name='Wolf 1061 b', host_name='Wolf 1061', discovery_method='Radial Velocity', discovery_year=2015, controversial_flag=False, orbital_period=4.8869, planet_radius=1.21, planet_mass=1.91, semi_major_radius=0.0375, eccentricity=0.15, equilibrium_temperature=None, insolation_flux=7.34),
                             Planet(planet_name='Wolf 1061 c', host_name='Wolf 1061', discovery_method='Radial Velocity', discovery_year=2015, controversial_flag=False, orbital_period=17.8719, planet_radius=1.66, planet_mass=3.41, semi_major_radius=0.089, eccentricity=0.11, equilibrium_temperature=None, insolation_flux=1.3),
                             Planet(planet_name='YZ Cet b', host_name='YZ Cet', discovery_method='Radial Velocity', discovery_year=2017, controversial_flag=False, orbital_period=2.02087, planet_radius=0.913, planet_mass=0.7, semi_major_radius=0.01634, eccentricity=0.06, equilibrium_temperature=471.0, insolation_flux=8.21),
                             Planet(planet_name='ups And b', host_name='ups And', discovery_method='Radial Velocity', discovery_year=1996, controversial_flag=False, orbital_period=4.617033, planet_radius=14.0, planet_mass=218.531, semi_major_radius=0.059222, eccentricity=0.0215, equilibrium_temperature=None, insolation_flux=None),
                             Planet(planet_name='ups And d', host_name='ups And', discovery_method='Radial Velocity', discovery_year=1999, controversial_flag=False, orbital_period=1276.46, planet_radius=12.5, planet_mass=3257.74117, semi_major_radius=2.51329, eccentricity=0.2987, equilibrium_temperature=None, insolation_flux=None)],
                     'q16': [Planet(planet_name='TOI-712 d', host_name='TOI-712', discovery_method='Transit', discovery_year=2022, controversial_flag=False, orbital_period=84.8396, planet_radius=2.474, planet_mass=6.68, semi_major_radius=0.3405, eccentricity=0.073, equilibrium_temperature=314.0, insolation_flux=1.6),
                             Planet(planet_name='Wolf 1061 b', host_name='Wolf 1061', discovery_method='Radial Velocity', discovery_year=2015, controversial_flag=False, orbital_period=4.8869, planet_radius=1.21, planet_mass=1.91, semi_major_radius=0.0375, eccentricity=0.15, equilibrium_temperature=None, insolation_flux=7.34),
                             Planet(planet_name='Wolf 1061 c', host_name='Wolf 1061', discovery_method='Radial Velocity', discovery_year=2015, controversial_flag=False, orbital_period=17.8719, planet_radius=1.66, planet_mass=3.41, semi_major_radius=0.089, eccentricity=0.11, equilibrium_temperature=None, insolation_flux=1.3),
                             Planet(planet_name='YZ Cet b', host_name='YZ Cet', discovery_method='Radial Velocity', discovery_year=2017, controversial_flag=False, orbital_period=2.02087, planet_radius=0.913, planet_mass=0.7, semi_major_radius=0.01634, eccentricity=0.06, equilibrium_temperature=471.0, insolation_flux=8.21),
                             Planet(planet_name='ups And b', host_name='ups And', discovery_method='Radial Velocity', discovery_year=1996, controversial_flag=False, orbital_period=4.617033, planet_radius=14.0, planet_mass=218.531, semi_major_radius=0.059222, eccentricity=0.0215, equilibrium_temperature=None, insolation_flux=None)],
                     'q17': 256,
                     'q18': Star(spectral_type='K8V', stellar_effective_temperature=5144.0, stellar_radius=0.79, stellar_mass=0.82, stellar_luminosity=-0.401, stellar_surface_gravity=4.55, stellar_age=7.48),
                     'q19': 12.888118811881188,
                     'q20': [Planet(planet_name='Kepler-1663 b', host_name='Kepler-1663', discovery_method='Transit', discovery_year=2020, controversial_flag=False, orbital_period=17.6046, planet_radius=3.304, planet_mass=10.9, semi_major_radius=0.1072, eccentricity=0.0, equilibrium_temperature=362.0, insolation_flux=4.07)]}
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
        val = simpe_compare(sorted(list(expected.keys())), sorted(list(actual.keys())))
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
    
    global Star
    star_attributes = ['spectral_type', 'stellar_effective_temperature', 'stellar_radius', 'stellar_mass', 'stellar_luminosity', 'stellar_surface_gravity', 'stellar_age']
    Star = namedtuple('Star', star_attributes)
    expected_namedtuples.append(Star)
    global Planet
    planets_attributes = ['planet_name', 'host_name', 'discovery_method', 'discovery_year', 'controversial_flag', 'orbital_period', 'planet_radius', 'planet_mass', 'semi_major_radius', 'eccentricity', 'equilibrium_temperature', 'insolation_flux']
    Planet = namedtuple('Planet', planets_attributes)
    expected_namedtuples.append(Planet)
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
