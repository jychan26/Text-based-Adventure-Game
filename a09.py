##=========================================
## Chan Jia Yi (20783900)
## CS 116 Winter 2019
## Assignment 09
##=========================================


import check


class Thing:
    '''Fields: id (Nat),
               name (Str),
               description (Str)
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        
    def __repr__(self):
        return '<thing #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        
class Player:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               location (Room),
               inventory ((listof Thing))
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.location = None
        self.inventory = []
        
    def __repr__(self):
        return '<player #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.inventory) != 0:
            print('Carrying: {0}.'.format(
                ', '.join(map(lambda x: x.name,self.inventory))))
 
class Room:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               contents ((listof Thing)),
               exits ((listof Exit))
    '''    
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.contents = []
        self.exits = []
        
    def __repr__(self):
        return '<room {0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.contents) != 0:
            print('Contents: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.contents))))
        if len(self.exits) != 0:
            print('Exits: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.exits)))) 
 
class Exit:
    '''Fields: name (Str), 
               destination (Room)
               key (Thing)
               message (Str)
    '''       
    
    def __init__(self,name,dest):
        self.name = name
        self.destination = dest
        self.key = None
        self.message = ''
        
    def __repr__(self):
        return '<exit {0}>'.format(self.name)

##********************************************************************

class World:
    '''Fields: rooms ((listof Room)), 
               player (Player)
    '''       
    
    msg_look_fail = "You don't see that here."
    msg_no_inventory = "You aren't carrying anything."
    msg_take_succ = "Taken."
    msg_take_fail = "You can't take that."
    msg_drop_succ = "Dropped."
    msg_drop_fail = "You aren't carrying that."
    msg_go_fail = "You can't go that way."
    
    msg_quit = "Goodbye."
    msg_verb_fail = "I don't understand that."
    
    
    def __init__(self, rooms, player):
        self.rooms = rooms
        self.player = player


    def look(self, noun):
        '''prints the name and description of noun where noun is
           the name of the thing the and returns None. If the noun is
           the word "me", look at the player. If the noun is the word 
           "here", look at the player's current room. Then, if noun is
           one of the Things in the player's inventory or room, look 
           at that. Otherwise, print self.msg_look_fail.
           Effects: prints the name and description of noun if noun
                    is either one of the Things in the player's 
                    inventory or room, or if noun is the word "me" or 
                    "here". Otherwise, print self.msg_look_fail.
                    
           look: World Str -> None
           requires: When there is a match, the match is unique.
        '''
        player_inv = self.player.inventory
        curr_room_contents = self.player.location.contents
        things_inventory = list(map(lambda thing: thing.name, 
                                    player_inv))    
        things_room = list(map(lambda content: content.name, 
                               curr_room_contents))
        if noun == "me":
            self.player.look()
        elif noun == "here":
            self.player.location.look()
        elif noun in things_inventory:
            ind_inv = things_inventory.index(noun)
            player_inv[ind_inv].look()
        elif noun in things_room:
            ind_room = things_room.index(noun)
            curr_room_contents[ind_room].look()
        else:
            print(self.msg_look_fail)
            
            
    def inventory(self):
        '''prints a formatted list of the names of the Things that the
           Player is currently carrying. If the Player is carrying
           anything, the class method prints text in the following
           format: "Inventory: ", followed by a list of the names of
           the Things in the Player's inventory, separated by ", ".
           If the Player's inventory is empty, print 
           self.msg_no_inventory.
           This class method returns None.
           Effects: prints a formatted list of the names of the Things
                    the Player is currently carrying with the 
                    specified format. Print self.msg_no_inventory if
                    the Player's inventory is empty.
            
           inventory: World -> None
        '''
        things_inventory = list(map(lambda thing: thing.name, 
                                    self.player.inventory))
        if len(self.player.inventory) != 0:
            print("Inventory: " + ", ".join(things_inventory))
        else:
            print(self.msg_no_inventory)
            
            
    def take(self, noun):
        '''consumes noun where noun is the name of the thing to pick
           up and returns None. If the noun matches the name of one of
           the Things in the player's current room, mutate self  
           so that the thing is removed from the room's contents and 
           appended to the player's inventory. The method then prints
           self.msg_take_succ. Otherwise, print self.msg_take_fail.
           Effects: If noun matches the name of one of the Things in  
                    the player's current room, mutate self by
                    mutating the room's contents and the player's 
                    inventory. self.msg_take_succ is also printed. 
                    Otherwise, self.msg_take_fail is printed.
                    
           take: Str -> None
        '''
        curr_room = self.player.location
        item_names = list(map(lambda thing: thing.name, 
                              curr_room.contents))
        if noun in item_names:
            index = item_names.index(noun)
            item_taken = curr_room.contents[index]
            curr_room.contents.remove(item_taken)
            self.player.inventory.append(item_taken)
            print(self.msg_take_succ)
        else: 
            print(self.msg_take_fail)

            
    def drop(self, noun):
        '''consumes noun where noun is the name of the thing to put
           down and returns None. If the noun matches the name of one
           of the things in the player's inventory, mutate self
           so that the thing is removed from their inventory and 
           appended to the contents of the player's current room.
           The method then prints self. msg_drop_succ. Otherwise, 
           print self.msg_drop_fail.
           Effects: If the noun matches the name of one of the things
                    in the player's inventory, mutate self by 
                    mutating the player's inventory and the contents 
                    of the current room the player is in. 
                    self.msg_drop_succ is also printed. Otherwise, 
                    print self.msg_drop_fail.
                    
           drop: World Str -> None                   
        '''
        player_inv = self.player.inventory
        curr_room_items = self.player.location.contents
        thing_names = list(map(lambda thing: thing.name, player_inv))
        if noun in thing_names:
            index_thing = thing_names.index(noun)
            item_dropped = player_inv[index_thing]
            player_inv.remove(item_dropped)
            curr_room_items.append(item_dropped)
            print(self.msg_drop_succ)
        else:
            print(self.msg_drop_fail)

        
    def go(self, noun):
        '''consumes noun where noun is the name of the exit to go
           through and returns None. If the noun matches the name of 
           one of the exits in the player's current room, mutate the
           contents of self so that the player moves to the room
           at the other end of that exit. (The player can only move
           if the exit doesn't have a key or if the player has the key
           to the exit). The method should also look at their new
           room, so the user sees where they ended up. If the player
           doesn't have the key, print the exit's message. If no exit 
           with that name exists, print self.msg_go_fail. In these
           two cases, no mutation occurs.
           Effects: mutate World and print the description of the new
                    room if noun matches the name of one of the exits 
                    in the player's current room and the exit
                    doesn't need a key/player has the key. Otherwise,
                    self.msg_go_fail is printed if the exit doesn't
                    exit, and the exit's message is printed if the
                    player doesn't have the key. In both cases, no
                    mutation occurs.
           
           go: World Str -> None
           requires: no room contains two exits of the same name.         
        '''
        player_loc = self.player.location
        exits_available = player_loc.exits
        names_only = list(map(lambda exit: exit.name, 
                              exits_available))
        if noun in names_only:
            index = names_only.index(noun)
            exit = exits_available[index]
            if exit.key == None:
                self.player.location = exit.destination
                self.player.location.look()
            elif exit.key in self.player.inventory:
                self.player.location = exit.destination
                self.player.location.look()
            else:
                print(exit.message)
        else:
            print(self.msg_go_fail)
    
                
    def play(self):
        player = self.player
        
        player.location.look()
        
        while True:
            line = input( "- " )
            
            wds = line.split()
            verb = wds[0]
            noun = ' '.join( wds[1:] )
            
            if verb == 'quit':
                print( self.msg_quit )
                return
            elif verb == 'look':
                if len(noun) > 0:
                    self.look(noun)  
                else:
                    self.look('here')
            elif verb == 'inventory':
                self.inventory()     
            elif verb == 'take':
                self.take(noun)    
            elif verb == 'drop':
                self.drop(noun)
            elif verb == 'go':
                self.go(noun)   
            else:
                print( self.msg_verb_fail )

    ## Q3
    def save(self, fname):
        '''consumes fname and writes the complete state of the game
           to fname after playing it for a while (mutating self).
           Effects: writes to a file called fname
           
           save: World Str -> None
           requires: The information stored in fname must be in the 
                 following format:
                 1. First, all the things in the world (can be in
                    rooms or in the player's inventory) must be 
                    listed (represented in two lines of text): 
                    1st: thing #(insert number) (insert name of thing)
                    2nd: (insert description of thing)
                    
                 2. Next, list all the rooms in the World (represented
                    in 3 lines of text):
                    1st: room #(insert number) (insert room name)
                    2nd: description of room
                    3rd: contents (insert numeric code of the things
                         currently in that room)
                         
                 3. Next, describe the game's one and only player
                    using 4 lines of text:
                    1st: player #(insert number) (insert player's name)
                    2nd: description of player
                    3rd: inventory (insert numeric code of the things
                         in the player's inventory)
                    4th: location (insert numeric code of the room 
                         where the player currently is)
                         
                 4. Finally, give all the exits that lead from one
                    room to another (described in one or two lines):
                    
                    exits without keys:
                    1st: exit (insert numeric code of rooms that have 
                         this exit) (insert numeric code of rooms that
                         the exit leads to) (insert exit name)
                         
                    exits with keys:
                    1st: keyexit (insert numeric code of rooms that 
                         have this exit) (insert numeric code of rooms
                         that the exit leads to) (insert exit name)
                    2nd: (insert numeric code of key) (insert exit 
                         message)  
        '''
        new_file = open(fname, "w")
        rooms = self.rooms
        for room in self.rooms: 
            room_things = room.contents
            for thing in room_things:
                first = "thing #" + str(thing.id) + ' ' + \
                        thing.name + '\n'
                sec = thing.description + '\n'
                new_file.writelines([first, sec])
                
        player_things = self.player.inventory 
        for thing in player_things: 
            first = "thing #" + str(thing.id) + ' ' + thing.name+ '\n'
            sec = thing.description + '\n'
            new_file.writelines([first, sec])
            
        for room in rooms:
            first = "room #" + str(room.id) + ' ' + room.name + '\n' 
            sec = room.description + '\n'
            third = "contents " + \
                " ".join(list(map(lambda x:'#'+ str(x.id), 
                                  room.contents))) + '\n'
            new_file.writelines([first,sec,third])
        
        player = self.player
        loc_id = player.location.id
        first = 'player #' + str(player.id) + ' ' + player.name + '\n'
        sec = player.description + '\n'
        third = 'inventory ' + \
            " ".join(list(map(lambda x:'#'+ str(x.id), 
                              player_things))) + '\n'
        fourth = 'location #' + str(loc_id) + '\n'
        new_file.writelines([first,sec,third,fourth])
            
        for room in rooms:
            for exit in room.exits:
                dest_id = exit.destination.id
                if exit.key == None:
                    line = "exit " + \
                        ' '.join(list(map(lambda x: '#' + str(x), 
                                          [room.id,dest_id]))) + ' '+\
                        exit.name + '\n'
                    new_file.write(line)
                else:
                    line1 = "keyexit " + \
                        ' '.join(list(map(lambda x: '#' + str(x), 
                                          [room.id,dest_id]))) + ' '+\
                        exit.name + '\n'     
                    line2 = "#" + str(exit.key.id) + " " + \
                        exit.message + "\n"
                    new_file.writelines([line1,line2])                
                
        new_file.close()
     

## Q2
def load(fname):
    '''consumes fname where fname is the name of a text file to read
       from, and returns a World constructed from the information in
       the text file.
       Effects: Reads file called fname
       
       load: Str -> World
       requires: The information stored in fname must be in the 
                 following format:
                 1. First, all the things in the world (can be in
                    rooms or in the player's inventory) must be 
                    listed (represented in two lines of text): 
                    1st: thing #(insert number) (insert name of thing)
                    2nd: (insert description of thing)
                    
                 2. Next, list all the rooms in the World (represented
                    in 3 lines of text):
                    1st: room #(insert number) (insert room name)
                    2nd: description of room
                    3rd: contents (insert numeric code of the things
                         currently in that room)
                         
                 3. Next, describe the game's one and only player
                    using 4 lines of text:
                    1st: player #(insert number) (insert player's name)
                    2nd: description of player
                    3rd: inventory (insert numeric code of the things
                         in the player's inventory)
                    4th: location (insert numeric code of the room 
                         where the player currently is)
                         
                 4. Finally, give all the exits that lead from one
                    room to another (described in one or two lines):
                    
                    exits without keys:
                    1st: exit (insert numeric code of rooms that have 
                         this exit) (insert numeric code of rooms that
                         the exit leads to) (insert exit name)
                         
                    exits with keys:
                    1st: keyexit (insert numeric code of rooms that 
                         have this exit) (insert numeric code of rooms
                         that the exit leads to) (insert exit name)
                    2nd: (insert numeric code of key) (insert exit 
                         message)  
                         
                 Assume that fname uses the format above (all numeric
                 codes are unique and they correspond to legal objects
                 that have already been defined).
                 
                 Every world must have exactly 1 player and >= 1 room.
    '''
    opened_file = open(fname)
    lst = opened_file.readlines()
    rooms_lst = []
    things_dict = {}
    has_exit_dict = {}
    exit_to_dict = {}
    k = 0
    
    for line in lst:
        new_lst = line.split()
        
        if new_lst != []:
            if new_lst[0] == "thing":
                obj_id = int(new_lst[1][1:])
                obj = Thing(obj_id)
                obj.name = " ".join(new_lst[2:]).strip()
                obj.description = lst[k+1].strip()
                things_dict[obj_id] = obj
                
            elif new_lst[0] == "room":
                room_id = int(new_lst[1][1:])
                room = Room(room_id)
                room.name = " ".join(new_lst[2:]).strip()
                room.description = lst[k+1].strip()
                room.contents = []
                room.exits = []    
                content_ids = lst[k+2].split()[1:]
                ids = list(map(lambda x: int(x[1:]), content_ids))
                for num in ids:
                    room.contents.append(things_dict[num])
                rooms_lst.append(room)
            
            elif new_lst[0] == "player":
                player_id = int(new_lst[1][1:])         
                player_loc_id = int(lst[k+3].split()[1][1:])
                player = Player(player_id)
                player.name = " ".join(new_lst[2:]).strip()
                player.description = lst[k+1].strip()
                inv_sent_list = lst[k+2].split()[1:]
                inv_ids = list(map(lambda x: int(x[1:]), 
                                   inv_sent_list))
                player.inventory = []
                for num in inv_ids:
                    player.inventory.append(things_dict[num])
                                 
            elif new_lst[0] == "exit" or new_lst[0] == "keyexit":
                has_exit_id = int(new_lst[1][1:])
                exit_to_id = int(new_lst[2][1:])
                exit_name = " ".join(new_lst[3:]).strip()
                dest = list(filter(lambda x: x.id == exit_to_id, 
                                   rooms_lst))[0]              
                    
                exit = Exit(exit_name, dest) 
                exit_to_dict[exit] = exit_to_id
                
                if has_exit_id in has_exit_dict:
                    has_exit_dict[has_exit_id].append(exit)
                else:
                    has_exit_dict[has_exit_id] = [exit]
                    
                if new_lst[0] == 'keyexit':
                    line2 = lst[k+1].split()
                    exit.key = things_dict[int(line2[0][1:])]
                    exit.message = " ".join(line2[1:]).strip()            
        
        k += 1
        
    if has_exit_dict != {}:
        for x in rooms_lst:
            if x.id in has_exit_dict:
                x.exits = has_exit_dict[x.id]
    curr_location = (list(filter(lambda x: x.id == player_loc_id , 
                                rooms_lst)))[0]
    player.location = curr_location
    opened_file.close()
    construct_world = World(rooms_lst, player)
    return construct_world    
                       

def makeTestWorld(usekey):
    wallet = Thing(1)
    wallet.name = 'wallet'
    wallet.description = 'A black leather wallet containing a WatCard.'
    
    keys = Thing(2)
    keys.name = 'keys'
    keys.description = 'A metal keyring holding a number of office and home keys.'
    
    phone = Thing(3)
    phone.name = 'phone'
    phone.description = 'A late-model smartphone in a Hello Kitty protective case.'
    
    coffee = Thing(4)
    coffee.name = 'cup of coffee'
    coffee.description = 'A steaming cup of black coffee.'
    
    hallway = Room(5)
    hallway.name = 'Hallway'
    hallway.description = 'You are in the hallway of a university building. \
Students are coming and going every which way.'
    
    c_and_d = Room(6)
    c_and_d.name = 'Coffee Shop'
    c_and_d.description = 'You are in the student-run coffee shop. Your mouth \
waters as you scan the room, seeing many fine foodstuffs available for purchase.'
    
    classroom = Room(7)
    classroom.name = 'Classroom'
    classroom.description = 'You are in a nondescript university classroom. \
Students sit in rows at tables, pointedly ignoring the professor, who\'s \
shouting and waving his arms about at the front of the room.'
    
    player = Player(8)
    player.name = 'Stu Dent'
    player.description = 'Stu Dent is an undergraduate Math student at the \
University of Waterloo, who is excelling at this studies despite the fact that \
their name is a terrible pun.'
    
    c_and_d.contents.append(coffee)
    player.inventory.extend([wallet,keys,phone])
    player.location = hallway
    
    hallway.exits.append(Exit('shop', c_and_d))
    ex = Exit('west', classroom)
    if usekey:
        ex.key = coffee
        ex.message = 'On second thought, it might be better to grab a \
cup of coffee before heading to class.'
    hallway.exits.append(ex)
    c_and_d.exits.append(Exit('hall', hallway))
    classroom.exits.append(Exit('hall', hallway))
    
    return World([hallway,c_and_d,classroom], player)

testworld = makeTestWorld(False)
testworld_key = makeTestWorld(True)