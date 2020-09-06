import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from setuptools import find_packages, setup


def get_extra_requires(extras_location):
    with open(extras_location) as extras_file:
        extra_deps = defaultdict(set)
        for line in map(str.strip, extras_file):
            if line and not line.startswith("#"):
                package_tags = set()
                if ":" in line:
                    dependency, tags_list = line.split(":")
                    package_tags.update(tag.strip() for tag in tags_list.split(","))
                    package_tags.add(re.split("[<=>]", dependency)[0])
                    for tag in package_tags:
                        extra_deps[tag].add(dependency)

        extra_deps["all"] = {
            dependency
            for dependencies_set in extra_deps.values()
            for dependency in dependencies_set
        }

    return extra_deps


PACKAGE_NAME = "helloworld"
SUMMARY = "Template python project"
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
]
AUTHOR = "Mtrqq"
COPYRIGHT = "Copyright 2020 {0}".format(AUTHOR)


HERE: Path = Path(__file__).parent
README: str = Path(HERE, "README.md").read_text(encoding="utf-8")
VERSION: str = Path(HERE, "VERSION").read_text()
REQUIREMENTS: List[str] = Path(HERE, "requirements.txt").read_text().splitlines()
EXTRA_REQUIREMENTS: Dict[str, List[str]] = get_extra_requires(HERE / "extras.txt")


if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        author=AUTHOR,
        description=SUMMARY,
        classifiers=CLASSIFIERS,
        version=VERSION,
        long_description=README,
        long_description_content_type="text/markdown",
        packages=find_packages(exclude="tests.*"),
        install_requires=REQUIREMENTS,
        extras_require=EXTRA_REQUIREMENTS,
    )
