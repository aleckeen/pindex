import sys

from pindex.core import Pindex
from pindex.walker import walk


def main():
    config = Pindex()
    errs = config.check()
    if errs is None:
        walk(config)
        exit(0)
    else:
        for err in errs:
            print(err, file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
