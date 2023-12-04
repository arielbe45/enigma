import random

from decipher import decipher
from oracle import get_random_settings, encrypt, get_random_position, decrypt


def main():
    seed = int(input('enter seed: '))
    settings, ground_settings = get_random_settings(random.Random(seed))
    print('random settings:', settings, f'{ground_settings=}')
    message = input('enter message: ')
    key_settings = get_random_position(random.Random())
    print('key settings:', key_settings)
    ciphertext = encrypt(plaintext=message, settings=settings, ground_settings=ground_settings,
                         key_settings=key_settings)
    print('ciphertext:', ciphertext)

    print('breaking the enigma...')
    guess_settings, guess_ground_settings = decipher(seed)
    print('guess settings:', guess_settings, f'{guess_ground_settings=}')
    deciphered = decrypt(ciphertext=ciphertext, settings=guess_settings, ground_settings=guess_ground_settings)
    print('deciphered text:', deciphered)


if __name__ == '__main__':
    main()
