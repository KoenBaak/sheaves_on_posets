from sage.categories.morphism import Morphism

class LocFreeSheafMorphism(Morphism):
    
    def __init__(self, parent, component_dict):
        Morphism.__init__(self, parent)
        self._components = component_dict
    
    def _latex_(self):
        pass
    
    def _repr_(self):
        pass
    
    def __bool__(self):
        return True
    
