import os
import openbabel
from openbabel import *

xyz_all = [i for i in os.listdir('./') if i.endswith('.xyz')]


for i in xyz_all:
        ii = open(i, 'r')
        ii.readline()
        inchikey = ii.readline().split('\t')[0]
        os.system('babel -i xyz %s  -o mol2 %s' %(i, inchikey.rstrip()+'_prop.mol2'))
