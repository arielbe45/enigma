import os
import itertools
import json
from typing import Tuple
from collections import defaultdict

from enigma import Enigma, EnigmaSettings
from permutation import Permutation
from oracle import oracle
import permutation
import machines

FILENAME = 'data.json'


def get_catalog_settings_options(seed: int) -> Tuple[EnigmaSettings, str]:
    permutations = get_seed_characteristic_permutations(seed=seed)
    catalog = Catalog()
    catalog.load_if_exists()
    options = catalog.mapping[get_cycle_lengths(permutations)]
    return options


def get_cycle_lengths(permutations: list[Permutation]) -> str:
    cycle_lengths = [[len(cycle) for cycle in p.cycles()] for p in permutations]
    return str([sorted(p) for p in cycle_lengths])


def get_seed_characteristic_permutations(seed):
    mappings = [{}, {}, {}]
    while any(len(mapping) < len(permutation.ALPHABET) for mapping in mappings):
        word = oracle(seed)
        mappings[0][word[3]] = word[0]
        mappings[1][word[4]] = word[1]
        mappings[2][word[5]] = word[2]
    permutations = [Permutation(mapping=mapping) for mapping in mappings]
    return permutations


def get_settings_characteristic_permutations(settings: EnigmaSettings, ground_settings: str):
    machine = Enigma(settings=settings)
    machine.set_positions(ground_settings)

    permutations = []
    for _ in range(6):
        machine.tick()
        permutations.append(machine.get_permutation())

    compositions = [permutations[i].composite(permutations[i + 3]) for i in range(3)]
    return compositions


def iterate_all_settings():
    for reflector in machines.ENIGMA1_REFLECTORS.values():
        for rotors in itertools.permutations(machines.ENIGMA1_ROTORS.values(), 3):
            for ground_settings in itertools.product(permutation.ALPHABET, permutation.ALPHABET, permutation.ALPHABET):
                ground_settings = ''.join(ground_settings)
                yield EnigmaSettings(plugboard=permutation.get_id(), rotors=rotors, ring_settings=[0, 0, 0],
                                     reflector=reflector), ground_settings


class Catalog:
    def __init__(self):
        self.mapping: dict[str, list[Tuple[EnigmaSettings, str]]] = {}

    def load_if_exists(self):
        if os.path.isfile(FILENAME):
            self.load_catalog()
        else:
            self.generate_catalog()
            self.save_catalog()

    def generate_catalog(self):
        cycle_lengths = defaultdict(list)
        for settings, ground_settings in iterate_all_settings():
            permutations = get_settings_characteristic_permutations(settings=settings, ground_settings=ground_settings)
            cycle_lengths[get_cycle_lengths(permutations)].append((settings, ground_settings))
        self.mapping = cycle_lengths

    def save_catalog(self):
        with open(FILENAME, 'w') as file:
            data = defaultdict(list)
            for k, v in self.mapping.items():
                for settings, ground_settings in v:
                    data[k].append(([r.name for r in settings.rotors], settings.reflector.name, ground_settings))
            json.dump(data, file, indent=2)

    def load_catalog(self):
        with open(FILENAME) as file:
            data = json.load(file)
            self.mapping = defaultdict(list)
            for k, v in data.items():
                for rotor_names, reflector_name, ground_settings in v:
                    self.mapping[k].append(
                        (EnigmaSettings(ring_settings=[0, 0, 0], reflector=machines.ENIGMA1_REFLECTORS[reflector_name],
                                        rotors=[machines.ENIGMA1_ROTORS[name] for name in rotor_names],
                                        plugboard=permutation.get_id()),
                         ground_settings))
