from create_matrix_E_pub import create_E_pub, create_matrix_E_1_and_E_2_and_all, create_E_pub_with_permutation_matrix
from generate_vector_y import generate_vector_y_for_one_E, generate_vector_y_for_two_E
from attack_matrix_to_quasi_form import attack_with_use_H_pub_main, attack_with_two_matrix_E
from test_idea import main_3
from create_matrix_H_pub import create_matrix_H_pub
import numpy as np


def main_test_with_one_matrix_time(n, k, r_D, t, l, p, count):
    create_E_pub(n, k, r_D)
    # generate_vector_y_for_one_E(np.round(np.random.random(k)).astype(int), t)
    # test_sum, cw = 0, np.load("codeword_with_errors\\cw.npy")
    test_sum = 0
    time_all, time_iters = 0, 0
    for _ in range(count):
        generate_vector_y_for_one_E(np.round(np.random.random(k)).astype(int), t)
        only_e = np.load("codeword_with_errors\\only_vector_error.npy")
        cw = np.load("codeword_with_errors\\cw.npy")
        y_now, e, time_now, iter_now = attack_with_use_H_pub_main(t, l, p)
        time_all, time_iters = time_all + time_now, time_iters + iter_now
        test_sum += all(y_now == cw)
        print(sum(only_e), all(y_now == cw))
        print()

    print(time_all / count, time_iters / count)
    print(test_sum)
    return time_all / count, time_iters / count

def main_test_with_two_matrix_time(n, k, r_D, t, l, p, count, count_iteration_for_matrix_p):
    # create_matrix_E_1_and_E_2_and_all(n, k, r_D)
    # generate_vector_y_for_two_E(np.round(np.random.random(k)).astype(int), t)
    E_pub = create_E_pub_with_permutation_matrix(n, k, r_D)
    generate_vector_y_for_one_E(np.round(np.random.random(k)).astype(int), t)
    test_sum, cw = 0, np.load("codeword_with_errors\\cw.npy")
    y = np.load("codeword_with_errors\\y.npy")
    time_all, time_iters = 0, 0

    G_pub = np.load("Matrix_and_other\\G_pub_new.npy")
    H_pub = create_matrix_H_pub(G_pub)
    m_orig_m_2 = main_3(n, t, count_iteration_for_matrix_p)
    matrix_2 = (np.dot(m_orig_m_2, H_pub.T)) % 2
    matrix_1 = (np.dot((E_pub + m_orig_m_2) % 2,  H_pub.T)) % 2
    for _ in range(count):
        s = (y @ H_pub.T) % 2
        e_2, e_1, iter_now, time_now = attack_with_two_matrix_E(matrix_1, matrix_2, s, t, l, p)
        time_all, time_iters = time_all + time_now, time_iters + iter_now
        test_sum += all((y - e_2 @ E_pub) % 2 == cw)
        print()

    print(time_all / count, time_iters / count)
    print(test_sum)
    return time_all / count, time_iters / count

if __name__ == "__main__":
    # n, k, r_D, t, l, p, count = 255, 123, 10, 11, 10, 2, 100
    # n, k, r_D, t, l, p, count = 255, 191, 6, 5, 10, 2, 2
    # main_test_with_one_matrix_time(n, k, r_D, t, l, p, count)
    n, k, r_D, t, l, p, count, iteration = 255, 123, 10, 11, 10, 2, 10, 255
    main_test_with_two_matrix_time(n, k, r_D, t, l, p, count, iteration)

