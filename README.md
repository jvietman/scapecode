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


## How to make custom levels
### Symbols definition
Empty fields are walkable paths by default
- S = Startfield
- E = Endfield(s)
- \# = Wall