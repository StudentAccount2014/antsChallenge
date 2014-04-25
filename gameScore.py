import re
import string
import random
import glob

global mutationRate, crossoverRate
mutationRate = 1000
crossoverRate = .5

def main():
	# open replay file
	gamefile = open("./game_logs/0.replay", 'r')
	gameOutput = gamefile.read()
	gamefile.close()
	chromosomeFiles = glob.glob("./Chromosome/New/*")
	chromosomeFiles.sort()
	botScore = []
	for cFile in chromosomeFiles:
		botScore.append(scoreFinder(gameOutput, cFile.split("_")[1]))

	gameLogs = glob.glob("./game_logs/*.input")
	gameLogs.sort()
	antsLeft = []
	for counter in range(len(gameLogs)):
		fileName = gameLogs[counter]
		# open bot input file
		antFile = open(fileName, 'r')
		antOutput = antFile.read()
		antFile.close()
		antsLeft.append(antFinder(antOutput))

	# open chromosome file
	chromosomeList = []
	
	for fileCount in range(len(chromosomeFiles)):
		chromoFile = open(chromosomeFiles[fileCount], 'r')
		chromosomeList.append(chromoFile.read())
		chromoFile.close()

	creationType = ["M", "C1", "C2"]
	crossoverLocation = chromosomeSplit(chromosomeList[0])

	for create in creationType:
		outputList = glob.glob("./Chromosome/Processed/*")
		# Output file name format [00000_(M|C)]
		tempUniq = 0
		if (len(outputList) == 0):
			pass
		else:
			for fN in outputList:
				if (int(fN.split("/")[-1][-5:]) > tempUniq):
					tempUniq = int(fN.split("/")[-1][-5:])
			tempUniq += 1

		fileName = setFileName(create, tempUniq, botScore, antsLeft)

		if (create == "M"):
			if (botScore[0] > botScore[1]):
				newChromosome = mutateChromosome(chromosomeList[0])
			elif (botScore[1] > botScore[0]):
				newChromosome = mutateChromosome(chromosomeList[1])
			elif (botScore[0] == botScore[1]):
				if (antsLeft[0] > antsLeft[1]):
					newChromosome = mutateChromosome(chromosomeList[0])
				elif (antsLeft[1] > antsLeft[0]):
					newChromosome = mutateChromosome(chromosomeList[1])
				else:
					newChromosome = mutateChromosome(chromosomeList[0])
		elif (create == "C1"):
			newChromosome = crossoverChromosome(chromosomeList[0], chromosomeList[1], crossoverLocation)
		elif (create == "C2"):
			newChromosome = crossoverChromosome(chromosomeList[1], chromosomeList[0], crossoverLocation)

		fileWrite(newChromosome, fileName)


# find score for bot
def	scoreFinder(gameInfo, scoreIndex):
	scoreIndex = int(scoreIndex)
	findScore = re.compile("\"score\"\:.*\],")
	score = findScore.search(gameInfo).group()
	for char in [",", "[", "]", ":", "\""]:
		score = string.replace(score, char, "")
	score = score.split(" ")

	return int(score[scoreIndex])

# find remaining ants for bot
def antFinder(antInfo):
	findTurnAnt = re.compile("playerturns [0-9]* .*", re.DOTALL)
	finalTurn = findTurnAnt.search(antInfo).group()
	countAnts = re.compile("a [0-9]* [0-9]* [0-9]*")
	ants = len(countAnts.findall(finalTurn))
	return ants


def mutateChromosome(chromo):
	splitChromo = chromo.split(" ")
	directions = ["n", "e", "s", "w"]
	for indChromo in splitChromo:
		if (random.randint(1,mutationRate) == 1):
			tempSplit = indChromo.split("-")
			tempSplit[2] = directions[random.randint(0,3)]
			indChromo = tempSplit[0] + "-" + tempSplit[1] + "-" + tempSplit[2]

	newChromo = ""
	for chromosome in splitChromo:
		newChromo += chromosome + " "

	newChromo = newChromo.strip()
	return newChromo

def chromosomeSplit(parent):
	upperBound = len(parent.split(" "))
	return int(upperBound * crossoverRate)


def crossoverChromosome(parentOne, parentTwo, splitLocation):
	pSplitOne = parentOne.split(" ")
	pSplitTwo = parentTwo.split(" ")

	tempChromosome = []

	for geneNumber in range(splitLocation):
		tempChromosome.append(pSplitOne[geneNumber].strip())

	for geneNumber in range(splitLocation, len(pSplitTwo)):
		tempChromosome.append(pSplitTwo[geneNumber].strip())

	newChromosome = ' '.join(tempChromosome)

	newChromosome = newChromosome.strip()

	return newChromosome


# output score, remaining ants, and chromosome to a new file
def fileWrite(chromosome, fileName):
	if (chromosome.find("Chromosome: ") == -1):
		outputFile = open(fileName, 'w')
		outputFile.write(chromosome)
		outputFile.close()

	return


def setFileName(create, tempUniq, botScore, antsLeft):
	fileName = "./Chromosome/Processed/"
	if (botScore[0] > botScore[1]):
		tempNum = ((botScore[0]*10)+(antsLeft[0]*2))
	elif (botScore[1] > botScore[0]):
		tempNum = ((botScore[1]*10)+(antsLeft[1]*2))
	elif (botScore[0] == botScore[1]):
		if (antsLeft[0] > antsLeft[1]):
			tempNum = ((botScore[0]*10)+(antsLeft[0]*2))
		elif (antsLeft[1] > antsLeft[0]):
			tempNum = ((botScore[1]*10)+(antsLeft[1]*2))
		else:
			tempNum = (botScore[0]*10)+(antsLeft[0]*2)

	if create == "M":
		pass
	else:
		tempNum = int(tempNum*crossoverRate)

	return fileName + str(tempNum) + str(tempUniq).zfill(5)


main()
