class Vector:
    @classmethod
    def add(cls,v1:iter,v2:iter):
        resultant = [sum(components) for components in zip(v1, v2)]
        return resultant

    @classmethod
    def subtract(cls,v1:iter,v2:iter):
        v2_negated=Vector.scale(v2,-1)
        resultant = [sum(components) for components in zip(v1, v2_negated)]
        return resultant

    @classmethod
    def scale(cls,v1:iter,k:float):

        resultant = [components * k for components in v1]
        return resultant

