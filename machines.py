import enigma
import permutation

ENIGMA1_ROTORS = {
    'I': enigma.Rotor(p=permutation.get_permutation_from_order('ekmflgdqvzntowyhxuspaibrcj'),
                      turnover_notch_pos=[permutation.ALPHABET.index('r')],
                      name='I'),
    'II': enigma.Rotor(p=permutation.get_permutation_from_order('ajdksiruxblhwtmcqgznpyfvoe'),
                       turnover_notch_pos=[permutation.ALPHABET.index('f')],
                       name='II'),
    'III': enigma.Rotor(p=permutation.get_permutation_from_order('bdfhjlcprtxvznyeiwgakmusqo'),
                        turnover_notch_pos=[permutation.ALPHABET.index('w')],
                        name='III')
}

ENIGMA1_REFLECTORS = {
    'B': enigma.Reflector(
        p=permutation.get_permutation_from_cycles(
            ['ay', 'br', 'cu', 'dh', 'eq', 'fs', 'gl', 'ip', 'jx', 'kn', 'mo', 'tz', 'vw']),
        name='B'),
    'C': enigma.Reflector(
        p=permutation.get_permutation_from_cycles(
            ['af', 'bv', 'cp', 'dj', 'ei', 'go', 'hy', 'kr', 'lz', 'mx', 'nw', 'tq', 'su']),
        name='C')
}
