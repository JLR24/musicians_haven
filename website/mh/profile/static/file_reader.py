import csv
from flask_login import current_user

def get_instruments():
    '''Returns a list of instrument strings from the .txt file - REMOVES the instruments the user already plays'''
    file = open("static/instruments_reduced.txt", "r")
    instruments = file.read().split("\n")
    file.close()

    # Remove any instruments that have already been chosen
    to_remove = []
    for inst in instruments:
        for p in current_user.getInstruments():
            if inst == p.instrument:
                to_remove.append(inst)
                break
    instruments = [i for i in instruments if i not in to_remove] # Source: https://www.geeksforgeeks.org/python-remove-all-values-from-a-list-present-in-other-list/
    return instruments


def get_countries():
    '''Returns a list of countries strings from the .csv file'''
    file = open("static/countries.csv", "r")
    countries = file.read()
    countries = countries.split(",")
    countries = [i[4:-1] for i in countries] # Remove the area codes and additional quote marks
    file.close()
    return countries


def get_cities():
    '''Returns a list of cities strings from the .csv file'''
    file = open("static/cities.csv", "r")
    cities = []
    for row in csv.reader(file):
        cities.append(f"{row[1]} - {row[4]} ({row[7]})")
    file.close()
    return cities

def get_genres():
    '''Returns a list of genres from the .txt file - REMOVES the genres the user has already selected'''
    file = open("static/genres.txt", "r")
    genres = file.read().split("\n")
    file.close()

    to_remove = []
    for g in genres:
        for i in current_user.getGenres():
            if g == i.genre:
                to_remove.append(g)
                break
    return [i for i in genres if i not in to_remove]
