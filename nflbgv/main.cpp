#include <iostream>
#include <string>
#include <vector>
#include "nfl.hpp"
#include "tools.h"
using namespace std;

// <align, degree, modulus>
using poly_t = nfl::poly_from_modulus<uint64_t, 16, 550>;

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

// ****** template for NTT ******
void DFT (mpz_t *a, int len) {
  if (len == 1) {
          cout << "out" <<endl;
          return;
  }
  mpz_t *a0 = new mpz_t[len/2];
  mpz_t *a1 = new mpz_t[len/2];
  cout << "here" << endl;
  for (int i = 0; i < len; i+=2) {
    cout << "III" << endl;
    mpz_set(a0[i/2], a[i]);
    cout << "i+1=" << i+1 << endl;
    mpz_set(a1[i/2], a[i+1]);
    
  }
  
  DFT(a0, len/2);
  DFT(a1, len/2);

  //cout << "middle" <<endl;
  mpz_t w, wn;
  
  cout << "XXXXX" << endl;
  mpz_init_set_str(wn, "1", 10);  // n-th primitive root
  mpz_init_set_str(w, "1", 10);
  for (int i = 0; i < len/2; i++) {
    mpz_t rop1;
    mpz_t rop2;

    mpz_mul(rop1, w, a1[i]);
    mpz_add(rop2, a0[i], rop1);
    mpz_set(a[i], rop2);

    mpz_t rop3;
    mpz_t rop4;

    mpz_mul(rop3, w, a1[i]);
    mpz_sub(rop4, a0[i], rop3);
    mpz_set(a[i+len/2], rop4);
    
    mpz_mul(w, w, wn);
  }
  delete[] a0;
  delete[] a1;
}

int main() {
  //run<64, 248, uint32_t>();

  auto st = std::chrono::high_resolution_clock::now();

  poly_t P{1,1};
  poly_t Q{1,2};
  P.ntt_pow_phi();
  Q.ntt_pow_phi();
  //poly_t numerator{P - Q*Q};
  //numerator.invntt_pow_invphi();
  
  poly_t R =  Q-P;
  R = R * Q;
  //R = R - Q;
  R.invntt_pow_invphi();
  //cout << R << endl;
  std::array<mpz_t, 16> coefficients = R.poly2mpz();

  mpz_t *test = new mpz_t[16];
  for (int i = 0; i < 16; i++) {
    mpz_set(test[i], coefficients[i]);
  }
  DFT(test, 16);
  //delete[] test;

  auto ed = std::chrono::high_resolution_clock::now();
  auto multime = std::chrono::duration_cast<std::chrono::microseconds>(ed - st).count();
  std::cout << "mult generated in " << multime << " microsec." << std::endl;
  //cout << R << endl;

  
 

  auto clt_offline_st = std::chrono::high_resolution_clock::now();
  
  mpz_t q;
  mpz_t tmp;
  mpz_init_set_str(wn, "452312848531021619072928088353457404578753483289040917211364875968704413697", 10);
  // ******* Estimation of naive poly mult ******
  std::array<mpz_t, 32> prod;
  for (int i = 0; i < 16; i++) {
    for (int j = 0; j < 16; j++) { 
      mpz_mul(prod[i+j], coefficients[i], coefficient[j]);
      mpz_mod(prod[i+j], tmp, q);
    }
  }

    //mpz_mul(coefficients[0], coefficients[1], coefficients[1]);
    //mpz_cdiv_q(coefficients[0], coefficients[1], coefficients[0]);
    //mpz_mod(coefficients[0], coefficients[0], coefficients[0]);
  
  //mpz_mul(coefficients[0], coefficients[1], coefficients[1]);
  auto clt_offline_ed = std::chrono::high_resolution_clock::now();
  auto clt_offline_time = std::chrono::duration_cast<std::chrono::microseconds>(clt_offline_ed - clt_offline_st).count();
  std::cout << "mult generated in " << clt_offline_time << " microsec." << std::endl;


  gmp_printf("%Zd\n", coefficients[1]);

  return 0;
}
