import os
import RB_Tree

fileList = []

filenames = os.listdir('./input/')
for filename in filenames:
    tree = RB_Tree.rbtree()
    f = open('./input/'+filename, 'r')
    lines = f.readlines()
    for line in lines:
        value = int(line)
        #print("InputVal : " + str(value))
        if value > 0 :
            tree.insert_key(value)
        elif value < 0 :
            tree.delete_key(-value)
        elif value == 0 :
            tree.inorder_traverse()
            print("filename= " + filename)
            print("total= " + str(tree.totalCount))
            print("insert= " + str(tree.insertCount))
            print("deleted= " + str(tree.deleteCount))
            print("miss= " + str(tree.missCount))
            print("nb= " + str(tree.blackCount))
            print("bh= "+ str(tree.get_black_height()))
            for node in tree.inorderTraverseList:
                print(str(node.key), end = " ")
                if node.red :
                    print("R")
                else :
                    print("B")
    print("==========")  
print("END")
