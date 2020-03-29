# Python scripts for AutoDock Vina

- Install autodock vina and MGLTools (http://vina.scripps.edu/manual.html#linux)
- Download PDB receptor file and store in data/receptors
- Write configuration file for Vina as in http://vina.scripps.edu/manual.html#config , starting with 
    receptor = tmp/receptor.pdbqt
    ligand = tmp/ligand.pdbqt

### Docking from SMILES in .txt file 

If molecules have their SMILES written in myligands.txt , run : 
```
python dock_txt.py -t [pdb_target_prefix] -i [myligands.txt] -o [my_csv_output.csv]
```

### Docking SMILES from csv file : 

SMILES stored in a csv file with header row, SMILES in 'can' column. Run : 
```
python dock_df.py -t [pdb_target_prefix] -df [myligands.csv] -o [my_csv_output.csv]
```






