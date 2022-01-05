import re
import sys

string = '''
	HAI
	I HAS A num1 ITZ 3.14
	I HAS A num2 ITZ num1

	num1 R "sddfsdf"

	VISIBLE "Enter value for num2: "

	GIMMEH num2		BTW getting input from user

	VISIBLE num1 "is num1"
	VISIBLE num2 "is num2"

	KTHXBYE
'''

##dictionary for keywords
keywords = {

}

##dictionary for storing variables in the LOLCODE
variables = {

}

code = filter(None, re.split('\n|\t', string))

##Find value type and returns apprropriately typecasted value
def getType(assign):
	try: 											#Identify data type
		val = int(assign[1])						#NUMBR
	except:
		try:
			val = float(assign[1])					#NUMBAR
		except:
			if(assign[1] == "WIN"):					#TROOF
				val = True
			elif(assign[1] == "FAIL"):
				val = False
			elif(re.search(r"^\".*\"$",assign[1])):	#YARN
				val = assign[1]
			elif(assign[1] in variables):			#variable
				val = variables[assign[1]]
			else:									#anything else
				print("Invalid Variable Value")		#produces error message
				exit()								#Kill process
	return val

def interpret(code):
	for line in code:
		if re.search(r"I HAS A ",line):							##variable declaration
			if re.search(r"ITZ ",line):							##with value
				assign = re.split(r"I HAS A ", line)[1]
				assign = re.split(r" ITZ ", assign)
				var = assign[0]

				variables[var] = getType(assign)
			else:												#no value(NOOB)
				var = re.split(r"I HAS A ", line)[1]
				variables[var] = None
		
		elif(re.search(r" R ",line)):							##assignment
			assign = re.split(r" R ", line)
			var = assign[0]
			if var in variables:								#check if variable exists, if not, an error occurs
				variables[var] = getType(assign)
			else:
				print("Unknown variable", var)
				exit()
		else:
			print(line)



interpret(code)