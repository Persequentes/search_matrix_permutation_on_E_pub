import numpy as np
import random
from random_shuffle_matrix import random_matrix_from_given_elementary_transform
from test_matrix_is_nosingular import check_nonsingular

def write_in_np_save(name_file, data):
    np.save(f"Matrix_and_other\\{name_file}", data)

def create_matrix_permutation_P(n, name):
    permutation_list = list(range(n))
    random.shuffle(permutation_list)
    matrix_permutation_P = np.zeros((n, n), dtype=int)
    for i in range(n):
        matrix_permutation_P[permutation_list[i]][i] = 1
    write_in_np_save(f"permutation_matrix_P_list_{name}", permutation_list)
    write_in_np_save(f"permutation_matrix_P_{name}", matrix_permutation_P)
    return matrix_permutation_P

def create_matrix_random_W(n):
    matrix_random = [[random.randint(0,1) if i > j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        matrix_random[i][i] = 1
    matrix_random = random_matrix_from_given_elementary_transform(matrix_random, 1000, 2)
    matrix_random = np.array(matrix_random)
    write_in_np_save("random_matrix_W", matrix_random)
    return matrix_random

def create_matrix_D(n, r_D):
    permutation_list = random.sample(list(range(n)), r_D)
    matrix_diagonal_D = np.zeros((n, n), dtype=int)
    for i in range(r_D):
        matrix_diagonal_D[permutation_list[i]][permutation_list[i]] = 1
    write_in_np_save(f"diagonal_matrix_D_list", permutation_list)
    write_in_np_save(f"diagonal_matrix_D", matrix_diagonal_D)
    return matrix_diagonal_D

def create_matrix_G_and_U(k, n):
    G = np.random.random((k, n))
    U = np.random.random((n, k))
    G, U = np.round(G), np.round(U)
    G, U = G.astype(int), U.astype(int)
    write_in_np_save(f"matrix_G", G)
    write_in_np_save(f"matrix_U", U)
    return G, U

def create_matrix_G_and_U_and_H(k, n):
    M = np.random.random((k, n - k))
    U = np.random.random((n, k))
    M, U = np.round(M), np.round(U)
    G = np.concatenate([np.eye(k), M], axis=1)
    H = np.concatenate([M.T, np.eye(n-k)], axis=1)
    U, G, H = U.astype(int), G.astype(int), H.astype(int)
    return U, G, H

def create_E_pub(k, n, r_D):
    W = create_matrix_random_W(n)
    D = create_matrix_D(n, r_D)
    P_1 = create_matrix_permutation_P(n, "1")
    P_2 = create_matrix_permutation_P(n, "2")
    while check_nonsingular((W @ D @ P_1 + P_2) % 2) == False:
        P_1 = create_matrix_permutation_P(n, "1")
        P_2 = create_matrix_permutation_P(n, "2")
        print("*")
    G, U = create_matrix_G_and_U(k, n)
    P_3 = create_matrix_permutation_P(n, "3")
    # E_pub = ((W @ D @ (U @ G + P_1) + P_2) @ P_3) % 2
    E_pub = np.dot((np.dot(np.dot(W, D), (np.dot(U, G) + P_1)) + P_2), P_3) % 2
    E_pub = np.round(E_pub)
    E_pub = E_pub.astype(int)
    write_in_np_save(f"E_pub", E_pub)
    return E_pub

def create_matrix_erasures(n, k, r_D):
    W = create_matrix_random_W(n)
    D = create_matrix_D(n, r_D)
    P_1 = create_matrix_permutation_P(n, "_for_erasures")
    U, G, H = create_matrix_G_and_U_and_H(k, n)
    E_1 = np.dot(np.dot(W, D), np.dot(U, G) + P_1) % 2
    E_1 = np.round(E_1)
    E_1 = E_1.astype(int)
    write_in_np_save(f"E_1_test", E_1)
    write_in_np_save("matrix_H", H)
    return E_1, H


if __name__ == "__main__":
    E_pub = create_E_pub(100, 200, 8)
    # print(create_matrix_erasures(100, 50, 5))


