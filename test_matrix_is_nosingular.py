import numpy as np

def div_string(matrix, e, i):
    for j in range(len(matrix)):
        if i != j:
            k_for_step = matrix[j][i]
            matrix[j] = (matrix[j] - matrix[i] * k_for_step) % 2
            e[j] = (e[j] - e[i] * k_for_step) % 2
    return matrix, e


def swap_two_string_in_matrix(matrix, e, i):
    for j in range(i + 1, len(matrix)):
        if matrix[j][i] != 0:
            time_line = [el for el in matrix[i]]
            matrix[i] = matrix[j]
            matrix[j] = time_line
            time_line = [el for el in e[i]]
            e[i] = e[j]
            e[j] = time_line
            break
    else:
        print("Данная матрица не имеет обратной... Она имеет зависимые строки")
        return "Error", "Error", "Error"

    return matrix, e, "=)"


def my_rev_matrix_fast(matrix):
    e = np.eye(len(matrix), dtype=int)
    for i in range(len(matrix)):
        if matrix[i][i] == 0:
            matrix, e, error = swap_two_string_in_matrix(matrix, e, i)
            # for cryptanalysis
            if error == "Error":
                return np.zeros((len(matrix), len(matrix)), int)

        matrix, e = div_string(matrix, e, i)
    return e

def check_nonsingular(matrix):
    e = np.eye(len(matrix), dtype=int)
    for i in range(len(matrix)):
        if matrix[i][i] == 0:
            matrix, e, error = swap_two_string_in_matrix(matrix, e, i)
            # for cryptanalysis
            if error == "Error":
                return False

        matrix, e = div_string(matrix, e, i)
    return True