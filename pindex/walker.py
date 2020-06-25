import os
import json

from typing import List, Dict, Any

from pindex.core import Pindex
from pindex.duplicates import find_duplicates
from pindex.util import Printer, human_readable, concat


def index(config: Pindex) -> Dict[int, List[Dict[str, Any]]]:
    all_files = {}
    total_size = 0
    printer = Printer(1)
    for root, _, files in os.walk(config.root):
        relative_path = os.path.relpath(root, config.root)
        for name in files:
            printer.print(
                f"Processed {human_readable(total_size)}   \r", end="")
            entry = {
                "name": name,
                "path": relative_path
            }
            try:
                size = os.path.getsize(os.path.join(root, name))
                total_size += size
                entry["size"] = size
                if size not in all_files.keys():
                    all_files[size] = []
                all_files[size].append(entry)
            except (FileNotFoundError, PermissionError):
                pass
    printer.print_last()
    print(f"\n{len(concat(all_files.values()))} "
          "file(s) have been indexed successfully")
    return all_files


def walk(config: Pindex):
    all_files = index(config)
    if config.find_duplicates:
        find_duplicates(config, all_files.copy())

    all_files = concat(all_files.values())

    with open(config.save, "w") as f:
        f.write(json.dumps({
            "root": config.root,
            "files": all_files
        }, indent=2))
