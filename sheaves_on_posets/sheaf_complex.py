
from sage.structure.category_object import CategoryObject
from sage.combinat.posets.posets import Poset
from sage.categories.homset import Hom
from sage.rings.integer_ring import ZZ

from sage.matrix.special import identity_matrix
from sage.matrix.special import block_matrix
from sage.matrix.constructor import matrix
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
                  
    def below_bound(self):
        return self._min
    
    def above_bound(self):
        max(self._sheaves)
    
    def sheaf_at(self, place):
        if place not in self._sheaves:
            stalks = {x:0 for x in self._domain_poset.list()}
            res = {tuple(r):0 for r in self._domain_poset.cover_relations()}
            return LocallyFreeSheafFinitePoset(stalks, res, self._base_ring, self._domain_poset)
        return self._sheaves[place]
    
    def differential(self, place):
        hom = Hom(self.sheaf_at(place), self.sheaf_at(place + 1))
        if place not in self._diff:
            return hom.zero()
        return hom(self._diff[place])
    
    def _check_zero_composition(self):
        for place in range(self.below_bound(), self.above_bound()):
            pass
    
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
    end_base = sorted(poset.maximal_chains())
    for p in range(-1*dim, 0):
        start_base = end_base
        end_base = sorted(filter(lambda c: len(c) == -1*p, poset.chains()))
        differential = dict()
        for x in poset.list():
            point_start_base = filter(lambda c: poset.is_less_than(x, c[-1]), start_base)
            point_end_base = filter(lambda c: poset.is_less_than(x, c[-1]), end_base)
            rows = []
            for end_chain in point_end_base:
                blocks = []
                for start_chain in point_start_base:
                    if all(p in start_chain for p in end_chain):
                        for y in start_chain:
                            if y not in end_chain and y != start_chain[-1]:
                                sign = 1 if start_chain.index(y)%2 == 0 else -1
                                blocks.append(identity_matrix(base_ring, rank))
                                break
                        else:
                            blocks.append(matrix(base_ring, rank, rank))    
                    else:
                        blocks.append(matrix(base_ring, rank, rank))        
                rows.append(blocks)
            differential[x] = block_matrix(rows, subdivide = False)    
        data.append(_dualizing_sheaf(poset, p, base_ring, rank))
        data.append(differential)
    data.append(_dualizing_sheaf(poset, 0, base_ring, rank))
    return LocFreeSheafComplex(data)









       
        
        
        
        
        
        
        
        
        
        
