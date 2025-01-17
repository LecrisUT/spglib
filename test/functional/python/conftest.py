"""Pytest configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import numpy as np
import pytest

_dirnames = (
    "cubic",
    "hexagonal",
    "monoclinic",
    "orthorhombic",
    "tetragonal",
    "triclinic",
    "trigonal",
    "distorted",
    "virtual_structure",
)


@pytest.fixture(scope="session")
def root_data_dir() -> Path:
    _data_dir = Path(__file__).parent.absolute() / "data"
    return _data_dir


@pytest.fixture(scope="session")
def dirnames(root_data_dir) -> list[Path]:
    """Return test directory names."""
    return [root_data_dir / d for d in _dirnames]


@pytest.fixture(scope="session")
def all_filenames(root_data_dir) -> list[Path]:
    """Return all filenames in test directories."""
    all_filenames = []
    for d in (root_data_dir / _d for _d in _dirnames):
        all_filenames += [d / fname for fname in d.iterdir()]
    return all_filenames


@pytest.fixture(scope="session")
def read_vasp() -> Callable:
    """Return function to read POSCAR."""

    def _read_vasp(filename):
        with open(filename) as f:
            lines = f.readlines()
            return _get_cell(lines)

    return _read_vasp


# def read_vasp_from_strings(strings):
#     return _get_cell(StringIO(strings).readlines())


def _get_cell(lines):
    line1 = [x for x in lines[0].split()]
    if _is_exist_symbols(line1):
        symbols = line1
    else:
        symbols = None

    scale = float(lines[1])

    lattice = []
    for i in range(2, 5):
        lattice.append([float(x) for x in lines[i].split()[:3]])
    lattice = np.array(lattice) * scale

    try:
        num_atoms = np.array([int(x) for x in lines[5].split()])
        line_at = 6
    except ValueError:
        symbols = [x for x in lines[5].split()]
        num_atoms = np.array([int(x) for x in lines[6].split()])
        line_at = 7

    numbers = _expand_symbols(num_atoms, symbols)

    if lines[line_at][0].lower() == "s":
        line_at += 1

    is_cartesian = False
    if lines[line_at][0].lower() == "c" or lines[line_at][0].lower() == "k":
        is_cartesian = True

    line_at += 1

    positions = []
    for i in range(line_at, line_at + num_atoms.sum()):
        positions.append([float(x) for x in lines[i].split()[:3]])

    if is_cartesian:
        positions = np.dot(positions, np.linalg.inv(lattice))

    return (lattice, positions, numbers)


def _expand_symbols(num_atoms, symbols=None):
    expanded_symbols = []
    is_symbols = True
    if symbols is None:
        is_symbols = False
    else:
        if len(symbols) != len(num_atoms):
            is_symbols = False
        else:
            for s in symbols:
                if s not in symbol_map:
                    is_symbols = False
                    break

    if is_symbols:
        for s, num in zip(symbols, num_atoms):
            expanded_symbols += [
                symbol_map[s],
            ] * num
    else:
        for i, num in enumerate(num_atoms):
            expanded_symbols += [
                i + 1,
            ] * num

    return expanded_symbols


def _is_exist_symbols(symbols):
    for s in symbols:
        if s not in symbol_map:
            return False
    return True


symbol_map = {
    "H": 1,
    "He": 2,
    "Li": 3,
    "Be": 4,
    "B": 5,
    "C": 6,
    "N": 7,
    "O": 8,
    "F": 9,
    "Ne": 10,
    "Na": 11,
    "Mg": 12,
    "Al": 13,
    "Si": 14,
    "P": 15,
    "S": 16,
    "Cl": 17,
    "Ar": 18,
    "K": 19,
    "Ca": 20,
    "Sc": 21,
    "Ti": 22,
    "V": 23,
    "Cr": 24,
    "Mn": 25,
    "Fe": 26,
    "Co": 27,
    "Ni": 28,
    "Cu": 29,
    "Zn": 30,
    "Ga": 31,
    "Ge": 32,
    "As": 33,
    "Se": 34,
    "Br": 35,
    "Kr": 36,
    "Rb": 37,
    "Sr": 38,
    "Y": 39,
    "Zr": 40,
    "Nb": 41,
    "Mo": 42,
    "Tc": 43,
    "Ru": 44,
    "Rh": 45,
    "Pd": 46,
    "Ag": 47,
    "Cd": 48,
    "In": 49,
    "Sn": 50,
    "Sb": 51,
    "Te": 52,
    "I": 53,
    "Xe": 54,
    "Cs": 55,
    "Ba": 56,
    "La": 57,
    "Ce": 58,
    "Pr": 59,
    "Nd": 60,
    "Pm": 61,
    "Sm": 62,
    "Eu": 63,
    "Gd": 64,
    "Tb": 65,
    "Dy": 66,
    "Ho": 67,
    "Er": 68,
    "Tm": 69,
    "Yb": 70,
    "Lu": 71,
    "Hf": 72,
    "Ta": 73,
    "W": 74,
    "Re": 75,
    "Os": 76,
    "Ir": 77,
    "Pt": 78,
    "Au": 79,
    "Hg": 80,
    "Tl": 81,
    "Pb": 82,
    "Bi": 83,
    "Po": 84,
    "At": 85,
    "Rn": 86,
    "Fr": 87,
    "Ra": 88,
    "Ac": 89,
    "Th": 90,
    "Pa": 91,
    "U": 92,
    "Np": 93,
    "Pu": 94,
    "Am": 95,
    "Cm": 96,
    "Bk": 97,
    "Cf": 98,
    "Es": 99,
    "Fm": 100,
    "Md": 101,
    "No": 102,
    "Lr": 103,
    "Rf": 104,
    "Db": 105,
    "Sg": 106,
    "Bh": 107,
    "Hs": 108,
    "Mt": 109,
    "Ds": 110,
    "Rg": 111,
    "Cn": 112,
    "Nh": 113,
    "Fl": 114,
    "Mc": 115,
    "Lv": 116,
    "Ts": 117,
    "Og": 118,
}
