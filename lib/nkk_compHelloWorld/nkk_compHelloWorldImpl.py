# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import sys
import subprocess as _subprocess
import csv
from pybel import *
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from csv import DictReader
from installed_clients.KBaseReportClient import KBaseReport

#END_HEADER


class nkk_compHelloWorld:
    '''
    Module Name:
    nkk_compHelloWorld

    Module Description:
    A KBase module: nkk_compHelloWorld
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_nkk_compHelloWorld(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_nkk_compHelloWorld
        sim_dir = '~/../simulation'
        os.system('ls')
        import pandas as pd
        print('input:',params['Input_File'])
        
        # Reads InChI and InChI-key from .csv file
        #with open(params['Input_File']) as f:
             #InChI_key = [row["InChI-Key"].split('InChIKey=')[1] for row in DictReader(f)]
             #InChI_key = [row["id"] for row in DictReader(f)] 
        df = pd.read_csv(params['Input_File'], sep ='\t')
        print(df)
        InChI_key = df['id']
        InChIes = df['structure']
        print(InChI_key)
        print(InChIes)
            #print('InChI_key:',InChI_key)
        
#        with open(params['Input_File']) as f:
#             InChIes   = [row["structure"] for row in DictReader(f)]
             #print('InChIes: ',InChIes)

        import inchi_to_submission as its
        import extract_properties_mulliken_charges_mol2 as mul
       
        its.inchi_to_dft(InChI_key,InChIes)

        #cwd = os.getcwd()
        #print('Main:',cwd)
        length = len(InChI_key)
        #print('Before get NumAtoms')
        for i in range(length):
            os.chdir('./'+InChI_key[i]+'/dft')
            file1 = open('nwchem.out', 'r')
            #print('File1: ',file1)
            nAtoms = mul.getNumberOfAtoms(file1)
            #print(nAtoms)
            energy = mul.getInternalEnergy0K(file1)
            #print('Energy:',energy)
            charge =mul.getMullikenCharge(file1,nAtoms)
            #print('Charge:',charge)
            file1.close()
           
        
            mul.nAtoms = nAtoms
            mul.E0K = energy

            mul.calculate(InChI_key[i])


        for j in range(length):
            cwd = os.getcwd()
            print('Current Dir:',cwd)
            os.chdir('./'+InChI_key[j]+'/dft')
            os.system('ls')
            with open(InChI_key[j]+'_Mulliken.mol2') as IN:
                with open('../../Total_Output.txt','a') as out:
                    for line in IN:
                        out.write(line)
            os.chdir('../..')


        os.system('ls')
        os.system('more Total_Output.txt')
        
#        print('InChI_key before calc:',InChI_key)
#        mul.calculate(InChI_key[0])
        
        
        report = KBaseReport(self.callback_url)
        report_info = report.create({'report':{'objects_created':[],
                                               'text_message': params['Input_File'],
                                               'text_message':params['calculation_type']},
                                               'workspace_name': params['workspace_name']})
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }

        
        return [output]
        
        #END run_nkk_compHelloWorld

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_nkk_compHelloWorld return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
