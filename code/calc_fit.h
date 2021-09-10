#ifndef CALC_FIT_H__
#define CALC_FIT_H__

#include <stdlib.h>
#include <stdio.h>

#include <vector>
#include <string>
#include <numeric>
#include <cmath>

using namespace std;

void set_params(vector< vector<float> > r_aux, vector< vector<float> > samples_train_aux, vector< vector<float> > samples_val_aux, vector< vector<float> > samples_test_aux, vector< vector<float> > y_train_aux, vector< vector<float> > y_val_aux, vector< vector<float> > y_test_aux);

void clean_r();

float division(float x, float y);
float square(float x);
float natLog(float x);
float tangent(float x);

vector< vector<float> > calc_vector(vector< vector<string> > ind);
vector<float> calc_fit(vector< vector<string> > ind, string type, vector<string> measures);

#endif /* CALC_FIT__ */

