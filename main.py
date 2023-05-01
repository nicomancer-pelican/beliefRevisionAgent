from sympy import to_cnf

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

    def printBeliefBase(self):
        beliefBaseList = []
        if self.beliefBase:
            for element in self.beliefBase:
                beliefBaseList.append('(' + str(element) + ')')
        print('( ' + ' & '.join(beliefBaseList), ')')

    def cnfToSet(self, cnf):
        formulaSet = set(())
        if len(cnf.args) < 2:
            # a clause of R has len 0 and no args
            # a clause of ~R has len 1 and args of R
            # for both cases we want to add the clause itself since the clause == the literal
            formulaSet.add(cnf)
        else:
            # if a clause has more than one literal we want to add all of them to the set
            for args in cnf.args:
                formulaSet.add(args)
        return formulaSet
    
    def reviseBeliefBase(self, formula):
        # turn into cnf
        newFormulaCnf = to_cnf(formula)

        # check it does not already exist in belief base
        newFormulaSet = self.cnfToSet(newFormulaCnf)
        if newFormulaSet.issubset(self.beliefBase):
            print('\nFormula already exists in belief base')
            return

        # check entailment
        res = self.entail(newFormulaCnf)
        if res == True:
            # current KB entails the new formula so can add directly
            self.beliefBase = self.beliefBase.union(newFormulaSet)
            print('\nAdding new formula...')
            print('New knowledge base:')
            self.printBeliefBase()
        else:
            # contractidions so must revise
            newBeliefBase = self.beliefBase.copy()
            for element in self.beliefBase:
                if element == ~newFormulaCnf:
                    newBeliefBase.remove(element)
            self.beliefBase = newBeliefBase
            self.beliefBase.add(newFormulaCnf)

    def entail(self, new_clauses):
        # getting negated cnf of new clause and adding it to the KB
        new_clauses = to_cnf(new_clauses)
        new_clausesNegated = to_cnf(~new_clauses)
        newClausesSet = self.cnfToSet(new_clausesNegated)
        if newClausesSet.issubset(self.beliefBase):
            return False
        
        new_beliefBase = self.beliefBase.copy()
        new_beliefBase = new_beliefBase.union(newClausesSet)

        # Looping over new beliefbase to perform resolve function on all pairs.
        # using resolve function
        res = self.resolveKB(new_beliefBase)
        return res

    def resolveKB(self, beliefBase):
        flag = 'NonEmptySet'
        while flag=='NonEmptySet':
            beliefBaseCNF, flag = self.resolvePairs(beliefBase)
            beliefBaseCNF = to_cnf(beliefBaseCNF)
            for args in beliefBaseCNF.args:
                beliefBase.add(args)

        if flag=='EmptySet':
            print('\nResolved to yield empty clause')
            return True
        elif flag=='NothingToResolve':
            print('\nCannot resolve any further')
            return False

    def resolvePairs(self, beliefBase):
        for clause1 in beliefBase:
            set1 = self.cnfToSet(clause1)
            for clause2 in beliefBase:
                set2 = self.cnfToSet(clause2)
                
                # get the negated versions of the sets we are comparing
                negatedSet2 = set(())
                for element in set2:
                    negatedSet2.add(~element)
                    
                negatedSet1 = set(())
                for element in set1:
                    negatedSet1.add(~element)

                # check both combinations i.e. clause1 == ~clause2 and ~clause1 == clause2
                if set1.intersection(negatedSet2):
                    intersection = set1.intersection(negatedSet2)
                elif negatedSet1.intersection(set2):
                    intersection = negatedSet1.intersection(set2)
                else:
                    # no intersection so nothing to resolve
                    continue
                
                # get negated intersection
                negatedIntersection = set(())
                for element in intersection:
                    negatedIntersection.add(~element)

                # find out if literal1 or ~literal1 is what needs to be removed from clause 1
                set1New = set1.copy()
                if intersection.issubset(set1):
                    for element in intersection:
                        set1New.remove(element)
                elif negatedIntersection.issubset(set1):
                    for element in negatedIntersection:
                        set1New.remove(element)
                
                # find out if literal2 or ~literal2 is what needs to be removed from clause 2
                set2New = set2.copy()
                if intersection.issubset(set2):
                    for element in intersection:
                        set2New.remove(element)
                elif negatedIntersection.issubset(set2):
                    for element in negatedIntersection:
                        set2New.remove(element)

                # get the resolved clause
                resolvedClause = set((to_cnf(set1New.union(set2New))))

                # remove clause1 and clause2 from belief base
                beliefBase.remove(clause1)
                beliefBase.remove(clause2)
                beliefBase = beliefBase.union(resolvedClause)
                print('Resolving ', clause1, ' and ', clause2, ' to... ', resolvedClause)
                if not resolvedClause:
                    flag = 'EmptySet' # resolved to empty set
                    return beliefBase, flag
                else:
                    flag = 'NonEmptySet' # resolved to a non empty set
                    return beliefBase, flag
        return beliefBase, 'NothingToResolve' # tried to resolve all cluase combinations in KB
                    
                    
def getUserInput(agent):
    print('\nSelect Command:')
    userInput = input()

    if userInput == 'help':
        printCommands()
    elif userInput == 'print':
        print('\nPrinting current belief base')
        agent.printBeliefBase()
    elif userInput == 'revise':
        print('\nEnter new formula:')
        formula = input()
        agent.reviseBeliefBase(formula)
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
    help: Print this guide again
    quit: Quit
    ''')


if __name__=='__main__':
    print('\n===Belief Base Revision Engine===\n')
    printCommands()
    agent = BeliefBase()
    getUserInput(agent)
