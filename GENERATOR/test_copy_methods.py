import copy

def printMatrix(matrix):
    print(matrix)

def modifyMatrix(matrix, i):
    matrix[0][1] = (i + 1) * 10
    
def recCond(matrix):
    if matrix[0][1] == 20:
        print("0,1 element of the matrix IS 20 --> return")
        return True
    else:
        return False
        
def testCopyMethod(matrix, copyMethod):
    for i in range (3):
        copyMatrix = copy.deepcopy(matrix)

        print(f"Iteration {i}: Before modifying the matrix:")
        print("Original matrix:")
        printMatrix(matrix)
        print("Copy matrix:")
        printMatrix(copyMatrix)

        modifyMatrix(matrix, i)
    
        print(f"\n\nIteration {i}: After modifying the matrix:")
        print("Original matrix:")
        printMatrix(matrix)
        print("Copy matrix:")
        printMatrix(copyMatrix)
        
        if recCond(matrix):
            return
        
        if copyMethod == 1:
            print("\nI am using regular assignment")
            matrix = copyMatrix
        elif copyMethod == 2:
            print("\nI am using copy.copy")
            matrix = copy.copy(copyMatrix)
        elif copyMethod == 3:
            print("\nI am using deepcopy")
            matrix = copy.deepcopy(copyMatrix)
        elif copyMethod == 4:
            print("\nI that wierd chatgpt syntax")
            matrix[:] = copyMatrix
            
        print(f"\n\nIteration {i}: After setting back the snapshot:")
        print("Original matrix:")
        printMatrix(matrix)
        print("Copy matrix:")
        printMatrix(copyMatrix)
        print("-------------------------------------------")

initMatrix = [
                [1, 2],
                [3, 4]
            ]

testCopyMethod(initMatrix, 2)

print("\n\nAt the end the init matrix:")
printMatrix(initMatrix)