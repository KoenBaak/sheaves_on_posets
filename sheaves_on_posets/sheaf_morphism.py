
from sage.structure.element import Element

from sage.matrix.special import identity_matrix


class LocFreeSheafMorphism(Element):
    
    def __init__(self, parent, component_dict, name="sheaf morpism"):
        Element.__init__(self, parent)
        self._parent = parent
        self._components = component_dict
        self._base_ring = self._parent._base_ring
        self._domain_poset = self._parent._domain_poset
        self._name = name
        
    def domain(self):
        return self._parent.domain()
    
    def codomain(self):
        return self._parent.codomain()
    
    def component(self, point):
        h = Hom(self.domain().stalk(point), self.codomain().stalk(point))
        if self._components[point] == 0:
            phi = h.zero()
        elif self._components[point] == 1:
            phi = h(identity_marix(self._base_ring, self.domain()._stalk_dict[point]))
        else:
            phi = h(self._components[point])    
        phi._name = "Component of {} at {}".format(self._name, point)
        
    def __getitem__(self, i):
        return self.component(i)
    
    def _latex_(self):
        return r'\mbox{' + str(self) + r'}'
    
    def _repr_(self):
        return "Generic Morphism of Locally Free Sheaves of Modules over {} on {}\n From: {}\n To: {}".format(self._base_ring, self._domain_poset, self.domain(), self.codomain())
