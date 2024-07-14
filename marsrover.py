"""
For Multiverse

This is a solution to the problem documented in the following file:
Multiverse engineering take-home challenge (2).pdf

Author: Iain Argent (iainargent007@gmail.com)

Approach:
This was written in a functional style (as opposed to object-oriented)
using a recursive function to process one movement at a time.
Although Python does not support tail recursion other languages do
and an equivalent implementation in Elixir would be tail recursive.
I chose Python to complete this challenge as it is fairly easy to read
and I know it better than Elixir. 

Usage:
You can use this program in interactive mode like this:

Windows:
python.exe marsrover.py

Mac/BSD/Linux:
python3 marsrover.py

Or you can save commands in a file (e.g. marsrove.txt)
and execute all the commands like this:

Windows:
type .\marsrover.txt | python.exe marsrover.py

Mac/BSD/Linux:
cat marsrover.txt | python3 marsrover.py

Test suite:
There is an accompanying test suite called test_marsrover.py
"""

import re


# implements a simple circular list for finding
# the next direction in a list of directions
# when rotating left or right
# returns a char with the new direction
def direction_change(dirs: list, curdir: str, isRight: bool):
    curpos = dirs.index(curdir)
    increment = 1 if isRight else -1
    return dirs[(curpos + increment) % len(dirs)]


# update the rover's position from its
# last location and the direction it was facing
# returns a pair of integers with the new position
def go_forward(xloc: int, yloc: int, dir: str):
    if dir == "N":
        return (xloc, yloc + 1)
    if dir == "E":
        return (xloc + 1, yloc)
    if dir == "S":
        return (xloc, yloc - 1)
    if dir == "W":
        return (xloc - 1, yloc)
    raise ValueError("Invalid direction: " + dir)


# recursive function which executes one instruction
# at the head of movestr
# returns a string with the report of the final location
def do_move(
    xloc: int, yloc: int, dir: str, gridWidth: int, gridHeight: int, movestr: list
):
    dirs = ["N", "E", "S", "W"]
    if movestr == []:
        return f"({xloc}, {yloc}, {dir})"
    else:
        curmove, *tailstr = movestr
        if curmove not in ["L", "R", "F"]:
            raise ValueError("Invalid command found: " + curmove)
        if curmove == "F":
            (newxloc, newyloc) = go_forward(xloc, yloc, dir)

            # check if rover is out of bounds
            if (
                newxloc < 0
                or newxloc > (gridHeight - 1)
                or newyloc < 0
                or newyloc > (gridHeight - 1)
            ):
                return f"({xloc}, {yloc}, {dir}) LOST"
            else:
                return do_move(newxloc, newyloc, dir, gridWidth, gridHeight, tailstr)
        else:
            newdir = direction_change(dirs, dir, curmove == "R")
        return do_move(xloc, yloc, newdir, gridWidth, gridHeight, tailstr)


if __name__ == "__main__":
    gridstr = input()

    # retrieve the two numbers from the string (as integers)
    (gridx, gridy) = map(int, gridstr.split())

    while True:
        try:
            comstr = input()
        except EOFError:
            break
        pattern = r"\(([^,]+)\W*([^,]+).*\W*([^\)]+)\)\W([LRF]*)"
        (xloc, yloc, dir, movestr) = re.findall(pattern, comstr)[0]
        result = do_move(int(xloc), int(yloc), dir, gridx, gridy, list(movestr))
        print(result)
