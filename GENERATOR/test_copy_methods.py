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

        print(f"Memory adresses of matrix vals before modifying:\n{list(map(id, matrix))}")
        print(f"Memory adresses of copy matrix vals before modifying:\n{list(map(id, copyMatrix))}")
        print(f"Memory adress of matrix before modifying:\n{id(matrix)}")
        print(f"Memory adress of copy matrix before modifying:\n{id(copyMatrix)}")
        print()

        modifyMatrix(matrix, i)
        
        print(f"Memory adresses of matrix vals after modifying:\n{list(map(id, matrix))}")
        print(f"Memory adresses of copy matrix vals after modifying:\n{list(map(id, copyMatrix))}")
        print(f"Memory adress of matrix after modifying:\n{id(matrix)}")
        print(f"Memory adress of copy matrix after modifying:\n{id(copyMatrix)}")
        print()

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
            
        print(f"Memory adresses of matrix vals after resetting:\n{list(map(id, matrix))}")
        print(f"Memory adresses of copy matrix vals after resetting:\n{list(map(id, copyMatrix))}")
        print(f"Memory adress of matrix after resetting:\n{id(matrix)}")
        print(f"Memory adress of copy matrix after resetting:\n{id(copyMatrix)}")
        print()
        print()
        print()

initMatrix = [
                [1, 2],
                [3, 4]
            ]

print("#####@@@@@@@@")
print(f"Memory adress of initMatrix:\n{id(initMatrix)}")
print(f"Memory adresses of initMatrix vals:\n{list(map(id, initMatrix))}")
print("@@@@@########")
print()

testCopyMethod(initMatrix, 2)

print("\n\nAt the end the init matrix:")
print(f"Memory adress of initMatrix:\n{id(initMatrix)}")
print(f"Memory adresses of initMatrix vals:\n{list(map(id, initMatrix))}")
printMatrix(initMatrix)