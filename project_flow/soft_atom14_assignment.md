# Differentiable residue assignment from atom14 coordinates

**Current implementation:** Each non-designed residue is defined at the atomic position, including atom positions, element types and charge. The designed residues on the  other hand are encoded using the 14-atom representation. These 14 atom slots represent the position of the four backbone atoms followed by 10 virtual atoms. By superimposing the virtual atoms to the backbone atoms by counting the number of atoms within 0.5 A  of each backbone atom, the residue type can be identified. Each virtual atom is currently assigned to its nearest backbone atom. [1]

**Problem:** We want to implement pI guidance. However, now the gradients of the pI with respect to the amino acid sequence can not propagate to the atomic coordinates. 

**Goal.** Convert BoltzGen's continuous atom14 coordinates into soft amino acid assignments, allowing gradients to propagate from a sequence-level objective to atomic coordinates.

For residue $i$, let $\mathbf{x}^{\mathrm{BB}}_{ik}\in\mathbb{R}^3$ denote backbone reference slot $k\in\{1,\ldots,4\}$ and $\mathbf{x}^{\mathrm{SC}}_{ij}\in\mathbb{R}^3$ denote additional slot $j\in\{1,\ldots,10\}$.

## 1. Distances and soft assignments

Calculate pairwise distances:

$$
d_{ijk}=\left\|\mathbf{x}^{\mathrm{BB}}_{ik}-\mathbf{x}^{\mathrm{SC}}_{ij}\right\|_2.
$$

Replace the hard nearest-reference assignment with a softmax:

$$
q_{ijk}=\frac{\exp(-d_{ijk}/T_a)}{\sum_{\ell=1}^{4}\exp(-d_{ij\ell}/T_a)},\qquad \sum_{k=1}^{4}q_{ijk}=1.
$$

Here $q_{ijk}$ is the weight assigning additional slot $j$ to reference slot $k$; $T_a>0$ controls assignment softness.

### Remark

Je kunt \(T_a\) afleiden uit de gewenste verhouding tussen twee softmaxgewichten.

Voor twee afstanden \(d_1<d_2\):

\[ \frac{q_1}{q_2} =\exp\left(\frac{d_2-d_1}{T_a}\right) \]

Dus:

\[ \boxed{T_a=\frac{d_2-d_1}{\ln(q_1/q_2)}} \]

Stel dat twee atomen 0.5 Å uit elkaar liggen in afstand tot een referentiepunt. Je wilt dat het dichtstbijzijnde atoom vijf keer zoveel gewicht krijgt:

\[ T_a=\frac{0.5}{\ln(5)} \approx0.31\ \text{Å} \]

Dit is een fysisch interpreteerbare manier om de temperatuur te kiezen.

## 2. Smooth inclusion gate

The original decoder discards slots farther than a threshold $\tau$ from every reference position. Approximate this with

$$
d^{\min}_{ij}=\min_k d_{ijk},\qquad
 g_{ij}=\sigma\!\left(\frac{\tau-d^{\min}_{ij}}{T_g}\right),\qquad
\sigma(z)=\frac{1}{1+e^{-z}}.
$$

Here $g_{ij}\in(0,1)$ is the slot inclusion weight, $\tau=0.5$ is the default threshold in the original implementation's coordinate units, and $T_g>0$ controls gate sharpness. The minimum is differentiable almost everywhere; a soft minimum can be used if smoothness everywhere is required.     

## 3. Expected counts

Compute a continuous four-component count vector:

$$
\hat c_{ik}=\sum_{j=1}^{10}g_{ij}q_{ijk},\qquad
\hat{\mathbf c}_i=(\hat c_{i1},\ldots,\hat c_{i4}).
$$

## 4. Amino acid scores

For reference count pattern $\mathbf c^{\mathrm{ref}}_a$ associated with amino acid $a$, define

$$
E_{ia}=\left\|\hat{\mathbf c}_i-\mathbf c^{\mathrm{ref}}_a\right\|_2^2,
\qquad
P_i(a)=\frac{\exp(-E_{ia}/T_r)}{\sum_{b\in\mathcal A}\exp(-E_{ib}/T_r)}.
$$

Here $\mathcal A$ is the set of 20 standard amino acids, $P_i(a)$ is a **surrogate** residue probability, and $T_r>0$ controls its sharpness. This expression assumes one reference pattern per amino acid; if multiple patterns exist, score patterns separately and aggregate appropriately by amino acid.

Remark: up until here we have 3 hyperparametrs to tune $T_a$, $T_g$, and $T_r$ ;

- assignment_temperature: float = 0.5,
- gate_temperature: float = 0.5,
- residue_temperature: float = 0.5,

## **2. Determine** \(T_g\) **from the desired transition width**

A principled way to select \(T_g\) is to specify the distance interval over which the gate should decrease from 0.9 to 0.1.

For the sigmoid:

\[ g(\tau-\Delta)=0.9,\qquad g(\tau+\Delta)=0.1 \]

Solving gives:

\[ \Delta=T_g\ln(9) \]

Therefore, the full 90%–10% transition width is:

\[ \boxed{W_{90-10}=2T_g\ln(9)\approx4.394T_g} \]

Or equivalently:

\[ \boxed{T_g=\frac{W_{90-10}}{4.394}} \]

| Desired transition width | \(T_g\) |
| ------------------------ | ------- |
| 0.5 Å                    | 0.114 Å |
| 1.0 Å                    | 0.228 Å |
| 2.0 Å                    | 0.455 Å |
| 4.0 Å                    | 0.910 Å |

## 5. Application to pI guidance

Expected amino acid counts are

$$
n_a=\sum_{i=1}^{L}P_i(a).
$$

Combine their expected side-chain charges with fixed framework contributions and terminal-group charges to obtain $Q_{\mathrm{net}}(\mathrm{pI}_{\mathrm{target}})$, then use

$$
\mathcal L_{\mathrm{pI}}=\left[Q_{\mathrm{net}}(\mathrm{pI}_{\mathrm{target}})\right]^2,
\qquad
\nabla_X\mathcal L_{\mathrm{pI}}
$$

for coordinate guidance restricted to designable CDR positions.

**Caveats.** $T_a$, $T_g$, and $T_r$ are tunable parameters, not physical temperatures. The soft scores are not necessarily calibrated probabilities; verify uniqueness of BoltzGen's count patterns, agreement with its hard decoder, and gradient behavior on valid structures. Applying this decoder to denoised coordinates is generally more reliable than applying it directly to highly noisy diffusion states.
