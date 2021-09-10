from math import isnan
import numpy as np

import ind_creation
import calc_fit

def load_data_aux(kind, params) :

	path = '%s_%s.csv' % (params.dataPath, kind)
	data = open(path, 'r')
	mat = [[float(x.strip(' ,\n')) for x in line.split(',')] for line in data]
	mat = np.array(mat)
	data.close()

	X = mat[:,:params.nDim]
	y = mat[:,params.nDim:]

	if kind == 'train' :
		global samplesTrain
		global yTrain
		samplesTrain = X
		yTrain = y
	if kind == 'val' :
		global samplesVal
		global yVal
		samplesVal = X
		yVal = y
	if kind == 'test' :
		global samplesTest
		global yTest
		samplesTest = X
		yTest = y

def set_params_calc_fit(params) :

	r_aux = calc_fit.VecVecFloat()
	samples_train_aux = calc_fit.VecVecFloat()
	samples_val_aux = calc_fit.VecVecFloat()
	samples_test_aux = calc_fit.VecVecFloat()
	y_train_aux = calc_fit.VecVecFloat()
	y_val_aux = calc_fit.VecVecFloat()
	y_test_aux = calc_fit.VecVecFloat()

	sizeJ = max(len(samplesTrain), len(samplesVal), len(samplesTest))

	r_aux = [[1.0 for j in range(sizeJ)] for i in range(params.nRegisters)]
	samples_train_aux = samplesTrain
	samples_val_aux = samplesVal
	samples_test_aux = samplesTest
	y_train_aux = yTrain
	y_val_aux = yVal
	y_test_aux = yTest

	calc_fit.set_params(r_aux, samples_train_aux, samples_val_aux, samples_test_aux, y_train_aux, y_val_aux, y_test_aux)

def load_data(params) :
	load_data_aux('train', params)
	load_data_aux('val', params)
	load_data_aux('test', params)
	set_params_calc_fit(params)

def fit_ind(ind, kind, params) :

	if not ind :
		return [float('Inf')]*len(params.fitMeasures)

	vec = calc_fit.VecVecString()
	vec = ind
	errMeasures = calc_fit.VecString()
	errMeasures = params.fitMeasures

	try :
		result = calc_fit.VecFloat()
		result = calc_fit.calc_fit(vec, kind, errMeasures)
	except :
		return [float('Inf')]*len(params.fitMeasures)

	for x in result :
		if isnan(x) :
			return [float('Inf')]*len(params.fitMeasures)

	return list(result)

def fit_pop(pop, kind, params) :
 	return [fit_ind(ind, kind, params) for ind in pop]

def auto_test() :

	ind = [['pow', '0', 'r0', 'c3.0'],
	       ['pow', '1', 'r1', 'c2.0'],
	       ['+', '0', 'r0', 'r1'],
	       ['+', '0', 'r0', 'r2']]

#	ind = [['AND', '4', 'r0', 'r1'],
#	       ['NOR', '5', 'r0', 'r1'],
#	       ['OR', '0', 'r4', 'r5'],
#	       ['AND', '4', 'r2', 'r3'],
#	       ['NOR', '5', 'r2', 'r3'],
#	       ['OR', '1', 'r4', 'r5'],
#	       ['AND', '4', 'r0', 'r1'],
#	       ['NOR', '5', 'r0', 'r1'],
#	       ['OR', '0', 'r4', 'r5']]

#	ind = ind_creation.create_ind(params)
#	ind, effInsts = ind_creation.remove_introns(ind, params)

	function = 'nguyen1'
#	function = 'par4'
	load_data(params)
	set_params_calc_fit(params)

	print('samplesTrain:\n%s' % np.array(samplesTrain))
	print('\nsamplesVal:\n%s' % np.array(samplesVal))
	print('\nsamplesTest:\n%s' % np.array(samplesTest))

	print('\nyTrain:\n%s' % np.array(yTrain))
	print('\nyVal:\n%s' % np.array(yVal))
	print('\nyTest:\n%s' % np.array(yTest))

	print('\nfitTrain: %s' % fit_ind(ind, 'train', params))
	print('fitVal: %s' % fit_ind(ind, 'val', params))
	print('fitTest: %s' % fit_ind(ind, 'test', params))
#	print('\nfitTrain: %s' % fit_ind(ind, 'train', params))
#	print('fitVal: %s' % fit_ind(ind, 'val', params))
#	print('fitTest: %s' % fit_ind(ind, 'test', params))

	print('\nInd:\n%s' % ind_creation.generate_program(ind, params))

#Auto-test
if __name__ == '__main__' :
	auto_test()

