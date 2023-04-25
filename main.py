from sympy import to_cnf, And, Or, Implies
from sympy.abc import P, R, L

class BeliefBase():
    def __init__(self):
        self.beliefBase = None

        self.importSampleBeliefs()

    def importSampleBeliefs(self):
        with open('sampleBeliefs.txt', 'r') as f:
            lines = f.read()
            self.beliefBase = to_cnf(str(lines))

    def addToBeliefBase(self, formula):
        # turn into cnf
        cnf = to_cnf(formula)
        current = self.beliefBase[0]

        self.beliefBase.append(cnf)
        
        # split cnf to clauses
        clauses = str(cnf).split('&')
        for clause in clauses:
            clause = clause.strip('() ')
            if clause not in self.beliefBase:
                # check for duplication and resolve
                self.entail(clause)
                self.beliefBase.append(clause)
    
    def printBeliefBase(self):
        print(self.beliefBase)

    def entail(self, new_clause):
        # getting negated cnf of new clause and adding it to the KB
        new_clause = to_cnf(new_clause)
        new_clause = to_cnf(~new_clause)
        
        new_beliefBase = self.beliefBase.copy()

        for clause in new_clause.args:
            new_beliefBase.append(clause)

        # Looping over new beliefbase to perform resolve function on all pairs.
        new  = set()
        length = len(new_beliefBase)
        for i in range(length):
            for j in range(length):
                if i != j:
                    pairs = [new_beliefBase[i], new_beliefBase[j]]
                    # using resolve function
                    res = self.resolve(pairs)
                    if res == None:
                        return True
                    else:
                        new = new.union(set(res))
                    
                    if new.issubset(set(new_beliefBase)): return False

                    for clause in new:
                        if clause not in new_beliefBase:
                            new_beliefBase.append(clause)


    def resolve(self, beliefBase):
        for clause1 in beliefBase.args:
            for part1 in clause1.args:
                if len(clause1.args) == 1:
                    part1 = clause1
                for clause2 in beliefBase.args:
                    for part2 in clause2.args:
                        if len(clause2.args) == 1:
                            part2 = clause2
                        if part1 == ~part2:
                            print('\n', beliefBase)
                            print('\ncomplement')
                            print('clause1: ', clause1)
                            print('clause2: ', clause2)
                            print('part1: ', part1)
                            print('part2: ', part2)
                            
                            # remove clause 1 and clause 2 from belief base
                            temp1 = str(clause1)
                            temp2 = str(clause2)
                            temp3 = str(beliefBase)
                            temp3 = temp3.replace(' ', '').replace('(', '').replace(')', '').split('&')

                            temp1 = str(clause1).replace(' ', '').replace('(', '').replace(')', '')
                            temp3.remove(temp1)
                            temp2 = str(clause2).replace(' ', '').replace('(', '').replace(')', '')
                            temp3.remove(temp2)

                            # remove complement bits from clause 1 and clause 2
                            temp1 = temp1.split('|')
                            temp1.remove(str(part1))
                            temp2 = temp2.split('|')
                            temp2.remove(str(part2))

                            # create new clause and add to belief base
                            temp4 = temp1 + temp2
                            temp5 = ''
                            for clause in temp4:
                                temp5 += (clause + ' | ')
                            temp3.append(temp5[:-3])
                            temp6 = ''
                            for clause in temp3:
                                temp6 += ('(' + clause + ') & ')
                            if temp6:
                                beliefBase = to_cnf(temp6[:-3])
                                self.resolve(beliefBase)
                            else:
                                return

def getUserInput(agent):
    print('\nSelect Command:')
    userInput = input()

    if userInput == 'print':
        print('\nPrinting current belief base')
        agent.printBeliefBase()
    elif userInput == 'revise':
        print('\nEnter new formula:')
        formula = input()
        agent.addToBeliefBase(formula)
    elif userInput == 'resolve':
        print('\nResolving current belief base')
        agent.resolve(agent.beliefBase)
    elif userInput == 'quit':
        print('\n===Closing Agent===\n')
        return
    else:
        print('\nCommand not recognised')

    getUserInput(agent)

def printCommands():
    print('''
    Available Commands:
    print: Print the current belief base
    revise: Add a new formula to the belief base
    resolve: Resolve the current belief base
    quit: Quit
    ''')


if __name__=='__main__':
    print('\n===Belief Base Revision Engine===\n')
    printCommands()
    agent = BeliefBase()
    getUserInput(agent)
