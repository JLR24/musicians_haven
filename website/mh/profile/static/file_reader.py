import csv
from flask_login import current_user

def GetInstruments():
    '''Returns a list of instrument strings from the .txt file'''
    file = open("static/instruments_reduced.txt", "r")
    all = file.read()
    instruments = all.split("\n")
    file.close()

    # Remove any instruments that have already been chosen
    to_remove = []
    for inst in instruments:
        for p in current_user.GetInstruments():
            if inst == p.instrument:
                to_remove.append(inst)
                break
    instruments = [i for i in instruments if i not in to_remove] # Source: https://www.geeksforgeeks.org/python-remove-all-values-from-a-list-present-in-other-list/
    return instruments


def GetCountries():
    '''Returns a list of countries strings from the .csv file'''
    file = open("static/countries.csv", "r")
    countries = file.read()
    countries = countries.split(",")
    countries = [i[4:-1] for i in countries] # Remove the area codes and additional quote marks
    file.close()
    return countries


def GetCities():
    '''Returns a list of cities strings from the .csv file'''
    file = open("static/cities.csv", "r")
    cities = []
    for row in csv.reader(file):
        cities.append(f"{row[1]} - {row[4]} ({row[7]})")
    file.close()
    return cities