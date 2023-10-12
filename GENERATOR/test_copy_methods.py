import copy

# This function is not needed, since it is just a print() call
#def print_matrix(matrix):
#    print(matrix)

# snake_case is default for function and variable name syntax, this applies to all function and variable names in the code
def modify_matrix(matrix, i):
    matrix[0][1] = (i + 1) * 10
    
def rec_cond(matrix):
    # it is enough to return the statement value instead of using if cond: True else: False syntax
    return matrix[0][1] == 20

def test_copy_method(matrix, copy_method):
    for i in range(3):
        copy_matrix = copy.deepcopy(matrix)

        # usage of f-strings is good for saving space and managing readability
        print(f"Iteration {i}: Before modifying the matrix:")
        print(f"Original matrix:\n{matrix}")
        print(f"Copy matrix:\n{copy_matrix}")

        modify_matrix(matrix, i)
    
        print(f"\n\nIteration {i}: After modifying the matrix:")
        print(f"Original matrix:\n{matrix}")
        print(f"Copy matrix:\n{copy_matrix}")
        
        if rec_cond(matrix):
            print("0,1 element of the matrix IS 20 ---> return")
            return

        # match is a replacement of many if else cases. It does the same but easier to read
        match copy_method:
            case 1:
                print("\nI am using regular assignment")
                matrix = copy_matrix

            case 2:
                print("\nI am using copy.copy")
                matrix = copy.copy(copy_matrix)

            case 3:
                print("\nI am using deepcopy")
                matrix = copy.deepcopy(copy_matrix)

            case 4:
                print("\nI that wierd chatgpt syntax")
                matrix[:] = copy_matrix

            case _:
                pass
            
        print(f"\n\nIteration {i}: After setting back the snapshot:")
        print(f"Original matrix:\n{matrix}")
        print(f"Copy matrix:\n{copy_matrix}")
        print("-------------------------------------------")

init_matrix = [
                [1, 2],
                [3, 4]
            ]

test_copy_method(init_matrix, 4)

print(f"\n\nAt the end the init matrix:\n{init_matrix}")