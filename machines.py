from enigma import *

ENIGMA1_ROTORS = {
    'I': Rotor(p=get_permutation_from_order('ekmflgdqvzntowyhxuspaibrcj'), turnover_notch_pos=[ALPHABET.index('r')]),
    'II': Rotor(p=get_permutation_from_order('ajdksiruxblhwtmcqgznpyfvoe'), turnover_notch_pos=[ALPHABET.index('f')]),
    'III': Rotor(p=get_permutation_from_order('bdfhjlcprtxvznyeiwgakmusqo'), turnover_notch_pos=[ALPHABET.index('w')])
}

ENIGMA1_REFLECTORS = {
    'B': get_permutation_from_cycles(['ay', 'br', 'cu', 'dh', 'eq', 'fs', 'gl', 'ip', 'jx', 'kn', 'mo', 'tz', 'vw']),
    'C': get_permutation_from_cycles(['af', 'bv', 'cp', 'dj', 'ei', 'go', 'hy', 'kr', 'lz', 'mx', 'nw', 'tq', 'su'])
}
