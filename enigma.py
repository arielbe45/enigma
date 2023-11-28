from permutation import *

from dataclasses import dataclass


@dataclass
class Rotor:
    p: Permutation
    turnover_notch_pos: list[int]


@dataclass
class EnigmaSettings:
    plugboard: Permutation
    rotors: list[Rotor]
    ring_settings: list[int]
    reflector: Permutation


@dataclass
class Enigma:
    settings: EnigmaSettings
    rotor_positions: list[int]

    def get_permutation(self):
        rotors = []
        for i in range(3):
            offset = get_offset_p(self.rotor_positions[i] - self.settings.ring_settings[i])
            rotors.append(composition(offset.inverse(), self.settings.rotors[i].p, offset))
        p = composition(*rotors, self.settings.plugboard)
        return composition(p.inverse(), self.settings.reflector, p)

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
