#-------------------------------------------------------------------------------
# Name:        Candidate Selector
# Purpose:	   To select the best candidates
#
# Author:      Arun Osborn
#
# Created:     05/10/2020
# Copyright:   (c) AOs Productions 2020
# Version:	   0.1
#-------------------------------------------------------------------------------

from tkinter import *

def file_len(fname):
    i=-1
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

members = 245 #Manually enter member count
totalUp = 0
totalDown = 0
#Had 152 total votes last time

array = []
def inputArray():
	global totalUp
	global totalDown
	global array
	array = []
	name = ""
	name = input("Enter name of candidate\nEnter 'import' to import saved array")
	if name == "import":
		array = importArray()
		return array
	while name != "":
		up = int(input("Input up-votes"))
		totalUp += up
		down = int(input("Input down-votes"))
		totalDown += down
		array.append([name,up,down])
		name = input("Enter name of candidate (leave blank to stop)")
	return array

def exportArray():
	global array
	arrayFile = open("candidates.txt","w")
	for x in range(len(array)):
		arrayFile.write(array[x][0]+","+str(array[x][1])+","+str(array[x][2])+"\n")
	arrayFile.close()

def importArray():
	global totalUp
	global totalDown
	global array
	try:
		arrayFile = open("candidates.txt","r")
	except FileNotFoundError:
		return []
	array = []
	for x in range(file_len("candidates.txt")):
		line = arrayFile.readline()
		array.append(line.split(","))
		array[x][1] = int(array[x][1])
		array[x][2] = int(array[x][2])
	arrayFile.close()

	totalUp = 0
	totalDown = 0
	for x in range(len(array)):
		totalUp += array[x][1]
		totalDown += array[x][2]

def calculateResults():
	global resultsArray
	global totalUp
	global totalDown
	global array
	candidateNo = len(array)
	votesPerMember = (totalUp+totalDown)/members
	averageUp = totalUp/candidateNo
	averageDown = totalDown/candidateNo
	resultsArray = []
	print("Election Results:")
	for x in range(candidateNo):
		if array[x][1] > averageUp: #Upvotes must be more than average
			if array[x][1] > array[x][2]*2: #Must have at least 2X more upvotes than downvotes
				if array[x][2] < round(totalDown/2): #Candidates has less than half the total amount of downvotes
					if array[x][1]-array[x][2] > members*2/(totalUp+totalDown): #Checks if score is high enough compared to voters. (The more members that vote, the more elected)
						print("\n   MEMBER ELECTED : "+array[x][0]+"\n   Upvotes :",array[x][1],"\n   Downvotes :",array[x][2])
						resultsArray.append(str("MEMBER ELECTED : "+array[x][0]+"\n   Upvotes :"+str(array[x][1])+"\n   Downvotes :"+str(array[x][2])))
					else:
						print("\n   "+array[x][0]+" didn't have a high enough vote proportion (A score higher than",round((0.5+members*2/(totalUp+totalDown))*10)/10,"was needed but only a score of ",(array[x][1]-array[x][2]),"was gotten)")
						resultsArray.append(str(array[x][0]+" didn't have a high enough vote proportion (A score higher than",round((0.5+members*2/(totalUp+totalDown))*10)/10,"was needed but only a score of ",(array[x][1]-array[x][2]),"was gotten)"))
				else:
					print("\n   "+array[x][0]+" has more than half of the total downvotes")
					resultsArray.append(str(array[x][0]+" has more than half of the total downvotes"))
			else:
				print("\n   "+array[x][0]+" has too many downvotes compared to upvotes")
				resultsArray.append(str(array[x][0]+" has too many downvotes compared to upvotes"))
		else:
			print("\n   "+array[x][0]+" has less than average upvotes (",round(averageUp*10)/10,")")
			resultsArray.append(str(array[x][0]+" has less than average upvotes ("+str(round(averageUp*10)/10)+")"))
	refreshResults()

def refreshResults():
	global window
	global resultsArray
	displayTextArray = []

	for x in range(len(resultsArray)):
		# Numbered colum on the left
		tempTextDisplay = Text(window,width=2,height=3,wrap=WORD,bd=4,bg="#36393f",fg="WHITE",highlightcolor="PURPLE",pady=8,font=("Helvetica",15),relief=FLAT)
		tempTextDisplay.grid(row = x,column=0)
		tempTextDisplay.insert(END,"\n"+str(x+1)+":")
		tempTextDisplay.config(state=DISABLED)
		displayTextArray.append(tempTextDisplay)

		# Candidate information
		tempTextDisplay = Text(window,width=50,height=3,wrap=WORD,bd=4,bg="GREY",fg="WHITE",highlightcolor="PURPLE",padx=4,font=("Helvetica",14),relief=FLAT)
		tempTextDisplay.grid(row = x,column=1)
		tempTextDisplay.insert(END,resultsArray[x])
		tempTextDisplay.config(state=DISABLED)
		displayTextArray.append(tempTextDisplay)

resultsArray = []

window=Tk()
window.title("Candidate Decider V3")
window.geometry("640x680")
window.config(bg="#36393f")

MenuBar=Menu(window)
FileMenu=Menu(MenuBar,tearoff=0)
MenuBar.add_cascade(label="File",menu=FileMenu)
FileMenu.add_command(label="New",command=inputArray)
FileMenu.add_command(label="Import",command=importArray)
FileMenu.add_command(label="Export",command=exportArray)

ViewMenu=Menu(MenuBar,tearoff=0)
MenuBar.add_cascade(label="View",menu=ViewMenu)
ViewMenu.add_command(label="Refresh",command=calculateResults)

window.config(menu=MenuBar)



Quit=Button(window,text="Quit",command=window.destroy,bg="RED",fg="WHITE",font=("Helvetica",10),relief=FLAT)
Quit.grid(row=len(resultsArray)+1,column=1,sticky=E)

window.mainloop()
