import glob

def main():
	fileOne = open("./Chromosome/Processed/1400000", "r")
	fileTwo = open("./Chromosome/Processed/1400003", "r")

	fOne = fileOne.read().split(" ")
	fTwo = fileTwo.read().split(" ")

	for files in range(len(fOne)):
		if (fOne[files] != fTwo[files]):
			print("File 1: " + fOne[files] + "\tFile 2: " + fTwo[files] + "\n")
		else:
			pass

main()
