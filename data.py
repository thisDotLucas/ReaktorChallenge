from bs4 import BeautifulSoup
from requests import get
import re

data_map = {}
inverted_dependencies = {}


def main():
    soup = create_soup(
        'https://gist.githubusercontent.com/lauripiispanen/29735158335170c27297422a22b48caa/raw/61a0f1150f33a1f31510b8e3a70cbac970892b2f/status.real')
    data = soup.text
    data = data.split("\n\n")  # Always an empty line between packages.

    for i in range(0, len(data)):
        get_package_data(data[i])


def get_package_data(data):
    package_data_map = {}
    key1 = "Package: "
    key2 = "Depends: "
    key3 = "Description: "
    package = None
    dependencies = None
    description = None

    data_in_lines = data.split("\n")

    for i in range(0, len(data_in_lines)):
        if key1 in data_in_lines[i]:
            package = data_in_lines[i][len(key1):]  # We slice away "Package:" so we only store the name.
            break
        else:
            print("Invalid package")  # Package name is always on the first line, otherwise something is wrong.

    for j in range(i, len(data_in_lines)):
        if key2 in data_in_lines[j]:
            # re.sub(r'\([^()]*\)', '', string) removes parentheses => version numbers.
            line = re.sub(r' \([^()]*\)', '', data_in_lines[j][len(key2):])
            dependencies = line.split(", ")  # split dependencies into an array.
            map_inverted_dependencies(package, dependencies)  # Inverted dependencies are mapped in a
            break                                             # separate dictionary.

        elif key3 in data_in_lines[j]:  # If we reach description we can be certain there are no dependencies,
            break                       # since description is mandatory and is always located after dependencies.

    for k in range(j, len(data_in_lines)):
        if key3 in data_in_lines[k]:  # Description found.
            description = data_in_lines[k][len(key3):]
            for l in range(k + 1, len(data_in_lines)):  # Keep on going until description is over. If description
                if data_in_lines[l][0] == " ":          # continues on the next line it will start with a white spaces.
                    description = description + data_in_lines[l]
                else:
                    break

    # We map dependency and description values in our nested dictionary and put it
    # in the main dictionary with package name as key.
    package_data_map[key2[:-2]] = dependencies
    package_data_map[key3[:-2]] = description
    data_map[package] = package_data_map


# All the Y dependencies that package X was depending on gets package X appended to their list of inverted dependencies.
def map_inverted_dependencies(package, dependencies):
    for dependency in dependencies:
        if dependency in inverted_dependencies:  # If key already exists we just append all the dependencies.
            inverted_dependencies[dependency].append(package)
        else:  # If key does not exist we create one and append all dependencies.
            inverted_dependencies[dependency] = [package]


# I use BeautifulSoup to parse the Html.
def create_soup(url):
    page = get(url).text
    return BeautifulSoup(page, "html.parser")


def get_data():
    return data_map


def get_sorted_keys():
    return sorted(data_map.keys())


def get_inverted_dependencies():
    return inverted_dependencies


if __name__ == "__main__":
    main()