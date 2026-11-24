# Isoelectric Point (pI) of Therapeutic Proteins

## 1. Definition

The **isoelectric point (pI)** is the pH at which a biomolecule carries **zero net electrical charge**.

The relationship between pH and pI determines the overall charge of a protein:

- **pH < pI:** The protein has a net positive charge.
- **pH = pI:** The protein has zero net charge.
- **pH > pI:** The protein has a net negative charge.

Importantly, zero net charge does not imply the absence of charged residues on the protein surface.

Important: the lower the pH the more acidic the solution => protonation of the amino acids vs the higher the pH the more basic the solution

## 2. Importance of pI

The pI is a key **physicochemical parameter** that influences protein behavior, including:

- **Surface electrostatics:** Determines the overall charge of a protein at a given pH.
- **Intermolecular interactions:** Surface charge affects interactions with other proteins, membranes, and biological receptors.
- **Pharmacokinetics:** Charge properties can influence tissue distribution, cellular uptake, and systemic clearance.
- **Drug delivery:** Electrostatic properties can affect transport across biological barriers and accumulation in target tissues.

### Global pI versus local charge patches

**The overall pI is not sufficient to describe the electrostatic properties of a protein.**

Proteins can contain positively and negatively charged surface patches, even when their overall net charge is zero.

These **local charge patches** can strongly influence molecular recognition, nonspecific binding, solubility, and interactions with cellular membranes.

Consequently, both the global pI and the spatial distribution of surface charges should be considered when evaluating therapeutic proteins.

## 3. pI as an Active Protein Design Parameter

The pI can be deliberately modified through amino acid substitutions, particularly involving ionizable residues.

Modulating the pI and surface charge distribution can be used to optimize therapeutic proteins by:

- Regulating interactions with endothelial receptors, including FcRn for Fc-containing proteins.
- Modifying cellular uptake and transendothelial transport.
- Influencing target tissue accumulation and biodistribution.
- Improving systemic pharmacokinetics and circulation half-life.
- Potentially reducing nonspecific interactions and off-target accumulation.

![image-20261027105306898](/home/sarah/.config/Typora/typora-user-images/image-20261027105306898.png)

## 4. pI calculation

There are different models available to calculate the pI of a protein. There are sequence and structure based models. IPC 2.0 is currently a good model. However, their is still room for improvement especially in the case of proteins. Calculating the pI of proteins is more complicated than that of peptides as the secondary structure influences the pKa values of the residues, additionally, the 3D folding influences the pI calculation. 

A simple way to calculate the pI of a protein is making use of the pKa values of the individual residues. 

In a first step of this project, we assume that the pKa's are fixed and are independent of the 3D structure. Note that this is a simplification. By consequence, we can calculate the pI of a protein using the Henderson-Hasselbalch equation. 

The Henderson-Hasselbalch equation [1] relates the pH of a solution to the pKa and the ratio of concentrations of the ionized and un-ionized forms of an acid or base. We use this equation to calculate the charge of each AA at a certain pH. 

- **For acids (HA):**

  - \(HA \rightleftharpoons H^+ + A^-\)
  - \(\displaystyle pH=pK_a+\log_{10}\left(\frac{[A^-]}{[HA]}\right)\)
  - \(\displaystyle \frac{[A^-]}{[HA]}=10^{pH-pK_a}\)

  **For bases (B):**

  - \(BH^+ \rightleftharpoons H^+ + B\)
  - \(\displaystyle pH=pK_a+\log_{10}\left(\frac{[B]}{[BH^+]}\right)\)
  - \(\displaystyle \frac{[B]}{[BH^+]}=10^{pH-pK_a}\)

The average charge is the fraction that is positively charged:

\[ q= (+1)\frac{[BH^+]}{[BH^+]+[B]}\]

\[ q_{\text{basic}}=\frac{+1}{1+10^{pH-pK_a}} \]

The average charge is the fraction that is negatively charged:

\[ q=(-1)\frac{[A^-]}{[HA]+[A^-]} \]

\[ q_{\text{acidic}}=\frac{-1}{1+10^{pK_a-pH}} \]

We use the following pKa's:

![image-20261116100701843](/home/sarah/.config/Typora/typora-user-images/image-20261116100701843.png)

Reference points for comparisons of two-dimensional maps of proteins from different human cell types defined in a pH scale where isoelectric points correlate with polypeptide compositions 

Remark: These pKa's are not the most accurate pKa values we can obtain but are a good start for the first implementation of the algorithm

## Sources

[1] Glossary of terms used in physical organic chemistry