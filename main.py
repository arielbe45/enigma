from machines import *


def main():
    settings = EnigmaSettings(plugboard=get_id(), reflector=ENIGMA1_REFLECTORS['B'], ring_settings=[0, 0, 0],
                              rotors=[ENIGMA1_ROTORS['I'], ENIGMA1_ROTORS['I'], ENIGMA1_ROTORS['I']])
    machine = Enigma(settings=settings, rotor_positions=[0, 0, 0])
    print(machine.encrypt('aaaaaaaaaa'))


if __name__ == '__main__':
    main()
