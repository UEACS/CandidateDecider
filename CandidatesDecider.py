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
						resultsArray.append(str(array[x][0]+" didn't have a high enough vote proportion (A score higher than "+str(round((0.5+members*2/(totalUp+totalDown))*10)/10)+" was needed but only a score of "+str(array[x][1]-array[x][2])+" was gotten)"))
				else:
					print("\n   "+array[x][0]+" has hlaf or more than the total downvotes")
					resultsArray.append(str(array[x][0]+" has more than half of the total downvotes"))
			else:
				print("\n   "+array[x][0]+" has too many downvotes compared to upvotes")
				resultsArray.append(str(array[x][0]+" has too many downvotes compared to upvotes"))
		else:
			print("\n   "+array[x][0]+" has fewer than average upvotes (",round(averageUp*10)/10,")")
			resultsArray.append(str(array[x][0]+" has fewer than average upvotes ("+str(round(averageUp*10)/10)+")"))
	refreshResults()

def refreshResults():
	global window
	global canvas
	global resultsArray
	global displayTextArray

	for i in range(len(displayTextArray)):
		displayTextArray[i].destroy()

	displayTextArray = []
	for x in range(len(resultsArray)):
		# Numbered colum on the left
		tempTextDisplay = t.Text(canvas,width=2,height=3,wrap=t.WORD,bd=4,bg="#36393f",fg="WHITE",highlightcolor="PURPLE",pady=8,font=("Helvetica",15),relief=t.FLAT,yscrollcommand = scrollBar.set)
		tempTextDisplay.grid(row = x,column=0)
		tempTextDisplay.insert(t.END,"\n"+str(x+1)+":")
		tempTextDisplay.config(state=t.DISABLED)
		displayTextArray.append(tempTextDisplay)

		# Candidate information
		tempTextDisplay = t.Text(canvas,width=50,height=3,wrap=t.WORD,bd=4,bg="GREY",fg="WHITE",highlightcolor="PURPLE",padx=4,font=("Helvetica",14),relief=t.FLAT,yscrollcommand = scrollBar.set)
		tempTextDisplay.grid(row = x,column=1)
		tempTextDisplay.insert(t.END,resultsArray[x])
		tempTextDisplay.config(state=t.DISABLED)
		displayTextArray.append(tempTextDisplay)


def displayAboutWindow():
	aboutWindow=t.Tk()
	aboutWindow.title("About CD3")
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
window.title("Candidate Decider V3")
window.geometry(width+"x"+height)
window.config(bg="#36393f")
window.grid_anchor(t.N)

frame = t.Frame(window)
frame.config(width=1,height=1)
frame.grid(row=0,column=0)
#frame.columnconfigure(0,1)
canvas = t.Canvas(frame)
canvas.configure(width=int(width)/2,height=int(height)*0.9)
canvas.grid(row=0,column=0)
scrollBar = t.Scrollbar(frame,orient=t.VERTICAL)
scrollBar.config(command=canvas.yview)
scrollBar.grid(row=0,column=2,sticky="e")
canvas.config(yscrollcommand=scrollBar.set)

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



Quit = t.Button(window,text="Quit",command=window.destroy,bg="RED",fg="WHITE",font=("Helvetica",10),relief=t.FLAT)
Quit.grid(row=len(resultsArray)+1,column=1,sticky=t.E)

window.mainloop()