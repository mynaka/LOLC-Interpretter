import re

string = '''
	HAI
	I HAS A num1
	I HAS A num2 ITZ 123456

	num1 R MAEK num2 NUMBAR
	
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
	'Implicit IT' : [None, "NOOB"]
}

code = filter(None, re.split('\n|\t', string))

def procExpression(expr):
	op = list(filter(None, re.split(r" OF |\s|AN", expr)))
	operandStack = []
	operatorStack = []
	arithmeticOps = ["SUM", "DIFF", "PRODUKT", "QUOSHUNT", "MOD"]

	for i in op:
		if i in arithmeticOps:
			operatorStack.append(i)
		else:
			try:
				operandStack.append(int(i))
			except:
				operandStack.append(float(i))
		
		if len(operandStack) == 2:
			operator = operatorStack[-1]

			if operator == "SUM":
				operandStack[0] = operandStack[0] + operandStack[1]
			elif operator == "DIFF":
				operandStack[0] = operandStack[0] - operandStack[1]
			elif operator == "PRODUKT":
				operandStack[0] = operandStack[0] * operandStack[1]
			elif operator == "QUOSHUNT":
				operandStack[0] = operandStack[0] / operandStack[1]
			elif operator == "MOD":
				operandStack[0] = operandStack[0] % operandStack[1]
			operatorStack.pop()
			operandStack.pop()

	print(operandStack[0])

##Typecast variable x into cast data type
def typeCast(x, cast):
	val = None
	varType = "NOOB"
	try:
		if cast == "NUMBR":
			val = int(variables[x][0]), 
			val = val[0]
			varType = "NUMBR"
		elif cast == "NUMBAR":
			val = float(variables[x][0])
			varType = "NUMBAR"
		elif cast == "YARN":
			if variables[x][1] == "TROOF" or variables[x][1] == "NOOB":			##From TROOF or NOOB
				raise Exception
			else:
				if str(variables[x][1]) == "NUMBAR":	#From NUMBAR to YARN, round to two decimals
					val = str(round(variables[x][0],2))
				else:									#Other Data types
					val = str(variables[x][0])
			varType = "YARN"
		elif cast == "TROOF":
			val = bool(variables[x][0])
			varType = "TROOF"
		else:
			raise Exception
	except Exception:
		print("Cannot cast", x, "to", cast)
		exit()
	return [val, varType]

##Find value type and returns apprropriately typecasted value
def getType(assign):
	val = None
	varType = "NOOB"
	try: 											#Identify data type
		val = int(assign[1])						#NUMBR
		varType = "NUMBR"
	except:
		try:
			val = float(assign[1])					#NUMBAR
			varType = "NUMBAR"
		except:
			if(assign[1] == "WIN"):					#TROOF
				val = True
				varType = "TROOF"
			elif(assign[1] == "FAIL"):
				val = False
				varType = "TROOF"
			elif(re.search(r"(?<=^\").*(?=\"\s*$)",assign[1])):		#YARN
				val = re.findall(r"(?<=^\").*(?=\"\s*$)",assign[1])[0]
				varType = "YARN"
			elif(assign[1] in variables):			#variable
				val = variables[assign[1]][0]
				varType = variables[assign[1]][1]
			else:									#anything else
				print("Invalid value for",assign[0])		#produces error message
				exit()								#Kill process
	res = [val, varType]
	#print(res)
	return res

##Check if variable is valid. Else, print error message and exit
def checkValidVar(variable):
	if not(re.match(r"^[\w\d]*$", variable)):
		print("Invalid variable name", variable)
		exit(1)

def interpret(code):
	for line in code:
		if re.search(r"I HAS A ",line):							#variable declaration
			assign = re.split(r"I HAS A ", line)[1]
			if re.search(r"ITZ ",line):							##with ITZ expression
				assign = re.split(r" ITZ ", assign)
				var = assign[0]
				checkValidVar(var)
				
				variables[var] = getType(assign)				#assign value to variable
			else:												#no value(NOOB)
				checkValidVar(assign)
				variables[assign] = [None, "NOOB"]
		
		elif(re.search(r" R ",line)):							##assignment
			assign = re.split(r" R ", line)
			var = assign[0]
			if var in variables:								#check if variable exists, if not, an error occurs
				if re.search(r"MAEK | ",assign[1]):				#recast variable
					castVar = re.split(r"MAEK | ",assign[1])[1]
					castType = re.split(r"MAEK | ",assign[1])[2]
					variables[var] = typeCast(castVar, castType)	#typeCast and reassign
				else:											#assign variable
					variables[var] = getType(assign)
			else:
				print("Unknown variable", var)
				exit()

		elif(re.search(r"VISIBLE ",line)):							##printing
			printLine = re.split(r"VISIBLE ", line)[1]
			
			printStack = filter(None, re.split(r"[^\S\"]+|(\".*\")", printLine))
			
			for printVal in printStack:
				variables["Implicit IT"] = getType(["Implicit IT", printVal])
				result = typeCast("Implicit IT", "YARN")
				print(result[0], end="")
			print()												#reset print for next line

			variables["Implicit IT"] = [None, "NOOB"]			#reset value of IT

		elif(re.search(r" IS NOW A ",line)):							##typecasting
			var = re.split(r" IS NOW A ", line)[0]
			cast = re.split(r" IS NOW A ", line)[1]

			try:									#check if variable exists
				_ = variables[var]
			except:
				print("Unknown Variable", var)
				exit()

			variables[var] = typeCast(var, cast)

		else:
			continue

interpret(code)
procExpression("SUM OF PRODUKT OF SUM OF 3 AN 4 AN 2 AN 1")