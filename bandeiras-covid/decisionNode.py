class decisionNode:
    def __init__(self, divisionCriteria, satisfiedData, notSatisfiedData, nodeDepth):
        self.criteria = divisionCriteria
        self.satisfied = satisfiedData
        self.notSatisfied = notSatisfiedData
        self.isLeaf = False
        self.nodeDepth = nodeDepth