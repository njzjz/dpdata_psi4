import numpy as np
from dpdata.format import Format
from dpdata.unit import LengthConversion, EnergyConversion, ForceConversion

from .read_psi4 import read_psi4


length_convert = LengthConversion("bohr", "angstrom").value()
energy_convert = EnergyConversion("hartree", "eV").value()
force_convert = ForceConversion("hartree/bohr", "eV/angstrom").value()


@Format.register("psi4")
class PSI4Format(Format):
    def from_labeled_system(self, file_name, **kwargs):
        symbols, coord, energy, forces = read_psi4(file_name)

        atom_names, atom_types, atom_numbs = np.unique(symbols, return_inverse=True, return_counts=True)
        natoms = coord.shape[0]

        return {
            "atom_types": atom_types,
            "atom_names": list(atom_names),
            "atom_numbs": list(atom_numbs),
            "coords": (coord * length_convert).reshape((1, natoms, 3)),
            "energies": np.array([energy * energy_convert]),
            "forces": (forces * force_convert).reshape((1, natoms, 3)),
            "cells": np.zeros((1, 3, 3)),
            "orig": np.zeros(3),
            "nopbc": True,
        }
