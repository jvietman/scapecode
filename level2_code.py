from scapecode import *

# put in file path of the level.json
load_level("level2.json")

# YOUR CODE HERE
while True:
    if not isMovePossible():
        break
    move()
turnRight()
while True:
    if not isMovePossible():
        break
    move()

# END OF CODE

print(results()) # print out results, but you can use the results however you want