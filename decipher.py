from catalog import get_catalog_settings_options, get_settings_characteristic_permutations, \
    get_seed_characteristic_permutations
from oracle import get_random_settings
from plugboard import get_plugboard

import random


def get_settings(seed: int):
    real_p = get_seed_characteristic_permutations(seed)
    options = get_catalog_settings_options(seed)

    solutions = []
    for settings, ground_settings in options:
        guess_p = get_settings_characteristic_permutations(settings=settings, ground_settings=ground_settings)
        plugboard = get_plugboard(guess_p, real_p)
        if plugboard is not None:
            settings.plugboard = plugboard
            solutions.append((settings, ground_settings))
    if len(solutions) != 1:
        raise Exception('solution not found:', solutions)
    return solutions[0]


def main():
    seed = 10
    secret_settings, secret_ground_settings = get_random_settings(rng=random.Random(seed))
    print('solution:', secret_settings, secret_ground_settings)
    print(get_settings(seed))


if __name__ == '__main__':
    main()