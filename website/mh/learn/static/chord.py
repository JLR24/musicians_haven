# # # # # # # # # # # # # # # #
# Jack Ricketts
# 17/10/2023
# Chord analyser
# # # # # # # # # # # # # # # #
# This file will process the
# fretboard positions from the
# website into chord names.
# # # # # # # # # # # # # # # #

SHARP_NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
FLAT_NOTES = ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]

NOTE_COUNT = 12

# MAJOR_SCALE = [2, 2, 1, 2, 2, 2, 1]
# MINOR_SCALE = [2, 1, 2, 2, 1, 2, 2]

def GetChordName(notes):
    '''Takes root note and array of notes as input and returns chord name'''
    notes = _ConvertToSharps(notes)
    print(notes)
    root = notes[0]
    for note in notes:
        if note == root:
            continue
        print(note, _GetDistance(root, note))


def _ConvertToSharps(notes):
    '''Changes all flat notes to their sharp counterpart'''
    for i, n in enumerate(notes):
        if "b" in n: # If it is a flat note, convert to a sharp
            notes[i] = SHARP_NOTES[FLAT_NOTES.index(n) - 1][0] + "#"
    return notes


def _GetDistance(root, note):
    '''Returns the "distance" between the root and given note'''
    start = SHARP_NOTES.index(root)
    count = 0
    for i in range(NOTE_COUNT):
        if SHARP_NOTES[(i + start) % NOTE_COUNT] == note:
            return count
        count += 1
    return -1 # Something has broken...
    

GetChordName(["G", "Bb", "D"])
GetChordName(["Bb", "F", "Db"])