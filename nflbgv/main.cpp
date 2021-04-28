#include <iostream>
#include <string>
#include <vector>
#include "nfl.hpp"
#include "tools.h"
using namespace std;

using poly_t = nfl::poly_from_modulus<uint32_t, 16, 312>;

/*
template <size_t degree, size_t modulus, class T>
bool run() {
  using poly_t = nfl::poly_from_modulus<T, degree, modulus>;

  bool ret_value = true;

  // Set a random number generator
  gmp_randclass prng(gmp_randinit_default);
  //prng.seed(0);

  // define a random polynomial
  poly_t& p0 = *alloc_aligned<poly_t, 32>(1, nfl::uniform());
  //poly_t P(nfl::non_uniform(2));
  poly_t P{1,1};
  poly_t Q{1,2};
  //P.ntt_pow_phi();
  P = P - Q;
  //P.invntt_pow_invphi();
  cout << "P = " << P << endl;

  // get the corresponding array of mpz_t
  std::array<mpz_t, degree> coefficients = p0.poly2mpz();

  // construct a polynomial from mpz_t coefficients
  poly_t& p1 = *alloc_aligned<poly_t, 32>(1, 0);
  p1.mpz2poly(coefficients);

  //cout << p1 << endl;
  // verify that the first and second polynomials are equal
  ret_value &= (p0 == p1);
  cout << ret_value << endl;

  // construct a vector of mpz_class
  std::vector<mpz_class> coefficients_mpz_class(poly_t::degree);
  for (size_t i = 0; i < poly_t::degree; i++) {
    coefficients_mpz_class[i] = mpz_class(coefficients[i]);
  }

  // construct a polynomial from mpz_class coefficients
  poly_t& p2 = *alloc_aligned<poly_t, 32>(1, 0);
  p2.set_mpz(coefficients_mpz_class.begin(), coefficients_mpz_class.end());

  // verify that the first and third polynomials are equal
  ret_value &= (p0 == p2);

  // Generate a random vector of mpz_class
  std::vector<mpz_class> big_array;
  for (size_t i = 0; i < poly_t::nmoduli * poly_t::degree; i++) {
    // (say) 200 bits, it doesn't matter as long as it is > 64 bits for the
    // tests
    big_array.push_back(prng.get_z_bits(200));
  }

  // construct a polynomial from the big_array vector
  poly_t& p3 = *alloc_aligned<poly_t, 32>(1, 0);
  p3.set_mpz(big_array.begin(), big_array.end());

  // verify that the coefficients of the polynomial have been set correctly
  for (size_t cm = 0; cm < poly_t::nmoduli; cm++) {
    mpz_class modulus_mpz_class(std::to_string(poly_t::get_modulus(cm)));
    for (size_t i = 0; i < poly_t::degree; i++) {
      mpz_class coeff(std::to_string(p3(cm, i)));
      ret_value &=
          ((big_array[cm * poly_t::degree + i] % modulus_mpz_class) == coeff);
    }
  }

  // Cleaning
  for (size_t i = 0; i < poly_t::degree; i++) {
    mpz_clear(coefficients[i]);
  }
  free_aligned(1, &p0);
  free_aligned(1, &p1);
  free_aligned(1, &p2);
  free_aligned(1, &p3);

  return ret_value;
}
*/

int main() {
  //run<64, 248, uint32_t>();
  
  poly_t P{1,1};
  poly_t Q{1,2};
  P.ntt_pow_phi();
  Q.ntt_pow_phi();
  //poly_t numerator{P - Q*Q};
  //numerator.invntt_pow_invphi();
  
  poly_t R =  Q-P;
  //R = R - Q;
  //R = R - Q;
  R.invntt_pow_invphi();
  //cout << R << endl;
  std::array<mpz_t, 16> coefficients = R.poly2mpz();

  cout << R << endl;
  gmp_printf("%Zd\n", coefficients[1]);

  return 0;
}
