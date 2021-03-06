"""
  Finite Locally Free Sheaves of Modules on Finite Posets. 
"""

# imports 
from sage.structure.category_object import CategoryObject
from sage.categories.homset import Hom
from sage.matrix.special import identity_matrix
from sage.matrix.special import block_matrix, block_diagonal_matrix
from sage.matrix.constructor import Matrix, matrix
from sage.homology.chain_complex import ChainComplex
from sage.rings.integer_ring import ZZ
from sage.combinat.posets.posets import Poset
from sage.tensor.modules.finite_rank_free_module import FiniteRankFreeModule

from .sheaf_homset import LocFreeSheafHomset

#-------------------------------------------------------------------------------
def _composition_free_module_morphism(psi, phi):
    """
      Returns the composition of two compasable morphisms of free modules of 
      finite rank over the same base ring.
    """    
    hom = Hom(phi.domain(), psi.codomain())
    if phi.is_zero() or psi.is_zero():
        return hom.zero()
    return hom(psi.matrix() * phi.matrix())

def ConstantSheaf(domain_poset, base_ring = ZZ, rank=1):
    stalk_dict = {x:rank for x in domain_poset.list()}
    res_dict = {tuple(r):1 for r in domain_poset.cover_relations()}
    return LocallyFreeSheafFinitePoset(stalk_dict, res_dict, base_ring = base_ring, domain_poset = domain_poset)

def ZeroSheaf(domain_poset, base_ring = ZZ):
    return ConstantSheaf(domain_poset, base_ring, rank = 0)
    
def LocFreeSheaf(stalk_dict = {}, res_dict = {}, base_ring = ZZ, domain_poset = None):
    '''
      Construct a finite locally free sheaf of modules on a poset, given 
      certain input. Checks are performed to check if the given input indeed
      defines a sheaf. 
      
      INPUT:
      
      - ``stalk_dict`` -- (default: ``{}``); a dictionary where the keys are the points in the poset
          and the values are the ranks of the corresponding stalks.
      
      - ``res_dict`` -- (default: ``{}``); a dictionary where the keys are cover-relations of the poset
         (as tuples) and the values are the matrices of the corresponding restriction maps.
         Instead of a matrix, the input ``0`` is accepted and interpreted as the zero map 
         and the input ``1`` is accepted and interpreted as the identity matrix. 
         
      - ``base_ring`` -- (default: ``ZZ``); the ring over which the sheaf of modules is defined. 
          Can be any commutative ring, but to be able to calculate sheaf cohomology, one should 
          use rings that can be used as base ring for a ``ChainComplex``. Fields or `\mathbb{Z}` work fine. 
      
      - ``domain_poset`` -- (default: ``None``); the finite poset on which the sheaf is defined. 
          If the domain_poset is None, a domain poset will be build from the data in the stalk-
          and restriction dictionaries.  
      
      OUTPUT:
      
      An instance of  :class:`LocallyFreeSheafFinitePoset`.
      
    '''
    
    # Build a poset from the data in the stalk dict and the res dict
    build_poset_dict = dict()
    for key in stalk_dict:
        build_poset_dict[key] = []
    for relation in res_dict:
        build_poset_dict[relation[0]].append(relation[1])
    try:
        built_poset = Poset(build_poset_dict)
    except:
        raise ValueError("Data does not determine a sheaf on a poset.")
    
    # If a domain poset was provided, check if it matches the poset structure 
    # obtained from the stalk and res dictionaries. 
    if domain_poset is not None:
        if not domain_poset.is_isomorphic(built_poset):
            raise ValueError("Data does not determine a sheaf on the given poset.")
    else:
        domain_poset = built_poset
    
    # Build the sheaf and check if it is indeed a valid sheaf. 
    sheaf = LocallyFreeSheafFinitePoset(stalk_dict, res_dict, base_ring, domain_poset)
    if not sheaf._sheaf_data_valid():
        raise ValueError("The sheaf data is not valid")
    
    return sheaf
    
class LocallyFreeSheafFinitePoset(CategoryObject):
    """
      A Finite Locally Free Sheaf of Modules over a Commutative Ring on a Finite Poset.
      
      It is assumed that the provided inputs determine a valid sheaf. No checks 
      to assure this are performed. It is recommanded to build sheafs with 
      :func:`LocFreeSheaf`
      
      INPUT:
      
      - ``stalk_dict`` -- a dictionary where the keys are the points in the poset
          and the values are the ranks of the corresponding stalks.
      
      - ``res_dict`` -- a dictionary where the keys are cover-relations of the poset
         (as tuples) and the values are the matrices of the corresponding restriction maps.
         Instead of a matrix, the input ``0`` is accepted and interpreted as the zero map 
         and the input ``1`` is accepted and interpreted as the identity matrix. 
         
      - ``base_ring`` -- the ring over which the sheaf of modules is defined. 
          Can be any commutative ring, but to be able to calculate sheaf cohomology, one should 
          use rings that can be used as base ring for ``ChainComplex``. Fields or `\mathbb{Z}` work fine. 
      
      - ``domain_poset`` -- the finite poset on which the sheaf is defined. 
    """
    def __init__(self, stalk_dict, res_dict, base_ring, domain_poset):
        """
          Constructor of :class:`LocallyFreeSheafFinitePoset`
        """
        self._stalk_dict = stalk_dict
        self._res_dict = res_dict
        self._base_ring = base_ring
        self._domain_poset = domain_poset
    
    def stalk(self, point):
        """
          Return the stalk of ``self`` at the point ``point``.
          
          INPUT:
          
          - ``point`` -- A point in the domain poset of ``self``. 
          
          OUTPUT:
          
          The stalk of ``self`` at ``point``
        """
        stalk = FiniteRankFreeModule(self._base_ring, self._stalk_dict[point], name="Stalk of {} at {}".format(self, point))
        stalk.basis('e')
        return stalk
    
    def _cover_relation_to_restriction(self, relation):
        """
          Returns the restriction morphism associated to a cover relation of the domain
          poset of ``self``. 
        """
        hom = Hom(self.stalk(relation[0]), self.stalk(relation[1]))
        if self._res_dict[relation] == 0:
            return hom.zero()
        elif self._res_dict[relation] == 1:
            return hom(identity_matrix(self._stalk_dict[relation[0]]))
        else:
            return hom(self._res_dict[relation])
    
    def _cover_chain_to_restriction(self, chain):
        """
          Builds the restriction map from ``chain[0]`` to ``chain[1]`` 
          by composing the restrictions of all cover relations in the chain.  
        """
        phi = self._cover_relation_to_restriction((chain[0], chain[1]))
        for i, v in enumerate(chain[1:-1]):
            psi = self._cover_relation_to_restriction((v, chain[i+2]))
            phi = _composition_free_module_morphism(psi, phi)
        return phi
     
    def restriction(self, frompoint, topoint):
        """
          Return the restriction map of ``self`` from ``frompoint`` to ``topoint``.
        """
        if not self._domain_poset.is_less_than(frompoint, topoint):
            raise ValueError("{} is not a specialization of {}".format(frompoint, topoint))
        chains =  list(filter(lambda c: (frompoint in c) and (topoint in c), self._domain_poset.chains()))
        chains = [c[c.index(frompoint):c.index(topoint)+1] for c in chains]
        cover_chain = sorted(chains, key=lambda c: len(c), reverse=True)[0]
        morphism = self._cover_chain_to_restriction(cover_chain)
        morphism._name = "Restriction Map of {} from {} to {}".format(self, frompoint, topoint)
        return morphism 
    
    def _sheaf_data_valid(self):
        """
          Checks if the data in the restriction dictionary of ``self``
          makes a valif sheaf. That it, is check whether the provided data is functorial.
        """
        for relation in filter(lambda r: r[0] != r[1], self._domain_poset.relations()):
            restriction = None
            frompoint = relation[0]
            topoint = relation[1]
            chains =  list(filter(lambda c: (frompoint in c) and (topoint in c), self._domain_poset.chains()))
            chains = [c[c.index(frompoint):c.index(topoint)+1] for c in chains]
            maxlength = max([len(c) for c in chains])
            cover_chains = filter(lambda c: len(c) == maxlength, chains)
            for c in cover_chains:
                if restriction is None:
                    restriction = self._cover_chain_to_restriction(c)
                elif restriction != self._cover_chain_to_restriction(c):
                    return False
        return True
                
    def base_ring(self):
        """
          Return the base ring.
        """
        return self._base_ring
    
    def domain_poset(self):
        """
          Return the poset on which the sheaf is defined.
        """    
        return self._domain_poset
    
    def _godement_complex_differential(self, start_base, end_base):
        """
          Construct the differential of the godement cochain complex from 
          the free module with basis ``start_base`` to the free module with basis
          ``end_base``.
        """
        
        rows = []
        for to_chain in end_base:
            blocks = []
            m = self._stalk_dict[to_chain[-1]]
            for from_chain in start_base:
                n = self._stalk_dict[from_chain[-1]]
                if all(x in to_chain for x in from_chain):
                    for point in to_chain:
                        if point not in from_chain:
                            index = to_chain.index(point)
                            sign = 1 if index % 2 == 0 else - 1
                            if index != len(to_chain) - 1:
                                blocks.append(sign*identity_matrix(self._base_ring, m))
                            else:
                                mat = self.restriction(from_chain[-1], point).matrix()
                                blocks.append(sign*mat)
                            break 
                else:
                    blocks.append(Matrix(self._base_ring, m, n))
            rows.append(blocks)
        return block_matrix(rows, subdivide=False)
        
    
    def godement_cochain_complex(self):
        """
          Construct the Godement cochain complex of ``self``. 
        """
        # The case that the domain_space has dimension 0
        if self._domain_poset.height() == 1:
            rank = sum(self._stalk_dict[key] for key in self._stalk_dict)
            differential = matrix(self._base_ring, 0, rank)
            return ChainComplex([rank, differential], base_ring=self._base_ring)
        
        # Other cases
        end_base = sorted([[x] for x in self._domain_poset.list()])
        diff_dict = dict()
        for p in range(1, self._domain_poset.height()):
            start_base = end_base
            end_base = list(filter(lambda c: len(c)==p+1, self._domain_poset.chains()))
            end_base = sorted(end_base)
            diff_dict[p-1] = self._godement_complex_differential(start_base, end_base)
        return ChainComplex(diff_dict, base_ring = self._base_ring)
    
    def cohomology(self, degree=None):
        """
          Return the cohomology of ``self``. 
        """
        return self.godement_cochain_complex().homology(degree)
    
    def global_sections(self):
        """
          Return the global sections of ``self``.  
        """
        c = self.cohomology(0)
        return FiniteRankFreeModule(self._base_ring, c.ngens(), name="Global Sections of {}".format(self))
    
    def extend_by_zero(self, inclusion_map):
        """
          Return the extension by zero of ``self`` to the codomain of ``inclusion_map``.
          
          INPUT:
          
          - ``inclusion_map`` -- An embedding of posets.
          
          OUTPUT:
          
          The extension by zero of ``self`` to the codomain of ``inclusion_map``.  
        """
        
        # check if inlcusion_map is indeed an embedding 
        image = [inclusion_map(x) for x in self._domain_poset.list()]
        if any(x not in image for x in inclusion_map.codomain().order_filter(image)):
            raise ValueError("The given inclusion map is not an embedding.")
        
        inverse = dict()
        for p in self._domain_poset.list():
            inverse[inclusion_map(p)] = p
        target_poset = inclusion_map.codomain()
        target_stalks = dict()
        target_res = dict()
        for p in self._domain_poset.list():
            target_stalks[inclusion_map(p)] = self._stalk_dict[p]
        for p in target_poset.list():
            if p not in target_stalks:
                target_stalks[p] = 0
        for a, b in target_poset.cover_relations():
            if target_stalks[a]  == 0:
                target_res[(a, b)] = 0
                continue
            target_res = self._res_dict[(inverse(a), inverse(b))]
        return LocallyFreeSheafFinitePoset(target_stalks, target_res, base_ring = self._base_ring, domain_poset = target_poset)
    
    def pushforward(self, poset_map):
        if self._domain_poset.cardinality() == 1:
            point = self._domain_poset.list()[0]
            image = poset_map(point)
            supported = poset_map.codomain().order_ideal([image])
            stalks = {x:self._stalk_dict[point] if x in supported else 0 for x in poset_map.codomain().list()}
            restrictions = {tuple(r):1 if r[1] in supported else 0 for r in poset_map.codomain().cover_relations()}
            return LocallyFreeSheafFinitePoset(stalks, restrictions, self._base_ring, poset_map.codomain())
        raise NotImplementedError("For now only sheaves on a singleton can be pushed forward")
    
    def restrict_to(self, open_set):
        """
          Construct the restriction sheaf of ``self`` to ``open_set``. 
        """
        
        # Check whether the given set is indeed upwards closed
        if any(r[1] not in open_set for r in filter(lambda x: x[0] in open_set, self._domain_poset.relations())):
            raise ValueError("The given set is not upward closed.")
            
        s_dict = dict(filter(lambda (key, value): key in open_set, self._stalk_dict.items()))
        r_dict = dict(filter(lambda (key, value): key[0] in open_set, self._res_dict.items()))
        poset_dict = {x:self._domain_poset.order_filter([x])[1:] for x in s_dict}
        return LocallyFreeSheafFinitePoset(s_dict, r_dict, self._base_ring, Poset(poset_dict))
        
    def sections(self, open_set):    
        """
          Return the sections of ``self`` on ``open_set``.
        """
        s = self.restrict_to(open_set).global_sections()
        s._name = "Sections of {} on {}".format(self, open_set)
        return s
    
    def euler_characteristic(self):
        """
          Calculate the Euler Characteristic of ``self``. 
        """
        coh = self.cohomology()
        result = 0
        alt = lambda x: 1 if x%2 == 0 else -1
        for key, value in coh.items():
            result += alt(key)*value.ngens()
        return result 
    
    def godement_sheaf(self):
        """
          Returns the Godement sheaf of ``self``.
        """
        g0_stalks = dict()
        g0_res = dict()
        for p in self._domain_poset.list():
            g0_stalks[p] = sum(self._stalk_dict[x] for x in self._domain_poset.order_filter([p]))
        for relation in self._domain_poset.cover_relations():
            frombase = sorted(self._domain_poset.order_filter([relation[0]]))
            tobase = sorted(self._domain_poset.order_filter([relation[1]]))
            rows = []
            for row in tobase:
                m = self._stalk_dict[row]
                blocks = []
                for x in frombase:
                    if x == row:
                        blocks.append(identity_matrix(m))
                    else:
                        blocks.append(Matrix(m, self._stalk_dict[x]))
                rows.append(blocks)    
            g0_res[tuple(relation)] = block_matrix(rows, subdivide=False)    
        G0 = LocallyFreeSheafFinitePoset(g0_stalks, g0_res, self._base_ring, self._domain_poset)
        hom = Hom(self, G0)
        eps_dict = dict()
        for p in self._domain_poset.list():
            rows = []
            for x in sorted(self._domain_poset.order_filter([p])):
                if x == p:
                    rows.append([identity_matrix(self._base_ring, self._stalk_dict[p])])
                else:
                    rows.append([self.restriction(p, x).matrix()])
            eps_dict[p] = block_matrix(rows, subdivide=False)
        epsilon = hom(eps_dict)
        return epsilon, G0  
        
    def _direct_sum(self, other):
        if not (self._base_ring == other._base_ring and self._domain_poset == other._domain_poset):
            raise TypeError("Sheaves are not defined on same poset or not defined over same ring")
        direct_sum_stalks = {x:self._stalk_dict[x] + other._stalk_dict[x] for x in self._domain_poset.list()}
        direct_sum_res = {tuple(r):block_diagonal_matrix(self.restriction(r[0], r[1]).matrix(), other.restriction(r[0], r[1]).matrix(), subdivide = False) for r in self._domain_poset.cover_relations()}
        return LocallyFreeSheafFinitePoset(direct_sum_stalks, direct_sum_res, self._base_ring, self._domain_poset)
    
    def __add__(self, other):
        return self._direct_sum(other)
    
    def __radd__(self, other):
        return other._direct_sum(self)
            
    def _latex_(self):
        return r'\mbox{' + str(self) + r'}'
    
    def _repr_(self):
        return "Locally Free Sheaf of Modules over {} on {}".format(self._base_ring, self._domain_poset)
    
    def _Hom_(self, other, category=None):
        if not (other._domain_poset == self._domain_poset and other._base_ring == self._base_ring):
            raise ValueError("Sheaves have different domain posets or different base rings.")
        return LocFreeSheafHomset(self, other) 
    
        
        
