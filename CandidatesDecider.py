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

def file_len(fname):
    i=-1
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

members = 213 #Manually enter member count
totalUp = 0
totalDown = 0
#Had 152 total votes last time

array = []
def inputArray():
	name = ""
	name = input("Enter name of candidate")
	while name != "":
		up = int(input("Input up-votes"))
		totalUp += up
		down = int(input("Input down-votes"))
		totalDown += down
		array.append([name,up,down])
		name = input("Enter name of candidate (leave blank to stop)")

def exportArray():
	arrayFile = open("candidates.txt","w")
	for x in range(len(array)):
		arrayFile.write(array[x]+"\n")
	arrayFile.close()

def importArray():
	try:
		arrayFile = open("candidates.txt","r")
	except FileNotFoundError:
		return []
	array = []
	for x in range(file_len(arrayFile)):
		line = arrayFile.readline()
		array.append(line.split(","))
	arrayFile.close()
	return array

candidateNo = len(array)
votesPerMember = (totalUp+totalDown)/members
averageUp = totalUp/candidateNo
averageDown = totalDown/candidateNo
for x in range(candidateNo):
	if array[x][1] > averageUp: #Upvotes must be more than average
		if array[x][1] > array[x][2]*2: #Must have at least 2X more upvotes than downvotes
			if array[x][2] < totalDown/2: #Candidates has less than half the total amount of downvotes
				if (array[x][1]-array[x][2])/members > (0.7/10): #Checks their score is high enough compared to the total votes from the last polls
					print("\nMEMBER ELECTED : "+array[x][0]+"\nUpvotes :",array[x][1],"\nDownvotes :",array[x][2])

