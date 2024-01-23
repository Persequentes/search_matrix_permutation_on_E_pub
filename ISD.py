import numpy as np
from itertools import combinations
import time
from math import log2
import random

def div_string(matrix, i, k):
    for j in range(len(matrix)):
        if i != j:
            if matrix[j][k] == 0:
                continue
            matrix[j] = (matrix[j] + matrix[i]) % 2
    return matrix

def swap_two_string_in_matrix(matrix, i, k):
    for j in range(i + 1, len(matrix)):
        if matrix[j][k] != 0:
            time_line = [el for el in matrix[i]]
            matrix[i] = matrix[j]
            matrix[j] = time_line
            break
    else:
        # print("Преобразованием строк не получится, надо еще менять местами столбцы")
        # print_matrix(matrix.astype(int))
        return matrix, "Error"

    return matrix, "=)"

def generate_X_and_Y(list_all):
    # set_x = np.random.choice(list_all, len(list_all)//2, replace=False)
    # set_y = np.array(list(set(list_all) - set(set_x)))
    middle = len(list_all) // 2
    return list_all[:middle], list_all[middle:]

def generate_p_vector(p, n):
    vectors = []
    for indices in combinations(range(n), p):
        vector = [1 if i in indices else 0 for i in range(n)]
        vectors.append(vector)
    return np.array(vectors)

def create_dictionary(matrix):
    dict = {}
    for i in range(len(matrix[0])):
        if tuple(matrix[:, i]) not in dict:
            dict[tuple(matrix[:, i])] = {"x": [i]}
        else:
            dict[tuple(matrix[:, i])]["x"].append(i)
    return dict

def test_key_in_dict_for_Y(dict_x, matrix):
    for i in range(len(matrix[0])):
        now_value = tuple(matrix[:, i])
        if now_value in dict_x:
            if 'y' not in dict_x[now_value]:
                dict_x[now_value]["y"] = [i]
            else:
                dict_x[now_value]["y"].append(i)
    return dict_x


def matrix_X_plus_syndrome(matrix_X, syndrom):
    for i in range(len(matrix_X[0])):
        matrix_X[:,i] = (matrix_X[:,i] + syndrom) % 2
    return matrix_X

def spisok_in_vector(spisok, n):
    result = [0] * n
    for el in spisok:
        result[el] = 1
    return result

def list_number(list_value, vector):
    list_ones = []
    for i in range(len(vector)):
        if vector[i] == 1:
            list_ones.append(list_value[i])
    return list_ones

def generate_syndrome_for_p_vectors(dict_all, vectors_X, vectors_Y, H3, t, p, position_col, set_x, set_y, n, syndrome):
    for key in dict_all.keys():
        if "y" in dict_all[key]:
            now_x, now_y = dict_all[key]["x"], dict_all[key]["y"]
            for x in now_x:
                for y in now_y:
                    concatenate_v = np.concatenate((vectors_X[x], vectors_Y[y]))
                    # concatenate_v = concatenate_vectors(set_x, set_y, vectors_X[x], vectors_Y[y])
                    now_syndrom_for_H3 = ((H3 @ concatenate_v.T) % 2 + np.array(syndrome)) % 2
                    if np.sum(now_syndrom_for_H3) <= t - 2 * p:
                        spisok_ones =   spisok_in_vector(list_number(position_col, now_syndrom_for_H3), n)
                        spisok_ones_x = spisok_in_vector(list_number(set_x, vectors_X[x]), n)
                        spisok_ones_y = spisok_in_vector(list_number(set_y, vectors_Y[y]), n)
                        return np.array(spisok_ones) + np.array(spisok_ones_x) + np.array(spisok_ones_y)

    return False


def only_Gauss(matrix, l, p, t, no_candidate_for_take="False"):
    n = len(matrix[0])-1
    # matrix = np.concatenate((matrix, z[:, np.newaxis]), axis=1).astype(int)
    candidate_for_take = [i for i in range(len(matrix[0]) - 1)]
    if no_candidate_for_take != "False":
        candidate_for_take = list(set(candidate_for_take) - set(no_candidate_for_take))
    position_col = []
    for i in range(len(matrix) - l):
        for j in range(len(candidate_for_take)):
            if matrix[i][candidate_for_take[j]] == 1:
                matrix = div_string(matrix, i, candidate_for_take[j])
                position_col.append(candidate_for_take[j])
                parametr_break = 1
                del candidate_for_take[j]
                break
            else:
                matrix, error = swap_two_string_in_matrix(matrix, i, candidate_for_take[j])
                if error == "Error":
                    continue
                matrix = div_string(matrix, i, candidate_for_take[j])
                position_col.append(candidate_for_take[j])
                del candidate_for_take[j]
                parametr_break = 1
                break
        else:
            for j in range(len(no_candidate_for_take)):
                if matrix[i][no_candidate_for_take[j]] == 1:
                    matrix = div_string(matrix, i, no_candidate_for_take[j])
                    position_col.append(no_candidate_for_take[j])
                    parametr_break = 1
                    del no_candidate_for_take[j]
                    break
                else:
                    matrix, error = swap_two_string_in_matrix(matrix, i, no_candidate_for_take[j])
                    if error == "Error":
                        continue
                    matrix = div_string(matrix, i, no_candidate_for_take[j])
                    position_col.append(no_candidate_for_take[j])
                    del no_candidate_for_take[j]
                    parametr_break = 1
                    break
            else:
                parametr_break = 0
        if parametr_break == 1:
            continue
        else:
            print("*", end="")
            return False

    candidate_for_take_X_and_Y = np.array(list(set([i for i in range(n)]) - set(position_col)))
    candidate_for_take_X_and_Y = np.sort(candidate_for_take_X_and_Y)
    # print(candidate_for_take_X_and_Y)
    H3 = matrix[:-l, candidate_for_take_X_and_Y]

    set_X, set_Y = generate_X_and_Y(candidate_for_take_X_and_Y)

    # H2 = matrix[-l:, set_X]
    #
    # H1 = matrix[-l:, set_Y]
    H1 = matrix[-l:, set_X]

    H2 = matrix[-l:, set_Y]

    vectors_X = generate_p_vector(p, len(H1[0]))
    vectors_Y = generate_p_vector(p, len(H2[0]))

    matrix_X = np.dot(H1, vectors_X.T) % 2

    matrix_X = matrix_X_plus_syndrome(matrix_X, matrix[-l:, -1])
    # print(matrix_X)
    dict_X = create_dictionary(matrix_X)
    # print(dict_X)

    matrix_Y = np.dot(H2, vectors_Y.T) % 2

    dict_result = test_key_in_dict_for_Y(dict_X, matrix_Y)
    # print(dict_result)

    result_vector = generate_syndrome_for_p_vectors(dict_result, vectors_X, vectors_Y, H3, t, p, position_col, set_X, set_Y, n, matrix[:-l, -1])

    syndrome = matrix[:, -1]
    # for i in range(len(matrix)):
    #     print(f"string {i} weight = {np.sum(matrix[i][:-1])}, type = {matrix[i][-1]}")
    if type(result_vector) == bool:
        print("-", end=" ")
    return result_vector

def ISD(matrix, t, l, p):
    count, n, r = 1, len(matrix[0]) - 1, len(matrix)
    list_position = [i for i in range(n)]
    no_candidate_for_take = random.sample(list_position, n - r + l)
    vector = only_Gauss(matrix, l, p, t, no_candidate_for_take)
    while type(vector) == bool:
        no_candidate_for_take = random.sample(list_position, n - r + l)
        vector = only_Gauss(matrix, l, p, t, no_candidate_for_take)
        count += 1
    return vector, count

if __name__ == "__main__":
    matrix = np.random.randint(2, size=(10, 20))
    z = np.array([0]*10)
    matrix_orig = np.copy(matrix)
    l = 10
    p = 2
    t = 5
    time_now = time.time()
    matrix, syndrome, vector = only_Gauss(matrix, z, l, p, t)
    print(time.time()-time_now)
    print(matrix_orig, syndrome, vector)
    print(matrix_orig @ np.array(vector).T % 2)