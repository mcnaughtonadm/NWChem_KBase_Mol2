#!/bin/csh -f
#SBATCH -N 1
#SBATCH --ntasks-per-node 4
#SBATCH -t 1:00:00
#SBATCH -A emslc51198
#SBATCH -o ./FFQKYPRQEYGKAF-UHFFFAOYSA-L.out.%j
#SBATCH -e ./FFQKYPRQEYGKAF-UHFFFAOYSA-L.err.%j
#SBATCH -J FFQKYPRQEYGKAF-UHFFFAOYSA-L
#SBATCH --export ALL
##SBATCH --mail-type=FAIL,END
##SBATCH --mail-user rajendra.joshi@emsl.pnl.gov

############################################################################
# Print out some information for refund purposes
############################################################################

echo "refund: UserID = thom510"
echo "refund: SLURM Job ID = ${SLURM_JOBID}"
echo "refund: Number of nodes          = 1"
echo "refund: Number of cores per node = 1"
echo "refund: Number of cores          = 1"
echo "refund: Amount of time requested = 0:30"
echo "refund: Directory = ${PWD}"
echo " "
echo Processor list
echo " "
echo "${SLURM_JOB_NODELIST}"
echo " "

# Actually run the job
source /etc/profile.d/modules.csh
module purge
#module load nwchem/6.3
# module load intel/14.0.3
# module load micsetup
# module load impi
# module load intel/ips_17_u4
# module load impi/5.1.2.150
module load nwchem/6.8.1_rhel7

cd /scratch

setenv ARMCI_DEFAULT_SHMMAX 131072
#this disables xeon phi offload
setenv NWC_RANKS_PER_DEVICE 0
setenv OMP_NUM_THREADS 1
setenv MKL_NUM_THREADS 1
setenv NWC_RANKS_PER_DEVICE 0
setenv ARMCI_OPENIB_DEVICE mlx4_0
setenv OFFLOAD_INIT on_offload


setenv MPIRETURN 999
srun --mpi=pmi2 -n $SLURM_NPROCS -K1    /dtemp/scicons/bin/nwchem6.8.1_rhel7 /dtemp/emslc51198/Comp_chem_dG/Joshi/resources_for_all/testrdkit/FFQKYPRQEYGKAF-UHFFFAOYSA-L/dft/FFQKYPRQEYGKAF-UHFFFAOYSA-L.nw
setenv MPIRETURN $?

############################################################################
# End of the job script
############################################################################

exit $MPIRETURN
