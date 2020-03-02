
from sage.categories.homset import Hom
from sage.structure.sage_object import SageObject

class LocFreeSheafMorphism(SageObject):
    
    def __init__(self, parent, component_dict):
        #Morphism.__init__(self, parent)
        self._components = component_dict
        self._parent = parent
        
    def domain(self):
        return self._parent.domain()
    
    def codomain(self):
        return self._parent.codomain()
    
    def category(self):
        return self._parent.category()
    
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
    
    def __call__(self, point):
        return self.component(point)
