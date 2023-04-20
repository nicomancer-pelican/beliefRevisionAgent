from sympy import to_cnf

class BeliefBase():
    def __init__(self):
        self.beliefBase: list = []

        self.importSampleBeliefs()

    def importSampleBeliefs(self):
        with open('sampleBeliefs.txt', 'r') as f:
            lines = f.read()
            clauses = str(lines).split(' & ')
            for clause in clauses:
                clause = str(to_cnf(clause)).split('&')
                for i in range(len(clause)):
                    self.beliefBase.append(clause[i])         

    def addToBeliefBase(self, formula):
        # turn into cnf
        cnf = to_cnf(formula)
        # split cnf to clauses
        clauses = str(cnf).split(' & ')
        for clause in clauses:
            if clause not in self.beliefBase:
                # check for duplication and resolve
                self.resolution(clause)
                self.beliefBase.append(clause)
    
    def printBeliefBase(self):
        print(self.beliefBase)

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
    quit: Quit
    ''')


if __name__=='__main__':
    print('\n===Belief Base Revision Engine===\n')
    printCommands()
    agent = BeliefBase()
    getUserInput(agent)
