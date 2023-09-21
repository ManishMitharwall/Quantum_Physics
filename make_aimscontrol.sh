#!/usr/bin/bash
name=name
functional=pbe0
relex_geom=1
PBC=0
relex_cell=0
spin_polarized=1
charge=0
plotcube=1
plotDOS=0
plot_APDOS=0
geometry=geometry.in
k_grid="1 1 1"
DOS_Kgrid="5 5 5"
scf_type=1

#    NOW Every-thing Done


if [ $spin_polarized -eq 1 ]
then
    Spin=collinear
else
    Spin=none
fi


cat << EOF > control.in
## Physical model

  xc                $functional
#  hybrid_xc_coeff   0.4
  vdw_correction_hirshfeld
  spin               $Spin
  relativistic atomic_zora scalar
  charge             $charge
EOF

if [ $PBC -eq 1 ]
then
    echo -e "  k_grid ${k_grid}
  exx_band_structure_version 1 \n" >> control.in
fi

if [ $scf_type -eq 1 ]
then
    echo -e "#  SCF convergence
#
  occupation_type    gaussian 0.05
  mixer              pulay
    n_max_pulay        7
    charge_mix_param   0.25
  sc_accuracy_rho    1E-4
  sc_accuracy_eev    1E-3
  sc_accuracy_etot   1E-6
  sc_accuracy_forces 1E-4 \n" >> control.in
else
    echo -e "#  SCF convergence
#
  adjust_scf always 2 \n" >> control.in
fi


echo -e "#  Relaxation \n#" >> control.in

if [ $relex_geom -eq 1 ]
then
    echo -e "relax_geometry  bfgs 5.e-3
RI_method       lvl_fast \n" >> control.in
fi

if [ $relex_cell -eq 1 ]
then
    echo -e "relax_unit_cell  full #fixed_angles \n" >> control.in
fi

echo -e "## Outputs: #" >> control.in

#if [ $relex_cell -eq 1 ]
#then
#    echo -e "output mulliken \n" >> control.in
#fi
#echo -e "output mulliken \n" >> control.in


if [ $plotcube -eq 1 ]
then
    echo -e "output cube total_density" >> control.in 
    echo -e "output cube hartree_potential" >> control.in
    homo_index=$(homo_index.sh )
    let low=homo_index-3
    let hig=homo_index+3
    if [ $spin_polarized -eq 1 ]
    then
        echo -e "output cube spin_density\n" >> control.in
    fi

    for ((i=$low; i <= $hig; i++))
    do 
        echo -e "output cube eigenstate ${i}" >> control.in
    done
    if [ $spin_polarized -eq 1 ]
    then
        for ((i=$low; i <= $hig; i++))
        do 
            echo -e "output cube eigenstate ${i}\n cube spinstate 2" >> control.in

        done
    fi
fi

if [ $plotDOS -eq 1 ]
then
    echo -e "\noutput dos -16.0 4.0 401 0.05" >> control.in
    if [ $PBC -eq 1 ]
    then
        echo -e "dos_kgrid_factors $DOS_Kgrid \n" >> control.in
    fi
    echo -e "output species_proj_dos -16.0 4.0 401 0.05 " >> control.in
    if [ $PBC -eq 1 ]
    then
        echo -e "dos_kgrid_factors $DOS_Kgrid \n" >> control.in
    fi
fi

if [ $plot_APDOS -eq 1 ]
then
    echo -e "output atom_proj_dos -16.0 4.0 401 0.05 \n" >> control.in
fi

kk=$(grep -n "atom" geometry.in | awk '{ print $NF }' | awk '{for (i=1;i<=NF;i++) if (!a[$i]++) printf("%s%s",$i,FS)}{printf("\n")}')

for spec in $kk; do
    file=$(ls /storage/praha1/home/manishkumar/mybin/opt/codes/FHI-AIMS/fhi-aims.221103/species_defaults/defaults_2020/light | grep "_${spec}_" )
    cat /storage/praha1/home/manishkumar/mybin/opt/codes/FHI-AIMS/fhi-aims.221103/species_defaults/defaults_2020/light/$file >> control.in

done



cat << EOF > runaims.sh
#!/bin/bash
#PBS -l select=1:ncpus=16:mem=100gb:scratch_local=50gb
#PBS -l walltime=240:00:00
#PBS -q luna
#PBS -r n
#PBS -j oe
#PBS -N $name
module add intel-parallel-studio/intel-parallel-studio-cluster.2019.4-intel-19.0.4-iifs5gt
module add openmpi/openmpi-4.0.4-intel-19.0.4-gpu-xri6uan
ulimit -s unlimited
export OMP_NUM_THREADS=1

cd  \${PBS_O_WORKDIR}

AIMS_PATH=/storage/praha1/home/ondracek/fhi-aims.200112/bin/
AIMS=\$AIMS_PATH/aims.200112.scalapack.mpi.x
mpirun \$AIMS --mca opal_warn_on_missing_libcuda 0 > out_orbs 2> err_orbs

EOF


