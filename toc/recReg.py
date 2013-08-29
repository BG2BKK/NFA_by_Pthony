#_*_ coding:utf-8 _*_
import sys
import Reg
import NFA
NonTerminal = 'ABCDEFGHIJKLMNSOPQRTUVWXYZ'
Terminal='abcdefghijklmnopqrstuvwxyz1234567890'
Stackbet = Terminal+NonTerminal+'|!'
StartSymbol = 'S'

def	countTerminal(s):
	count = 0
	for i in range(len(s)):
		if s[i] in Terminal:
			count += 1
	return count
	
def	checkRule(rule,exp,RuleSets):
	result=None
	while rule != '' and exp != '':
		if rule[0] == exp[0]:
			rule = rule.replace(rule[0],'',1)
			exp  = exp.replace(exp[0],'',1)
		elif rule[0] in Terminal:
			break
		elif rule[0] in NonTerminal:
		#	print 'NonTerminal'
		#	print rule
		#	print exp
			Rule = []
			if isinstance(RuleSets[rule[0]],str) == True:
				Rule.append(RuleSets[rule[0]])
			else:
				RuleSets[rule[0]].reverse()
				for r in RuleSets[rule[0]]:
					Rule.append(r)
			for r in Rule:
				if r == '!':
					r = ''
				new_rule = rule.replace(rule[0],r,1)
				if countTerminal(new_rule) > len(exp):
					continue
				result = checkRule(new_rule,exp,RuleSets)
				if result == 'match':
					break
			if result == 'match':
				return result
			elif result == None:
				break
	if isNone(exp) and isNone(rule):
		return 'match'
	elif not isNone(exp) and isNone(rule):
		return None
	elif isNone(exp) and not isNone(rule):
		exp = exp + 'a'
		rule = rule + 'a'
		result = checkRule(rule,exp,RuleSets)
		if result == 'match':
			return result
	return None

def	isNone(exp):
		if exp == '' or exp == '!':
			return True


def	main():
	draw = True
	args = sys.argv[1:]
	if len(args)== 3 or len(args)==2:
		if len(args) == 3:
			draw = True
		elif len(args) == 2:
			draw = False
	else:
		print 'you should input the correct arguments such as "[-v]" <regex> <textFile>'
		exit(0)

	regex = sys.argv[-2]
	f_name = sys.argv[-1]
	reg = Reg.Reg() 
	#regex = '(010)^((a|b)+c+)*(b..c)(m*n)*(000)$'
	reg.setExp(regex)
	reg.genRule()
	RuleSets = {}
	for r in reg.RuleSets:
		RuleSets[r] = reg.RuleSets[r]
	print 'the Regular for regex '+regex+' is:'
	print RuleSets

	#generate a NFA by rules generated by the regex
	if draw:
		
		nfa = NFA.nfa()
		nfa.setExp(regex)
		nfa.genRule()
		nfa.genNFA()
		print 'the NFA generated from regex '+regex+' is'
		print nfa.RuleNFA
		nfa.drawNFA()

	f = open(f_name)
	lines = f.readlines()
	print 'the Result of checkRule from textfile fname is :'
	longest = False
#	print lines
	linelist = []
	lenlist = {}
	x=[]
	for line in lines:
		if line == '\n': continue
		line = line.replace('\n','')
		lineset = line.split(' ')
		for word in lineset:
			if checkRule('S',word,RuleSets):
				print 'the line:	'+line
				print 'the column:	'+str(line.find(word))
				print 'the string:	'+word
				print ''
				longest = True
				linelist.append(word)
	if longest:
		for r in linelist:
			lenlist[len(r)]=r
			x.append(len(r))
		x.sort()
		print	'the longest string is:		'+lenlist[x[-1]]
		string = lenlist[x[-1]]
		for line in lines:
			line = line.replace('\n','')
			lineset = line.split(' ')
			if string in line:
				for word in lineset:
					if string == word:
						print 'it\'s in the line:	'+line
						print 'the column is:		'+str(line.find(string))


if	__name__=='__main__':
	main()

