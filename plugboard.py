import itertools

import permutation
from permutation import Permutation


def iterate_cycle_order(p: Permutation):
    for cycles_permutation in itertools.permutations(p.cycles()):
        if sorted(cycles_permutation, key=len) == list(cycles_permutation):
            yield cycles_permutation


def iterate_cycle_rotations(cycle: str):
    for _ in range(len(cycle)):
        cycle = cycle[1:] + cycle[0]
        yield cycle


def iterate_permutation_representations(p: Permutation):
    for cycle_order in iterate_cycle_order(p):
        for cycle_rotation in itertools.product(*[iterate_cycle_rotations(c) for c in cycle_order]):
            yield cycle_rotation


def get_representation_diff(p1_representation: list[str], p2: Permutation):
    p2_representation = sorted(p2.cycles(), key=len)
    p1_concat = ''.join(p1_representation)
    p2_concat = ''.join(p2_representation)
    diff = list(set(min(x, y) + max(x, y) for x, y in zip(p1_concat, p2_concat) if x != y))
    valid = all(''.join(diff).count(x) <= 1 for x in permutation.ALPHABET)
    return permutation.get_permutation_from_cycles(diff), valid


def get_conjugate(p1: Permutation, p2: Permutation):
    """
    Finds the conjugate permutation x given p1 = x * p2 * x.inverse()
    :param p1: Permutation
    :param p2: Permutation
    :return: the conjugate permutation
    """
    min_diff = None
    for p1_repr in iterate_permutation_representations(p1):
        diff, valid = get_representation_diff(p1_repr, p2)
        if valid and (min_diff is None or len(diff.cycles()) < len(min_diff.cycles())):
            min_diff = diff
    conjugate = min_diff
    valid = (conjugate is not None) and permutation.composition(conjugate, p1, conjugate).mapping == p2.mapping
    return conjugate, valid


def get_plugboard(real_characteristic_permutations: list[Permutation],
                  guest_characteristic_permutations: list[Permutation]):
    ad_r, be_r, cf_r = real_characteristic_permutations
    ad_g, be_g, cf_g = guest_characteristic_permutations
    ad_conj, ad_valid = get_conjugate(ad_r, ad_g)
    be_conj, be_valid = get_conjugate(be_r, be_g)
    cf_conj, cf_valid = get_conjugate(cf_r, cf_g)
    if ad_valid and be_valid and cf_valid:
        conj = set(list(ad_conj.cycles()) + list(be_conj.cycles()) + list(cf_conj.cycles()))
        return permutation.get_permutation_from_cycles(list(conj))
    return None
