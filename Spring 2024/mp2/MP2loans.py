import os
import json
import pandas as pd
from zipfile import ZipFile, ZIP_DEFLATED
from io import TextIOWrapper
import csv
import os

class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            if r in race_lookup:
                self.race.add(race_lookup[r])
    def __repr__(self):
        race = sorted(self.race)
        return f"Applicant('{self.age}', {race})"
    def lower_age(self):
        cur = self.age.replace(">", "")
        cur = cur.replace("<", "")
        cur = cur.split("-")
        return int(cur[0])
    def __lt__(self, other):
        return self.lower_age() < other.lower_age()
    

race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "5": "White",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander"
}

class Loan:
    def __init__(self, values):
        try: 
            self.loan_amount = float(values["loan_amount"])
        except ValueError:
            self.loan_amount = float(-1)
        try:
            self.property_value = float(values["property_value"])
        except ValueError:
            self.property_value = float(-1)
        try:
            self.interest_rate = float(values["interest_rate"])
        except ValueError:
            self.interest_rate = float(-1)
        applist = []
        racelist1 = []
        racelist1.append(values["applicant_race-1"])
        racelist1.append(values["applicant_race-2"])
        racelist1.append(values["applicant_race-3"])
        racelist1.append(values["applicant_race-4"])
        racelist1.append(values["applicant_race-5"])
        applist.append(Applicant(values["applicant_age"], racelist1))
        
        if values["co-applicant_age"] != "9999":
            racelist2 = []
            racelist2.append(values["co-applicant_race-1"])
            racelist2.append(values["co-applicant_race-2"])
            racelist2.append(values["co-applicant_race-3"])
            racelist2.append(values["co-applicant_race-4"])
            racelist2.append(values["co-applicant_race-5"])
            applist.append(Applicant(values["co-applicant_age"], racelist2))
        
        self.applicants = applist
    
    def __str__(self):
        length = len(self.applicants)
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {length} applicant(s)>"
    
    def __repr__(self):
        length = len(self.applicants)
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {length} applicant(s)>"
    
    def yearly_amounts(self, yearly_payment):
        # TODO: assert interest and amount are positive
        #result = []
        amt = self.loan_amount
        assert(self.interest_rate >0)
        assert(amt >0)
        while amt > 0:
            #result.append(amt)
            yield amt
            # TODO: add interest rate multiplied by amt to amt
            amt += (self.interest_rate/100)*amt
            # TODO: subtract yearly payment from amt
            amt -= yearly_payment

class Bank:
    def __init__(self, bank):
        with open('banks.json', 'r') as f:
            names = json.load(f)
        found = 0
        for dicty in names:
            if dicty["name"] == bank:
                self.lei = str(dicty["lei"])
                found = 1
                break
        if found == 0:
            raise ValueError
        
    def load_from_zip(self, path):
        lolist = []
        with ZipFile(path) as zf:
            with zf.open("wi.csv", "r") as f:
                tio = TextIOWrapper(f)
                reader = csv.DictReader(tio)
                for row in reader:
                    if row["lei"] == self.lei:
                        lolist.append(Loan(row))
        self.loanlist = lolist
    
    def __getitem__(self, index):
        return self.loanlist[index]
    
    def __len__(self):
        return len(self.loanlist)
            
    def average_interest_rate(self):
        total = 0
        counter = 0
        for loan in self.loanlist:
            try:
                total += loan.interest_rate
                counter += 1
            except ValueError:
                continue
        return total/counter
    
    def num_applicants(self):
        total = 0
        for loan in self.loanlist:
            total += len(loan.applicants)
        return total
    
    def ages_dict(self):
        start = {}
        for loan in self.loanlist:
            for applicant in loan.applicants:
                if applicant.age not in start:
                    start[applicant.age] = 1
                else:
                    start[applicant.age] += 1
        return dict(sorted(start.items()))