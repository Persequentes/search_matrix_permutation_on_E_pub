import random
def random_matrix_from_given_elementary_transform(matrix, n, p):
    for_row, for_col = range(len(matrix)), range(len(matrix[0]))
    for _ in range(n):
        choice = random.randint(1,4)
        if choice == 1:
            first, second = random.sample(for_row, 2)
            matrix = add_string_with_matrix(matrix, first, second, p)
        elif choice == 2:
            first, second = random.sample(for_col, 2)
            matrix = add_col_with_matrix(matrix, first, second, p)
        elif choice == 3:
            first, second = random.sample(for_row, 2)
            matrix = swap_two_string_in_matrix(matrix, first, second)
        elif choice == 4:
            first, second = random.sample(for_col, 2)
            matrix = swap_two_column_in_matrix(matrix, first, second)
    return matrix

def add_string_with_matrix(matrix, i, j, p):
    for k in range(len(matrix[0])):
        matrix[j][k] = (matrix[j][k] + matrix[i][k]) % p
    return matrix

def add_col_with_matrix(matrix, i, j, p):
    for k in range(len(matrix)):
        matrix[k][j] = (matrix[k][j] + matrix[k][i]) % p
    return matrix

def swap_two_string_in_matrix(matrix, i, j):
    time_line = [el for el in matrix[i]]
    matrix[i] = matrix[j]
    matrix[j] = time_line
    return matrix

def swap_two_column_in_matrix(matrix, i, j):
    time_col = [matrix[l][i] for l in range(len(matrix))]
    for l in range(len(matrix)):
        matrix[l][i] = matrix[l][j]
        matrix[l][j] = time_col[l]
    return matrix
