from sage.structure.parent import Parent
from sage.categories.sets_cat import Sets

from .sheaf_morphism import LocFreeSheafMorphism

class LocFreeSheafHomset(Parent):
    
    Element = LocFreeSheafMorphism
    
    def __init__(self, sheaf1, sheaf2):
        Parent.__init__(self, category=Sets())
    
    def _latex_(self):
        pass
    
    def __call__(self, component_dict):
        return self.element_class(self, component_dict)
