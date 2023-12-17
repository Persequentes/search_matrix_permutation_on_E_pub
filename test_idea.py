import numpy as np
import random
from prettytable import PrettyTable

def create_vector_weight_t(n, t):
    list_val = random.sample([i for i in range(n)], t)
    e = np.array([0] * n)
    for el in list_val:
        e[el] = 1
    return e

def create_result_P2_P3(P_2, P_3):
    result = np.dot(P_2, P_3) % 2
    list_position_1 = np.array([0] * len(P_2))
    list_position_2 = np.array([0] * len(P_2))
    for i in range(len(P_2)):
        for j in range(len(P_3)):
            if result[i][j] == 1:
                list_position_1[i] = j
    return list_position_1



def main(n, d, t, r_D,value_count_e):
    my_table = PrettyTable()
    my_table.field_names = [i for i in range(n)]
    E_pub = np.load("Matrix_and_other\\E_pub.npy")
    E_pub = E_pub.astype(int)
    count, count_2, count_value_in_place = 0, 0, np.array([0] * n)
    while count < value_count_e:
        vector_e_E = np.dot(create_vector_weight_t(n, t), E_pub) % 2
        count_2 += 1
        if sum(vector_e_E) < d:
            count += 1
            print(count, end=" ")
            for i in range(n):
                if vector_e_E[i] == 1:
                    count_value_in_place[i] += 1
    my_table.add_row(count_value_in_place)
    D_list = np.load("Matrix_and_other\\diagonal_matrix_D_list.npy")
    print("\n", D_list, sep="")
    print(my_table)
    print(count_2)
    print(sum(count_value_in_place))

def main_2(n, r_D, count):
    E_1 = np.load("Matrix_and_other\\E_1_test.npy")
    H = np.load("Matrix_and_other\\matrix_H.npy")
    s = np.dot(np.dot(create_vector_weight_t(n, r_D), E_1), H.T) % 2
    print(*s)
    for i in range(count):
        now_vec = create_vector_weight_t(n, r_D)
        if np.array_equal(s, np.dot(np.dot(now_vec, E_1), H.T) % 2):
            print(*now_vec, *(np.dot(np.dot(now_vec, E_1), H.T) % 2))

def main_3(n, d, t, r_D, value_count_e):
    my_table = PrettyTable()
    my_table.field_names = [i for i in range(n)]
    E_pub = np.load("Matrix_and_other\\E_pub.npy")
    E_pub = E_pub.astype(int)
    count, count_2, count_value_in_place = 0, 0, np.array([set(["-"]) for _ in range(n)])
    while count < value_count_e:
        vector_e = create_vector_weight_t(n, t)
        vector_e_E = np.dot(vector_e, E_pub) % 2
        count_2 += 1
        if sum(vector_e_E) == t:
            count += 1
            print(count, end=" ")
            spisok_place = []
            for j in range(n):
                if vector_e_E[j] == 1:
                    spisok_place.append(j)
            spisok_place = np.array(spisok_place)
            for i in range(n):
                if vector_e[i] == 1:
                    if len(count_value_in_place[i]) == 1 and count_value_in_place[i] == set(["-"]):
                        count_value_in_place[i] = set(spisok_place)
                    elif len(count_value_in_place[i]) != 1:
                        count_value_in_place[i] = count_value_in_place[i] & set(spisok_place)
    my_table.add_row(count_value_in_place)
    D_list = np.load("Matrix_and_other\\diagonal_matrix_D_list.npy")
    P_2 = np.load("Matrix_and_other\\permutation_matrix_P_2.npy")
    P_3 = np.load("Matrix_and_other\\permutation_matrix_P_3.npy")
    composition_permutation_1 = create_result_P2_P3(P_2, P_3)
    my_table.add_row(composition_permutation_1)
    print("\n", D_list, sep="")
    print(my_table)
    print(count_2)



if __name__ == "__main__":
    # main(100, 12, 4, 4, 100)
    # main_2(100, 2, 100)
    main_3(200, 24, 8, 8, 50)