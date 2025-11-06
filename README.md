# scapecode
Definitely not a Codescape clone, but in Python, open source and with custom levels.


## How to play
Levels are played by using the scapecode library. All you have to do to play a level is to import the scapecode library and loading in the level json file. Then you simply write your code that will solve the level inbetween the two comments. At the end of your code, use the ```results()``` method to get the information about the state of the level.
Here is the base code you have to include to navigate in the level:
```python
from scapecode import *

# put in file path of the level.json
load_level("")

# YOUR CODE HERE



# END OF CODE

print(results()) # print out results, but you can use the results however you want
```
### Explanations
**To clarify things you can check out the example levels and code solutions provided.**
In the ```load_level()``` method you put in the file name of the level, or if not in same directory, put in the full path.
You put you code to solve the level between the two comments
The ```results()``` returns the results of the level, like if you succeeded (if on end field = True, if not reached or died = False), the actions you made (actionlog) and the endstate of you character (room index and position)
Use that method only at the end of the code, because using this method stops the game. You can use the actionlogs for the purpose of animating all of the moves of the character (which I will make possible soon). The success and state values are more like debug values what you will need if you print out the results in the console.

### Moveset
- ```move()``` = moves one field forward
- ```turnRight()``` = rotates to the right
- ```turnLeft()``` = rotates to the left
- ```isMovePossible()``` = checks if move is possible (if nothing is blocking its way or if still in map)
- ```isOnEnd()``` = check if character is on an end field (because here the code doesnt terminate on its on, which adds to the difficulty ;) )

### Actions definition
*(Not relevant for you if you are just a player)*
These are actions you will find the actionlogs.
- move = moves one field forward
- try_move = tried to move, there was something in the way
- turn_right = rotates to the right
- turn_left = rotates to the left
- check_move = checks if move is possible (if nothing is blocking its way)
- check_end = check if character is on an end field
- dead = character died
- teleport = character got teleported


## How to make custom levels (WIP...)
### Structure
This structure always has to be included.
```json
{
    "rooms": [],
    "objects": []
}
```
(Check any provided level for examples)

The rooms (yes, there are multiple rooms in a level) are the map the character walks on. Here you can create different shapes of rooms, set the start and end fields and add objects.

### Symbols definition
Empty fields are walkable paths by default
- S = Startfield, gets automatically detected and player will start there
- E = Endfield(s), if on this field, then the level is solved
- \# = Wall
- @ = Teleporter

### Objects
Objects are things in a room that have a certain function. The object key in the level json is there to give the symbols you have on the map a function.

Objects always have to be included in the map , that means as a symbol in the rooms strings. To give them a function you will need to add them to the objects array.
You can then program the objects to have a certain function as you wish.

Functions of an object (like teleporting a player) only get checked when the player moved. For example the teleport only happens AFTER a player moved onto a teleporter. If the player is already on a teleporter and turns right, the function does not execute. Only when the character moves the function executes.

All objects have a different structure, but all objects need to have a name and objects themselves are always declared as a dictionary.

#### Teleporter ("tp")
A Teleporter can teleport the character from point A to B (or get you killed :3).

Template:
```json
{
    "name": "tp",
    "p1": [x1, y1],
    "p2": [x2, y2]
}
```
- p1 = One position
- p2 = Another position

Positions dont have to be in order, so the teleporter you go into doesnt have to be the first teleporter.

There are different mechanics of a teleporter you can use for some creative level designs:
1. Normal usage, two teleporters
You can use two teleporters and link them together using the p1 and p2 keys.

2. Only using one teleporter
You can set any position (p1 or p2) to the teleporter you go through and set the other position to be any field you want in the level. In short, you can create one way teleporters that teleport you away but dont teleport back.

3. Not setting a reference
If you just have a teleporter in your level without any positions (any object p1 or p2) set to it, the teleporter will try to teleport you, but doesnt know where, and this leads to death. In short, walking through a teleporter that doesnt have a position configured kills you.

4. Using more than 2 teleporters
You can link multiple teleporters together, so you can for example have three or more teleporters in a circle, each teleporting you to the teleporter next to them.