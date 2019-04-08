class Vector:
    @classmethod
    def add(cls,v1:iter,v2:iter):
        resultant = [sum(components) for components in zip(v1, v2)]
        return resultant

    @classmethod
    def scale(cls,v1:iter,k:float):

        resultant = [components * k for components in v1]
        return resultant

