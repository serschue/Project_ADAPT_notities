# Developability criteria

Article: A high-throughput platform for biophysical antibody developability assessment to enable AI/ ML model training (https://doi.org/10.1080/19420862.2025.2593055)

To achieve useful therapeutic activity:

1. high affinity and specificity
2. suitable developability properties 

Both are inherent to a given antibody amino acid sequence. 

They build a high-throughput antibody developability assay platform (PROPHET-Ab: Platform for reliable outcome prediction in high-throughput evaluation of therapeutic antibodies) designed to generate large datasets needed to train improved ML models. 

=> Dataset of 246 benchmark antibodies available, with the following developability properties 

![image-20261012102024494](/home/sarah/.config/Typora/typora-user-images/image-20261012102024494.png)

1. **Upstream expressibility:** can the antibody be produced efficiently

   Titer: amount of antibody produced per liter of culture (higher better)

   Expression yield: depends on protein folding, secretion and chain assembly

2. **Purity:** Is the produced antibody intact and free of aggregates?

   - **CE-SDS (Capillary Electrophoresis–SDS)**

     Detects protein fragmentation, cleavage (clipping) and chain integrity.

     - Readout: %LC+HC (light and heavy chains)
     - For conventional antibodies, a higher proportion of intact chains is desirable.)![image-20261012104440233](/home/sarah/.config/Typora/typora-user-images/image-20261012104440233.png)

   - **SE-HPLC (Size-Exclusion High-Performance Liquid Chromatography)**

     Separates monomeric antibodies from larger aggregates and smaller fragments.

     - Readout: %Monomer
     - Higher monomer content is generally desirable.
     - Aggregates can increase immunogenicity and reduce product quality.
     - ![image-20261012104509591](/home/sarah/.config/Typora/typora-user-images/image-20261012104509591.png)

3. **Conformational or thermal stability**: does the antibody maintain its folded structure under different conditions (higher better)

   Tm1: First apparent melting temperature, where an unfolding transition occurs.

   Tm2: Second apparent melting temperature, when multiple structural domains or transitions are present.

   Relevance: Thermally unstable antibodies may unfold or aggregate during manufacturing, transport or storage.

   (https://doi.org/10.1021/acsami.5c19073)

4. **Hydrophobicity:** does the antibody exposes hydrophobic patches on its surface?

   Hydrophobic amino acids generally prefer to be buried within the protein core. When large hydrophobic patches are exposed to water, they can promote interactions with other proteins.

   Assays: HIC-HPLC and SMAC

   - HIC-HPLC (Hydrophobic Interaction Chromatography): Measures how strongly the protein interacts with a hydrophobic chromatography surface.
   - SMAC (Stand-up Monolayer Adsorption Chromatography): Probes surface interactions associated with hydrophobicity and colloidal behavior.

   Both commonly report retention time (RT). Longer retention can indicate stronger undesirable surface interactions, depending on the assay.

   There is therefore a trade-off: hydrophobic interactions may improve target binding while simultaneously worsening developability.

5. **Self-association and colloidal stability:** Do antibody molecules remain dispersed in solution, or do they attract each other?

   AC-SINS (Affinity-Capture Self-Interaction Nanoparticle Spectroscopy) (higher better)

   - Measures antibody self-association using antibody-coated nanoparticles.
   - Readout: Change in maximum absorbance wavelength (\(\Delta\lambda_{\max}\)).
   - A larger wavelength shift generally indicates stronger self-interactions.

   DLS-kD (Dynamic Light Scattering – diffusion interaction parameter)

   - Measures how the diffusion coefficient changes with protein concentration.
   - Readout: \(k_D\), usually in mL/g.
   - More negative values generally indicate stronger attractive interactions and poorer colloidal stability.

   These properties are especially important for highly concentrated antibody formulations, where self-association can increase viscosity and complicate injection.

6. **Biological attributes:** Does the antibody interact with biological molecules other than its intended target?

   **HAC - Heparin affinity chromatography**

   Heparin is a highly negatively charged molecule that can interact with positively charged protein surface regions.

   - Readout: Retention time (RT).
   - Longer retention generally indicates stronger heparin binding.
   - Strong heparin binding can suggest a risk of nonspecific interactions with negatively charged biological components.

   This may affect pharmacokinetics, including tissue distribution and clearance.

   **Polyreactivity**

   Polyreactivity describes an antibody's ability to interact with multiple unrelated molecules rather than exclusively recognizing its intended antigen.

   Assays measure binding to complex biological mixtures or unrelated proteins, such as CHO cell lysate or ovalbumin.

   - Readout: Polyreactivity score (PR score).
   - Higher scores generally indicate more nonspecific binding.
   - Polyreactivity can contribute to off-target binding and unfavorable pharmacokinetics.

   Importantly, polyreactivity is not the same as cross-reactivity. Cross-reactivity can involve recognition of related epitopes, whereas polyreactivity generally involves binding to structurally unrelated molecules.


General additional information about antibody properties and developability: 

https://www.tamarind.bio/blog/predicting-antibody-properties-developability