import argparse
import sys

ALPHABETS = {
    "en": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "bg": "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЮЯ",
    "ru": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
    "de": "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß",
    "tr": "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ",
    "gr": "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ",
}


def setup_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Mode of operation (encrypt or decrypt)")
    parser.add_argument("text", nargs="?", help="Text to be processed")
    parser.add_argument("-k", "--key", type=int, required=True, help="Key for encryption/decryption")
    parser.add_argument("-a", "--alphabet", default="en", help="Alphabet to use")
    return parser.parse_args()


def transform_word(word, key, language):
    return "".join(transform_letter(c, key, language) for c in word)


def transform_letter(letter, key, language):
    alphabet_in_use = ALPHABETS[language]

    is_upper = letter.isupper()
    letter = letter.upper()

    if letter not in alphabet_in_use:
        return letter if is_upper else letter.lower()

    index = alphabet_in_use.find(letter)
    new_index = (index + key) % len(alphabet_in_use)

    if not is_upper:
        return alphabet_in_use[new_index].lower()
    return alphabet_in_use[new_index]


def encrypt(word, key, language):
    return transform_word(word, key, language)


def decrypt(word, key, language):
    return transform_word(word, -key, language)


if __name__ == "__main__":
    args = setup_cli()
    mode = args.mode
    text = args.text
    key = args.key
    alphabet = args.alphabet

    print(f"Helpful debug info: {mode=}, {key=}, {alphabet=}, {text=}")

    alphabet = alphabet.lower()

    if alphabet not in ALPHABETS:
        print(f"Unrecognized alphabet {alphabet}. Supported values are: {", ".join(ALPHABETS.keys())}")
        sys.exit(1)

    if text is None:
        text = input()

    if not 1 <= key < len(ALPHABETS[alphabet]):
        print(f"Key {key} is not valid")
        sys.exit(1)

    if key == 0 or key == len(ALPHABETS[alphabet]):
        print("Key results in no change")
        sys.exit(1)

    if mode == "encrypt":
        result = encrypt(text, key, alphabet)
    elif mode == "decrypt":
        result = decrypt(text, key, alphabet)
    else:
        print("This isn't suppose to happen !")
        sys.exit(1)

    print(result)
