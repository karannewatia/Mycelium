This is an implementation of the BGV FHE crypto-system, used to benchmark FHE costs.

Requirements:
- python (version v>3)
- sympy (can be installed using `pip install sympy`)
- python2 (2.7) (for playing around with the FHE implementation; see below)


To test the time taken for a ciphertext encryption:
- `python encryption_test.py`

To test the time taken for a ciphertext-ciphertext addition:
- `python addition_test.py`

To test the time taken for 10 ciphertext-ciphertext multiplications:
- `python multiplication_test.py`

The costs we got when benchmarking on our machine are in `crypto_costs.txt`. Times may vary slightly based on machine resources.

To play around with the FHE implementation:
- change the variables (lgP, lgM, lgN, l) in `input_gen.py` as needed
- Run `python2 input_gen.py`
- The generated p and w values will be printed out
- Note that the number of ciphertext additions and multiplications which can be performed
 depends on the values of the plaintext modulus, ciphertext modulus, and the polynomial degree.
 See `noise.py` for details.
- After changing the inputs to the function in `noise.py`, run using `python noise.py`
 to check whether the desired number of additions and multiplications is possible with the given set of parameters.
- Copy the variable values (lgP, lgM, lgN, l) from `input_gen.py` to `fhe_test.py`
- Copy the generated p and w values into lines 13 and 14 respectively of `fhe_test.py`
- Add/remove FHE operations (using the functions in `lwe.py`) in `fhe_test.py` as needed
- Run `python fhe_test.py`
