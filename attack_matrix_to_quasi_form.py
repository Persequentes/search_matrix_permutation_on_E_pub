import numpy as np
from ISD import ISD
import time
from create_matrix_H_pub import create_matrix_H_pub

def div_string(matrix, i):
    for j in range(len(matrix)):
        if i != j:
            if matrix[j][i] == 0:
                continue
            matrix[j] = (matrix[j] + matrix[i]) % 2
    return matrix

def swap_two_string_in_matrix(matrix, i):
    for j in range(i + 1, len(matrix)):
        if matrix[j][i] != 0:
            time_line = [el for el in matrix[i]]
            matrix[i] = matrix[j]
            matrix[j] = time_line
            break
    else:
        # print("Преобразованием строк не получится, надо еще менять местами столбцы")
        # print_matrix(matrix.astype(int))
        return matrix, "Error"

    return matrix, "=)"

def matrix_to_quasi_form_new(matrix_concatenation, s):
    matrix, list_position = np.concatenate((matrix_concatenation, s[:, np.newaxis]), axis=1), []
    for i in range(len(matrix)):
        if matrix[i][i] == 0:
            matrix, error = swap_two_string_in_matrix(matrix, i)
            if error == "Error":
                continue
        matrix = div_string(matrix, i)
        list_position.append(i)

    return matrix, list_position

def create_e_1(e_1, n, r_D):
    result = np.array([0]*n)
    for i in range(len(r_D)):
        if e_1[i] == 1:
            result[r_D[i]] = 1
    return result

def attack_with_two_matrix_E(matrix_1, matrix_2, s, t, l, p):
    n = len(matrix_1)
    # time_start, iter = time.time(), 0
    matrix_concatenation = np.concatenate((matrix_1, matrix_2), axis=0).T
    matrix_new, position_r_D = matrix_to_quasi_form_new(matrix_concatenation, s)
    # print(position_r_D)
    time_start, iter = time.time(), 0
    e_2, count = ISD(np.delete(matrix_new[:, len(matrix_new[0]) // 2:], position_r_D, axis=0), t, l, p)
    e_1 = (np.dot(e_2, matrix_new[position_r_D, n:-1].T) + matrix_new[position_r_D, -1].T) % 2
    e_1 = create_e_1(e_1, n, position_r_D)
    return e_2, e_1, count, time.time() - time_start

def attack_with_use_H_pub_main(t, l, p):
    E_pub, y = np.load("Matrix_and_other\\E_pub.npy"), np.load("codeword_with_errors\\y.npy")
    G_pub = np.load("Matrix_and_other\\G_pub_new.npy")
    H_pub = create_matrix_H_pub(G_pub)
    s = np.dot(y, H_pub.T)
    time_now = time.time()
    error_vector, iter = ISD(np.concatenate((np.dot(H_pub, E_pub.T) % 2, s[:, np.newaxis]), axis=1), t, l, p)
    end_time = time.time()
    c_origin = (y - np.dot(error_vector, E_pub)) % 2
    return c_origin, error_vector, end_time - time_now, iter


if __name__ == "__main__":
    E_1, E_2  = np.load("Matrix_and_other/E_1_new.npy"), np.load("Matrix_and_other/E_2_new.npy")
    H_pub, y = np.load("Matrix_and_other/H_pub_new.npy"), np.load("codeword_with_errors/y.npy")
    # t, l, p = 5, 10, 2
    t, l, p = 11, 10, 2

    start_time = time.time()

    e_2_candidate, e_1_candidate, count = attack_with_two_matrix_E(np.dot(E_1, H_pub.T) % 2, np.dot(E_2, H_pub.T) % 2, np.dot(y, H_pub.T) % 2, t, l, p)

    print(time.time() - start_time)

    e_2 = np.load("codeword_with_errors/e_2.npy")
    e_1 = np.load("codeword_with_errors/e_1.npy")
    print(e_2_candidate)
    print(np.array(e_2))
    print(e_1_candidate)
    print(e_1)
    cw_real = np.load("codeword_with_errors/cw.npy")
    our_cw = (y + np.dot(e_1, E_1) + np.dot(e_2, E_2)) % 2
    print("===" * 20)
    print(cw_real % 2)
    print(our_cw)
    print(count)
