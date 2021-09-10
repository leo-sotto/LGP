from random import randint, random
import parameters

def remove_introns(ind, params) :

	if not ind :
		return ind, []

	#Effective registers for a given instruction
	r_eff = [False for i in range(params.nRegisters)]

	#Vector of initial effective instructions
	effInsts = [False for i in range(len(ind))]

	#Mark last instructions that attribute to the destination registers
	destRegs = [True for i in range(params.nOut)] + [False for i in range(params.nRegisters-params.nOut)]	

	for i in range(len(ind)-1,-1,-1) :
		dest = int(ind[i][1])
		if destRegs[dest] :
			destRegs[dest] = False
			effInsts[i] = True
	
	#Fill the effective registers for a given instruction
	def fill_r_eff(inst) :
		for arg in inst[2:(2+params.funcArity[inst[0]])] :
			if arg[0] == 'r' :
				r_eff[int(arg[1:])] = True

	effInd = []

	#Add effective instructions to build effective ind
	for i in range(len(ind)-1,-1,-1) :
		dest = int(ind[i][1])
		if r_eff[dest] or effInsts[i] :
			effInd.insert(0,ind[i])
			effInsts[i] = True
			r_eff[dest] = False
			fill_r_eff(ind[i])

	#Return effective ind and vector with positions of effective instructions	
	return effInd, effInsts

def generate_instruction(params) :

	#Choose operator
	idxOp = randint(0, len(params.functions)-1)
	op = params.functions[idxOp]

	#Choose destination register
	idxDest = randint(0, params.nRegisters-1)
	dest = '%d'%idxDest

	#Choose first argument
	idxArg1 = randint(0, params.nRegisters-1)
	arg1 = 'r%d'%idxArg1

	#Choose second argument
	if random() < params.probCons :
		idxArg = randint(0, len(params.consts)-1)
		arg2 = 'c%f' % params.consts[idxArg]
	else :
		idxArg2 = randint(0, params.nRegisters-1)
		arg2 = 'r%d'%idxArg2

	#Return instruction
	return [op, dest, arg1, arg2]

def create_ind(params) :
	return [generate_instruction(params) for i in range(params.initIndSize)]

def create_pop(params) :
	return [create_ind(params) for i in range(params.popSize)]

def print_ind(ind) :
	for i in range(len(ind)) :
		print('[%d]: %s' % (i, ind[i]))

def generate_program(ind, params) :

	program = ""

	for inst in ind :

		part = "r[" + inst[1] + "] ="
		program = program + part
		
		op = inst[0]
	
		i = 2
		for el in params.funcPrint[op] :
			if el!='' :
				part = " " + el
				program = program + part
			else :
				argType = inst[i][0]
				if argType == "c" :
					part = " " + inst[i][1:]
				else :
					part = " " + argType + "[" + inst[i][1:] + "]"
				program = program + part
				i = i + 1
		
		program = program + '\n'
	
	return program

def auto_test() :

	params = parameters.Parameters()
	params.functions = ['+', '-', '*', '/', 'sin', 'cos', 'e', 'ln']
	params.nOut = 1
	params.nRegisters = 10
	params.initIndSize = 10
	params.probCons = 0.0
	params.consts = [float(const) for const in range(1,2)]

	ind = create_ind(params)
	effInd, effInsts = remove_introns(ind, params)

	print_ind(ind)
	print('')
	print_ind(effInd)
	print('')
	print(effInsts)

#	print(generate_program(ind, params))
#	print(generate_program(effInd, params))

#Auto-test
if __name__ == '__main__' :
	auto_test()

