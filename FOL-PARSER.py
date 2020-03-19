# CDSummative.py 
import re # Regular expression (standard python library) 
import pydot # For drawing parse tree

# Take an input 
filename = input("Please enter a filename (including .txt): ") 

# Create a log file
global log 
log = open("log.txt", "w", encoding="utf-8")
log.write(("### Corresponding log file for {} ###\n\n").format(filename))

valid_definitions = ["variables:", "constants:", "predicates:", "equality:", "connectives:", "quantifiers:", "formula:"]
order_definitions = [] 

# Make sure file exists, if not, exit 
try:
    f = open(filename, 'r')
except:
    print("The file you have entered does not exist.") 
    exit() 

for i in f:
    if i.split(None, 1)[0] in valid_definitions:
        order_definitions.append(i.split(None, 1)[0]) 

# Create lists for each set
global variables 
variables = [] 
global constants
constants = [] 
global predicates 
predicates = [] 
global equality 
equality = [] 
global connectives 
connectives = []
global quantifiers  
quantifiers = [] 
global formula 
formula = []
global negative 
negative = [] 


f = open(filename, 'r')
for i in order_definitions:
    counter = 0 
    for line in f:
        for word in (line.split()):
            if counter < 6:
                if word == order_definitions[counter+1]:
                    counter += 1
                if word != order_definitions[counter]:
                    (globals()[(order_definitions[counter].replace(':', ''))].append(word))
            else:
                (globals()[(order_definitions[counter].replace(':', ''))].append(word))

# We have now read the input file in, and creating lists for each definition
# Function for map 

def arity(x):
    x = x.replace('[', '(')  
    x = x.replace(']', ')') 
    arityNum = re.search('\d+', x).group()
    term = "<term>" 
    term2 = "<term>, "
    if int(arityNum) == 1:
        return(x.replace(arityNum, term))
    else:
        newterm = (term2 * (int(arityNum) - 1)) + term
        return(x.replace(arityNum, newterm))
    
# Defining the grammar

# Make a seperate set for negative + remove it from connectives
try: 
    negative.append(connectives[4])
    del connectives[4]
    log.write("INPUT FILE: Valid\n")
except:
    log.write("The input file you have provided is INVALID.") 
    exit() 

# Create grammar file
grammar = open("grammar.txt", "w", encoding="utf-8")
grammar.write("### Corresponding grammar for the language of valid FO formulae ###\n\n")
grammar.write("P =\t{\n")
grammar.write('\t\t<variable> \t::=\t {}\n'.format(' | '.join(list(variables))))
grammar.write('\t\t<constant> \t::=\t {}\n'.format(' | '.join(list(constants))))
grammar.write('\t\t<term> \t\t::=\t <variable> | <constant>\n')
grammar.write('\t\t<equality> \t::=\t {}\n'.format(' | '.join(list(equality))))
grammar.write('\t\t<negative> \t::=\t {}\n'.format(' | '.join(list(negative))))
grammar.write('\t\t<connective> \t::=\t {}\n'.format(' | '.join(list(connectives))))
grammar.write('\t\t<quantifier> \t::=\t {}\n'.format(' | '.join(list(quantifiers))))
grammar.write('\t\t<predicate> \t::=\t {}\n'.format(' | '.join(list(map(arity, predicates)))))
grammar.write('\t\t<atom> \t\t::=\t <predicate> | (<term> <equality> <term>)\n')
grammar.write('\t\t<formula> \t::=\t <atom> | (<formula> <connective> <formula>) | <negative><formula> | <quantifier><variable><formula>\n')
grammar.write("\t}\n\n")
grammar.write("S = { <formula> }\n")


# We have now wrote the production rules and start symbol to grammar.txt 
# Creating seperate lists for terminals and non-terminals
standards = ['(', ')', ','] 
terminals = standards + variables + constants + equality + connectives + negative + quantifiers
non_terminals = ['<variables>', '<constants>', '<term>', '<equality>', '<negative>', '<connectives>', '<quantifier>', '<predicate>', '<atom>', '<formula>'] 

# Formatting formula 
formatted_formula = [] 
predicate_checker = []
arities = []

for predicate in predicates:
    checker = predicate.replace('[', '') 
    checker = checker.replace(']', '')
    for char in checker:
        if char.isdigit() == True:
            checker = checker.replace(char, '') 
    predicate_checker.append(checker) 

# Finding the arity of each predicate 
for predicate in predicates:
    arities.append(int(''.join(c for c in predicate if c.isdigit())))

for i in formula:
    if i in terminals:
        formatted_formula.append(i) 
    else:
        for x in predicate_checker:
            if x in i:
                formatted_formula.append(x) 
                i = i.replace(x, '')
        
        i = i.replace('(', ' ( ')
        i = i.replace(')', ' ) ') 
        i = i.replace(',', ' , ') 
        i = i.split() 
        formatted_formula += list(i) 

# formatted_formula now contains a list of strings, each representing a token
# Defining the terminals + non-terminals in the grammar output file 
terminals += predicate_checker 

terminals_str = "{ "
non_terminals_str = "{ " 

count = 1

# Just formats terminal list into a nice formal string 
for i in terminals:
    if i in standards:
        if count == len(terminals):
            terminals_str += "\"{}\" }".format(i)
        else:
            terminals_str += "\"{}\", ".format(i) 
            count += 1
    else:
        if count == len(terminals):
            terminals_str += (i + ' }')
        else:
            terminals_str += (i + ', ') 
            count += 1

count = 1 

# Just formats non-terminal list into a nice formal string 
for i in non_terminals:
    if count == len(non_terminals):
        non_terminals_str += (i + ' }') 
    else:
        if i[-2] == 's':
            i = i[:-2] + i[-2+1:]  # removing s so non-terminal isnt plural 
        non_terminals_str += "{}, ".format(i) 
        count += 1
 
grammar = open("grammar.txt", "a", encoding="utf-8")
grammar.write("\nVt =  {}\n ".format(terminals_str))
grammar.write("\nVn =  {} ".format(non_terminals_str))
grammar.close()  

print("Wrote grammar.txt to current directory") 

# Function for error checking 

def log_error(non_terminal):
    if non_terminal == "<term>":
        log.write("{}\n{}\n".format(" ".join(variables), " ".join(constants)))
    elif non_terminal == "<variable>":
        log.write("{}\n".format(" ".join(variables)))
    elif non_terminal == "<formula>":
        log.write("(\n{}\n{}\n{}\n".format(" ".join(predicate_checker), " ".join(negative), " ".join(quantifiers)))
    elif non_terminal == "<connective>":
        log.write("{}\n".format(" ".join(connectives)))
    elif non_terminal == "<equality>":
        log.write("{}\n".format(" ".join(equality)))
    elif non_terminal == "<negative>":
        log.write("{}\n".format(" ".join(negative)))
    elif non_terminal == "<quantifier>":
        log.write("{}\n".format(" ".join(quantifiers)))
    elif non_terminal == "<predicate>":
        log.write("{}\n".format(" ".join(predicate_checker)))
    elif non_terminal == "<atom>":
        log.write("(\n{}\n".format(" ".join(predicate_checker)))
    print("Wrote log.txt to current directory")
    return 

# Parsing formatted_formula 
parse_formula = ['<formula>']

G = pydot.Dot(graph_type='graph')

nodeid = 0 

G.add_node(pydot.Node(nodeid, label='"<formula>"')) 
leaves = [0] 
 
parse_counter = 0 # Increment this when parse_formula[parse_counter] == token 
for token in formatted_formula:

    while parse_formula[parse_counter] != token:

        #print(parse_formula)

        if token in quantifiers: # QUANTIFIER CHECK
            parent = leaves[parse_counter] 
            if parse_formula[parse_counter] == "<formula>": 
                leaves.remove(parent) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<quantifier>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = "<quantifier>"
                leaves.insert(parse_counter, nodeid)

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<variable>"'))
                G.add_edge(pydot.Edge(parent, nodeid)) 
                parse_formula.insert(parse_counter+1, "<variable>")
                leaves.insert(parse_counter+1, nodeid) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<formula>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+2, "<formula>")
                leaves.insert(parse_counter+2, nodeid)  

            elif parse_formula[parse_counter] == "<quantifier>":
                leaves.remove(parent) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label=token))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = token
                leaves.insert(parse_counter, nodeid) 

            else:
                # QUANTIFIER CHECK
                #print("Invalid formula (quantifier check)")
                log.write("FORMULA: Invalid\n\nError in formula at symbol {}.\n\n".format(parse_counter+1))
                log.write("Recieved:\t{}\n\nExpected:\n".format(formatted_formula[parse_counter]))
                log_error(parse_formula[parse_counter]) 
                exit() 
        
        elif token in variables: # VARIABLE CHECK                   
            parent = leaves[parse_counter] 
            if parse_formula[parse_counter] == "<variable>":
                leaves.remove(parent) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label=token))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = token
                leaves.insert(parse_counter, nodeid)
            
            elif parse_formula[parse_counter] == "<term>":
                leaves.remove(parent)
    
                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<variable>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = "<variable>"
                leaves.insert(parse_counter, nodeid) 

            elif parse_formula[parse_counter] == "<formula>":   
                leaves.remove(parent) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<atom>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = "<atom>"
                leaves.insert(parse_counter, nodeid) 
  
            elif parse_formula[parse_counter] == "<atom>": 
                leaves.remove(parent)

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='('))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = '('
                leaves.insert(parse_counter, nodeid)

                nodeid += 1 
                G.add_node(pydot.Node(nodeid, label='"<term>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+1, "<term>")
                leaves.insert(parse_counter+1, nodeid)

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<equality>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+2, "<equality>")
                leaves.insert(parse_counter+2, nodeid) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<term>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+3, "<term>")
                leaves.insert(parse_counter+3, nodeid)

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label=')'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+4, ')')
                leaves.insert(parse_counter+4, nodeid)
            else:
                # VARIABLE ERROR
                #print("Invalid formula (variable check)")
                log.write("FORMULA: Invalid\n\nError in formula at symbol {}.\n\n".format(parse_counter+1))
                log.write("Recieved:\t{}\n\nExpected:\n".format(formatted_formula[parse_counter]))
                log_error(parse_formula[parse_counter]) 
                exit()
        
        elif token in constants: # CONSTANT CHECK               
            parent = leaves[parse_counter]

            if parse_formula[parse_counter] == "<constant>":
                leaves.remove(parent) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label=token))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = token
                leaves.insert(parse_counter, nodeid)
            
            elif parse_formula[parse_counter] == "<term>":
                leaves.remove(parent) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<constant>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = "<constant>" 
                leaves.insert(parse_counter, nodeid) 

            elif parse_formula[parse_counter] == "<formula>": 
                leaves.remove(parent) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<atom>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = "<atom>"
                leaves.insert(parse_counter, nodeid)

            elif parse_formula[parse_counter] == "<atom>": 
                leaves.remove(parent) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='('))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = '('
                leaves.insert(parse_counter, nodeid)

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<term>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+1, "<term>")
                leaves.insert(parse_counter+1, nodeid)

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<equality>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+2, "<equality>")
                leaves.insert(parse_counter+2, nodeid) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<term>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+3, "<term>")
                leaves.insert(parse_counter+3, nodeid)

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label=')'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+4, ')')
                leaves.insert(parse_counter+4, nodeid)
            else:
                # CONSTANT ERROR 
                #print("Invalid formula (constant check)")
                log.write("FORMULA: Invalid\n\nError in formula at symbol {}.\n\n".format(parse_counter+1))
                log.write("Recieved:\t{}\n\nExpected:\n".format(formatted_formula[parse_counter]))
                log_error(parse_formula[parse_counter]) 
                exit()  
        
        elif token == '(': # BRACKET CHECK
            parent = leaves[parse_counter] 
            if parse_formula[parse_counter] == "<formula>":
                if formatted_formula[parse_counter+2] in equality:
                    leaves.remove(parent) 

                    nodeid += 1
                    G.add_node(pydot.Node(nodeid, label='"<atom>"'))
                    G.add_edge(pydot.Edge(parent, nodeid))
                    parse_formula[parse_counter] = "<atom>"
                    leaves.insert(parse_counter, nodeid) 
                else:
                    leaves.remove(parent) 

                    nodeid += 1
                    G.add_node(pydot.Node(nodeid, label='('))
                    G.add_edge(pydot.Edge(parent, nodeid))
                    parse_formula[parse_counter] = '('
                    leaves.insert(parse_counter, nodeid)

                    nodeid += 1
                    G.add_node(pydot.Node(nodeid, label='"<formula>"'))
                    G.add_edge(pydot.Edge(parent, nodeid))
                    parse_formula.insert(parse_counter+1, "<formula>")
                    leaves.insert(parse_counter+1, nodeid) 

                    nodeid += 1
                    G.add_node(pydot.Node(nodeid, label='"<connective>"'))
                    G.add_edge(pydot.Edge(parent, nodeid))
                    parse_formula.insert(parse_counter+2, "<connective>")
                    leaves.insert(parse_counter+2, nodeid) 

                    nodeid += 1
                    G.add_node(pydot.Node(nodeid, label='"<formula>"'))
                    G.add_edge(pydot.Edge(parent, nodeid))
                    parse_formula.insert(parse_counter+3, "<formula>")
                    leaves.insert(parse_counter+3, nodeid) 

                    nodeid += 1
                    G.add_node(pydot.Node(nodeid, label=')'))
                    G.add_edge(pydot.Edge(parent, nodeid))
                    parse_formula.insert(parse_counter+4, ')')
                    leaves.insert(parse_counter+4, nodeid)


            elif parse_formula[parse_counter] == "<atom>":  
                leaves.remove(parent) 
                 
                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='('))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = '('
                leaves.insert(parse_counter, nodeid) 

                nodeid += 1 
                G.add_node(pydot.Node(nodeid, label='"<term>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+1, "<term>")
                leaves.insert(parse_counter+1, nodeid) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<equality>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+2, "<equality>") 
                leaves.insert(parse_counter+2, nodeid) 

                nodeid += 1 
                G.add_node(pydot.Node(nodeid, label='"<term>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+3, "<term>")
                leaves.insert(parse_counter+3, nodeid) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='")"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+4, ')')
                leaves.insert(parse_counter+4, nodeid) 

            else:
                # BRACKET ERROR 
                #print("Invalid formula (bracket check)")
                log.write("FORMULA: Invalid\n\nError in formula at symbol {}.\n\n".format(parse_counter+1))
                log.write("Recieved:\t{}\n\nExpected:\n".format(formatted_formula[parse_counter]))
                log_error(parse_formula[parse_counter]) 
                exit() 
        
        elif token in predicate_checker: # PREDICATE CHECK
            parent = leaves[parse_counter] 
            if parse_formula[parse_counter] == "<formula>":
                leaves.remove(parent)

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<atom>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = "<atom>"
                leaves.insert(parse_counter, nodeid) 

                 
            elif parse_formula[parse_counter] == "<predicate>":
                leaves.remove(parent)


                nodeid += 1
                G.add_node(pydot.Node(nodeid, label=token))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = token
                leaves.insert(parse_counter, nodeid) 
            
                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='('))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+1, '(')
                leaves.insert(parse_counter+1, nodeid)

                nodeid += 1
                predicate_counter = parse_counter + 2 

                counter = 1
                for i in range(1, arities[predicate_checker.index(token)]+1): 
                    if counter > 1:
                        nodeid += 1
                    G.add_node(pydot.Node(nodeid, label='"<term>"'))             
                    G.add_edge(pydot.Edge(parent, nodeid))                                   
                    parse_formula.insert(parse_counter+counter+i, "<term>")
                    leaves.insert(predicate_counter, nodeid)
                    predicate_counter += 1 
                    nodeid += 1 

                    counter += 1
                    G.add_node(pydot.Node(nodeid, label='","'))               
                    G.add_edge(pydot.Edge(parent, nodeid))
                    parse_formula.insert(parse_counter+counter+i, ",")
                    if i == arities[predicate_checker.index(token)]:
                        break 
                
                    leaves.insert(predicate_counter, nodeid)
                    predicate_counter += 1 
                
                G.add_node(pydot.Node(nodeid, label=')'))
                #G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter+counter+i] = ')'
                leaves.insert(predicate_counter, nodeid) 

            
            elif parse_formula[parse_counter] == "<atom>":
                leaves.remove(parent) 
        
                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<predicate>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = "<predicate>"
                leaves.insert(parse_counter, nodeid) 
            else:
                # PREDICATE ERROR
                #print("Invalid formula (predicate check)")
                log.write("FORMULA: Invalid\n\nError in formula at symbol {}.\n\n".format(parse_counter+1))
                log.write("Recieved:\t{}\n\nExpected:\n".format(formatted_formula[parse_counter]))
                log_error(parse_formula[parse_counter]) 
                exit() 
        
        elif token in connectives: # CONNECTIVE CHECK
            parent = leaves[parse_counter] 
            if parse_formula[parse_counter] == "<connective>":
                leaves.remove(parent) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label=token))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = token
                leaves.insert(parse_counter, nodeid) 
            else:
                # CONNECTIVE ERROR 
                #print("Invalid formula (connective check)")
                log.write("FORMULA: Invalid\n\nError in formula at symbol {}.\n\n".format(parse_counter+1))
                log.write("Recieved:\t{}\n\nExpected:\n".format(formatted_formula[parse_counter]))
                log_error(parse_formula[parse_counter]) 
                exit()

        elif token in negative: # NEGATIVE CHECK
            parent = leaves[parse_counter]
            if parse_formula[parse_counter] == "<formula>":
                leaves.remove(parent)

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<negative>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = "<negative>"
                leaves.insert(parse_counter, nodeid) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label='"<formula>"'))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula.insert(parse_counter+1, "<formula>")
                leaves.insert(parse_counter+1, nodeid) 

            elif parse_formula[parse_counter] == "<negative>":
                leaves.remove(parent) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label=token))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = token
                leaves.insert(parse_counter, nodeid) 

            else:
                # NEGATIVE ERROR
                #print("Invalid formula (negative check)")
                log.write("FORMULA: Invalid\n\nError in formula at symbol {}.\n\n".format(parse_counter+1))
                log.write("Recieved:\t{}\n\nExpected:\n".format(formatted_formula[parse_counter]))
                log_error(parse_formula[parse_counter])
                exit() 
        
        elif token in equality: # EQUALITY CHECK
            parent = leaves[parse_counter] 
            if parse_formula[parse_counter] == "<equality>":
                leaves.remove(parent) 

                nodeid += 1
                G.add_node(pydot.Node(nodeid, label=token))
                G.add_edge(pydot.Edge(parent, nodeid))
                parse_formula[parse_counter] = token
                leaves.insert(parse_counter, nodeid) 
            else: 
                # EQUALITY ERROR 
                #print("Invalid formula (equality check)")
                log.write("FORMULA: Invalid\n\nError in formula at symbol {}.\n\n".format(parse_counter+1))
                log.write("Recieved:\t{}\n\nExpected:\n".format(formatted_formula[parse_counter]))
                log_error(parse_formula[parse_counter]) 
                exit()

    parse_counter += 1 


#print("Formula parsed successfully")  

#if formatted_formula == parse_formula:
    #print("Formula matches parsed formula")

print("Wrote parse_tree.png to current directory") 
G.write_png('parse_tree.png')

# Write to log file that formula has been parsed successfully 
print("Wrote log.txt to current directory") 
log.write("FORMULA: Valid\nParse tree generated (parse_tree.png) in the current directory.\n")
log.close() 



        