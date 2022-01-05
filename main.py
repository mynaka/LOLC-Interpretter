import re
import sys

string = '''
	HAI
	I HAS A num1
	I HAS A num2 ITZ num1

	num1 R "sddf @#$%^&*s"" sdf"       

	VISIBLE "Enter value for num2: "

	GIMMEH num2

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
			elif(re.search(r"(?<=^\").*(?=\"\s*$)",assign[1])):		#YARN
				val = re.findall(r"(?<=^\").*(?=\"\s*$)",assign[1])[0]
			elif(assign[1] in variables):			#variable
				val = variables[assign[1]]
			else:									#anything else
				print("Invalid value for",assign[0])		#produces error message
				exit()								#Kill process
	return val

##Check if variable is valid. Else, print error message and exit
def checkValidVar(variable):
	if not(re.match(r"^[\w\d]*$", variable)):
		print("Invalid variable name", variable)
		exit(1)

def interpret(code):
	for line in code:
		if re.search(r"I HAS A ",line):							##variable declaration
			assign = re.split(r"I HAS A ", line)[1]
			if re.search(r"ITZ ",line):							##with value
				assign = re.split(r" ITZ ", assign)
				var = assign[0]
				checkValidVar(var)
				
				variables[var] = getType(assign)				#assign value to variable
			else:												#no value(NOOB)
				checkValidVar(assign)
				variables[assign] = None
		
		elif(re.search(r" R ",line)):							##assignment
			assign = re.split(r" R ", line)
			var = assign[0]
			if var in variables:								#check if variable exists, if not, an error occurs
				variables[var] = getType(assign)
			else:
				print("Unknown variable", var)
				exit()

		elif(re.search(r"VISIBLE ",line)):							##printing
			printLine = re.split(r"VISIBLE ", line)[1]
			
			printStack = filter(None, re.split(r"[^\S\"]+|(\".*\")", printLine))
			
			for printVal in printStack:
				print(getType(['IT', printVal]), end=" ")
			print()												#reset print for next line

		else:
			continue

interpret(code)