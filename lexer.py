from sys import*

tokens = []
num_stack = []
symbols = {}

def open_file(filename):
	data = open(filename, "r").read()
	data += "<EOF>"
	return data

def lex(filecontents):
	tok = ""
	var = ""
	state = 0
	varstate = 0
	isexpr = 0
	varStarted = 0
	varstring = ""
	string = ""
	expr = ""
	n = ""
	filecontents = list(filecontents)
	for char in filecontents:
		
		tok += char
		if tok == " ":
			if state == 0:
				tok =""
			else:
				tok=" "
		elif tok =="\n" or tok == "<EOF>":
			if expr != "" and isexpr == 1:
				tokens.append("EXPR:"+expr)
				expr = ""
				isexpr = 0
			elif expr != "" and isexpr == 0:
				tokens.append("NUM:"+expr)
				expr = ""
			elif var != "":
				tokens.append("VAR:"+var[3:])
				var = ""
				varStarted = 0
			tok = ""


		elif tok == "=" and state == 0:
			
			if var != "":
				tokens.append("VAR:"+var[3:])
				var = ""
				varStarted = 0
			tokens.append("EQUALS")
			tok = ""

		elif tok == "putStrLn":
			tokens.append("PRINT")
			tok = ""
		
		elif tok == "let" and state == 0:
			varStarted = 1
			var += tok
			tok = ""

		elif varStarted == 1:
			
			var+=tok
			tok = ""

		elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
			expr += tok 
			tok = ""
		elif tok == "+" or tok =="-" or tok =="/" or tok =="*" or tok == "%":
			isexpr = 1
			expr+=tok
			tok = ""

		elif tok == "\"":
			if state == 0:
				state = 1
				
			elif state == 1:
				tokens.append("STRING:" + string + "\"")
				string = ""
				state = 0
				tok = ""
		elif state == 1:
			string += tok
			tok = ""
		elif tok == "print" and state == 0:
			tokens.append("PRINT")
			varstate = 1	
			tok = ""
		elif tok == ")":
			
			varstate = 0
			tokens.append("VAR:"+varstring[1:])
			varstring = ""
			tok = ""
		elif varstate == 1:
			
			
			varstring+=tok
			tok = ""
			
		
	#print("\nThe tokens for the source code are :\n")
	print("\n\n\n\n\n\n\n\nThe Tokens List\n---------------------------------------")
	print(tokens)

	print("---------------------------------------\n\n\n\n\n\n\n\nExecuted code\n-------------------------------------------------")
	
	#print(symbols)
	return tokens
	

def eval_expression(expr):
	return eval(expr)

#	expr = "," + expr
#	i = len(expr)-1
#	num = ""
#
#	while i >= 0:
#		if (expr[i] == "+" or expr[i] == "-" or expr[i] == "*" or expr[i] == "/" or expr[i] == "%"):
#			num=num[::-1]
#			num_stack.append(num)
#			num_stack.append(expr[i])
#			num = ""
#		elif (expr[i] == ","):
#			num = num[::-1]
#			num_stack.append(num)
#			num = ""
#		else:
#			num+=expr[i]
#		
#		i-=1;
#	print(num_stack)


def assignVar(name, value):
	symbols[name[4:]] = value


def parse(toks):
	i=0
	while(i<len(toks)):
		#print(toks[i] + " " + toks[i+1][0:6])
		if toks[i] == "PRINT":
			if toks[i+1][0:6] == "STRING":
				print(toks[i+1][8:-1])
				i+=2
			elif toks[i+1][0:3] == "NUM":
				print(toks[i+1][4:])
				i+=2
			elif toks[i+1][0:4] == "EXPR":
				print(eval_expression(toks[i+1][5:]))
				i+=2
			elif toks[i+1][0:3] == "VAR":
				try:
					ans = symbols[toks[i+1][4:]]
					if ans[0:3] == "NUM":
						print(ans[4:])
					if ans[0:6] == "STRING":
						print(ans[8:-1])
				except Exception as e:
					raise e
				i+=2

		if i>=len(toks):
			break

		if toks[i][0:3] == "VAR":

			if toks[i][0:3]+" "+toks[i+1]+" "+toks[i+2][0:6] == "VAR EQUALS STRING":
				assignVar(toks[i],toks[i+2])
				i+=3
			elif toks[i][0:3]+" "+toks[i+1]+" "+toks[i+2][0:3] == "VAR EQUALS NUM":	
				assignVar(toks[i],toks[i+2])
				i+=3
			elif toks[i][0:3]+" "+toks[i+1]+" "+toks[i+2][0:4] == "VAR EQUALS EXPR":
				assignVar(toks[i],"NUM:"+str(eval_expression(toks[i+2][5:])))
				i+=3
	print("---------------------------------------\n\n\n\n\n\n\n\nThe Symbol Table\n---------------------------------------")			
	print(symbols)
	print("---------------------------------------\n\n\n\n\n")
def run():
	data = open_file(argv[1])
	print("\n\n\nRascal - Custom Haskell Interpretter")
	print("created by - V DHEERAJ")
	print("Disclaimer - This is a haskell interpretter for a very small subset of instructions")

	print("")
	toks = lex(data)
	parse(toks)

run()