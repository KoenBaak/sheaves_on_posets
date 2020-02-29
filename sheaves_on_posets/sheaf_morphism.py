from sage.categories.morphism import Morphism
from sage.categories.homset import Hom

class LocFreeSheafMorphism(Morphism):
    
    def __init__(self, parent, component_dict):
        Morphism.__init__(self, parent)
        self._components = component_dict
    
    def component(self, point):
        domain = self.domain().stalk(point)
        codomain = self.codomain().stalk(point)
        hom = Hom(domain, codomain)
        return hom(self._components[point])
    
    def _latex_(self):
        pass
    
    def _repr_(self):
        pass
    
    def is_injective(self):
        return all(component.right_kernel().rank() == 0 for component in self._components)
    
    def __bool__(self):
        return True
    
    __nonzero__ = __bool__
    
    def _call_(self, point):
        return self.component(point)
