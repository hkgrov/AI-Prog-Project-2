from random import randint
import math
import numpy as np
import time
import copy

player = {False: "Player 2", True: "Player 1"}


class Game():
    
    def __init__(self, state, verbose, mcts):
        #self.choose_player(player)
        self.root = state
        self.max = state.max
        self.current_state = self.root
        self.game_play = mcts
        self.verbose = verbose
        #self.play()
        
    #Easiest to use false and true and toggle between them using not. You can still create the game by typing 1, 2 or mix, but I 
    #would just switch it to true and false in this method?
    
    
    #This should maybe be moved into another class? Then this would just be a state manager without any spec
    def play(self):
        while ( not self.current_state.is_terminal() ):
            if(self.game_play):
                #print("Starter MCTS")
                mc = Mcts(self.current_state)
                action = mc.run()
            
            else:
                action = self.random_action()
                
            num_pieces = self.current_state.pieces - action
            
            if(self.verbose):
                print(str(player[self.current_state.player]) + " took " + str(action) + " piece(s), " + str(num_pieces) + " left")
            
            self.current_state = Stateman(num_pieces, (not self.current_state.player), self.max, seen=True)
            #print(self.current_state.pieces)
        
        return (not self.current_state.player)
                    
    
    #Is this method ment to only find out how many stones to take and return it to the play method?
    def random_action(self):
        possible_actions = self.current_state.get_available_actions()    
        action = possible_actions[randint(0,len(possible_actions)-1)]
        return action
        

#Kanskje feil å kalle klassen stateman!?
class Stateman():
    def __init__(self, num_pieces, player, k, action=None, parent=None, seen=False):
        #In this game this is the state. The only thing that matters is the pieces left and player. This would change when we use a grid in gomoku or hex. self.pieces would then equal the current state of the grid (where the pieces are located on the grid). 
        self.pieces = num_pieces
        self.player = player
        self.action = action
        
        #These variables are important to keep track of the structure. When a node is added it should always have a parent (if not root node) and should always have children (unless leaf node)
        self.parent = parent
        self.children = []
        self.max = k
        #Needed for the MCTS algorithm
        self.num_visits = 0
        self.total_wins = 0
        self.rollout = seen
        
        
    #Method for adding children. This would be done for example when expanding the three in MCTS    
    def add_child(self, state):
        self.children.append(state)
        
    
    #Don't need this at the moment. 
    def get_next_state(self, action):
        remaining_pieces = self.state.pieces - action
        player = not(self.state.player)
        child = Node(remaining_pieces, player, self.state)
        self.current_node = child
        
        
    
    def get_available_actions(self):
        if(self.pieces < self.max):
            actions = list(range(1, self.pieces + 1))
        else:
            actions = list(range(1, self.max + 1))
            
        #Is an array of all the possible actions from this state
        return actions
    
    
    #Returns True if this is a terminal state, false otherwise
    def is_terminal(self):
        if(self.pieces == 0):
            return True
        else:
            return False
            
    def add_visit(self):
        self.num_visits += 1
    
    def add_win(self, value):
        self.total_wins += value
        
    def rolled_out(self):
        self.rollout = True



class Mcts():
    
    def __init__(self, root):
        self.current_state = root
        #self.total_runs = 0
     
     
    def print_tree(self, state):
        print("------------------------Tree------------------------")
        for child in state.children:
            print(player[child.player])
            print("Action: " + str(child.action) + ", Pieces: " + str(child.pieces) + ", num_wins: " + str(child.total_wins) + ", Visits: " + str(child.num_visits))
            for chil in child.children:
                print(player[chil.player])
                print("Action: " + str(chil.action) + ", Pieces: " + str(chil.pieces) + ", num_wins: " + str(chil.total_wins) + ", Visits: " + str(chil.num_visits))
            print("__________________________________________________")
    
    
    def run(self):
        for i in range(100):
            #print("Har nå kjørt " + str(i) + " gang(er)")
            self.tree_policy()
            
            
            #print("Valgt node")
        
        
            #print("--------------------------------------------------------")
            #print("Dette er forelderen: " + str(self.current_state.parent))
            
            
            
       # for child in self.current_state.children:
        #    print("Visits: " + str(child.num_visits) + ", wins: " + str(child.total_wins))
       # print(self.total_runs)
       
        chosen_node = []
        for child in self.current_state.children:
            chosen_node.append(child.num_visits)
            
        
        #chosen_node = self.selection(self.current_state)
        #time.sleep(100)
        #print("Dette er valgt action: " + str(chosen_node.action))
        #if(self.current_state.player):
        action = np.argmax(np.array(chosen_node)) + 1
        
        #else:
         #   action = np.argmin(np.array(chosen_node)) + 1
        #self.print_tree(self.current_state)
        
        #print(indice+1)
        #time.sleep(100)
        return action
    
    
    def tree_policy(self):
        current_state = self.current_state
        
        while(current_state.children):
            next_state = self.selection(current_state)
            current_state = next_state
        
        if(current_state.rollout):
            self.node_expansion(current_state)
        else:
            self.default_policy(current_state)
        
        
    
    
    def selection(self, state):
        poss_next_state = []
        
        
        for child in state.children:
            
            if(child.num_visits == 0):
                if(state.player):
                    poss_next_state.append(9999)
                else:
                    poss_next_state.append(-9999)
                
            else:
                if(state.player):
                    poss_next_state.append(((child.total_wins/child.num_visits) + (5 * math.sqrt((math.log(state.num_visits))/(1+child.num_visits)))))
                else:
                    poss_next_state.append(((child.total_wins/child.num_visits) - (5 * math.sqrt((math.log(state.num_visits))/(1+child.num_visits)))))
                    
                    
        if(state.player):
            next_state = state.children[np.argmax(np.array(poss_next_state))]
        else:
            next_state = state.children[np.argmin(np.array(poss_next_state))]
        return next_state
    
    
    
    def node_expansion(self, state):
        
        #Check to see if the current state is a terminal state.
        if(state.is_terminal()):
            if(state.player):
                #If the player is player 1 in this state it means player 2 won. Being the player at a terminal state means
                self.backprop(-2, not state.player, state)
            else:
                self.backprop(2, not state.player, state)
            return
            
        #Get possible actions from this state.
        actions = state.get_available_actions()
        #print("Dette er mulige actions" + str(actions))
       # time.sleep(10)
       
       #For each legal action, create a new state which is the child of the current state. 
        for action in actions:
            num_pieces = state.pieces - action
            child = Stateman(num_pieces, (not state.player), state.max, action, state)
            state.add_child(child)
        
        
        #Choose the first of the new children as the current state
        next_state = state.children[0]
        
        self.default_policy(next_state)
            
        
    
    
    def default_policy(self, current_state):
        rollout_game = Game(copy.copy(current_state), False, False)
        #print("Pieces left: " + str(self.current_state.pieces) + ", player: " + str(player[self.current_state.player]))
        winner = rollout_game.play()
        #print(player[winner])
        #time.sleep(10)
        current_state.rolled_out()
        
        #Setting the value to be added to the states when hitting a terminal state
        if(winner):
            value = 1
        else:
            value = -1
            
        self.backprop(value, winner, current_state)
    
    
    #Fix so I dont update wins on root node
    def backprop(self, value, winner, current_state):
        current_state.add_visit()
        #adding a value to the state. Either it is a win for player 1 => +1 or a win for player 2 => -1
        current_state.add_win(value)
        
        while (current_state.parent):
            current_state = current_state.parent
            current_state.add_visit()
            current_state.add_win(value)
            
    
            
    
    
def choose_player(player):
    if (player == "mix"):
        return bool(randint(0,1))
    if(player == 1):
        return True
    if(player == 2):
        return False
    else:
        print("Not a valid option")
                

def main():
    g = 3
    #The parameters are on the form: Max number of stones allowed to pick, Total number of stones, Verbose (True/False), Starting player (Either        1, 2 or mix)
    player1_turn = choose_player(1)

    statistikk = 0
    for i in range(1, g+1):
        print("------------------------Spill " + str(i) + "------------------------")
        #print("Kjører game nummer: " + str(i))
        start_state = Stateman(99, player1_turn, 6, seen=True)
        test = Game(start_state, True, True)
        vinner = test.play()
        print(str(player[vinner]) + " won this round")
        if(vinner):
            statistikk += 1
        #time.sleep(10)
    print("Player 1 vant " +str(statistikk)+ " av " + str(g) + " kamper " + str((statistikk/g)*100) + "%")
            
    #print(list(range(1,2)))



if __name__ == "__main__":
    main()