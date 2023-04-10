import sys

from Application import Application


def main(args):
    # handle script arguments
    known_lang = args.get("--known", args.get("-k", "ru"))
    unknown_lang = args.get("--unknown", args.get("-u", None))

    Application(known_lang=known_lang, unknown_lang=unknown_lang)


if __name__ == "__main__":
    args_dict = {sys.argv[i]: sys.argv[i+1] for i in range(1, len(sys.argv), 2)}
    main(args_dict)
