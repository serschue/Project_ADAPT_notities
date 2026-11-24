# Gradient-Guided Diffusion for pI Optimization in BoltzGen

**Objective:** Steer BoltzGen-generated nanobodies toward a desired isoelectric point (pI) while maintaining favorable binding properties, with sequence modifications restricted to the CDR loops.

### 1. Probabilistic Framework

BoltzGen learns a conditional distribution \(p_\theta(x\mid c)\), where \(x\) represents the generated nanobody and \(c\) the target and design constraints.

Ideally, we want to sample from:

\[
p(x\mid y_{\mathrm{pI}},y_{\mathrm{bind}},c)
\propto p_\theta(x\mid c)\,
p(y_{\mathrm{pI}},y_{\mathrm{bind}}\mid x,c)
\]

Assuming conditional independence of the property likelihoods, this becomes:

\[
p(x\mid y_{\mathrm{pI}},y_{\mathrm{bind}},c)
\propto p_\theta(x\mid c)\,
p(y_{\mathrm{pI}}\mid x)\,
p(y_{\mathrm{bind}}\mid x,c)
\]

We approximate conditional generation by introducing property-specific gradients during diffusion. **This does not guarantee exact posterior sampling**, since the guidance generally approximates the conditional score at intermediate noise levels.

### 2. Differentiable pI Prediction

The original pI predictor uses discrete amino acid counts, which are not differentiable. We replace these with expected counts derived from continious AA probabilities. 
\[
n_a=\sum_{i=1}^{L}P_i(a)
\]

Subsequently, we calculate the expected net charge of the complete nanobody at the desired pI using Henderson–Hasselbalch equation.

\[Q_\text{net} = Q_\text{framework} + Q_\text{designed-residues} \]

During the design only the designed-residues can be altered, often those design residues are located in the CDR regions (CDR-restricted guidance). 

Instead of explicitly solving for the pI, minimize:

\[
\mathcal L_{\mathrm{pI}}=
\left[Q_{\mathrm{net}}(pI_{\mathrm{target}})\right]^2
\]

This provides a differentiable objective that encourages the predicted net charge to approach zero at the target pI.

### 3. Mapping Coordinate Gradients to Amino Acid Changes

### pI Guidance Gradient Flow

1. **Noisy atomic coordinates**
   - Input: \(X_t \in \mathbb{R}^{N \times 3}\)

   ↓

2. **Denoising network**
   - Predict denoised coordinates:
   - \(\hat{X}_0 = D_\phi(X_t,t)\)

   ↓

3. **Probabilistic Atom14 decoder**
   - Convert predicted atomic coordinates into amino acid probabilities (for each design position we then have a AA probability for each AA):
   - \(P_i(a) = h(\hat{X}_0)\)

   ↓

4. **pI loss calculation**
   
   - Estimate the isoelectric point from amino acid probabilities.
   - Calculate the loss relative to the target pI:
   - \(\mathcal{L}_{\mathrm{pI}} = \mathcal{L}_{\mathrm{pI}}(P)\)
   
   ↓
   
5. **Backpropagation (PyTorch autograd)**
   - Propagate the loss gradient through the decoder and denoising network:

   \[
   \nabla_{X_t}\mathcal{L}_{\mathrm{pI}}
   =
   J_{D_\phi}(X_t)^\top
   J_h(\hat{X}_0)^\top
   \nabla_P\mathcal{L}_{\mathrm{pI}}
   \]

   ↓

6. **Guided coordinate update**
   - Modify the diffusion update using the pI gradient:

   \[
   \Delta X_t^{\mathrm{guidance}}
   =
   -\eta_t\lambda\nabla_{X_t}\mathcal{L}_{\mathrm{pI}}
   \]

   ↓

7. **Updated atomic coordinates**
   - Continue the diffusion process with the guided coordinates.
   - Repeat at subsequent diffusion steps.

### 4. Combined pI and Binding Guidance

Combine gradients from the pI objective and a differentiable binding-related objective:

\[
\boxed{
g_t=
-\eta_t(t)\nabla_{X_t}\mathcal L_{\mathrm{pI}}
-\eta_t(t)\lambda_\text{guidance}\nabla_{X_t}\mathcal L_{\mathrm{bind}}
}
\]

The guidance is applied to designable coordinates during diffusion steps where amino acid identities can still change, while retaining BoltzGen's original denoising process.

### 5. Validation

Evaluate generated nanobodies based on:

- **pI accuracy:** Difference between the target pI and the predicted pI of the final discrete sequence.
- **Binding quality:** Predicted binding metrics and preservation of important interface interactions.
- **Structural validity:** Plausible geometry, folding, and absence of severe clashes.
- **Sequence diversity:** Diversity of generated CDR sequences compared with unguided BoltzGen.
- **Guidance trade-offs:** Effects of different guidance strengths on pI accuracy, binding metrics, and generation quality.

**Expected outcome:** An approximately conditional, gradient-guided BoltzGen workflow that enriches generated nanobodies for the desired pI while attempting to preserve favorable binding properties, without retraining the original diffusion model.





## Summary: complete differentiable mapping

![image-20261109161455435](/home/sarah/.config/Typora/typora-user-images/image-20261109161455435.png)

The three temperature parameters \(T_a\), \(T_g\), and \(T_r\) are hyperparameters that must be calibrated. 



