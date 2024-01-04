import string

ALPHABET = string.ascii_lowercase


class Permutation:
    """
    Represents a permutation on the alphabet abc...z
    """

    def __init__(self, mapping: dict[str, str]):
        self.mapping = mapping

    def composite(self, p: 'Permutation'):
        return Permutation(mapping={x: self.mapping[p.mapping[x]] for x in self.mapping})

    def inverse(self):
        return Permutation(mapping={self.mapping[x]: x for x in self.mapping})

    def check_valid(self):
        return all(x in ALPHABET for x in self.mapping) and len(self.mapping) == len(ALPHABET) and all(
            x in self.mapping.values() for x in ALPHABET)

    def cycles(self):
        cycles = []
        found = set()
        for x in self.mapping:
            if x not in found:
                cycle = []
                y = x
                while y not in found:
                    found.add(y)
                    cycle.append(y)
                    y = self.mapping[y]
                if len(cycle) != 1:
                    cycles.append(''.join(cycle))
        return cycles

    def __repr__(self):
        return str(self.cycles())


def get_permutation_from_cycles(cycles: list[str]):
    mapping = {x: x for x in ALPHABET}
    for cycle in cycles:
        for i in range(len(cycle) - 1):
            mapping[cycle[i]] = cycle[i + 1]
        mapping[cycle[-1]] = cycle[0]
    return Permutation(mapping=mapping)


def get_permutation_from_order(order: str):
    assert len(order) == len(ALPHABET) and set(order) == set(ALPHABET)
    return Permutation(mapping={ALPHABET[i]: order[i] for i in range(len(order))})


def composition(*permutations: Permutation):
    if len(permutations) == 1:
        return permutations[0]
    return permutations[0].composite(composition(*permutations[1:]))


def get_offset_p(i):
    return Permutation(mapping={ALPHABET[j]: ALPHABET[(j + i) % len(ALPHABET)] for j in range(len(ALPHABET))})


def get_id():
    return Permutation(mapping={x: x for x in ALPHABET})
