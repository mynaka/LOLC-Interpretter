import re

string = '''HAI
	I HAS A num1
	I HAS A num2

	num1 R 15

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

for i in code:
    print(i)