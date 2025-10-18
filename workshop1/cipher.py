import argparse


parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Mode of operation (encrypt or decrypt)")
parser.add_argument("text", nargs="?", help="Text to be processed")
parser.add_argument("-k", "--key", type=int, required=True, help="Key for encryption/decryption")
parser.add_argument("-a", "--alphabet", default="en", help="Alphabet to use")
args = parser.parse_args()

mode = args.mode
text = args.text
key = args.key
alphabet = args.alphabet

# print(f"Helpful debug info: {mode=}, {key=}, {alphabet=}, {text=}")


# свободни сте да пишете и променяте кода във файла както сметнете за най-удачно
# употребата на функции е препоръчителна
