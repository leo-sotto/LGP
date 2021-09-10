import os, itertools
from multiprocessing import Pool

import parameters
import LGP

nTests = 100
nParallel = 30
dataPath = '../datasets/'
logDir = '../logs/graph_GP/'

probDim = {'pagie1':2, 'nguyen3':1, 'nguyen5':1, 'nguyen7':1, 'adder1':3, 'adder2':5, 'adder3':7, 'mult2':4, 'mult3':6, 'par3':3, 'par4':4,
	      'par5':5, 'par6':6, 'par7':7, 'airfoil':5, 'concrete':8, 'energyCooling':8, 'energyHeating':8, 'yacht':6}

probOut = {'pagie1':1, 'nguyen3':1, 'nguyen5':1, 'nguyen7':1, 'adder1':2, 'adder2':3, 'adder3':4, 'mult2':4, 'mult3':6, 'par3':1, 'par4':1,
	      'par5':1, 'par6':1, 'par7':1, 'airfoil':1, 'concrete':1, 'energyCooling':1, 'energyHeating':1, 'yacht':1}

def configure(params, probType, problem, EA, mut) :

	if probType == 'regression' :
		params.functions = ['+', '-', '*', '/', 'sin', 'cos', 'e', 'ln']
	elif probType == 'add' or probType == 'par' :
		params.functions = ['AND','NAND','OR','NOR']
	elif probType == 'mult' :
		params.functions = ['AND','AND_INV1','XOR','OR']

	params.nDim = probDim[problem]
	params.nOut = probOut[problem]

	if probType == 'regression' :
		params.dataPath = dataPath + 'UCI_regression/' + problem
		params.fitMeasures = ['MAE']
		params.probCons = 0.5
		params.mutRate = 0.3
	elif probType == 'add' or probType == 'mult' or probType == 'par' :
		params.dataPath = dataPath + 'benchmarks_circuits/'  + problem
		params.fitMeasures = ['PERC']
		params.probCons = 0.0
		params.mutRate = 0.02

	if mut == 'macroMicro' :
		params.initIndSize = 20
		params.singleActiveMut = False
		logDirP1 = logDir + 'LGP-' + EA + '/'
	elif mut == 'micro' :
		params.initIndSize = 100
		params.singleActiveMut = True
		logDirP1 = logDir + 'LGP-micro-' + EA + '/'

	params.logDir = logDirP1 + problem + '/'

	try :
		os.mkdir(logDirP1)
	except OSError :
		pass

	try :
		os.mkdir(params.logDir)
	except OSError :
		pass

	params.validation = False
	params.stopValue = 1e-6
	params.verbose = False
	params.nExtraRegisters = 10
	params.maxIndSize = 100

	if EA == 'gen' or EA == 'steady' :
		params.popSize = 1000
		params.mi = 1000
		params.lambd = 1
	elif EA == 'lambda' :
		params.popSize = 1
		params.mi = 1
		params.lambd = 4

	params.tournSize = 10
	params.evoLoop = EA
	params.maxInstEvals = 10000000
	params.consts = [1.0]

def run(expConf) :

	EA = expConf[0]
	mut = expConf[1]
	probType = expConf[2][0]
	problem = expConf[2][1]
	params = parameters.Parameters()
	configure(params, probType, problem, EA, mut)
	LGPAlg = LGP.LGP(params)

	for i in range(nTests) :
		print('LGP-%s-%s on %s, run %d.' % (mut, EA, problem, i+1))
		LGPAlg.run()

	print('LGP-%s-%s on %s, all %d runs finished.' % (mut, EA, problem, nTests))	

if __name__ == '__main__' :

	try :
		os.mkdir(logDir)
	except OSError :
		pass

	EAVec = ['gen', 'steady', 'lambda']
	mutVec = ['macroMicro', 'micro']
#	probVec = [['regression', 'pagie1'], ['regression', 'nguyen3'], ['regression', 'nguyen5'], ['regression', 'nguyen7'] \\
#		   ['add', 'adder1'], ['add', 'adder2'], ['add', 'adder3'], ['mult', 'mult2'], ['mult', 'mult3'], ['par', 'par3'], \\
#		   ['par', 'par4'], ['par', 'par5'], ['par', 'par6'], ['par', 'par7']]
	probVec = [['regression', 'airfoil'], ['regression', 'concrete'], ['regression', 'energyCooling'], ['regression', 'energyHeating'],
		   ['regression', 'yacht']]

	expVec = itertools.product(EAVec, mutVec, probVec)
	pool = Pool(processes = nParallel)
	pool.map(run, expVec)

