import os

xyz_all  = [i for i in os.listdir('./') if i.endswith('.xyz')]

for xyz in xyz_all:
        key  = xyz.split('.')[0]
        mol2 = str(key) + '.mol2'

        xyzfile = open(xyz, 'r')
        mol2file = open(mol2, 'r')

        num_lines = sum(1 for line in open(mol2))

        natoms = xyzfile.readline().rstrip()
        xyzfile.readline()

        popn =  []
        for i in range(int(natoms)):
                xyz = xyzfile.readline().rstrip()
                popn.append(xyz.split('\t')[4])


        mol2_updated = key +'-Mulliken.mol2'
        ff = open(mol2_updated, 'w+')


        for i in range(7):
                abc = mol2file.readline()
                print(abc.rstrip())
                ff.write(abc)
        for i in range(7, 7+int(natoms)):
                geometry = mol2file.readline().rstrip()
                print(str((' '.join(geometry.split(' ')[:-1])) + popn[i-7]))
                ff.write(str((' '.join(geometry.split(' ')[:-1])) + popn[i-7] + '\n'))

        for i in range(7+int(natoms), int(num_lines)):
                cde = mol2file.readline()
                print(cde.rstrip())
                ff.write(cde)

        ff.close()
