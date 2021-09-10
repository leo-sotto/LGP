from random import randint, random, sample
import numpy as np

import ind_creation, parameters

def micro_mut_dest(ind, pos, params) :

	'''
	Changes the destination register of ind in instruction pos.
	'''

	if not ind :
		return

	copyInst = ind[pos][:]

	newDest = randint(0, params.nRegisters-1)
	while newDest == int(copyInst[1]) :
		newDest = randint(0, params.nRegisters-1)
			
	copyInst[1] = str(newDest)
	ind[pos] = copyInst

def micro_mut_arg(ind, pos, params) :

	'''
	Changes the argument register of ind in instruction pos.
	'''

	if not ind :
		return

	copyInst = ind[pos][:]

	#Argument to be mutated
	argType = 'c'
	while argType == 'c' :
		argPos = randint(2, len(copyInst)-1)
		argType = copyInst[argPos][0]
	arg = copyInst[argPos][1:]

#	if argType == 'r' :
	newArg = randint(0, params.nRegisters-1)
	while str(newArg) == arg :
		newArg = randint(0, params.nRegisters-1)
	newArg = 'r%d' % newArg
#	elif argType == 'c' :
#		value = float(arg)
#		newValue = float(value + np.random.normal(0.0, 0.5))
#		newArg = 'c%f' % newValue

	copyInst[argPos] = newArg
	ind[pos] = copyInst

def micro_mut_op(ind, pos, params) :

	'''
	Changes the operator of ind in instruction pos.
	'''

	if not ind :
		return 

	op = ind[pos][0]
	copyInst = ind[pos][:]

	newOp = randint(0, len(params.functions)-1)
	while params.functions[newOp] == op :
		newOp = randint(0, len(params.functions)-1)

	op = params.functions[newOp]
	copyInst[0] = op
	ind[pos] = copyInst

def macro_mut_insertion(ind, pos, params) :

	'''
	Inserts an instruction to ind in position pos.
	'''

	if not ind :
		return

	#Position to be mutated
	halfCopy = ind[pos+1:]
	inst = ind_creation.generate_instruction(params)

	for i in range(len(ind)-1, pos, -1) :
		del ind[i]
	ind.append(inst)
	ind.extend(halfCopy)

def macro_mut_remove(ind, pos) :

	'''
	Removes an instruction from ind in position pos.
	'''

	if not ind :
		return

	del ind[pos]

def macro_mut_replace(ind, pos, params) :

	'''
	Replaces an instruction from ind in position pos.
	'''

	if not ind :
		return

	inst = ind_creation.generate_instruction(params)
	ind[pos] = inst

def apply_mutations_rate(ind, params) :

	'''
	Apply mutations based on a mutation rate, defined in parameters.
	'''

	#Define instructions to be mutated
	nInsts = int(len(ind)*params.mutRate)
	if nInsts == 0 : nInsts = 1
	instsList = sample(range(len(ind)), nInsts)

	#Create copy of original individual, so that it is not mutated
	indCopy = ind[:]
	removed = 0

	#Mutate each of the defined instructions
	for inst in instsList :

		inst = inst - removed
		if inst < 0 : inst = len(indCopy) + inst

		if random() < params.probMacroMut :
			if random() < 0.66 :
				if len(indCopy) < params.maxIndSize :
					macro_mut_insertion(indCopy, inst, params)
				else :
					macro_mut_replace(indCopy, inst, params)
			else :
				macro_mut_remove(indCopy, inst)
				inst = inst - 1
				removed = removed + 1

		if random() < params.probMicroMut :
			p = random()
			if p < 0.333 :
				micro_mut_dest(indCopy, inst, params)
			elif p < 0.666 :
				micro_mut_arg(indCopy, inst, params)
			else :
				micro_mut_op(indCopy, inst, params)

	return indCopy

def check_activation(ind, effInsts, pos, params) :

	if effInsts[pos] :
		return False

	dest = ind[pos][1]
	assigned = False

	for i in range(pos+1, len(ind)) :

		if ind[i][1] == dest :
			assigned = True

		for arg in ind[i][2:(2+params.funcArity[ind[i][0]])] :
			if arg[1:] == dest and effInsts[i] and assigned == False :
				return True

	if assigned == False and int(dest) < params.nOut :
		return True
	else :
		return False

def apply_mutations_single(ind, effInsts, params) :

	'''
	Apply the single point mutation to ind (micro-mutation until hitting an effective instruction).
	'''

	if not ind :
		return

	#Create copy of original individual, so that it is not mutated
	indCopy = ind[:]

	#Vector of positions of mutated instructions
	mutated = [False for i in range(len(ind))]
	activation = False

	#Mutate instructions until hitting an effective instruction
	for i in range(10*len(ind)) :

		#Random position to mutate
		pos = randint(0,len(ind)-1)

		#Check if it is not duplicate and mutate
		if not mutated[pos] :
#			print('%d: %s' % (pos, effInsts[pos]))
			mutated[pos] = True
			p = random()
			if p < 0.333 :
				micro_mut_dest(indCopy, pos, params)
				activation = check_activation(indCopy, effInsts, pos, params)
			elif p < 0.666 :
				micro_mut_arg(indCopy, pos, params)
			else :
				micro_mut_op(indCopy, pos, params)

		#If instruction is or became effective, stop
		if effInsts[pos] or activation :
#			print('Active mutation, pos=%d, activation=%s' % (pos, activation))
			return indCopy

	return indCopy

def auto_test() :

	params = parameters.Parameters()
	params.functions = ['+', '-', '*', '/', 'sin', 'cos', 'e', 'ln']
	params.nOut = 1
	params.nRegisters = 10
	params.initIndSize = 10
	params.probCons = 0.0
	params.consts = [float(const) for const in range(1,2)]

	ind = ind_creation.create_ind(params)
	effInd, effInsts = ind_creation.remove_introns(ind, params)

	mutated = apply_mutations_single(ind, effInsts, params)

	ind_creation.print_ind(ind)
	print('')
	ind_creation.print_ind(mutated)

#Auto-test
if __name__ == '__main__' :
	auto_test()

