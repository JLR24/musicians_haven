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