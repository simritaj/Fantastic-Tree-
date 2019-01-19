#import back.py to use the blocks list
import back 


#store the coordinates of all the cells which are grey or green in a list
node_list = []

for row in range(len(back.blocks)):
    for col in range(len(back.blocks[0])):
        if back.blocks[row][col] == 'grey' or back.blocks[row][col] == 'green':
            node_list.append((row,col))

#simple sort function to find all the paths
path_list = []
for i in range(len(node_list)-1):
    
    for j in range(1+i, len(node_list)):
         
        if (abs(node_list[i][0] - node_list[j][0])==1 and node_list[i][1] - node_list[j][1]== 0) or (abs(node_list[i][1] - node_list[j][1])==1 and node_list[i][0] - node_list[j][0]== 0):
            path_list.append(((node_list[i]),(node_list[j])))

print(path_list)
