import json, os

class scapecode:
    def __init__(self):
        self.running = False
        self.level = ""
        self.rooms = []
        self.end_fields = []
        
        # values during runtime
        self.pos = [0, 0]
        self.cur_room = 0
        self.facing = 1 # 0 - 3 = up - left (clockwise rotation)
        
        # results
        self.actionlog = []
        self.succeeded = False
    
    def load_level(self, l: str):
        """Loads level data from a json file.

        Args:
            l (str): Json file of level
        """
        
        if not os.path.exists(l):
            print("Level file \""+l+"\" not found. Exiting...")
            exit()
        with open(l, "r") as f:
            self.running = True
            l = json.load(f)
            
            # load config
            self.level = l
            self.rooms = l["rooms"]
            # find start and endfield
            start_field = []
            for i in range(len(self.rooms)):
                for j in range(len(self.rooms[i])):
                    r = self.rooms[i][j]
                    
                    ef = r.find("E")
                    if not ef == -1:
                        self.end_fields.append([i, [ef, j]])
                        
                    sf = r.find("S")
                    if not sf == -1:
                        start_field = [i, [sf, j]]
            if not start_field:
                print("No start field defined. Please include one \"S\" block in one of your rooms.")
                exit()
            if not self.end_fields:
                print("No end field defined. Please include at least one \"E\" block in one of your rooms.")
                exit()
            
            # setup character
            self.cur_room, self.pos = start_field
                        
            f.close()
            
    def get_block(self, room: int, pos: list[int]) -> str:
        """Returns block in certain room and at certain position.

        Args:
            room (int): Room index
            pos (list[int]): Position

        Returns:
            str: Block as String
        """
        return self.rooms[room][pos[1]][pos[0]]
    
    def get_next(self) -> list[int]:
        """Return the position of the next field the character is facing.

        Returns:
            list[int]: _description_
        """
        next = [self.pos[0], self.pos[1]]
        mod = (self.facing+1) % 2
        next[mod] += ((-1+(mod*2)) * self.facing) + (-1+(3*(1-mod)))
        # I decided to calculate the next position mathematically instead of simply using an if one-liner everyone would easily understand, silly me :3
        return next
    
    def check_move(self) -> bool:
        """Checks if the next the block the character is facing to is free to move to (and if its still in map).

        Returns:
            bool: Is the move possible
        """
        
        next = self.get_next()
        # if outside of map
        if next[1] >= len(self.rooms[self.cur_room]) or next[0] >= len(self.rooms[self.cur_room][self.pos[1]]):
            return False
        
        # check for blocks
        match self.get_block(self.cur_room, next):
            case "#":
                return False
            case _:
                return True

###

# check if level running (including stopping when on end field)
def end() -> bool:
    """Returns game running status (and checks if on one of the end fields)

    Returns:
        bool: Game running status
    """
    for i in main.end_fields:
        if [main.cur_room, main.pos] == i:
            main.succeeded = True
            main.running = False
    return not main.running

# add something to actionlog
def log(action: str):
    """Adds action to the actionlog.
    
    The actionlog is there for another script to display all animations (all the things the character has done).
    
    ### Actions legend (all animations that can be displayed)
    - move = moves one field forward
    - try_move = tried to move, there was something in the way
    - turn_right = rotates to the right
    - turn_left = rotates to the left
    - check_move = checks if move is possible (if nothing is blocking its way)
    - check_end = check if character is on an end field

    Args:
        action (str): Action name to log.
    """
    
    main.actionlog.append(action)

# return actionlog for other script to show animation
def results() -> list:
    """Returns actionlog and ends the level (sets running boolean to false).

    Returns:
        list: Includes following content: [succeeded?, actionlog, end_state = [room_id, pos]]
            - [0]: if succeeded (if on end field)
            - [1]: the actionlog (list of action names for animation)
            - [2]: end state of character (0: room id, 1: position list with x and y)
    """
    main.running = False
    return [main.succeeded, main.actionlog, [main.cur_room, main.pos]]



### public methods ###

# initialize level
def load_level(roomname: str):
    """Loads level data from a json file.

    Args:
        roomname (str): Json file of level
    """
    main.load_level(roomname)

# commands
def move():
    """Move character one fild forward in the direction its facing.
    """
    if end(): return
    
    # get position where the character will land if he moves
    nextpos = main.get_next()
    
    # check if move is valid
    if main.check_move():
        # move, set new position
        main.pos = nextpos
        log("move")
    else:
        log("trymove")
    
    if end(): return
    
def turnRight():
    """Rotate character to the right.
    """
    if end(): return
    
    # add 1 to facing value; if higher than maximum (3) then set to 0
    main.facing = 0 if main.facing+1 > 3 else main.facing+1
    log("turn_right")

def turnLeft():
    """Rotate character to the left.
    """
    if end(): return
    
    # substract 1 from facing value; if lower than 0 then set to maximum (3)
    main.facing = 3 if main.facing-1 < 0 else main.facing-1
    log("turn_left")

def isMovePossible() -> bool:
    """Checks if the next the block the character is facing to is free to move to.

    Returns:
        bool: Is the move possible
    """
    if end(): return
    
    log("check_move")
    return main.check_move()

def isOnEnd() -> bool:
    """Checks if the character is on an end field.
    
    The original codescape terminates once on the end field. Here, you have to manually check if on end field and stop your code. This adds to the difficulty ;)

    Returns:
        bool: Is on an end field
    """
    
    log("check_end")
    return end()

### end of public methods ###



# if not executed as main -> if imported from other code
if not __name__=="__main__":
    main = scapecode()