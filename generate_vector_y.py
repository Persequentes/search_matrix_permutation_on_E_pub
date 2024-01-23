import numpy as np
import random

def generate_e_1(n, t):
    position = random.sample(list(range(n)), t)
    e_1 = np.array([0]*n)
    for i in range(t):
        e_1[position[i]] = 1
    return e_1

def generate_vector_y_for_two_E(m, t):
    G, M = np.load("Matrix_and_other/G_new.npy"), np.load("Matrix_and_other/random_matrix_M_new.npy")
    E_1, E_2, n = np.load("Matrix_and_other/E_1_new.npy"), np.load("Matrix_and_other/E_2_new.npy"), len(G[0])
    e_1, e_2 = np.round(np.random.random(n)).astype(int), generate_e_1(n, t)
    y = (np.dot(np.dot(m, G), M) + np.dot(e_1, E_1) + np.dot(e_2, E_2)) % 2
    np.save("codeword_with_errors/e_1", e_1)
    np.save("codeword_with_errors/cw", np.dot(np.dot(m, G), M)%2)
    np.save("codeword_with_errors/e_2", e_2)
    np.save("codeword_with_errors/y", y)
    np.save("codeword_with_errors/m", m)
    # print(e_1, e_2, y, m, sep="\n")

def generate_vector_y_for_one_E(m, t):
    G_pub = np.load("Matrix_and_other/G_pub_new.npy")
    E_pub, n = np.load("Matrix_and_other/E_pub.npy"), len(G_pub[0])
    e = generate_e_1(n, t)
    y = (np.dot(m, G_pub) + np.dot(e, E_pub)) % 2
    np.save("codeword_with_errors/e", e)
    np.save("codeword_with_errors/cw", np.dot(m, G_pub) % 2)
    np.save("codeword_with_errors/y", y)
    np.save("codeword_with_errors/m", m)
    W, D = np.load("Matrix_and_other/random_matrix_W.npy"), np.load("Matrix_and_other/diagonal_matrix_D.npy")
    P_1, P_2 = np.load("Matrix_and_other/permutation_matrix_P_1.npy"), np.load("Matrix_and_other/permutation_matrix_P_2.npy")
    only_error = (e @ (W @ D @ P_1 + P_2)) % 2
    np.save("codeword_with_errors/only_vector_error", only_error)
    # print(e, e_2, y, m, sep="\n")

if __name__ == "__main__":
    # k, t = 191, 5
    # k, t = 123, 11
    # generate_vector_y_for_two_E(np.round(np.random.random(k)).astype(int), t)
    k, t = 123, 5
    generate_vector_y_for_one_E(np.round(np.random.random(k)).astype(int), t)
