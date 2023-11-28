from machines import *


def main():
    settings = EnigmaSettings(plugboard=get_id(), reflector=ENIGMA1_REFLECTORS['B'], ring_settings=[12, 13, 3],
                              rotors=[ENIGMA1_ROTORS['III'], ENIGMA1_ROTORS['I'], ENIGMA1_ROTORS['II']])
    machine = Enigma(settings=settings, rotor_positions=[1, 2, 3])
    print(machine.encrypt('a' * 26, ignore=False))


if __name__ == '__main__':
    main()
