from copy import deepcopy
import random
import time

class Node:
    def __init__(self,parent,children,depth,state,moves):
        self.parent = parent
        self.children = children
        self.depth = depth
        self.state = state
        self.moves = moves


#function to expand node.
def expand(node):
    new_nodes = []
    for row in range(len(node.state)):
        for column in range(len(node.state[0])):

            #when 0 (empty point) is found, we have to check if there is available move to fill the empty space.
            #The way of checking this is looking for two 1's in a row or column. if there is two pegs consecutively,
            #then we can say that there is a possible move.
            if node.state[row][column] == 0:
                try:

                    #up side checking
                    if node.state[row-1][column] == 1 and node.state[row-2][column] == 1 and row-1>=0 and row -2>=0:
                        all_moves = deepcopy(node.moves)
                        new_move = str(row-2)+" "+ str(column)+ " -> " + str(row)+" "+ str(column) #possible move
                        all_moves.append(new_move)

                        temp_state = deepcopy(node.state)
                        temp_state[row][column] = 1
                        temp_state[row-1][column] = 0
                        temp_state[row-2][column] = 0
                        new_node = Node(node,any,node.depth+1,temp_state,all_moves)
                        new_nodes.append(new_node)

                    #right side checking
                    if node.state[row][column+1] == 1 and node.state[row][column+2] == 1:
                        all_moves = deepcopy(node.moves)
                        new_move = str(row)+" "+ str(column+2)+ " -> " + str(row)+" "+ str(column) #possible move
                        all_moves.append(new_move)

                        temp_state = deepcopy(node.state)
                        temp_state[row][column] = 1
                        temp_state[row][column+1] = 0
                        temp_state[row][column+2] = 0
                        new_node = Node(node,any,node.depth+1,temp_state,all_moves)
                        new_nodes.append(new_node)
                        
                    #left side checking
                    if node.state[row][column-1] == 1 and node.state[row][column-2] == 1 and column-1>=0 and column-2 >=0:
                        all_moves = deepcopy(node.moves)
                        new_move = str(row)+" "+ str(column-2)+ " -> " + str(row)+" "+ str(column) #possible move
                        all_moves.append(new_move)

                        temp_state = deepcopy(node.state)
                        temp_state[row][column] = 1
                        temp_state[row][column-1] = 0
                        temp_state[row][column-2] = 0
                        new_node = Node(node,any,node.depth+1,temp_state,all_moves)
                        new_nodes.append(new_node)

                    #down side checking
                    if node.state[row+1][column] == 1 and node.state[row+2][column] == 1:
                        all_moves = deepcopy(node.moves)
                        new_move = str(row+2)+" "+ str(column)+ " -> " + str(row)+" "+ str(column) #possible move
                        all_moves.append(new_move)

                        temp_state = deepcopy(node.state)
                        temp_state[row][column] = 1
                        temp_state[row+1][column] = 0
                        temp_state[row+2][column] = 0
                        new_node = Node(node,any,node.depth+1,temp_state,all_moves)
                        new_nodes.append(new_node)

                except IndexError:
                    continue
    #returns new_nodes in an array.
    return new_nodes

#finding remaining pegs and s will be zero if algorithm reaches goal state.
def score(node):
    # Count all pegs
    s = 0
    for peg in [p for row in node.state for p in row]:
        s += 1 if peg == 1 else 0

    # If there is only one peg left and it is in the center, the score is 0.
    if s == 1 and node.state[3][3] == 1:
        s = 0

    return s


def breadthFirstSearch(frontier,time_limit,initial_node,visited_node_array,start,elapsed,maxnode,expanded_node_number):
    try:
        while frontier and elapsed <= time_limit: 
            #checks the goal state is found or not.
            s = score(frontier[0])
            best_solution_found = False
            if s == 0:
                print("Optimum solution found.")

                print("Initial State: ")
                for row in initial_node.state:
                    print(row)


                print("")
                print("Board State: ")
                for row in frontier[0].state:
                    print(row) 


                print("The time spent: " + str(elapsed))
                print("The number of nodes expanded during the search: " + str(expanded_node_number))
                print("Max number of nodes stored in the memory during the search: " + str(maxnode))
                print("All moves to get goal solution from the beginning: ")
                for move in frontier[0].moves:
                    print(move)
                best_solution_found = True
                break
            else:
                new_nodes=expand(frontier[0])

                #increasing expanded node number count after calling expand function.
                expanded_node_number += 1

                #adding visited nodes to visited node array.
                visited_node_array.append(frontier[0])
                frontier.pop(0)

                #adding new children nodes to frontier after popping first item of frontier.
                frontier.extend(new_nodes)
                elapsed = time.time() - start

                #finding maximum node that is stored in frontier during all runtime.
                if (len(frontier) > maxnode):
                    maxnode = len(frontier)

    except MemoryError:
        print("No solution found - Out of Memory")


    # TIME LIMIT  
    if elapsed >= time_limit or best_solution_found == False:
        print("")
        #we assume that last visited node is the best solution.
        remaining_peg=score(visited_node_array[-1])
        print("No solution found - Time Limit.Sub-optimum Solution Found with " +str(remaining_peg)+ " remaining pegs")

        print("Initial State: ")
        for row in initial_node.state:
            print(row)
        print("")

        #Printing board state of sub-optimum solution.
        print("New Board State: ")
        for row in visited_node_array[-1].state:
            print(row)

        print("The time spent: " + str(elapsed))
        print("The number of nodes expanded during the search: " + str(expanded_node_number))
        print("Max number of nodes stored in the memory during the search: " + str(maxnode))
        print("All moves to get this solution from the beginning: ")
        for move in visited_node_array[-1].moves:
            print(move)



def depthFirstSearch(frontier,time_limit,initial_node,visited_node_array,start,elapsed,maxnode,expanded_node_number):
    try:
        while frontier and elapsed <= time_limit: 
            s = score(frontier[-1])
            best_solution_found = False
            if s == 0:
                #optimum solution found.

                print("Optimum solution found.")
                print("Initial State: ")
                for row in initial_node.state:
                    print(row)
                print("")
                print("Board State: ")
                for row in frontier[-1].state:
                    print(row)     
                print("The time spent: " + str(elapsed))
                print("The number of nodes expanded during the search: " + str(expanded_node_number))
                print("Max number of nodes stored in the memory during the search: " + str(maxnode))
                print("All moves to get goal solution from the beginning: ")
                for move in frontier[-1].moves:
                    print(move)
                best_solution_found = True
                break

            else:
                new_nodes = expand(frontier[-1])

                #increasing expanded node number count after calling expand function.
                expanded_node_number += 1

                #adding visited nodes to visited node array.
                visited_node_array.append(frontier[-1])
                frontier.pop()
                #new_nodes.reverse()

                #adding new children nodes to frontier after popping last item of frontier.
                frontier.extend(new_nodes)
                
                #finding maximum node that is stored in frontier during all runtime.
                if (len(frontier) > maxnode):
                    maxnode = len(frontier)
                
                elapsed = time.time() - start

    except MemoryError:
        print("No solution found - Out of Memory")
            
    # TIME LIMIT  
    if elapsed >= time_limit or best_solution_found == False:
        print("")
        #we assume that last visited node is the best solution initally, but after that 
        #we'll search visited node array to find best solution.
        best_solution = visited_node_array[-1]
        remaining_peg=score(best_solution)

        for node in visited_node_array:
            if score(node) < remaining_peg:
                best_solution = node
                remaining_peg = score(node)
        
        #finding best solution's remaining pegs.
        remaining_peg = score(best_solution) 
        print("No solution found - Time Limit. Sub-optimum Solution Found with " +str(remaining_peg)+ " remaining pegs.")
        
        print("Initial State: ")
        for row in initial_node.state:
            print(row)
        print("")
        #Printing board state of sub-optimum solution.
        print("New Board State: ")
        for row in best_solution.state:
            print(row)

        print("The time spent: " + str(elapsed))
        print("The number of nodes expanded during the search: " + str(expanded_node_number))
        print("Max number of nodes stored in the memory during the search: " + str(maxnode))
        print("All moves to get this solution from the beginning: ")
        for move in best_solution.moves:
            print(move)


def iterativeDeepeningSearch(frontier,time_limit,initial_node,visited_node_array,start,elapsed,maxnode,expanded_node_number):

    iteration = 0
    #iteration will be increased after each iteration
    while iteration <= 32:

        try:    
            while frontier and elapsed <= time_limit: 
                s = score(frontier[-1])
                best_solution_found = False
                if s == 0:
                    #optimum solution found.

                    print("Optimum solution found.")
                    print("Initial State: ")
                    for row in initial_node.state:
                        print(row)
                    print("")
                    print("Board State: ")
                    for row in frontier[-1].state:
                        print(row)     
                    print("The time spent: " + str(elapsed))
                    print("The number of nodes expanded during the search: " + str(expanded_node_number))
                    print("Max number of nodes stored in the memory during the search: " + str(maxnode))
                    print("All moves to get goal solution from the beginning: ")
                    for move in frontier[-1].moves:
                        print(move)
                    iteration = 33  #to exit outer while loop.
                    best_solution_found = True
                    break

                else:
                    if frontier[-1].depth <= iteration:
                        new_nodes = expand(frontier[-1])
                        #increasing expanded node number count after calling expand function.
                        expanded_node_number += 1

                        #adding visited nodes to visited node array.
                        visited_node_array.append(frontier[-1])
                        frontier.pop()
                        #new_nodes.reverse()

                        #adding new children nodes to frontier after popping last item of frontier.
                        frontier.extend(new_nodes)
                        elapsed = time.time() - start
                        #finding maximum node that is stored in frontier during all runtime.
                        if (len(frontier) > maxnode):
                            maxnode = len(frontier)
                    else:
                        break

            #algorithm will search nodes from the beginning.              
            frontier.clear()
            frontier.append(initial_node)
            iteration +=1
            
        except MemoryError:
            print("No solution found - Out of Memory")

    # TIME LIMIT            
    if elapsed >= time_limit or best_solution_found == False:
        print("")
        #we assume that last visited node is the best solution initally, but after that 
        #we'll search visited node array to find best solution.
        best_solution = visited_node_array[-1]
        remaining_peg=score(best_solution)

        for node in visited_node_array:
            if score(node) < remaining_peg:
                best_solution = node
                remaining_peg = score(node)
        
        #finding best solution's remaining pegs.
        remaining_peg = score(best_solution) 
        print("No solution found - Time Limit. Sub-optimum Solution Found with " +str(remaining_peg)+ " remaining pegs.")
        
        print("Initial State: ")
        for row in initial_node.state:
            print(row)
        print("")
        #Printing board state of sub-optimum solution.
        print("New Board State: ")
        for row in best_solution.state:
            print(row)

        print("The time spent: " + str(elapsed))
        print("The number of nodes expanded during the search: " + str(expanded_node_number))
        print("Max number of nodes stored in the memory during the search: " + str(maxnode))
        print("All moves to get this solution from the beginning: ")
        for move in best_solution.moves:
            print(move)

def DFSRandomSelectionSearch(frontier,time_limit,initial_node,visited_node_array,start,elapsed,maxnode,expanded_node_number):
    random_node = initial_node
    try:
        while frontier and elapsed <= time_limit: 
            s = score(random_node)
            best_solution_found = False
            if s == 0:
                #optimum solution found.
                print("Optimum solution found.")
                print("Initial State: ")
                for row in initial_node.state:
                    print(row)
                print("")
                print("Board State: ")
                for row in random_node.state:
                    print(row)     
                print("The time spent: " + str(elapsed))
                print("The number of nodes expanded during the search: " + str(expanded_node_number))
                print("Max number of nodes stored in the memory during the search: " + str(maxnode))
                print("All moves to get goal solution from the beginning: ")
                for move in random_node.moves:
                    print(move)
                break
                best_solution_found = True
            else:
                new_nodes = expand(random_node)
                expanded_node_number += 1

                #we are looking for the node that has no children. We want to go back to parents if this is an issue.
                if new_nodes==[]:
                    siblings = []
                    for node in frontier:
                        if node.parent == visited_node_array[-1].parent:
                            siblings.append(node)
                    if siblings == []:
                        while siblings != []: 
                            parent = visited_node_array[-1].parent
                            for node in frontier:
                                if node.parent == parent.parent:
                                    siblings.append(node)
                            random_node = random.choice(siblings)
                    else:
                        random_node = random.choice(siblings)

                else:
                    try: 
                        frontier.remove(random_node)
                    except ValueError:
                        pass
                    visited_node_array.append(random_node)
                    random_node = random.choice(new_nodes)
                    new_nodes.remove(random_node)
                    frontier.extend(new_nodes)
                    
                #finding maximum node that is stored in frontier during all runtime.
                if (len(frontier) > maxnode):
                    maxnode = len(frontier)
                
                elapsed = time.time() - start

    except MemoryError:
        print("No solution found - Out of Memory")
    

    # TIME LIMIT  
    if elapsed >= time_limit or best_solution_found == False:
        print("")
        #we assume that last visited node is the best solution initally, but after that 
        #we'll search visited node array to find best solution.
        best_solution = visited_node_array[-1]
        remaining_peg=score(best_solution)

        for node in visited_node_array:
            if score(node) < remaining_peg:
                best_solution = node
                remaining_peg = score(node)
        
        #finding best solution's remaining pegs.
        remaining_peg = score(best_solution) 
        print("No solution found - Time Limit. Sub-optimum Solution Found with " +str(remaining_peg)+ " remaining pegs.")
        
        print("Initial State: ")
        for row in initial_node.state:
            print(row)
        print("")
        #Printing board state of sub-optimum solution.
        print("New Board State: ")
        for row in best_solution.state:
            print(row)

        print("The time spent: " + str(elapsed))
        print("The number of nodes expanded during the search: " + str(expanded_node_number))
        print("Max number of nodes stored in the memory during the search: " + str(maxnode))
        print("All moves to get this solution from the beginning: ")
        for move in best_solution.moves:
            print(move)


def DFSWithHeuristic(frontier,time_limit,initial_node,visited_node_array,start,elapsed,maxnode,expanded_node_number):
    try:
        while frontier and elapsed <= time_limit: 
            s = score(frontier[-1])
            best_solution_found = False
            if s == 0:
                #optimum solution found.

                print("Optimum solution found.")
                print("Initial State: ")
                for row in initial_node.state:
                    print(row)
                print("")
                print("Board State: ")
                for row in frontier[-1].state:
                    print(row)     
                print("The time spent: " + str(elapsed))
                print("The number of nodes expanded during the search: " + str(expanded_node_number))
                print("Max number of nodes stored in the memory during the search: " + str(maxnode))
                print("All moves to get goal solution from the beginning: ")
                for move in frontier[-1].moves:
                    print(move)
                best_solution_found = True
                break

            else:
                new_nodes = expand(frontier[-1])

                #increasing expanded node number count after calling expand function.
                expanded_node_number += 1

                #adding visited nodes to visited node array.
                visited_node_array.append(frontier[-1])
                frontier.pop()
                #new_nodes.reverse()

                #calling heuristic function.
                new_nodes = heuristic(new_nodes)
                    
                #adding new children nodes to frontier after popping last item of frontier.
                frontier.extend(new_nodes)
                
                #finding maximum node that is stored in frontier during all runtime.
                if (len(frontier) > maxnode):
                    maxnode = len(frontier)
                
                elapsed = time.time() - start

    except MemoryError:
        print("No solution found - Out of Memory")
            
    # TIME LIMIT  
    if elapsed >= time_limit or best_solution_found == False:
        print("")
        #we assume that last visited node is the best solution initally, but after that 
        #we'll search visited node array to find best solution.
        best_solution = visited_node_array[-1]
        remaining_peg=score(best_solution)

        for node in visited_node_array:
            if score(node) < remaining_peg:
                best_solution = node
                remaining_peg = score(node)
        
        #finding best solution's remaining pegs.
        remaining_peg = score(best_solution) 
        print("No solution found - Time Limit. Sub-optimum Solution Found with " +str(remaining_peg)+ " remaining pegs.")
        
        print("Initial State: ")
        for row in initial_node.state:
            print(row)
        print("")
        #Printing board state of sub-optimum solution.
        print("New Board State: ")
        for row in best_solution.state:
            print(row)

        print("The time spent: " + str(elapsed))
        print("The number of nodes expanded during the search: " + str(expanded_node_number))
        print("Max number of nodes stored in the memory during the search: " + str(maxnode))
        print("All moves to get this solution from the beginning: ")
        for move in best_solution.moves:
            print(move)


#CHECKING IF THERE IS A CORNER PEG CAN BE SELECTED TO MAKE A MOVE.
def heuristic(new_nodes):
    for node in new_nodes:
        move = node.moves[-1]
        if ((move == str(0)+" "+ str(2)+ " -> " + str(0)+" "+ str(4)) or
            (move == str(0)+" "+ str(2)+ " -> " + str(2)+" "+ str(2)) or
            (move == str(0)+" "+ str(4)+ " -> " + str(0)+" "+ str(2)) or
            (move == str(0)+" "+ str(4)+ " -> " + str(2)+" "+ str(4)) or
            (move == str(2)+" "+ str(0)+ " -> " + str(2)+" "+ str(2)) or
            (move == str(2)+" "+ str(0)+ " -> " + str(4)+" "+ str(0)) or
            (move == str(2)+" "+ str(6)+ " -> " + str(2)+" "+ str(4)) or
            (move == str(2)+" "+ str(6)+ " -> " + str(4)+" "+ str(6)) or
            (move == str(4)+" "+ str(0)+ " -> " + str(4)+" "+ str(2)) or
            (move == str(4)+" "+ str(0)+ " -> " + str(2)+" "+ str(0)) or
            (move == str(4)+" "+ str(6)+ " -> " + str(4)+" "+ str(4)) or
            (move == str(4)+" "+ str(6)+ " -> " + str(2)+" "+ str(6)) or
            (move == str(6)+" "+ str(2)+ " -> " + str(6)+" "+ str(4)) or
            (move == str(6)+" "+ str(2)+ " -> " + str(4)+" "+ str(2)) or
            (move == str(6)+" "+ str(4)+ " -> " + str(6)+" "+ str(2)) or
            (move == str(6)+" "+ str(4)+ " -> " + str(4)+" "+ str(4))):
            

            #if there is a move comes from corner peg, then we took that node to end of the frontier
            #by removing and adding again at the end of the list.
            
            new_nodes.remove(node)
            new_nodes.append(node)
            
    return new_nodes





def main():
    initial_state = [[2,2,1,1,1,2,2],
                     [2,2,1,1,1,2,2],
                     [1,1,1,1,1,1,1],
                     [1,1,1,0,1,1,1],
                     [1,1,1,1,1,1,1],
                     [2,2,1,1,1,2,2],
                     [2,2,1,1,1,2,2]]
    initial_node = Node(any,any,0,initial_state,list())
    
    
    frontier = []
    frontier.append(initial_node)

    start = time.time()
    #time
    elapsed = 0
    maxnode = 0
    expanded_node_number = 0
    visited_node_array = []
    
    #INPUTS OF THE PROGRAM
    print()
    print("Please select a search method by writing 'a', 'b', 'c', 'd' or 'e'.")
    print("a. Breadth-First Search\nb. Depth-First Search\nc. Iterative Deepening Search\nd. Depth-First Search with Random Selection\ne. Depth-First Search with a Node Selection Heuristic")
    search_method = input()
    print()
    print("Please choose a time limit in terms of seconds.")
    time_limit = eval(input())
    
    if search_method == 'a':
        print("The Search Method is Breadth First Search. Time limit is " + str(time_limit) + " seconds.")
        breadthFirstSearch(frontier,time_limit,initial_node,visited_node_array,start,elapsed,maxnode,expanded_node_number)
    elif search_method == 'b':
        print("The Search Method is Depth First Search. Time limit is " + str(time_limit) + " seconds.")
        depthFirstSearch(frontier,time_limit,initial_node,visited_node_array,start,elapsed,maxnode,expanded_node_number)
    elif search_method == 'c':
        print("The Search Method is Iterative Deepening Search. Time limit is " + str(time_limit) + " seconds.")
        iterativeDeepeningSearch(frontier,time_limit,initial_node,visited_node_array,start,elapsed,maxnode,expanded_node_number)
    elif search_method == 'd':
        print("The Search Method is Depth-First Search with Random Selection. Time limit is " + str(time_limit) + " seconds.")
        DFSRandomSelectionSearch(frontier,time_limit,initial_node,visited_node_array,start,elapsed,maxnode,expanded_node_number)
    elif search_method == 'e':
        print("The Search Method is Depth-First Search with a Node Selection Heuristic. Time limit is " + str(time_limit) + " seconds.")
        DFSWithHeuristic(frontier,time_limit,initial_node,visited_node_array,start,elapsed,maxnode,expanded_node_number)
    else:
        print("Invalid input. Please run program again.")
        
    
main()





