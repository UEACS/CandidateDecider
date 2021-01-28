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

import tkinter as t

def file_len(fname):
    i=-1
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

members = 271 #Manually enter member count
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
		importArray()
	totalUp = 0
	totalDown = 0
	while name != "":
		up = int(input("Input up-votes"))
		totalUp += up
		down = int(input("Input down-votes"))
		totalDown += down
		array.append([name,up,down])
		name = input("Enter name of candidate (leave blank to stop)")

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
		array = []
		for x in range(file_len("candidates.txt")):
			line = arrayFile.readline()
			array.append(line.split(","))
			array[x][1] = int(array[x][1])
			array[x][2] = int(array[x][2])
		arrayFile.close()
	except FileNotFoundError:
		print("There was an error importing the file. Probably an empty file")

	totalUp = 0
	totalDown = 0
	for x in range(len(array)):
		totalUp += array[x][1]
		totalDown += array[x][2]

	calculateResults()

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
				if array[x][2] < round(totalDown/3): #Candidates has few than a third of the total amount of downvotes
					minVoteProportion = round((0.5+members*3/(totalUp+totalDown))*10)/10
					if array[x][1]-array[x][2] > minVoteProportion: #Checks if score is high enough compared to voters. (The more members that vote, the more elected)
						print("\n   MEMBER ELECTED : "+array[x][0]+"\n   Upvotes :",array[x][1],"\n   Downvotes :",array[x][2])
						resultsArray.append(str("MEMBER ELECTED : "+array[x][0]+"\n   Upvotes :"+str(array[x][1])+"\n   Downvotes :"+str(array[x][2])))
					else:
						print("\n   "+array[x][0]+" didn't have a high enough vote proportion (A score higher than",minVoteProportion,"was needed but only a score of ",(array[x][1]-array[x][2]),"was gotten)")
						resultsArray.append(str(array[x][0]+" didn't have a high enough vote proportion (A score higher than "+str(minVoteProportion)+" was needed but only a score of "+str(array[x][1]-array[x][2])+" was gotten)"))
				else:
					print("\n   "+str(array[x][0]+" has "+str(array[x][2])+" downvotes, more than a third of the total downvotes ("+str(round((totalDown/3)*10)/10)+")"))
					resultsArray.append(str(array[x][0]+" has "+str(array[x][2])+" downvotes, more than a third of the total downvotes ("+str(round((totalDown/3)*10)/10)+")"))
			else:
				print("\n   "+array[x][0]+" has too many downvotes "+str(array[x][2])+" compared to upvotes "+str(array[x][1]))
				resultsArray.append(array[x][0]+" has too many downvotes "+str(array[x][2])+" compared to upvotes "+str(array[x][1]))
		else:
			print("\n   "+array[x][0]+" has fewer than average upvotes (",round(averageUp*10)/10,")")
			resultsArray.append(str(array[x][0]+" has fewer than average upvotes ("+str(round(averageUp*10)/10)+")"))
	refreshResults()

def refreshResults():
	global window
	global width
	global height
	global canvas
	global selectionFrame
	global resultsArray
	global displayTextArray

	for i in range(len(displayTextArray)):
		displayTextArray[i].destroy()

	displayTextArray = []
	for x in range(len(resultsArray)):
		# Numbered colum on the left
		tempTextDisplay = t.Text(selectionFrame,width=3,height=3,wrap=t.WORD,bd=4,bg="#36393f",fg="#87898C",highlightcolor="PURPLE",padx=4,pady=4,font=("Helvetica",15),relief=t.FLAT)
		tempTextDisplay.grid(row = x+1,column=0,sticky=t.E)
		tempTextDisplay.insert(t.END,"\n  "+str(x+1)+":")
		tempTextDisplay.config(state=t.DISABLED)
		displayTextArray.append(tempTextDisplay)

		# Candidate information
		tempTextDisplay = t.Text(selectionFrame,width=40,height=3,wrap=t.WORD,bd=4,bg="#6B768C",fg="WHITE",highlightcolor="PURPLE",padx=4,font=("Helvetica",14),relief=t.FLAT)
		tempTextDisplay.grid(row = x+1,column=1,sticky=t.W)
		tempTextDisplay.insert(t.END,resultsArray[x])
		tempTextDisplay.config(state=t.DISABLED)
		displayTextArray.append(tempTextDisplay)
	window.geometry(width+"x"+str(int(height)+1))



def displayAboutWindow():
	aboutWindow=t.Tk()
	aboutWindow.title("About CD 3.1")
	aboutWindow.geometry("250x120")
	aboutWindow.config(bg="#81A2E6")
	aboutWindow.grid_anchor(t.N)

	aboutText = t.Text(aboutWindow,width=aboutWindow.winfo_width()*30,height=aboutWindow.winfo_height()*5,wrap=t.WORD,bd=4,bg="#36393f",fg="WHITE",highlightcolor="PURPLE",pady=8,font=("Helvetica",9),relief=t.GROOVE)
	aboutText.grid(row=0,column=0)
	aboutText.insert(t.END,"This is version 3 beta. This program has been completely made by Arun Osborn and the UI uses the Tkinter library. This message was last update 28.1.21")
	aboutText.config(state=t.DISABLED)

	aboutWindow.mainloop()


resultsArray = []
displayTextArray = []

width = "1600"
height = "760"

window=t.Tk()
window.title("Candidate Decider V3.1")
window.geometry(width+"x"+height)
window.config(bg="#403D37")
window.grid_anchor(t.N)

# Container or the votes
mainFrame = t.Frame(window,bg="BROWN",width=200,cursor="dotbox")
mainFrame.pack(fill=t.BOTH,expand=1)
canvas = t.Canvas(mainFrame,bg="#36393f",width=200)
canvas.pack(side=t.LEFT,fill=t.BOTH,expand=1)
# Scroll area
scrollBar = t.Scrollbar(canvas,orient=t.VERTICAL,command=canvas.yview)
scrollBar.pack(side=t.RIGHT,fill=t.Y)
canvas.configure(yscrollcommand=scrollBar.set)
canvas.bind("<Configure>",lambda e:canvas.configure(scrollregion = canvas.bbox("all")))

selectionFrame = t.Frame(canvas,bg="#36393f")
selectionFrame.grid_anchor(t.NE)
canvas.create_window((0,0),window=selectionFrame,anchor="nw")

numberHeader = t.Text(selectionFrame,width=3,height=1,wrap=t.WORD,bd=4,bg="#36393f",fg="#87898C",highlightcolor="PURPLE",padx=4,pady=8,font=("Helvetica",15),relief=t.FLAT)
numberHeader.grid(row = 0,column=0,sticky=t.E)
numberHeader.insert(t.END,"No.")
numberHeader.config(state=t.DISABLED)

candidateHeader = t.Text(selectionFrame,width=40,height=1,wrap=t.WORD,bd=4,bg="#6B768C",fg="WHITE",highlightcolor="PURPLE",padx=4,pady=8,font=("Helvetica",14),relief=t.FLAT)
candidateHeader.grid(row = 0,column=1,sticky=t.W)
candidateHeader.insert(t.END,"Candidate")
candidateHeader.config(state=t.DISABLED)


MenuBar=t.Menu(window)
FileMenu=t.Menu(MenuBar,tearoff=0)
MenuBar.add_cascade(label="File",menu=FileMenu)
FileMenu.add_command(label="New",command=inputArray)
FileMenu.add_command(label="Import",command=importArray)
FileMenu.add_command(label="Export",command=exportArray)

ViewMenu=t.Menu(MenuBar,tearoff=0)
MenuBar.add_cascade(label="View",menu=ViewMenu)
ViewMenu.add_command(label="Refresh",command=calculateResults)
ViewMenu.add_command(label="About",command=displayAboutWindow)

window.config(menu=MenuBar)


"""
Quit = t.Button(window,text="Quit",command=window.destroy,bg="RED",fg="WHITE",font=("Helvetica",10),relief=t.FLAT)
Quit.grid(row=len(resultsArray)+1,column=1,sticky=t.E)
"""
window.mainloop()