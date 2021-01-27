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
	arrayFile = open("candidates.txt","w")
	for x in range(len(array)):
		arrayFile.write(array[x][0]+","+str(array[x][1])+","+str(array[x][2])+"\n")
	arrayFile.close()

def importArray():
	global totalUp
	global totalDown
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
	for x in range(len(array)):
		totalUp += array[x][1]
		totalDown += array[x][2]
	return array

#array = inputArray()
array = importArray()
candidateNo = len(array)
votesPerMember = (totalUp+totalDown)/members
averageUp = totalUp/candidateNo
averageDown = totalDown/candidateNo
text = ""
print("Election Results:")
for x in range(candidateNo):
	if array[x][1] > averageUp: #Upvotes must be more than average
		if array[x][1] > array[x][2]*2: #Must have at least 2X more upvotes than downvotes
			if array[x][2] < round(totalDown/2): #Candidates has less than half the total amount of downvotes
				if array[x][1]-array[x][2] > members*2/(totalUp+totalDown): #Checks if score is high enough compared to voters. (The more members that vote, the more elected)
					print("\n   MEMBER ELECTED : "+array[x][0]+"\n   Upvotes :",array[x][1],"\n   Downvotes :",array[x][2])
					text = text + str("\n   MEMBER ELECTED : "+array[x][0]+"\n   Upvotes :"+str(array[x][1])+"\n   Downvotes :"+str(array[x][2]))
				else:
					print("\n   "+array[x][0]+" didn't have a high enough vote proportion (A score higher than",round((0.5+members*2/(totalUp+totalDown))*10)/10,"was needed but only a score of ",(array[x][1]-array[x][2]),"was gotten)")
					text = text + str("\n   "+array[x][0]+" didn't have a high enough vote proportion (A score higher than",round((0.5+members*2/(totalUp+totalDown))*10)/10,"was needed but only a score of ",(array[x][1]-array[x][2]),"was gotten)")
			else:
				print("\n   "+array[x][0]+" has more than half of the total downvotes")
				text = text + str("\n   "+array[x][0]+" has more than half of the total downvotes")
		else:
			print("\n   "+array[x][0]+" has too many downvotes compared to upvotes")
			text = text + str("\n   "+array[x][0]+" has too many downvotes compared to upvotes")
	else:
		print("\n   "+array[x][0]+" has less than average upvotes (",round(averageUp*10)/10,")")
		text = text + str("\n   "+array[x][0]+" has less than average upvotes ("+str(round(averageUp*10)/10)+")")
exportArray()

window=Tk()
window.title("Candidate Decider V3")
window.geometry("720x480")


DisplayText=Text(window,width=90,height=28,wrap=WORD)
DisplayText.grid(row=0,column=0)
DisplayText.insert(END,text)
DisplayText.config(state=DISABLED)

window.mainloop()
