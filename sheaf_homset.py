from sage.categories.homset import Homset

from .sheaf_morphism import LocFreeSheafMorphism

class LocFreeSheafHomset(Homset):
    
    Element = LocFreeSheafMorphism
    
    def __init__(self, sheaf1, sheaf2):
        print("in homset __init__")
        Homset.__init__(self, sheaf1, sheaf2)
        self._domain = sheaf1
        self._codomain = sheaf2
    
    def __call__(self, component_dict):
        print("in homset __call__")
        return self.element_class(self, component_dict)
    
    
    def _repr_(self):
        return "Set of morphisms from {} to {}".format(self._domain, self._codomain)
        
    def _latex_(self):
        return r'\mbox{' + str(self) + r'}'
