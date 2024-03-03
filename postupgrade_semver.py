#!/usr/bin/env python3

from pathlib import Path
from re import match
from shutil import copy
from tempfile import NamedTemporaryFile
from typing import List


def get_last_changelog(file: Path) -> List[str]:
    latest_changelog: List[str] = []
    with open(file) as textfile:
        for line in textfile:
            if line in ["\n", "\r\n"]:
                break
            latest_changelog.append(line.rstrip())

    return latest_changelog


def get_semver(changelog: List[str]) -> str:
    if match(r"#\d+\.\d+\.\d+", changelog[0]):
        return changelog[0][1:]
    return ""


def has_been_released(changelog: List[str]) -> bool:
    for line in changelog:
        if match(r"^([Rr]elease|[Hh]otfix)", line):
            return True
    return False


def contains_change(changelog: List[str], description: str) -> bool:
    for line in changelog:
        if line in description:
            return True
    return False


def increase_minor_version(version: str) -> str:
    major, minor, _ = version.split(".")
    new_minor: int = int(minor) + 1
    new_patch: int = 0

    return f"{major}.{new_minor}.{new_patch}"


def prepend_new_semver(semver_file: Path, version: str, description: str) -> None:
    new_semver: str = increase_minor_version(version)

    with NamedTemporaryFile("w", delete=False) as tmp:
        tmp.write(f"#{new_semver}\n")
        tmp.write(f"{description}\n\n")
        with open(semver_file, "r") as file:
            for line in file:
                tmp.write(line)

    copy(tmp.name, file.name)


def insert_semver_description(semver_file: Path, semver_description: str) -> None:
    with NamedTemporaryFile("w", delete=False) as tmp:
        with open(semver_file, "r") as file:
            tmp.write(file.readline())
            tmp.write(f"{semver_description}\n")
            for line in file:
                tmp.write(line)

    copy(tmp.name, semver_file.name)


def main() -> None:
    semver_file: Path = Path("semver.txt")
    semver_description: str = "Renovate: update dependencies"

    last_changelog: List[str] = get_last_changelog(semver_file)

    if not last_changelog:
        return

    version: str = get_semver(last_changelog)

    if not version:
        return

    if has_been_released(last_changelog):
        prepend_new_semver(semver_file, version, semver_description)
        return

    if not contains_change(last_changelog, semver_description):
        insert_semver_description(semver_file, semver_description)


if __name__ == "__main__":
    main()
