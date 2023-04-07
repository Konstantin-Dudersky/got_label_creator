#!/usr/bin/env python3

import csv
import sys
from typing import Final, NamedTuple
from pprint import pprint

STRUCTURE_FILE: Final[str] = "structure.csv"
EXPORT_FILE: Final[str] = "export.csv"


class Line(NamedTuple):
    label: str
    type_: str
    size: int


def process_line(line: Line, order: int, offset: int) -> tuple[list[str], int]:
    new_offset = offset + line.size
    line_str = [
        "",
        "{0}_{1}".format(line.label, order),
        line.type_,
        "D{0}".format(offset),
        *([""] * 16),
    ]
    return (line_str, new_offset)


def import_structure(filename: str) -> tuple[Line, ...]:
    rows: list[Line] = []
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if not len(row):
                continue
            rows.append(Line(label=row[0], type_=row[1], size=int(row[2])))
    return tuple(rows)


def export(structure: tuple[Line, ...], num: int, start_offset: int) -> None:
    with open(EXPORT_FILE, "w", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(["4", "AI_", *([""] * 18)])
        writer.writerow([*([""] * 20)])
        writer.writerow([*([""] * 20)])
        writer.writerow(
            [
                "",
                "Label Name",
                "Data Type",
                "Assign (Device)",
                "Comment",
                "Comment2",
                "Comment3",
                "Comment4",
                "Comment5",
                "Comment6",
                "Comment7",
                "Comment8",
                "Comment9",
                "Comment10",
                "Comment11",
                "Comment12",
                "Comment13",
                "Comment14",
                "Comment15",
                "Comment16",
            ]
        )
        new_offset = start_offset
        for i in range(num):
            for label in structure:
                line_str, new_offset = process_line(label, i, new_offset)
                writer.writerow(line_str)


if __name__ == "__main__":
    channels_amount = int(sys.argv[1])
    start_offset = int(sys.argv[2])
    print("Кол-во каналов:", channels_amount)
    print()
    print("Начальное смещение:", start_offset)
    print()
    structure = import_structure(STRUCTURE_FILE)
    print("Структура:")
    pprint(structure)
    export(structure, channels_amount, start_offset)
    print("\nФайл {0} создан, нажми Enter для выхода".format(EXPORT_FILE))
    wait = input()
