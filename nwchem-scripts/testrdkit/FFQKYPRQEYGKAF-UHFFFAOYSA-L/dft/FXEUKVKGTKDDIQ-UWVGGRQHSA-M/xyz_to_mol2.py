import os
import openbabel
from openbabel import *

xyz_all = [i for i in os.listdir('./') if i.endswith('.xyz')]

print(xyz_all)

for i in xyz_all:
        ii = open(i, 'r')
        ii.readline()
        inchikey = ii.readline().split('\t')[0]
        print(inchikey)
        os.system('cp %s %s' %(i, inchikey+'.xyz'))
        os.system('babel -i xyz %s  -o mol2 %s' %(i, inchikey+'.mol2')
