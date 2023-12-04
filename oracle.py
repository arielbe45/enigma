import random

from enigma import Enigma, EnigmaSettings
import machines
import permutation


def encrypt(plaintext: str, settings: EnigmaSettings, ground_settings: str, key_settings: str):
    machine = Enigma(settings)
    machine.set_positions(ground_settings)
    ciphertext = machine.encrypt(key_settings * 2)
    machine.set_positions(key_settings)
    ciphertext += machine.encrypt(plaintext)
    return ciphertext


def decrypt(ciphertext: str, settings: EnigmaSettings, ground_settings: str):
    machine = Enigma(settings)
    machine.set_positions(ground_settings)
    key_settings = machine.encrypt(ciphertext[:6])
    if key_settings[:3] != key_settings[3:6]:
        raise Exception("key settings not valid: ", key_settings[:3], "!=", key_settings[3:6])
    machine.set_positions(key_settings[:3])
    plaintext = machine.encrypt(ciphertext[6:])
    return plaintext


def get_random_plugboard(min_count: int, max_count: int, rng: random.Random):
    alphabet = [x for x in permutation.ALPHABET]
    rng.shuffle(alphabet)
    pairs = [alphabet[2 * i] + alphabet[2 * i + 1] for i in range(len(permutation.ALPHABET) // 2)]
    count = rng.randint(min_count, max_count)
    plugboard = permutation.get_permutation_from_cycles(pairs[:count])
    return plugboard


def get_random_position(rng: random.Random):
    return ''.join([rng.choice(permutation.ALPHABET) for _ in range(3)])


def get_random_settings(rng: random.Random):
    ground_settings = get_random_position(rng)
    ring_settings = [rng.randint(0, len(permutation.ALPHABET) - 1) for _ in range(3)]
    # ring_settings = [0, 0, 0]
    reflector = rng.choice(list(machines.ENIGMA1_REFLECTORS.values()))
    rotors = list(machines.ENIGMA1_ROTORS.values())
    rng.shuffle(rotors)
    rotors = rotors[:3]
    plugboard = get_random_plugboard(6, 6, rng=rng)
    settings = EnigmaSettings(plugboard=plugboard, reflector=reflector, ring_settings=ring_settings, rotors=rotors)
    return settings, ground_settings


def oracle(seed: int):
    rng = random.Random(seed)
    settings, ground_settings = get_random_settings(rng)
    key_settings = get_random_position(random.Random())
    ciphertext = encrypt(plaintext='', settings=settings, ground_settings=ground_settings, key_settings=key_settings)
    return ciphertext


def main():
    seed = 10
    print(oracle(seed))
    print(oracle(seed))


if __name__ == '__main__':
    main()
