#include "calc_fit.h"

using namespace std;

/* Variables (training, validation, and testing input and registers) */
vector< vector<float> > r;
vector< vector<float> > samples_train;
vector< vector<float> > samples_val;
vector< vector<float> > samples_test;
vector< vector<float> > y_train;
vector< vector<float> > y_val;
vector< vector<float> > y_test;

vector< vector<float> > samples;
vector< vector<float> > y;

/* Loads problem data and registers vector */
void set_params(vector< vector<float> > r_aux, vector< vector<float> > samples_train_aux, vector< vector<float> > samples_val_aux, vector< vector<float> > samples_test_aux, vector< vector<float> > y_train_aux, vector< vector<float> > y_val_aux, vector< vector<float> > y_test_aux) {
	r = r_aux;
	samples_train = samples_train_aux;
	samples_val = samples_val_aux;
	samples_test = samples_test_aux;
	y_train = y_train_aux;
	y_val = y_val_aux;
	y_test = y_test_aux;
}

/* Assigns input values to registers in a cyclic manner */
void clean_r() {
	for(int i=0; i<r.size(); i++) {
		for(int j=0; j<y.size(); j++) {
			r[i][j] = samples[j][i%samples[j].size()];
		}
	}
}

float division(float x, float y) {
	if(y != 0) return x/y;
	else return 1.0;
}

float square(float x) {
	if(x >= 0) return sqrt(x);
	else return 1.0;
}

float natLog(float x) {
	if(x > 0) return log(x);
	else return 1.0;
}

float tangent(float x) {
	if(cos(x) != 0) return tan(x);
	else return 1.0;
}

void print_vec(vector<float> vec) {
	for(int i=0; i<vec.size(); i++) {
		printf("%f ", vec[i]);
	}
	printf("\n");
}

/* Calculates output vector of an individual applied on input data instances */
vector< vector<float> > calc_vector(vector< vector<string> > ind) {

	clean_r();

	/* Process each instruction */
	for(int i = 0; i < ind.size(); i++) {

		/* Load elements from instruction */
		vector<string> inst = ind[i];

//		for(int pos=0; pos<inst.size(); pos++) {
//			printf("%s ", inst[pos].c_str());
//		}
//		printf("\n");

		string op = inst[0];
		string dest = inst[1];
		string arg1 = inst[2];
		string arg2 = inst[3];

		int destIdx = atoi(dest.c_str());
		int arg1Idx = atoi(arg1.substr(1).c_str());
		char arg2Type = arg2[0];
		int arg2Idx = atoi(arg2.substr(1).c_str());
		float arg2Val = atof(arg2.substr(1).c_str());

//		printf("%ld\n", r.size());

//		print_vec(r[destIdx]);
//		print_vec(r[arg1Idx]);
//		print_vec(r[arg2Idx]);

		/* Apply operator to arguments and store result to destination register */
		if (op == "+") {
			if(arg2Type == 'r') {
				for(int j=0; j<samples.size(); j++) {
					r[destIdx][j] = r[arg1Idx][j] + r[arg2Idx][j];
				}
			}
			else {
				for(int j=0; j<samples.size(); j++) {
					r[destIdx][j] = r[arg1Idx][j] + arg2Val;
				}
			}
		}
		else if (op == "-") {
			if(arg2Type == 'r') {
				for(int j=0; j<samples.size(); j++) {
					r[destIdx][j] = r[arg1Idx][j] - r[arg2Idx][j];
				}
			}
			else {
				for(int j=0; j<samples.size(); j++) {
					r[destIdx][j] = r[arg1Idx][j] - arg2Val;
				}
			}
		}
		else if (op == "*") {
			if(arg2Type == 'r') {
				for(int j=0; j<samples.size(); j++) {
					r[destIdx][j] = r[arg1Idx][j] * r[arg2Idx][j];
				}
			}
			else {
				for(int j=0; j<samples.size(); j++) {
					r[destIdx][j] = r[arg1Idx][j] * arg2Val;
				}
			}
		}
		else if (op == "/") {
			if(arg2Type == 'r') {
				for(int j=0; j<samples.size(); j++) {
					r[destIdx][j] = division(r[arg1Idx][j], r[arg2Idx][j]);
				}
			}
			else {
				for(int j=0; j<samples.size(); j++) {
					r[destIdx][j] = division(r[arg1Idx][j], arg2Val);
				}
			}
		}
		else if (op == "pow") {
			if(arg2Type == 'r') {
				for(int j=0; j<samples.size(); j++) {
					r[destIdx][j] = pow(r[arg1Idx][j], r[arg2Idx][j]);
				}
			}
			else {
				for(int j=0; j<samples.size(); j++) {
					r[destIdx][j] = pow(r[arg1Idx][j], arg2Val);
				}
			}
		}
		else if (op == "sqrt") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = square(r[arg1Idx][j]);
			}
		}
		else if (op == "exp") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = exp(r[arg1Idx][j]);
			}
		}
		else if (op == "log") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = natLog(r[arg1Idx][j]);
			}
		}
		else if (op == "sin") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = sin(r[arg1Idx][j]);
			}
		}
		else if (op == "cos") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = cos(r[arg1Idx][j]);
			}
		}
		else if (op == "tan") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = tangent(r[arg1Idx][j]);
			}
		}
		else if (op == "htan") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = tanh(r[arg1Idx][j]);
			}
		}
		if(op == "NOT") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = !(r[arg1Idx][j]);
			}
		}
		else if (op == "AND") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = r[arg1Idx][j] && r[arg2Idx][j];
			}
		}
		else if (op == "NAND") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = !(r[arg1Idx][j] && r[arg2Idx][j]);
			}
		}
		else if (op == "OR") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = r[arg1Idx][j] || r[arg2Idx][j];
			}
		}
		else if (op == "NOR") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = !(r[arg1Idx][j] || r[arg2Idx][j]);
			}
		}
		else if (op == "AND_INV1") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = !(r[arg1Idx][j]) && r[arg2Idx][j];
			}
		}
		else if (op == "XOR") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = (r[arg1Idx][j] || r[arg2Idx][j]) && (r[arg1Idx][j] != r[arg2Idx][j]);
			}
		}
		else if (op == "XNOR") {
			for(int j=0; j<samples.size(); j++) {
				r[destIdx][j] = !((r[arg1Idx][j] || r[arg2Idx][j]) && (r[arg1Idx][j] != r[arg2Idx][j]));
			}
		}
	}

	/* Create and fill output vector (output begins in register 0) */
	int lenX = y.size();
	int lenY = y[0].size();
	vector< vector<float> > resp(lenX, vector<float>(lenY,0));

	for(int i=0; i<lenX; i++) {
		for(int j=0; j<lenY; j++) {
			resp[i][j] = r[j][i];
		}
	}

	/* Return output vector */
	return resp;

}

/* Calculates fitness from individual */
vector<float> calc_fit(vector< vector<string> > ind, string type, vector<string> measures) {

	/* Load data type of data to be processed */
	if(type == "train") {
		samples = samples_train;
		y = y_train;
	}
	else if(type == "val") {
		samples = samples_val;
		y = y_val;
	}
	else if(type == "test") {
		samples = samples_test;
		y = y_test;
	}

	/* Calculated vector */
	vector< vector<float> > calc = calc_vector(ind);

	/* Vector with fitness measures */
	vector<float> ret;

	/* Calculate fitness using measures given (minimization always) */
	for(int i=0; i<measures.size(); i++) {

		string measure = measures[i];

		if(measure == "R2") { /* R^2 */

			vector<float> outputs;
			float ssres = 0.0;
			for(int i=0; i<samples.size(); i++) {
				ssres += pow(y[i][0]-calc[i][0], 2);
				outputs.push_back(y[i][0]);
			}

			float yBar = accumulate(outputs.begin(), outputs.end(), 0.0)/outputs.size();
			float sstot = 0.0;
			for(int i=0; i<samples.size(); i++) {
				sstot += pow(y[i][0]-yBar, 2);
			}

			float rSquared = 1.0 - ssres/sstot;
			ret.push_back(rSquared);

		}
		else if(measure == "MAE") { /* Mean Absolute Error (MAE) */

			vector<float> vec (samples.size());
			for(int i=0; i<samples.size(); i++) {
				vec[i] = abs(y[i][0]-calc[i][0]);
			}
			float meanError = accumulate(vec.begin(), vec.end(), 0.0)/vec.size();
			ret.push_back(meanError);

		}
		else if(measure == "RMSE") { /* Rooted Mean Squared Error (RMSE) */

			vector<float> vec (samples.size());
			for(int i=0; i<samples.size(); i++) {
				vec[i] = pow(y[i][0]-calc[i][0], 2);
			}
			float rmse = sqrt(accumulate(vec.begin(), vec.end(), 0.0)/vec.size());
			ret.push_back(rmse);
		}
		else if(measure == "SSE") { /* Sum of Squared Errors (SSE) */

			vector<float> vec (samples.size());
			for(int i=0; i<samples.size(); i++) {
				vec[i] = pow(y[i][0]-calc[i][0], 2);
			}
			float sse = accumulate(vec.begin(), vec.end(), 0.0);
			ret.push_back(sse);
		}
		else if(measure == "PERC") { /* Percentage of correct output bits */

			int correct = 0;
			int total = y.size() * y[0].size();

			for(int i=0; i<y.size(); i++) {
				for(int j=0; j<y[0].size(); j++) {
					if((calc[i][j] == y[i][j])) {
						correct = correct + 1;
					}
				}
			}

			float perc = correct/float(total);
			perc = 1 - perc;
			ret.push_back(perc);

		}
		else {
			printf("Measure %s not defined.\n", measure.c_str());
		}

	}

	/* Return fitness vector */
	return ret;

}

