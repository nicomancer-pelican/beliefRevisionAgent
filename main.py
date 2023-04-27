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
        
        entails = self.entail(cnf)
        if entails:
            newClauseSet = set(())
            if len(cnf.args) < 2:
                # a clause of R has len 0 and no args
                # a clause of ~R has len 1 and args of R
                # for both cases we want to add the clause itself since the clause == the literal
                newClauseSet.add(cnf)
            else:
                # if a clause has more than one literal we want to add all of them to the set
                for args in cnf.args:
                    newClauseSet.add(args)
            self.beliefBase = self.beliefBase.union(newClauseSet)
            print('KB entails ', formula)
            print('Adding new formula to KB')
            print('New KB:')
            self.printBeliefBase()
        else:
            print('KB does not entail', formula)
    
    def printBeliefBase(self):
        beliefBaseList = []
        for element in self.beliefBase:
            beliefBaseList.append('(' + str(element) + ')')
        print('( ' + ' & '.join(beliefBaseList), ')')

    def entail(self, newClause):
        # getting negated cnf of new clause and adding it to the KB
        newClause = to_cnf(~newClause)
        newClauseSet = set(())
        if len(newClause.args) < 2:
            # a clause of R has len 0 and no args
            # a clause of ~R has len 1 and args of R
            # for both cases we want to add the clause itself since the clause == the literal
            newClauseSet.add(newClause)
        else:
            # if a clause has more than one literal we want to add all of them to the set
            for args in newClause.args:
                newClauseSet.add(args)
        
        new_beliefBase = self.beliefBase.copy()
        new_beliefBase = new_beliefBase.union(newClauseSet)

        # Perform resolve function on all pairs.
        flag = self.resolveKB(new_beliefBase)
        if flag == 'EmptySet':
            return True
        else:
            return False

    def resolveKB(self, beliefBase):
        flag = 'NonEmptySet'
        while flag=='NonEmptySet':
            beliefBaseCNF, flag = self.resolvePairs(beliefBase)
            beliefBaseCNF = to_cnf(beliefBaseCNF)
            for args in beliefBaseCNF.args:
                beliefBase.add(args)

        if flag=='EmptySet':
            print('\nResolved to yield empty clause')
        elif flag=='NothingToResolve':
            print('\nCannot resolve any further')

        return flag

    def resolvePairs(self, beliefBase):
        for clause1 in beliefBase:
            set1 = set(())
            if len(clause1.args) < 2:
                # a clause of R has len 0 and no args
                # a clause of ~R has len 1 and args of R
                # for both cases we want to add the clause itself since the clause == the literal
                set1.add(clause1)
            else:
                # if a clause has more than one literal we want to add all of them to the set
                for args in clause1.args:
                    set1.add(args)

            for clause2 in beliefBase:
                set2 = set(())
                if len(clause2.args) < 2:
                    set2.add(clause2)
                else:
                    for args in clause2.args:
                        set2.add(args)
                
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
