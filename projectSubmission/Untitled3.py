import pickle

blocks = [[0 for x in range(10)] for y in range(10)] 
colors = ("grey", "white", "green", "red", "black")
i = 0
for x in range(10):
    for y in range(10):
        blocks[x][y]= "white"

blocks[3][9]= 'grey'
blocks[4][9]= 'white'
blocks[5][9]= 'green'
blocks[6][9]= 'red'

# pickle_in = open("Untitled3.blocks", "rb")
# blocks = pickle.load(pickle_in)

print(len(blocks))
print(len(blocks[0]))

print(blocks[1][1])