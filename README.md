To make it work, you need to add a folder codeword_with_errors 
  
  To find the permutation matrix P*=(P_2)P.
Either add your own E_pub matrix, or generate one in the file create_matrix_E_pub.py, using the function create_E_pub(k-information characters, n-code length, r_D - number of erasures or units in D)
Then in def main_3(n, d-code distance, t-number of errors, r_D, value_count_e-how many words of weight t to look for) this function already reconstructs the permutation.
If the E_pub was generated via the create_E_pub function, you can compare it to the P* that is actually there.

  There are 2 functions in this file test_time_work_algorithm.py, main_test_with_one_matrix_time for the first attack, main_test_with_two_matrix_time for the second. All matrices are generated for them according to the parameters and a random message. If desired, you can enter your own matrices and messages...
