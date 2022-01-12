import re

string = '''
	HAI
		I HAS A flag ITZ 5
		I HAS A anotherflag ITZ SUM OF 5 AN 5
		
		VISIBLE SUM OF flag AN anotherflag "nice" "    hooh haha"
		VISIBLE DIFF OF flag AN anotherflag
		flag R SUM OF 2 AN 6
		VISIBLE PRODUKT OF flag AN anotherflag
		VISIBLE QUOSHUNT OF flag AN anotherflag
		
		I HAS A flag5 ITZ 4
		VISIBLE flag5 " hihi" "  he flag  he " anotherflag flag
		VISIBLE flag " " anotherflag

		flag R MAEK flag NUMBAR
		VISIBLE "flag is now " flag
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

def isOperator(c):
    return c == "*" or c == "+" or c == "-" or c == "/" or c == "%" or c == " and " or c == " or " or c == "^"

def isNot(c):
	return c == "!"

def isExpression(c):
	return re.search("SUM|DIFF|PRODUKT|QUOSHUNT|MOD|BOTH|EITHER|WON|NOT", c)

def isLiteral(c):
	if not re.search("\"", c):
		try:
			float(c)
			return True
		except: return False
	else:
		return True

def procExpression(expr):
	op = list(filter(None, re.split(r" OF |\s|AN", expr)))
	res = []							#string that will contain the prefix stack
	for i in range(len(op)):	
		if op[i] == "SUM":				#check if keyword is operator
			res.append("+")					#change to equivalent symbol
		elif op[i] == "DIFF":
			res.append("-")   
		elif op[i] == "PRODUKT":
			res.append("*")
		elif op[i] == "QUOSHUNT":
			res.append("/")
		elif op[i] == "MOD":
			res.append("%")
		elif op[i] == "BOTH":
			res.append(" and ")
		elif op[i] == "EITHER":
			res.append(" or ")
		elif op[i] == "WON":
			res.append("^")
		elif op[i] == "NOT":
			res.append("!")
		else:
			try:
				float(op[i])			#operand is numeric
				res.append(op[i])			
			except:					#operator is either a variable or is invalid
				try:
					float(variables[op[i]][0])			#This checks proper data type and variable validity at the same time
					res.append(str(variables[op[i]][0]))
				except:
					if(op[i] == "WIN"):
						res.append("True")
					elif(op[i] == "FAIL"):
						res.append("False")
					else:
						raise Exception					#Will raise exception causing an invalid value exception
	stack = []
    #convert prefix to infix
	stackLength = len(res) - 1
	while stackLength >= 0:
		if isOperator(res[stackLength]):	# symbol is an operator
			strExpr = "(" + stack.pop() + res[stackLength] + stack.pop() + ")"	#added parentheses to make evaluation easier
			stack.append(strExpr)
		elif isNot(res[stackLength]):
			strExpr = "(not " + stack.pop() + ")"
			stack.append(strExpr)
		else:
			stack.append(res[stackLength])
		stackLength-=1
	result = eval(stack.pop())	#evaluate
	if result == True:
		return "WIN"
	elif result == False:
		return "FAIL"
	else:
		return result

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
##Input: 2-element list containing variable name and value as a string
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
				try:
					val = procExpression(assign[1])
					if type(val) == int:
						varType = "NUMBR"
					elif type(val) == float:
						varType = "NUMBAR"
					else:
						varType = "TROOF"
				except:
					print("Invalid value for",assign[0])		#produces error message
					exit()								#Kill process
	res = [val, varType]
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
				if re.search(r"MAEK | ",assign[1]) and not isExpression(assign[1]):				#recast variable
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
			
			printStack = list(filter(None,re.split(r"(\"[^\"]*\")", printLine)))
			try:
				printStack.remove(' ')		#junk parts in the stack may cause errors, must remove
			except:
				pass
			for printVal in printStack:
				if isLiteral(printVal) or isExpression(printVal):							#Literal or Expression
					variables["Implicit IT"] = getType(["Implicit IT", printVal])			#will assign string to IT
					result = typeCast("Implicit IT", "YARN")								#typecast to YARN
					print(result[0], end="")
				else:																		#Variable/s
					varia = filter(None,printVal.split(" "))
					for variable in varia:													#do the same but will take into account
						variables["Implicit IT"] = getType(["Implicit IT", variable])		#successive variables
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

		elif(re.search(r"GIMMEH",line)):
			var = list(filter(None, re.split(r"GIMMEH|\s", line)))[0]
			value = "\""+input()+"\""

			variables[var] = getType([var, value])
	
		else:
			continue

interpret(code)
print(procExpression("BOTH OF WIN AN NOT EITHER OF FAIL AN FAIL"))