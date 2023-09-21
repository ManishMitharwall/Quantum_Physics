#!/auto/vestec1-elixir/home/manishkumar/.conda/envs/kpython310/bin/python3.1
import numpy as np
import re
import sys

atomic_number = {
    'H' : 1,'He' : 2, 'Li' : 3, 'Be' : 4,
    'B' : 5, 'C' : 6, 'N' : 7, 'O' : 8,
    'F' : 9, 'Ne' : 10, 'Na' : 11, 'Mg' : 12,
    'Al' : 13, 'Si' : 14, 'P' : 15, 'S' : 16,
    'Cl' : 17, 'Ar' : 18, 'K' : 19, 'Ca' : 20,
    'Sc' : 21, 'Ti' : 22, 'V' : 23, 'Cr' : 24,
    'Mn' : 25, 'Fe' : 26, 'Co' : 27, 'Ni' : 28,
    'Cu' : 29, 'Zn' : 30, 'Ga' : 31, 'Ge' : 32,
    'As' : 33, 'Se' : 34, 'Br' : 35, 'Kr' : 36,
    'Rb' : 37, 'Sr' : 38, 'Y' : 39, 'Zr' : 40,
    'Nb' : 41, 'Mo' : 42, 'Tc' : 43, 'Ru' : 44,
    'Rh' : 45, 'Pd' : 46, 'Ag' : 47, 'Cd' : 48,
    'In' : 49, 'Sn' : 50, 'Sb' : 51, 'Te' : 52,
    'I' : 53, 'Xe' : 54, 'Cs' : 55, 'Ba' : 56,
    'La' : 57, 'Ce' : 58, 'Pr' : 59, 'Nd' : 60,
    'Pm' : 61, 'Sm' : 62, 'Eu' : 63, 'Gd' : 64,
    'Tb' : 65, 'Dy': 66, 'Ho' : 67, 'Er' : 68,
    'Tm' : 69, 'Yb' : 70, 'Lu' : 71, 'Hf' : 72,
    'Ta' : 73, 'W' : 74, 'Re' : 75, 'Os' : 76,
    'Ir' : 77, 'Pt' : 78, 'Au' : 79, 'Hg' : 80,
    'Tl' : 81, 'Pb' : 82, 'Bi' : 83, 'Po' : 84,
    'At' : 85, 'Rn' : 86, 'Fr' : 87, 'Ra' : 88,
    'Ac' : 89, 'Th' : 90, 'Pa' : 91, 'U' : 92,
    'Np' : 93, 'Pu' : 94, 'Am' : 95, 'Cm' : 96
}

def aims(file):
    n_atom = []
    for line in file:
        if re.search("atom",line):
            aux = line.split()
            n_atom.append(aux[-1])
    return(n_atom)


with open(sys.argv[1],'r') as file:
    no_of_el=0
    atom=aims(file)
    for i in range(len(atom)):
        no_of_el += atomic_number[atom[i]]
    s= no_of_el%2
    if s==0:
        homo=int(no_of_el/2)
    else:
        homo=int((no_of_el+1)/2)
    print(homo)
