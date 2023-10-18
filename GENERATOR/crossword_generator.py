import copy
from inspect import isawaitable

def importWordsAndQuestionsFromFile(inputFile):
    with open(inputFile, 'r') as file:
        lines = file.readlines()

    output = []
    for line in lines:
        tmpLine = line.split("&")
        tmpLine[0] = tmpLine[0].rstrip()
        tmpLine[0] = tmpLine[0].lstrip()
        tmpLine[1] = tmpLine[1].rstrip()
        tmpLine[1] = tmpLine[1].lstrip()
        output.append(tmpLine)

    return output

#TODO: Probably there is a built-in version of this, replace it later
def bubbleSortWordLength(listOfWords):
    n = len(listOfWords)

    for i in range(n):
        for j in range(0, n-i-1):
            if len(listOfWords[j][0]) < len(listOfWords[j+1][0]):
                listOfWords[j], listOfWords[j+1] = listOfWords[j+1], listOfWords[j]

def possiblePositions(currentWord, grid):
    listOfPossibleCoordinates = []

    wordLength = len(currentWord)

    for currRow in range(len(grid)):
        for currCol in range(len(grid[0])):
            #Only try to place if the first letter match or the place is empty
            if grid[currRow][currCol] == currentWord[0] or grid[currRow][currCol] == ".":
                if wordLength <= len(grid[0]) - currCol:
                    listOfPossibleCoordinates.append([currRow, currCol, "across"])

                if wordLength <= len(grid) - currRow:
                    listOfPossibleCoordinates.append([currRow, currCol, "down"])

    return listOfPossibleCoordinates

#TODO: if one word was completly overlay another word, ignore that. The initial mechanism is there
#(by bool isWordAlreadyOnBoard) but it is not considering if the letters of the word is already there (eg.: one letter only)
#but the question is not there on the grid yet --> think about this, is this mechanism needed??
def fits(currentWord, position, grid, questions):
    wordLength = len(currentWord)
    row0 = position[0]
    col0 = position[1]
    direction = position[2]

    if row0 == 0 or col0 == 0:
        return False
    
    isWordAlreadyOnBoard = True

    if direction == "across":
        if ( (grid[row0][col0-1] != ".") and (grid[row0][col0-1] not in questions) ):
            #If there is no place for the question before the word we return false
            return False
        else:
            for i in range(wordLength):
                if grid[row0][col0 + i] == ".":
                    isWordAlreadyOnBoard = False
                if grid[row0][col0 + i] != "." and grid[row0][col0 + i] != currentWord[i]:
                    return False
            if col0 + wordLength < len(grid[0]):
                if (grid[row0][col0+wordLength] != ".") and (grid[row0][col0+wordLength] not in questions):
                    #The word cannot end into another word, it has to be the border or a question box
                    return False
    else:
        if ( (grid[row0-1][col0] != ".") and (grid[row0-1][col0] not in questions) ):
            #If there is no place for the question before the word we return false
            return False
        else:
            for i in range(wordLength):
                if grid[row0 + i][col0] == ".":
                    isWordAlreadyOnBoard = False
                if grid[row0 + i][col0] != "." and grid[row0 + i][col0] != currentWord[i]:
                    return False
            if row0 + wordLength < len(grid):
                if (grid[row0+wordLength][col0] != ".") and (grid[row0+wordLength][col0] not in questions):
                    #The word cannot end into another word, it has to be the border or a question box
                    return False

    if isWordAlreadyOnBoard:
        return True
    else:
        return True

def placeWord(wordAndQuestionToPlace, position, grid, questions):
    currentWord = wordAndQuestionToPlace[0]
    currentQuestion = wordAndQuestionToPlace[1]
    
    wordLength = len(currentWord)
    
    row0 = position[0]
    col0 = position[1]
    direction = position[2]

    if direction == "across":
        for i in range(wordLength):
            grid[row0][col0 + i] = currentWord[i]
        if grid[row0][col0 - 1] == ".":
            #we have to create a new question box
            if not questions:
                #if there is no question dict we have to make it
                questions[1] = direction + ": " + currentQuestion
                grid[row0][col0 - 1] = 1
            else:
                questions[max(questions)+1] = direction + ": " + currentQuestion
                grid[row0][col0 - 1] = max(questions)
        else:
            #we extend the existing question box
            questions[grid[row0][col0 - 1]] += "\t" + direction + ": " + currentQuestion
    else:
        for i in range(wordLength):
            grid[row0 + i][col0] = currentWord[i]
        if grid[row0 - 1][col0] == ".":
            #we have to create a new question box
            if not questions:
                #if there is no question dict we have to make it
                questions[1] = direction + ": " + currentQuestion
                grid[row0 - 1][col0] = 1
            else:
                questions[max(questions)+1] = direction + ": " + currentQuestion
                grid[row0 - 1][col0] = max(questions)
        else:
            #we extend the existing question box
            questions[grid[row0 - 1][col0]] += "\t" + direction + ": " + currentQuestion

#Checks that a word which is already on the grid is truly in the list of words
#TODO: make sure that word repetition is not allowed
def isGridWordLegit(position, grid, refWordQuestionPairList, questions):
    row0 = position[0]
    col0 = position[1]
    direction = position[2]

    wordFromGrid = ""
    if direction == "across":
        i = 0
        while (col0 + i < len(grid[0])) and (grid[row0][col0 + i] != "0") and (grid[row0][col0+i] not in questions):
            wordFromGrid += grid[row0][col0+i]
            i += 1

    else:
        i = 0
        while (row0 + i < len(grid)) and (grid[row0 + i][col0] != "0") and (grid[row0 + i][col0] not in questions):
            wordFromGrid += grid[row0 + i][col0]
            i += 1

    for wordPair in refWordQuestionPairList:
        if wordFromGrid == wordPair[0]:
            return True
        

    print(f"The following grid word is not in the word list: {wordFromGrid}")
    return False

#Checks if the grid consists only words from the list
#Before calling it has to be sure that the grid is full!
def isGridLegit(grid, refWordQuestionPairList, questions):
    for currRow in range(len(grid)):
        for currCol in range(len(grid[0])):
            if grid [currRow][currCol] in questions:
                #We found a question position     
                if (currCol + 1 < len(grid[0])) and (grid[currRow][currCol + 1] != "0") and (grid[currRow][currCol+1] not in questions):
                    #check horizontal word if there is one
                    tmpPosition=[currRow, currCol+1, "across"]
                    if not isGridWordLegit(tmpPosition, grid, refWordQuestionPairList, questions):
                        return False
                if (currRow + 1 < len(grid)) and (grid[currRow + 1][currCol] != "0") and (grid[currRow + 1][currCol] not in questions):
                    #check vertical word
                    tmpPosition=[currRow+1, currCol, "down"]
                    if not isGridWordLegit(tmpPosition, grid, refWordQuestionPairList, questions):
                        return False
    print("Grid is legit, returning")
    #printGame(grid, questions)
    return True

def crossword(dynWordQuestionPairList, grid, questions, refWordQuestionPairList):
    #print("--------------------")
    #printGrid(grid)
    if countEmptyFields(grid) == 0:
        print("All fields are full")
        if isGridLegit(grid, refWordQuestionPairList, questions):
            return True
        else:
            return False
        
    # if countEmptyFields(grid) < 3:
    #     printGrid(grid)
    #     print(dynWordQuestionPairList)

    if not dynWordQuestionPairList:
        # print("All of the words has been used, still no solution has been found....")
        return False

    currentWordQuestionPair = dynWordQuestionPairList.pop(0)
    currentWord = currentWordQuestionPair[0]
    for pos in possiblePositions(currentWord, grid): 
        if fits(currentWord, pos, grid, questions):
            #Making deepcopy snapshots for the backtracking
            gridSnapshot = copy.deepcopy(grid)
            questionsSnapshot = copy.deepcopy(questions)
            
            placeWord(currentWordQuestionPair, pos, grid, questions)
            if crossword(dynWordQuestionPairList, grid, questions, refWordQuestionPairList):
                return True
            else:
                #Restoring the grid, since prev position did not lead to a solution   
                grid[:] = gridSnapshot
                questions.clear()
                questions.update(questionsSnapshot)

    
    if crossword(dynWordQuestionPairList, grid, questions, refWordQuestionPairList):
        return True
    else:
        #lets put back current word+question, beacuse we are going up one level
        dynWordQuestionPairList.insert(0, currentWordQuestionPair)
        # print("---------------------")
        # print(f"I put back= {currentWord}")
        # print(dynWordQuestionPairList)
        # print("---------------------")
        return False

def printGrid(grid):
    tmpRow = ""
    for currRow in range(len(grid)):
        for currCol in range(len(grid[0])):
            tmpRow += str(grid[currRow][currCol]) + "\t"
        print(tmpRow)
        tmpRow = ""

def printGame(grid, questions):
    printGrid(grid)
    
    print("\nQuestions:")
    for key, value in questions.items():
        print(f"{key}: {value}") 
    
def countEmptyFields(grid):
    emptyFields = 0
    for currRow in range(len(grid)):
        for currCol in range(len(grid[0])):
            if grid[currRow][currCol] == ".":
                emptyFields += 1
    return emptyFields

def main():
    grid = [
        ["0","0","0","0","0",".",".",".",".",".","0"],
        ["0","0","0","0","0","S","A","R","G","A","H"],
        ["0","0","0","0",".",".",".",".",".",".","A"],
        ["0","0","0","0",".",".",".",".",".",".","S"],
        ["0","0",".",".",".",".",".",".",".",".","U"],
        [".","C",".",".",".",".",".",".",".",".","."],
        [".","Q",".",".",".",".",".",".",".",".","."],
        ["0","K","O","R","H","A","X","K","A","L","Y"]
    ]

    questions = dict()
    print("The initial grid and questions: ")
    printGame(grid, questions)
    print()

    dynWordQuestionPairList = importWordsAndQuestionsFromFile("input.txt")
    bubbleSortWordLength(dynWordQuestionPairList)

    #Is used later to check if all words on the grid exists in the input list
    refWordQuestionPairList = copy.deepcopy(dynWordQuestionPairList)
    
    if crossword(dynWordQuestionPairList, grid, questions, refWordQuestionPairList):
        print("\nThe final grid and questions: ")
        printGame(grid, questions)
    else:
        print("No solution found, maybe more words have to be added...")

main()
