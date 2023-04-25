from sympy import to_cnf, And, Or, Implies
from sympy.abc import P, R, L, A

class BeliefBase():
    def __init__(self):
        self.beliefBase: set = set(())

        self.importSampleBeliefs()

    def importSampleBeliefs(self):
        with open('sampleBeliefs.txt', 'r') as f:
            lines = f.read()
            beliefBaseCNF = to_cnf(str(lines))
        for args in beliefBaseCNF.args:
            self.beliefBase.add(args)

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
                    res = self.resolveKB(pairs)
                    if res == None:
                        return True
                    else:
                        new = new.union(set(res))
                    
                    if new.issubset(set(new_beliefBase)): return False

                    for clause in new:
                        if clause not in new_beliefBase:
                            new_beliefBase.append(clause)

    def resolveKB(self, beliefBase):
        flag = False
        while not flag:
            beliefBaseCNF, flag = to_cnf(self.resolvePairs(beliefBase))
            for args in beliefBaseCNF.args:
                beliefBase.add(args)
        
        self.beliefBase = beliefBase

        if flag:
            print('Resolved to yield empty clause')
        else:
            print('No new clauses can be added')

    def resolvePairs(self, beliefBase):
        for clause1 in beliefBase:
            clause1Set = set(())
            if len(clause1.args) < 2: # a clause of l of ~l < 2
                clause1Set.add(clause1)
            else:
                for args in clause1.args:
                    clause1Set.add(args)

            for clause2 in beliefBase:
                clause2Set = set(())
                if len(clause2.args) < 2:
                    clause2Set.add(clause2)
                else:
                    for args in clause2.args:
                        clause2Set.add(args)
                
                negatedSet2 = set(())
                for element in clause2Set:
                    negatedSet2.add(~element)
                    
                negatedSet1 = set(())
                for element in clause1Set:
                    negatedSet1.add(~element)

                if clause1Set.intersection(negatedSet2):
                    intersection = clause1Set.intersection(negatedSet2)
                elif negatedSet1.intersection(clause2Set):
                    intersection = negatedSet1.intersection(clause2Set)
                else:
                    # no intersection so nothing to resolve
                    continue
                
                negatedIntersection = set(())
                for element in intersection:
                    negatedIntersection.add(~element)

                clause1SetNew = clause1Set.copy()
                if intersection.issubset(clause1Set):
                    for element in intersection:
                        clause1SetNew.remove(element)
                elif negatedIntersection.issubset(clause1Set):
                    for element in negatedIntersection:
                        clause1SetNew.remove(element)
                
                clause2SetNew = clause2Set.copy()
                if intersection.issubset(clause2Set):
                    for element in intersection:
                        clause2SetNew.remove(element)
                elif negatedIntersection.issubset(clause2Set):
                    for element in negatedIntersection:
                        clause2SetNew.remove(element)

                resolvedClause = set((to_cnf(clause1SetNew.union(clause2SetNew))))

                if resolvedClause.issubset(beliefBase):
                    return beliefBase, False

                # remove from belief base
                beliefBase.remove(clause1)
                beliefBase.remove(clause2)
                beliefBase = beliefBase.union(resolvedClause)
                print('Resolving to... ', beliefBase)
                if not resolvedClause:
                    flag = True # resolved to empty set
                    return beliefBase, flag
                    # flag = False # not resolved to empty set
                    # return beliefBase, flag
                # else:
                    
                    
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
        agent.resolveKB(agent.beliefBase)
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
