import os

xyz_all  = [i for i in os.listdir('./') if i.endswith('_prop.xyz')]

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
		xy = xyz.strip().split('\t')#[4])
		abc = [x for x in xy if x]
		popn.append(abc[4])


	mol2_key = key.split('_')[0]
	mol2_updated = mol2_key +'_Mulliken.mol2' 
	ff = open(mol2_updated, 'w+')


	for i in range(7):
		abc = mol2file.readline()
		ff.write(abc)
	for i in range(7, 7+int(natoms)):
		geometry = mol2file.readline().rstrip()
		ff.write(str((' '.join(geometry.split(' ')[:-1])) + popn[i-7] + '\n'))

	for i in range(7+int(natoms), int(num_lines)):
		cde = mol2file.readline()
		ff.write(cde)

	ff.close()
