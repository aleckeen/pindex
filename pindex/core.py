import os
import argparse
from typing import Optional, List


class Pindex:
    root: str
    save: str
    find_duplicates: bool

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--root", dest="root", type=str,
                            default="./")
        parser.add_argument("--save", dest="save", type=str,
                            default="./database.json")
        parser.add_argument("--find-duplicates", dest="find_duplicates",
                            action="store_true")
        args = parser.parse_args()

        self.root = os.path.abspath(args.root)
        self.save = os.path.abspath(args.save)
        self.find_duplicates = args.find_duplicates

    def check(self) -> Optional[List[str]]:
        errs = []

        if not os.path.isdir(self.root):
            errs.append(f"Root directory is not found: {self.root}")

        save_parent = os.path.abspath(os.path.join(self.save, os.pardir))
        if not os.path.isdir(save_parent):
            errs.append("Parent directory is not found to save the database: "
                        f"{save_parent}")

        if not len(errs) == 0:
            return errs
        return None
