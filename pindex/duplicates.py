import os
import io
import hashlib
import concurrent.futures
from typing import List, Dict, Any

from pindex.core import Pindex
from pindex.util import Printer, concat, human_readable


def chunk_reader(fd: io.TextIOWrapper, chunk_size: int = 1024):
    while True:
        chunk = fd.read(1024)
        if not chunk:
            return
        yield chunk


def get_hash(fd: io.TextIOWrapper, hashf=hashlib.sha1):
    hash_obj = hashf()

    for chunk in chunk_reader(fd, 65536):
        hash_obj.update(chunk)
    hashed = hash_obj.hexdigest()

    return hashed


def calculate_hash(config: Pindex, e: Dict[str, Any]) -> Dict[str, Any]:
    filename = os.path.join(config.root, e.get("path"), e.get("name"))
    with open(filename, "rb") as fd:
        hashed = get_hash(fd)
        e["hash"] = hashed
    return e


def hash_same_size(config: Pindex, same_size: List[Dict[str, Any]]):
    total_size = 0
    total_length = len(same_size)
    for entry in same_size:
        total_size += entry.get("size")
    print(f"{human_readable(total_size)} "
          "of data will have to be calculated for their hashes")

    def calculate(e):
        return calculate_hash(config, e)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(calculate, e) for e in same_size]

        printer = Printer(1)
        for e in concurrent.futures.as_completed(results):
            total_length -= 1
            total_size -= e.get("size")
            printer.print(f"{total_length} file(s) / "
                          f"{human_readable(total_size)} left      \r", end="")
        printer.print_last()

    print("\nAll possible duplicates have been successfully hashed")


def find_duplicates(config: Pindex, files: Dict[int, List[Dict[str, Any]]]):
    if 0 in files.keys():
        del files[0]
    same_size = list(filter(lambda e: len(e) > 1, files.values()))
    print(f"{len(same_size)} set(s) "
          "of files have been found to have equal sizes")
    hash_same_size(config, concat(same_size))
    hashed_files = {}
    for entry in concat(files.values()):
        if "hash" in entry.keys():
            entry_hash = entry.get("hash")
            if entry_hash not in hashed_files.keys():
                hashed_files[entry_hash] = []
            hashed_files[entry_hash].append(entry)
    duplicates = list(hashed_files.values())
    for files in duplicates.copy():
        if len(files) == 1:
            del files[0]["hash"]
            duplicates.remove(files)
    print(f"{len(duplicates)} set(s) of files are the same")
    total_size = 0
    reduced = 0
    for files in duplicates:
        reduced += files[0].get("size")
        for entry in files:
            total_size += entry.get("size")
    print(f"Total {human_readable(total_size)} -> "
          f"Reduced {human_readable(reduced)}")
    print(f"{human_readable(total_size - reduced)} of storage can be saved")
