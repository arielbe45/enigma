from permutation import *

from dataclasses import dataclass, field


@dataclass
class Rotor:
    p: Permutation
    turnover_notch_pos: list[int]
    name: str

    def __repr__(self):
        return self.name


@dataclass
class Reflector:
    p: Permutation
    name: str

    def __repr__(self):
        return self.name


@dataclass
class EnigmaSettings:
    plugboard: Permutation
    rotors: list[Rotor]
    ring_settings: list[int]
    reflector: Reflector


@dataclass
class Enigma:
    settings: EnigmaSettings
    rotor_positions: list[int] = field(default=None)

    def __post_init__(self):
        if self.rotor_positions is None:
            self.rotor_positions = [0] * len(self.settings.rotors)

    def set_positions(self, positions: str):
        if len(positions) != len(self.settings.rotors) or any(x not in ALPHABET for x in positions):
            raise ValueError
        self.rotor_positions = [ALPHABET.index(x) for x in positions]

    def get_permutation(self):
        rotors = []
        for i in range(3):
            offset = get_offset_p(self.rotor_positions[i] - self.settings.ring_settings[i])
            rotors.append(composition(offset.inverse(), self.settings.rotors[i].p, offset))
        p = composition(*rotors, self.settings.plugboard)
        return composition(p.inverse(), self.settings.reflector.p, p)

    def tick(self):
        self.rotor_positions[-1] = (self.rotor_positions[-1] + 1) % len(ALPHABET)
        if self.rotor_positions[-1] in self.settings.rotors[-1].turnover_notch_pos:
            self.rotor_positions[-2] = (self.rotor_positions[-2] + 1) % len(ALPHABET)
            if self.rotor_positions[-2] in self.settings.rotors[-2].turnover_notch_pos:
                self.rotor_positions[-3] = (self.rotor_positions[-3] + 1) % len(ALPHABET)

    def encrypt(self, plaintext, ignore: bool = False):
        ciphertext = ''
        for x in plaintext:
            if x in ALPHABET:
                self.tick()
                ciphertext += self.get_permutation().mapping[x]
            elif not ignore:
                ciphertext += x
        return ciphertext

    def reset(self):
        self.rotor_positions = [0] * len(self.settings.rotors)
