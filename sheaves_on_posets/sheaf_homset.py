from sage.categories.homset import Homset

from .sheaf_morphism import LocFreeSheafMorphism

class LocFreeSheafHomset(Homset):
    
    Element = LocFreeSheafMorphism
    
    def __init__(self, sheaf1, sheaf2):
        Homset.__init__(sheaf1, sheaf2)
    
    def _latex_(self):
        pass
    
    def _element_constructor_(self, component_dict):
        return self.element_class(self, component_dict)
