class Vector:
    @classmethod
    def add(cls,v1,v2):
        resultant = [sum(components) for components in zip(v1, v2)]
        return resultant

    @classmethod
    def scale(cls,v1,k):
        resultant = [components*k for components in v1]
        return resultant

