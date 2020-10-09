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
	global totalUp
	global totalDown
	array = []
	name = ""
	name = input("Enter name of candidate\nEnter 'import' to import saved array")
	if name == "import":
		array = importArray()
		for x in range(len(array)):
			totalUp += array[x][1]
			totalDown += array[x][2]
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
	return array

array = inputArray()
candidateNo = len(array)
votesPerMember = (totalUp+totalDown)/members
averageUp = totalUp/candidateNo
averageDown = totalDown/candidateNo
print("Election Results:")
for x in range(candidateNo):
	if array[x][1] > averageUp: #Upvotes must be more than average
		if array[x][1] > array[x][2]*2: #Must have at least 2X more upvotes than downvotes
			if array[x][2] < round(totalDown/2): #Candidates has less than half the total amount of downvotes
				if array[x][1]-array[x][2] > members*2/(totalUp+totalDown): #Checks if score is high enough compared to voters. (The more members that vote, the more elected)
					print("\nMEMBER ELECTED : "+array[x][0]+"\nUpvotes :",array[x][1],"\nDownvotes :",array[x][2])
				else:
					print("\n"+array[x][0]+" didn't have a high enough vote proportion")
			else:
				print("\n"+array[x][0]+" has more than half of the total downvotes")
		else:
			print("\n"+array[x][0]+" has too many downvotes compared to upvotes")
	else:
		print("\n"+array[x][0]+" has less than average upvotes")
exportArray()

