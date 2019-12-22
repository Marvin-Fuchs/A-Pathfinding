from tkinter import *
import random
import time

class Grid:
    def __init__(self,master,rows,cols,size,space,startX,startY,endX,endY):
        self.rows = rows
        self.cols = cols
        self.size = size
        self.space = space
        self.master = master
        #backEnd
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        self.data = []
    def draw(self):
        for i in range(self.rows):
            row=[]
            for j in range(self.cols):
                self.master.create_rectangle(j*self.size+self.space, i*self.size+self.space, j*self.size+self.size+self.space, i*self.size+self.size+self.space, fill="black", outline="white")
                row.append(0)
            self.data.append(row)
        self.data[self.startY][self.startX]='S'
        self.data[self.endY][self.endX]='E'
    def markNode(self,row,col,color):
        self.master.create_rectangle(col*self.size+self.space, row*self.size+self.space, col*self.size+self.size+self.space, row*self.size+self.size+self.space, fill=color, outline="white")
    def event(self,event):
        print(self.rows)
        row, col = (event.y-self.space)//self.size, (event.x-self.space)//self.size 
        if (0 <= row and row < self.rows and 0 <= col and col < self.cols):
            if not(row==self.startX and col==self.startY) and not(row==self.endX and col==self.endY):
                self.markNode(row,col,"grey")
                self.data[row][col]=1
    def printBoard(self):
        for row in self.data:
            print(row)

class Pathfinder(Grid):
    def __init__(self,master,rows,cols,size,space,startX,startY,endX,endY):
        Grid.__init__(self,master,rows,cols,size,space,startX,startY,endX,endY)
        self.draw()

    def findPath(self):
        # # init of open and closed List
        self.openList = []
        self.closedList = []
        self.startPos = (self.startX,self.startY)
        self.endPos = (self.endX,self.endY)
        #start node is in self.openList with fCost=0
        self.openList.append( {"nodePos":(self.startY,self.startX),"f":0,"g":0,"h":0,"parentPos":(0,9)} ) #node notation
        #repeat until either
        # - self.openList is empty (len==0)
        # - currentNode is endNode
        while len(self.openList)>0:
            # self.printOpenList()
            # self.printClosedList()
            #checks for the node with hightest priority in queue
            # (aka looks for lowest f-cost node in self.openList and pops it out of the self.openList)
            currentNode = self.removeMin()
            # print()
            # print("NODE:")
            # print(currentNode)
            #did we reach the endNode?
            if currentNode["nodePos"]==self.endPos:
                print("we made it")
                self.regoPath(currentNode)
                return True
            #we found the shortest possilbe path to the currentNode
            #to prevent futher unnecessary checking, lets append it to the self.closedList
            self.closedList.append(currentNode)
            self.markNode(currentNode["nodePos"][0],currentNode["nodePos"][1],"orange")
            #add the surrounding Nodes (neighbor nodes) to the self.openList
            self.addNeighborNodes(currentNode)
        return False #no path found

    def addNeighborNodes(self,currentNode):
        newWave = []
        currentPos = currentNode["nodePos"]
        posY, posX = currentPos
        left,right,bottom,top=-1,1,-1,1
        if posY == rows-1:
            top = 0
        if posY == 0:
            bottom = 0
        if posX == cols-1:
            right = 0
        if posX == 0:
            left = 0
        for i in list(range(bottom,top+1)):                
            for j in list(range(left,right+1)):                
                #no problem with diagonals because only (...): 

                    # X ... X
                    #... X ... are neighbors (X not)            
                    # X ... X
                                                            
                if (i==0 and j==0) or (i!=0 and abs(j)==1) or (self.data[posY+i][posX+j]==1):           
                    continue
                #if neigboor is already in self.closedList, skip it. No need to check again!
                pos = (posY+i,posX+j)
                if self.closedListContainsNodeWithPosition(pos):
                    continue
                #calculate new or updated gCost
                gCost = currentNode["g"] + 1
                #if neigboor is already in self.openList 
                #and his current g is lower than the new g 
                # aka (old way is better than current)   ----> Continue
                indexOfNode = self.openListContainsNodeWithPosition(pos)
                # print("!!!!!!!!!!")
                # print(pos,indexOfNode)
                # print("¡¡¡¡¡¡¡¡¡¡")
                if indexOfNode!=-1:
                    if self.openList[indexOfNode]["g"]<=gCost:
                        continue
                #if neigbor does not already exists in open list, create a new node with f,g,h and its parent 
                #else (if neigbhor already exists in open list then change f,g and its parent)
                if indexOfNode==-1:
                    h = self.manhattanDistanceFromPosToEndPos(pos)
                    self.openList.append({"nodePos":pos,"f":gCost+h,"g":gCost,"h":h,"parentPos":currentPos})
                    newWave.append(pos)
                else:
                    self.openList[indexOfNode]["g"] = gCost
                    self.openList[indexOfNode]["f"] = gCost + self.openList[indexOfNode]["h"]
                    self.openList[indexOfNode]["parentPos"] = currentPos
        self.visualizeWave(newWave)
        self.master.update()
        time.sleep(0.01)

    def visualizeWave(self, newWave):
        for node in newWave:
            self.markNode(node[0],node[1],"white")

    def manhattanDistanceFromPosToEndPos(self,pos):
        posY, posX = pos
        return abs(posY-self.endPos[0])+abs(posX-self.endPos[1])

    def removeMin(self):
        min = self.openList[0]["f"]
        minNode = self.openList[0]
        index = 0
        for i in range(len(self.openList)):
            if self.openList[i]["f"]<min:
                min = self.openList[i]["f"]
                minNode = self.openList[i]
                index = i

        # print("BEFORE POP")
        # for element in self.openList:
        #   print(element)
        self.openList.pop(index)
        # print("INBETWEENPOP")
        # for element in self.openList:
        #   print(element)
        # print("AFTER POP")
        return minNode

    def regoPath(self,currentNode):
        print("A*´s Suggestion:")
        print(currentNode["nodePos"])
        self.markNode(currentNode["nodePos"][0],currentNode["nodePos"][1],"red")
        while currentNode["parentPos"]!=self.startPos:
            print(currentNode["parentPos"])
            self.markNode(currentNode["nodePos"][0],currentNode["nodePos"][1],"red")
            currentNode = self.findParentNode(currentNode["parentPos"])
        print(self.startPos)
        self.markNode(currentNode["nodePos"][0],currentNode["nodePos"][1],"red")

    def findParentNode(self,parentPos):
        for element in self.closedList:
            if element["nodePos"]==parentPos:
                return element
        return None

    def closedListContainsNodeWithPosition(self,nodePos):
        for node in self.closedList:
            if node["nodePos"]==nodePos:
                return True
        return False

    def openListContainsNodeWithPosition(self,nodePos):
        for i in range(len(self.openList)):
            if self.openList[i]["nodePos"]==nodePos:
                return i
        return -1

    def printOpenList(self):
        print("------------------------------------------------------")
        print("self.openList")
        for element in self.openList:
            print(element)
        print() 

    def printClosedList(self):
        print("self.closedList")
        for element in self.closedList:
            print(element)
        print()

#defining rows and cols
rows,cols=30,30
def main():
    setup=True
    size=30
    space=3
    width,height = 903,921
    #StartNode
    startY,startX = 2,20
    #EndNode
    endY,endX = 15,20
    root = Tk()
    root.title('A*')
    canvas = Canvas(width=width, height=height)
    canvas.pack()
    #draw grid and create backend data
    aS = Pathfinder(canvas,rows,cols,size,space,startX,startY,endX,endY)
    #Start- und Endpunkt
    aS.markNode(startX,startY,"orange")
    aS.markNode(endX,endY,"red")
    #setup of boundaries
    canvas.bind("<B1-Motion>", aS.event)
    #A* Algorithm runs
    button = Button(canvas, text="run A*", command=aS.findPath).place(x=width/2-18,y=height-18)
    
    #A* Algorithm
    root.mainloop()

if __name__== "__main__":
  main()

