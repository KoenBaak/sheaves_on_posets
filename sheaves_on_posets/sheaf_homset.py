from sage.structure.parent import Parent
from sage.categories.sets_cat import Sets

from .sheaf_morphism import LocFreeSheafMorphism

class LocFreeSheafHomset(Parent):
    
    Element = LocFreeSheafMorphism
    
    def __init__(self, sheaf1, sheaf2):
        Parent.__init__(self, category=Sets())
        self._domain = sheaf1
        self._codomain = sheaf2
        print("in homset __init__")     
         
    def domain(self):
        return self._domain
    
    def codomain(self):
        return self._codomain
    
    def __call__(self, component_dict):
        print("in homset __call__")
        return self.element_class(self, component_dict)
    
    def _repr_(self):
        return "Set of morphisms from {} to {}".format(self._domain, self._codomain)
        
    def _latex_(self):
        return r'\mbox{' + str(self) + r'}'
   
