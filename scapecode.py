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
    nextpos = [main.pos[0], main.pos[1]]
    # Calculate the next position mathematically instead of simply using an if one-liner, silly me :3
    mod = (main.facing+1) % 2
    nextpos[mod] += ((-1+(mod*2)) * main.facing) + (-1+(3*(1-mod)))
        
    # check if move is valid depending on block it will land on
    match main.get_block(main.cur_room, nextpos):
        case "#":
            log("trymove")
        case _:
            main.pos = nextpos
            log("move")
    
    if end(): return

### end of public methods ###



# if not executed as main -> if imported from other code
if not __name__=="__main__":
    main = scapecode()