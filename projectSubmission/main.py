from tkinter import *
import Untitled3
import pickle


from collections import deque, namedtuple


# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
  return Edge(start, end, cost)


class Graph:
    def __init__(self, edges):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
          return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
             ) 
           )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
             if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours
      
 
 
    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        

        # 1. Mark all nodes unvisited and store them.
        # 2. Set the distance to zero for our initial node 
        # and to infinity for other nodes.
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            # 3. Select the unvisited node with the smallest distance, 
            # it's current node now.
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])

            # 6. Stop, if the smallest distance 
            # among the unvisited nodes is infinity.
            if distances[current_vertex] == inf:
                break

            # 4. Find unvisited neighbors for the current node 
            # and calculate their distances through the current node.
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost

                # Compare the newly calculated distance to the assigned 
                # and save the smaller one.
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

            # 5. Mark the current node as visited 
            # and remove it from the unvisited set.
            vertices.remove(current_vertex)


        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
                path.appendleft(current_vertex)
                
        return path

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    


    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)


    def init(data):
            data.rows = len(Untitled3.blocks)
            data.cols = len(Untitled3.blocks[0])
            data.margin = 100 # margin around grid
            data.selection = (-1, -1) # (row, col) of selection, (-1,-1) for none
    
    

    def pointInGrid(x, y, data):
            # return True if (x, y) is inside the grid defined by data.
            return ((data.margin <= x <= data.width-data.margin) and
                    (data.margin <= y <= data.height-data.margin))

    def getCell(x, y, data):
            # aka "viewToModel"
            # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
            if (not pointInGrid(x, y, data)):
                return (-1, -1)
            gridWidth  = data.width - 2*data.margin
            gridHeight = data.height - 2*data.margin
            cellWidth  = gridWidth / data.cols
            cellHeight = gridHeight / data.rows
            row = (y - data.margin) // cellHeight
            col = (x - data.margin) // cellWidth
            # triple-check that we are in bounds
            row = min(data.rows-1, max(0, row))
            col = min(data.cols-1, max(0, col))
            return (row, col)

    def getCellBounds(row, col, data):
            # aka "modelToView"
            # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
            gridWidth  = data.width - 2*data.margin
            gridHeight = data.height - 2*data.margin
            columnWidth = gridWidth / data.cols
            rowHeight = gridHeight / data.rows
            x0 = data.margin + col * columnWidth
            x1 = data.margin + (col+1) * columnWidth
            y0 = data.margin + row * rowHeight
            y1 = data.margin + (row+1) * rowHeight
            return (x0, y0, x1, y1)

    def mousePressed(event, data):
            (row, col) = getCell(event.x, event.y, data)
            # select this (row, col) unless it is selected
            if (data.selection == (row, col)):
                data.selection = (-1, -1)
            else:
                data.selection = (row, col)

    def keyPressed(event, data):
            pass

    
    def redrawAll(canvas, data):
        
            #color = 1
            # draw grid of cells
            for row in range(data.rows):
                for col in range(data.cols):
                    (x0, y0, x1, y1) = getCellBounds(row, col, data)
                    #fill = 'orange' if (data.selection == (row, col)) else "cyan"
                    fill = Untitled3.blocks[row][col]
                    
                    if (data.selection == (row, col) and row == 3 and col == data.cols-1 ):
                        Untitled3.i=0
                    elif (data.selection == (row, col) and row == 4 and col == data.cols-1):
                        Untitled3.i=1
                    elif (data.selection == (row, col) and row == 5 and col == data.cols-1):
                        Untitled3.i=2
                    elif (data.selection == (row, col) and row == 6 and col == data.cols-1):
                        Untitled3.i=3
                    elif (data.selection == (row, col) and row == 7 and col == data.cols-1):
                        Untitled3.i=4
                    
                    elif (data.selection == (row, col) and col< data.cols-1):
                        Untitled3.blocks[row][col]= Untitled3.colors[Untitled3.i] 
                    canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
                    canvas.create_text(575, 235, text="Road",font="Arial 13 bold", fill="black")
                    canvas.create_text(575, 315, text="Vacant",font="Arial 13 bold", fill="black")
                    canvas.create_text(575, 285, text="Blank",font="Arial 13 bold", fill="black")
                    canvas.create_text(575, 360, text="Full",font="Arial 13 bold", fill="black")
                    canvas.create_text(575, 400, text="Locn",font="Arial 13 bold", fill="white")
                    pickle_out = open("Untitled3.blocks", "wb")
                    pickle.dump(Untitled3.blocks, pickle_out)
                    pickle_out.close()


    # Set up data and call init
    class Struct(object): pass
    data = Struct()
   
    data.width = width
    data.height = height
    root = Tk()


    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    
    

    root.title ('Parking Lot')
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    #color = 1
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("Happy Journey!")


#import back.py to use the blocks list



#store the coordinates of all the cells which are grey or green in a list
node_list = []

for row in range(len(Untitled3.blocks)):
    for col in range(len(Untitled3.blocks[0])):
        if Untitled3.blocks[row][col] == 'grey' or Untitled3.blocks[row][col] == 'green':
            node_list.append((row,col))

#simple sort function to find all the paths
path_list1 = []
for i in range(len(node_list)-1):
    
    for j in range(1+i, len(node_list)):
         
        if (abs(node_list[i][0] - node_list[j][0])==1 and node_list[i][1] - node_list[j][1]== 0) or (abs(node_list[i][1] - node_list[j][1])==1 and node_list[i][0] - node_list[j][0]== 0):
            path_list1.append(((node_list[i]),(node_list[j])))
#user_location = input("Please enter your location in (x,y) format: ")
#parkingspot_location = input("Please enter the parking spot of your choice in (x,y) format: ")


while True:
  
    choice=input("Create or Navigate?")
    if choice=="Create":
        run(700,600)
    elif choice=="Navigate":
        print("Click on the black block on the extreme right and mark your location on the grid")
        run(700,600)
          
        CarLocation_x=-1
        CarLocation_y=-1
        CarLocation=(CarLocation_x,CarLocation_y)
        for x in range(10):
            for y in range(9):
                if Untitled3.blocks[x][y]=='black':
                    CarLocation_x=x
                    CarLocation_y=y
                    CarLocation=(CarLocation_x,CarLocation_y)

                    node_list = []
                    valid_list = []
                    node_list_final = []
                    green_list = []
                    Start_End = []
                    Start_End_len = []
                    Start_End_index = []


                    for row in range(len(Untitled3.blocks)):
                        for col in range(len(Untitled3.blocks[0])-1):
                            if Untitled3.blocks[row][col] == 'grey' or Untitled3.blocks[row][col] == 'green' or Untitled3.blocks[row][col] == 'black':
                                valid_list.append((row,col))

                    #simple sort function to find all the paths
                    path_list = []
                    for i in range(len(valid_list)-1):
                        
                        for j in range(1+i, len(valid_list)):
                            
                            if (abs(valid_list[i][0] - valid_list[j][0])==1 and valid_list[i][1] - valid_list[j][1]== 0) or (abs(valid_list[i][1] - valid_list[j][1])==1 and valid_list[i][0] - valid_list[j][0]== 0):
                                node_list.append(((valid_list[i]),(valid_list[j])))

                    for i in range(len(node_list)):
                        node_list_final.append((node_list[i][0],node_list[i][1], 1))

                    for row in range(len(Untitled3.blocks)):
                        for col in range(len(Untitled3.blocks[0])-1):
                            if Untitled3.blocks[row][col] == 'green':
                                green_list.append((row,col))


                    #print(graph.dijkstra(CarLocation, green_list[1]))



                    for i in range(len(green_list)):
                        Start_End.append((CarLocation, green_list[i]))

                    graph = Graph(node_list_final)

                    for i in range(len(Start_End)):
                        Start_End_index.append(i)
                        graph = Graph(node_list_final)
                        Start_End_len.append(len((graph.dijkstra(CarLocation, green_list[i]))))
                    #print(Start_End_len)

                    for passnum in range(len(Start_End_len)-1):
                        swapped = False
                        for i in range(len(Start_End_len)-1):
                            if Start_End_len[i]<Start_End_len[i+1]:
                                temp = Start_End_len[i]
                                Start_End_len[i]= Start_End_len[i+1]
                                Start_End_len[i+1]= temp

                                const = Start_End_index[i]
                                Start_End_index[i]= Start_End_index[i+1]
                                Start_End_index[i+1]= const
                                swapped= True
                        if not swapped:
                            break

                    Target_block = Start_End[Start_End_index[0]][1]

                    print("The closest parking space to you is: ",Target_block)                                #Closest available parking lot
                    graph = Graph(node_list_final)
                    print(graph.dijkstra(CarLocation, Target_block))   #path    
        
        
    else:
      break