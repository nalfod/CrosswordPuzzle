import copy

def importWordsFromFile(inputFile):
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

def bubbleSortWordLength(listOfWords):
    n = len(listOfWords)

    for i in range(n):
        for j in range(0, n-i-1):
            if len(listOfWords[j][0]) < len(listOfWords[j+1][0]):
                listOfWords[j], listOfWords[j+1] = listOfWords[j+1], listOfWords[j]

def possiblePositions(currentWord, grid):
    listOfPossibleCoordinates = []

    wordLength = len(currentWord)

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            #Only try to place if the first letter match or the place is empty
            if grid[row][col] == currentWord[0] or grid[row][col] == ".":
                if wordLength <= len(grid[0]) - col:
                    listOfPossibleCoordinates.append([row, col, "across"])

                if wordLength <= len(grid) - row:
                    listOfPossibleCoordinates.append([row, col, "down"])

    return listOfPossibleCoordinates

def fits(currentWord, position, grid, questions):
    wordLength = len(currentWord)
    row = position[0]
    col = position[1]
    direction = position[2]

    if row == 0 or col == 0:
        return False

    if direction == "across":
        if ( (grid[row][col-1] != ".") and (grid[row][col-1] not in questions) ):
            #If there is no place for the question before the word we return false
            return False
        else:
            for i in range(wordLength):
                if grid[row][col + i] != "." and grid[row][col + i] != currentWord[i]:
                    return False
            if col + wordLength < len(grid[0]):
                if (grid[row][col+wordLength] != ".") and (grid[row][col+wordLength] not in questions):
                    #The word cannot end into another word, it has to be the border or a question box
                    return False
    else:
        if ( (grid[row-1][col] != ".") and (grid[row-1][col] not in questions) ):
            #If there is no place for the question before the word we return false
            return False
        else:
            for i in range(wordLength):
                if grid[row + i][col] != "." and grid[row + i][col] != currentWord[i]:
                    return False
            if row + wordLength < len(grid):
                if (grid[row+wordLength][col] != ".") and (grid[row+wordLength][col] not in questions):
                    #The word cannot end into another word, it has to be the border or a question box
                    return False

    return True;

def placeWord(currentWordAndQuestion, position, grid, questions):
    currentWord = currentWordAndQuestion[0]
    currentQuestion = currentWordAndQuestion[1]
    
    wordLength = len(currentWord)
    
    row = position[0]
    col = position[1]
    direction = position[2]

    if direction == "across":
        for i in range(wordLength):
            grid[row][col + i] = currentWord[i]
        if grid[row][col - 1] == ".":
            #we have to create a new question box
            if not questions:
                #if there is no question dict we have to make it
                questions[1] = direction + ": " + currentQuestion
                grid[row][col - 1] = 1
            else:
                questions[max(questions)+1] = direction + ": " + currentQuestion
                grid[row][col - 1] = max(questions)
        else:
            #we extend the existing question box
            questions[grid[row][col - 1]] += "\t" + direction + ": " + currentQuestion
    else:
        for i in range(wordLength):
            grid[row + i][col] = currentWord[i]
        if grid[row - 1][col] == ".":
            #we have to create a new question box
            if not questions:
                #if there is no question dict we have to make it
                questions[1] = direction + ": " + currentQuestion
                grid[row - 1][col] = 1
            else:
                questions[max(questions)+1] = direction + ": " + currentQuestion
                grid[row - 1][col] = max(questions)
        else:
            #we extend the existing question box
            questions[grid[row - 1][col]] += "\t" + direction + ": " + currentQuestion

#Checks that a word which is already on the grid is truly in the list of words
#TODO: make sure that word repetition is not allowed
def isGridWordLegit(position, grid, words, questions):
    row = position[0]
    col = position[1]
    direction = position[2]

    wordFromGrid = ""
    if direction == "across":
        i = 0
        while (col + i < len(grid[0])) and (grid[row][col + i] != "0") and (grid[row][col+i] not in questions):
            wordFromGrid += grid[row][col+i]
            i += 1

    else:
        i = 0
        while (row + i < len(grid)) and (grid[row + i][col] != "0") and (grid[row + i][col] not in questions):
            wordFromGrid += grid[row + i][col]
            i += 1

    for wordPair in words:
        if wordFromGrid == wordPair[0]:
            return True

    return False

#Checks if the grid consists only words from the list
#Before calling it has to be sure that the grid is full!
def isGridLegit(grid, words, questions):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid [row][col] in questions:
                #We found a question position     
                if (col + 1 < len(grid[0])) and (grid[row][col + 1] != "0") and (grid[row][col+1] not in questions):
                    #check horizontal word if there is one
                    tmpPosition=[row, col+1, "across"]
                    if not isGridWordLegit(tmpPosition, grid, words, questions):
                        return False
                if (row + 1 < len(grid)) and (grid[row + 1][col] != "0") and (grid[row + 1][col] not in questions):
                    #check vertical word
                    tmpPosition=[row+1, col, "down"]
                    if not isGridWordLegit(tmpPosition, grid, words, questions):
                        return False
    print("Grid is legit, returning")
    #printGame(grid, questions)
    return True

def crossword(words, grid, questions, staticWords):
    if countEmptyFields(grid) == 0:
        print("All fields are full")
        if isGridLegit(grid, staticWords, questions):
            return True
        else:
            return False

    if not words:
        return False

    currentWordPair = words.pop(0)
    currentWord = currentWordPair[0]
    for pos in possiblePositions(currentWord, grid): 
        if fits(currentWord, pos, grid, questions):
            #Making deepcopy snapshots for the backtracking
            gridSnapshot = copy.deepcopy(grid)
            questionsSnapshot = copy.deepcopy(questions)
            
            placeWord(currentWordPair, pos, grid, questions)
            if crossword(words, grid, questions, staticWords):
                return True
            else:
                #Restoring the grid, since prev position did not lead to a solution   
                grid[:] = gridSnapshot
                questions.clear()
                questions.update(questionsSnapshot)

    #lets put back current word, beacuse we are going up one level
    words.insert(0, currentWordPair)
    return False


def printGame(grid, questions):
    tmpRow = ""
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            tmpRow += str(grid[row][col]) + "\t"
        print(tmpRow)
        tmpRow = ""
    
    print("\nQuestions:")
    for key, value in questions.items():
        print(f"{key}: {value}") 
    
def countEmptyFields(grid):
    emptyFields = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == ".":
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

    grid2 = [
        ["0","0","0","0","0",".",".",".",".",".","0"],
        ["0","0","0","0","0","S","A","R","G","A","H"],
        ["0","0","0","0",".","A","T",".","A",".","A"],
        ["0","0","0","0",".","L","A","C",".","A","S"],
        ["0","0",".",".","E","T",".","I","F",".","U"],
        [".","C","A","E","N",".","E","B","E","N","."],
        [".","Q",".","A","Y","A",".","A",".","A","C"],
        ["0","K","O","R","H","A","X","K","A","L","Y"]
    ]
    questions = dict()
    printGame(grid, questions)

    dynamicWords = importWordsFromFile("input.txt")
    bubbleSortWordLength(dynamicWords)

    #Is used later to check if all words on the grid exists in the input list
    staticWords = copy.deepcopy(dynamicWords)
    
    print(crossword(dynamicWords, grid, questions, staticWords))
    printGame(grid, questions)

main()
