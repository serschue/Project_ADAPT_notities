import sys
print("Python:", sys.executable)
import torch
print("PyTorch:", torch.__version__)

from boltzgen_adapt.data import const

PKA = {
    "D": 3.9,
    "E": 4.3,
    "H": 6.0,
    "C": 8.3,
    "Y": 10.1,
    "K": 10.5,
    "R": 12.5,
}

ACIDIC = {"D", "E", "C", "Y"}
BASIC = {"H", "K", "R"}

def acidic_charge(pH,pKa):
    """
    Calculate the acidic charge of a molecule given its pH and pKa.

    Parameters:
    pH (float): The pH of the solution.
    pKa (float): The pKa of the molecule.

    Returns:
    float: The acidic charge of the molecule.
    """
    return - 1 / (1 + 10**(pKa - pH))

def basic_charge(pH,pKa):
    """
    Calculate the basic charge of a molecule given its pH and pKa.

    Parameters:
    pH (float): The pH of the solution.
    pKa (float): The pKa of the molecule.

    Returns:
    float: The basic charge of the molecule.
    """
    return 1 / (1 + 10**(pH - pKa))

def amino_acid_charges(pH):
    pH = torch.as_tensor(pH, dtype=torch.float32)
    charges = []

    for token in const.canonical_tokens:
        aa = const.prot_letter_to_token[token]

        if aa in ACIDIC:
            charge = acidic_charge(pH, PKA[aa])

        elif aa in BASIC:
            charge = basic_charge(pH, PKA[aa])

        else:
            charge = torch.zeros_like(pH)

        charges.append(charge)

    return torch.stack(charges) #(20,)

def expected_sidechain_charge_designed_residues(res_type_probs, pH):
    charges = amino_acid_charges(pH).to(device=res_type_probs.device,dtype=res_type_probs.dtype) #(20,)
    return torch.sum(res_type_probs * charges) #()

def expected_total_charge(sequence, res_type_probs, design_mask, nanobody_mask, pH):
    design_mask = design_mask.bool()
    nanobody_mask = nanobody_mask.bool()

    # Designed nanobody residues
    designed_residues_charge = expected_sidechain_charge_designed_residues(res_type_probs,pH)  # (N, 20)

    # Fixed nanobody residues
    fixed_residues_charge = torch.zeros_like(designed_residues_charge)
    fixed_mask = nanobody_mask & ~design_mask  # (N,)

    for i, aa in enumerate(sequence):
        if fixed_mask[i].item():
            if aa in ACIDIC:
                fixed_residues_charge = fixed_residues_charge + acidic_charge(pH, PKA[aa])
            elif aa in BASIC:
                fixed_residues_charge = fixed_residues_charge + basic_charge(pH, PKA[aa])

    # Terminal charges
    n_terminal = basic_charge(pH, 9.0)
    c_terminal = acidic_charge(pH, 2.0)

    expected_charge = designed_residues_charge + fixed_residues_charge + n_terminal + c_terminal

    return expected_charge


def pi_guidance_loss(sequence, res_type_probs, design_mask, nanobody_mask, target_pi):
    expected_charge = expected_total_charge(sequence, res_type_probs, design_mask, nanobody_mask, target_pi)
    loss = (expected_charge - 0.0) ** 2  # We want the expected charge to be close to zero at the target pI
    return loss
