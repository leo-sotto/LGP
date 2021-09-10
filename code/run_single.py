import parameters
import LGP

def main() :

	#Instanciate an object of class Parameters
	params = parameters.Parameters()	

	#Instantiate and run the LGP algorithm
	LGPAlg = LGP.LGP(params)
	LGPAlg.run()

if __name__ == '__main__' :
	main()

