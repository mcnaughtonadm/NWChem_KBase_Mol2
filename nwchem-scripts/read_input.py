# -*- coding: utf-8 -*-
#BEGIN HEADER
import csv
import json
import logging
import os
from rdkit.Chem import AllChem, Descriptors
from installed_clients.DataFileUtilClient import DataFileUtil
import subprocess as _subprocess

#END_HEADER

def read_tsv(file_path, structure_field='structure',
             inchi_path='/kb/module/data/Inchikey_IDs.json', mol2_file_dir=None,
             callback_url=None):

    inchi_dict = json.load(open(inchi_path))
    cols_to_copy = {'name': str, 'deltag': float, 'deltagerr': float}
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    compounds = []
    w = csv.DictReader(open(file_path), dialect='excel-tab')
    for i, line in enumerate(w):
        user_id = line.get('id')
        mol2_source = line.get('mol2_source')
        handle_id = None
        if user_id and mol2_file_dir:
            if not mol2_source:
                raise ValueError('Please indicate mol2 file source in TSV file')
            mol2_file_path = None
            for root, dirs, files in os.walk(mol2_file_dir):
                for file in files:
                    if os.path.splitext(file)[0] == user_id:
                        logging.info('Found a matching mol2 file {} for compound {}'.format(str(file), user_id))
                        mol2_file_path = os.path.join(root, str(file))

            if mol2_file_path:
                dfu = DataFileUtil(callback_url)
                handle_id = dfu.file_to_shock({'file_path': mol2_file_path,
                                               'make_handle': True})['handle']['hid']
            else:
                logging.warning('Unable to find a matching mol2 file for compound: {}'.format(user_id))

        mol = None
        # Generate Mol object from InChI code if present
        if 'structure' in line:
            if "InChI=" in line['structure']:
                mol = AllChem.MolFromInchi(line['structure'])
            # Otherwise generate Mol object from SMILES string
            else:
                mol = AllChem.MolFromSmiles(line['structure'])
        elif 'smiles' in line:
            mol = AllChem.MolFromSmiles(line['smiles'])
        if not mol:
            logging.warning("Unable to Parse %s" % line[structure_field])
            continue
        comp = _make_compound_info(mol)

        if comp['inchikey'] in inchi_dict:
            comp['kb_id'] = inchi_dict[comp['inchikey']]
        else:
            comp['kb_id'] = '%s_%s' % (file_name, i + 1)

        if user_id:
            comp['id'] = user_id
        else:
            comp['id'] = comp['kb_id']

        for col in cols_to_copy:
            if col in line and line[col]:
                comp[col] = cols_to_copy[col](line[col])

        if handle_id:
            comp['mol2_handle_ref'] = handle_id
            comp['mol2_source'] = mol2_source

        compounds.append(comp)

    return compounds
