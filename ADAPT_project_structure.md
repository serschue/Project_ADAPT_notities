# ADAPT 

This file contains the information of the ADAPT project file structure.

**adapt-boltzgen:** the BoltzGen code adapted by Johannes such that it is compatible with the other implementations made in 

- **boltzgen:** cloned BoltzGen repository from Hannes Stark
- **boltzgen_adapt:** boltzGen code adapted by Johannes such that it is compatible with the adapted code in scr
- **scr/adapt_boltzgen:** boltzgen_adapted code model_design contains the code for the sampler (extra experimentele modellen bovenop boltzgen_adapt)!! Ook de mymodel_guidance.py zit hier in 

**adapt-build:** code to build data and test sets from publicly available data

**Important:** each time you start your job on the server set PATH correctly such that it finds python: 

```
export PATH=/opt/conda/bin:$PATH
hash -r
cd /project_ghent/ADAPT/adapt-boltzgen/scripts
bash install-cu13.sh

```

**To generate samples** 

```
cd /project_ghent/ADAPT/adapt-workbench

./run.sh --mode backbone
```

**Register Jupyter kernel**

```
/opt/conda/bin/python -m pip install ipykernel
/opt/conda/bin/python -m ipykernel install \
    --user \
    --name adapt-boltzgen \
    --display-name "Python (ADAPT BoltzGen)"
    
jupyter kernelspec list

```

`Ctrl + Shift + P` → `Developer: Reload Window`



Structuur van de dataset die gebruikt wordt om op te voorspellen. 

/project_ghent/ADAPT/adapt-workbench/data/rabd_v2_old/dataset.jsonl

{"**version**": "v2", "**pdb_id**": "5b8c", "**structure**": [{"chain_id": "B", "group": 1}, {"chain_id": "A", "group": 2}, {"chain_id": "C", "group": 3}], "**design**": **[{"******chain_id": "B"**,** "residues": [{"res_num": 26, "res_name": "GLY"}, {"res_num": 27, "res_name": "TYR"}, {"res_num": 28, "res_name": "THR"}, {"res_num": 29, "res_name": "PHE"}, {"res_num": 30, "res_name": "THR"}, {"res_num": 31, "res_name": "ASN"}, {"res_num": 32, "res_name": "TYR"}, {"res_num": 52, "res_name": "ASN"}, {"res_num": 53, "res_name": "PRO"}, {"res_num": 54, "res_name": "SER"}, {"res_num": 55, "res_name": "ASN"}, {"res_num": 56, "res_name": "GLY"}, {"res_num": 57, "res_name": "GLY"}, {"res_num": 99, "res_name": "ARG"}, {"res_num": 100, "res_name": "ASP"}, {"res_num": 101, "res_name": "TYR"}, {"res_num": 102, "res_name": "ARG"}, {"res_num": 103, "res_name": "PHE"}, {"res_num": 104, "res_name": "ASP"}, {"res_num": 105, "res_name": "MET"}, {"res_num": 106, "res_name": "GLY"}, {"res_num": 107, "res_name": "PHE"}, {"res_num": 108, "res_name": "ASP"}, {"res_num": 109, "res_name": "TYR"}]}, {**"chain_id": "A"**, "residues": [{"res_num": 24, "res_name": "ARG"}, {"res_num": 25, "res_name": "ALA"}, {"res_num": 26, "res_name": "SER"}, {"res_num": 27, "res_name": "LYS"}, {"res_num": 28, "res_name": "GLY"}, {"res_num": 29, "res_name": "VAL"}, {"res_num": 30, "res_name": "SER"}, {"res_num": 31, "res_name": "THR"}, {"res_num": 32, "res_name": "SER"}, {"res_num": 33, "res_name": "GLY"}, {"res_num": 34, "res_name": "TYR"}, {"res_num": 35, "res_name": "SER"}, {"res_num": 36, "res_name": "TYR"}, {"res_num": 37, "res_name": "LEU"}, {"res_num": 38, "res_name": "HIS"}, {"res_num": 54, "res_name": "LEU"}, {"res_num": 55, "res_name": "ALA"}, {"res_num": 56, "res_name": "SER"}, {"res_num": 57, "res_name": "TYR"}, {"res_num": 58, "res_name": "LEU"}, {"res_num": 59, "res_name": "GLU"}, {"res_num": 60, "res_name": "SER"}, {"res_num": 93, "res_name": "GLN"}, {"res_num": 94, "res_name": "HIS"}, {"res_num": 95, "res_name": "SER"}, {"res_num": 96, "res_name": "ARG"}, {"res_num": 97, "res_name": "ASP"}, {"res_num": 98, "res_name": "LEU"}, {"res_num": 99, "res_name": "PRO"}, {"res_num": 100, "res_name": "LEU"}, {"res_num": 101, "res_name": "THR"}**]}]**, "**hotspot**": [{"binder_id": "B", "target_id": "C", "res_pos": 60, "res_name": "GLY", "res_num": 61, "distance": 3.9632545969190534}], "**evaluation**": {"binder_ids": ["B", "A"], "target_ids": ["C"]}, "**domains**": [{"**chain_id": "B"**, "domain_type": "H", "**cdr1**": [{"res_num": 26, "res_name": "GLY"}, {"res_num": 27, "res_name": "TYR"}, {"res_num": 28, "res_name": "THR"}, {"res_num": 29, "res_name": "PHE"}, {"res_num": 30, "res_name": "THR"}, {"res_num": 31, "res_name": "ASN"}, {"res_num": 32, "res_name": "TYR"}], "**cdr2**": [{"res_num": 52, "res_name": "ASN"}, {"res_num": 53, "res_name": "PRO"}, {"res_num": 54, "res_name": "SER"}, {"res_num": 55, "res_name": "ASN"}, {"res_num": 56, "res_name": "GLY"}, {"res_num": 57, "res_name": "GLY"}], "**cdr3**": [{"res_num": 99, "res_name": "ARG"}, {"res_num": 100, "res_name": "ASP"}, {"res_num": 101, "res_name": "TYR"}, {"res_num": 102, "res_name": "ARG"}, {"res_num": 103, "res_name": "PHE"}, {"res_num": 104, "res_name": "ASP"}, {"res_num": 105, "res_name": "MET"}, {"res_num": 106, "res_name": "GLY"}, {"res_num": 107, "res_name": "PHE"}, {"res_num": 108, "res_name": "ASP"}, {"res_num": 109, "res_name": "TYR"}]}, {**"chain_id": "A"**, "domain_type": "K", "**cdr1**": [{"res_num": 24, "res_name": "ARG"}, {"res_num": 25, "res_name": "ALA"}, {"res_num": 26, "res_name": "SER"}, {"res_num": 27, "res_name": "LYS"}, {"res_num": 28, "res_name": "GLY"}, {"res_num": 29, "res_name": "VAL"}, {"res_num": 30, "res_name": "SER"}, {"res_num": 31, "res_name": "THR"}, {"res_num": 32, "res_name": "SER"}, {"res_num": 33, "res_name": "GLY"}, {"res_num": 34, "res_name": "TYR"}, {"res_num": 35, "res_name": "SER"}, {"res_num": 36, "res_name": "TYR"}, {"res_num": 37, "res_name": "LEU"}, {"res_num": 38, "res_name": "HIS"}], "**cdr2**": [{"res_num": 54, "res_name": "LEU"}, {"res_num": 55, "res_name": "ALA"}, {"res_num": 56, "res_name": "SER"}, {"res_num": 57, "res_name": "TYR"}, {"res_num": 58, "res_name": "LEU"}, {"res_num": 59, "res_name": "GLU"}, {"res_num": 60, "res_name": "SER"}], "**cdr3**": [{"res_num": 93, "res_name": "GLN"}, {"res_num": 94, "res_name": "HIS"}, {"res_num": 95, "res_name": "SER"}, {"res_num": 96, "res_name": "ARG"}, {"res_num": 97, "res_name": "ASP"}, {"res_num": 98, "res_name": "LEU"}, {"res_num": 99, "res_name": "PRO"}, {"res_num": 100, "res_name": "LEU"}, {"res_num": 101, "res_name": "THR"}]}]}



```
    def get_config(self):
        return {
            "num_sampling_steps": self.num_sampling_steps, #number of denoising steps
            
            # Parameters defining the noise schedule (sigma: the standard deviation of the Gaussian noise added to the atomic coordinates)
            
            "sigma_min": self.structure_module.sigma_min,
            "sigma_max": self.structure_module.sigma_max, #typically at the beginning of reverse diffusion
            "rho": self.structure_module.rho, #controls how intermediate noise levels are distributed between the extreems
            
            # Stochasticity and noise injection
            "gamma_min": self.gamma_min,
            "gamma_0": self.gamma_0,
            "coordinate_augmentation_inference": self.coordinate_augmentation_inference,
            "alignment_reverse_diff": self.alignment_reverse_diff,
            "step_scale": self.step_scale,
            "noise_scale": self.noise_scale, #scales the amount of random noise 
            "sampling_schedule": self.structure_module.sampling_schedule,
            "step_scale_function": self.structure_module.step_scale_function,
            "noise_scale_function": self.structure_module.noise_scale_function,
            
            "time_dilation_start": self.structure_module.time_dilation_start,
            "time_dilation_end": self.structure_module.time_dilation_end,
            "time_dilation": self.structure_module.time_dilation,
        }
```

![image-20261020164701652](/home/sarah/.config/Typora/typora-user-images/image-20261020164701652.png)

![image-20261020165418257](/home/sarah/.config/Typora/typora-user-images/image-20261020165418257.png)

./run.sh --mode pi_guidance --num 8 --seed 45 --sampling-steps 200 --
