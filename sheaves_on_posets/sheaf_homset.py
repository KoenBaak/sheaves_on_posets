from sage.structure.parent import Parent
from sage.categories.sets_cat import Sets
from sage.matrix.constructor import Matrix, matrix
from .sheaf_morphism import LocFreeSheafMorphism

class LocFreeSheafHomset(Parent):
    
    Element = LocFreeSheafMorphism
    
    def __init__(self, sheaf1, sheaf2):
        Parent.__init__(self, category=Sets())
        self._domain = sheaf1
        self._codomain = sheaf2     
        self._base_ring = sheaf1._base_ring
        self._domain_poset = sheaf1._domain_poset
         
    def domain(self):
        return self._domain
    
    def codomain(self):
        return self._codomain
    
    def zero(self):
        zero = dict()
        for i in self._domain_poset.list():
            zero[i] = matrix(self._base_ring, self._domain._stalk_dict[i], self._codomain._stalk_dict[i])
        return self(zero)
    
    def __call__(self, component_dict, name = "sheaf morphism"):
        mor = self.element_class(self, component_dict, name)
        for r in self._domain_poset.cover_relations():
            print("codomain restriction {} : {}".format(r, self._codomain.restriction(r[0], r[1]).matrix()))
            print('component {} : {}'.format(r[0], mor.component_matrix(r[0])))
            print("domain restriction {} : {}".format(r, self._codomain.restriction(r[0], r[1]).matrix()))
            print('component {} : {}'.format(r[1], mor.component_matrix(r[1])))
            if not self._codomain.restriction(r[0], r[1]).matrix() * mor.component_matrix(r[0]) == mor.component_matrix(r[1]) * self._domain.restriction(r[0], r[1]):
                raise ValueError("input does not define a morphism of sheaves")
        return mor
    
    def _repr_(self):
        return "Set of morphisms from {} to {}".format(self._domain, self._codomain)
        
    def _latex_(self):
        return r'\mbox{' + str(self) + r'}'
   
