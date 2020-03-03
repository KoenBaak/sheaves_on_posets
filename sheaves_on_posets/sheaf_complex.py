
from sage.structure.category_object import CategoryObject
from sage.combinat.posets.posets import Poset
from sage.categories.homset import Hom
from sage.rings.integer_ring import ZZ

from .sheaf import LocallyFreeSheafFinitePoset

class LocFreeSheafComplex(CategoryObject):
    
    def __init__(self, data):
        self._base_ring = data[1]._base_ring
        self._domain_poset = data[1]._domain_poset
        self._min = data[0]
        self._sheaves = dict()
        self._diff = dict()
        for c, v in enumerate(data[1:]):
            if c%2 == 0:
                self._sheaves[self._min + c//2] = v
            else:
                self._diff[self._min + (c-1)//2] = v
    
    def sheaf_at(self, place):
        if place not in self._sheaves:
            stalks = {x:0 for x in self._domain_poset.list()}
            res = {tuple(r):0 for r in self._domain_poset.cover_relations()}
            return LocallyFreeSheafFinitePoset(stalks, res, self._base_ring, self._domain_poset)
        return self._sheaves[place]
    
    def differential(self, place):
        if place not in self._diff:
            hom = Hom(self.sheaf_at(place), self.sheaf_at(place + 1))
            return hom.zero()
        return self._diff[place]
    
    def _repr_(self):
        return "(Cochain) Complex of Locally Free Sheaves of Modules over {} on {} with at least {} nonzero terms".format(self._base_ring, self._domain_poset, len(self._sheaves))
        

def _dualizing_sheaf(poset, degree, base_ring, rank):
    p = degree*-1
    chains = sorted(filter(lambda chain: len(chain)==p+1, poset.chains()))
    singleton = Poset({0:[]}, {})
    sheaf = LocallyFreeSheafFinitePoset({0:rank}, {}, base_ring = base_ring, domain_poset = singleton)
    result = None
    hom = Hom(singleton, poset)
    for c in chains:
        inclusion = hom(lambda point: {0:c[-1]}[point])
        to_add = sheaf.pushforward(inclusion)
        if result is None:
            result = to_add
        else:
            result = result + to_add
    return result
    
        
def dualizing_complex(poset, base_ring=ZZ, rank=1):
    dim = poset.height() - 1
    bound_below = -1*dim
    data = [bound_below]
    for p in range(0, dim):
        differential = 0
        data.append(_dualizing_sheaf(poset, -1*p, base_ring, rank))
        data.append(differential)
    data.append(_dualizing_sheaf(poset, -1*dim, base_ring, rank))
    return LocFreeSheafComplex(data)











       
        
        
        
        
        
        
        
        
        
        
