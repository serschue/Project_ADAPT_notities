#!/bin/bash

set -euo pipefail

WORKBENCH="/home/sarah/Documents/Project_Ugent/workbench"
PDB2FASTA="/home/sarah/Documents/Project_Ugent/pdb2fasta/pdb2fasta.sh"

cd "$WORKBENCH"

# Loop over all task directories
for task_dir in */; do

    backbone_dir="${task_dir}backbone"

    # Skip if backbone directory does not exist
    if [[ ! -d "$backbone_dir" ]]; then
        continue
    fi

    echo "Processing: $backbone_dir"

    # Loop over all PDB files
    for pdb_file in "$backbone_dir"/*.pdb; do

        # Skip if no PDB files exist
        [[ -f "$pdb_file" ]] || continue

        # Replace .pdb extension with .fasta
        fasta_file="${pdb_file%.pdb}.fasta"

        # Convert PDB to FASTA
        bash "$PDB2FASTA" "$pdb_file" > "$fasta_file"

        echo "Created: $fasta_file"

    done
done

echo "All conversions completed!"
