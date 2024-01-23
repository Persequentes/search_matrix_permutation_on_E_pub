import numpy as np

def create_matrix_H_pub(G):
    n, k = len(G[0]), len(G)
    M, permutation = gauss_matrix_for_H_pub(G)
    H = np.concatenate([M[:, k:].T, np.eye(n-k).astype(int)], axis=1)
    return take_place(H, permutation)

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
        return matrix, "Error"

    return matrix, "=)"

def swap_two_column_in_matrix(matrix, i, o):
    for k in range(i, len(matrix[0])):
        if matrix[i][k] != 0:
            time_col = [matrix[l][i] for l in range(len(matrix))]
            for l in range(len(matrix)):
                matrix[l][i] = matrix[l][k]
                matrix[l][k] = time_col[l]
            o[i], o[k] = o[k], o[i]
            break
    else:
        print("rank(G_pub) < k")
        return matrix, "Trouble"
    return matrix, o

def gauss_matrix_for_H_pub(G_pub):
    o = [i for i in range(len(G_pub[0]))]
    matrix = np.copy(G_pub)
    for i in range(len(G_pub)):
        if matrix[i][i] == 0:
            matrix, error = swap_two_string_in_matrix(matrix, i)
            if error == "Error":
                matrix, o = swap_two_column_in_matrix(matrix, i, o)

        matrix = div_string(matrix, i)

    return matrix, o

def take_place(matrix, o):
    if o == list(range(len(matrix[0]))):
        return matrix
    result = np.copy(matrix)
    for i in range(len(matrix)):
        result[:, o[i]] = matrix[: , i]
    return result

if __name__ == "__main__":
    G_pub = np.load("Matrix_and_other/G_pub_new.npy")
    H_pub = create_matrix_H_pub(G_pub)
    r = np.dot(G_pub, H_pub.T) % 2
    print(r)
    np.save("Matrix_and_other/H_pub_new", H_pub)
