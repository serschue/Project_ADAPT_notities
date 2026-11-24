# Hydrophobic Patch Detection BoltzGen

# Hydrophobic patches are detected using DBSCAN

## Objective
Estimate the area of the largest hydrophobic patch on a protein (e.g., a nanobody) by clustering spatially nearby hydrophobic atoms and summing their solvent-accessible surface areas (SASA).

## Current implementation in BoltzGen

```python
from sklearn.cluster import DBSCAN
import numpy as np

def largest_hydrophobic_patch_area(cif_path, distance_cutoff=6.0):
    result = compute_sasa(cif_path)
    if result is None or result[0].size == 0:
        return np.nan

    coords, sasa_vals = result
    if len(coords) == 0:
        return 0.0

    clustering = DBSCAN(eps=distance_cutoff, min_samples=1).fit(coords)
    labels = clustering.labels_

    max_patch_area = 0.0
    for label in np.unique(labels):
        area = sasa_vals[labels == label].sum()
        max_patch_area = max(max_patch_area, area)

    return max_patch_area
```

## How it works
1. `compute_sasa()` supplies atom coordinates and their SASA values.
2. `DBSCAN(eps=6.0, min_samples=1)` connects atoms within 6 Å (assuming coordinates are in Å). With `min_samples=1`, every atom belongs to a cluster, and chains of neighboring atoms can connect atoms farther than 6 Å apart.
3. For each cluster, sum the SASA values of its member atoms.
4. Return the maximum cluster sum, in the same area units as the input SASA (typically Å²).

## Important limitations
- **Hydrophobic selection:** The function measures a *hydrophobic* patch only if `compute_sasa()` returns hydrophobic atoms (or the coordinates are filtered accordingly). If all protein atoms are included, it does not measure hydrophobic patches.
- **Buried-atom bridges:** Atoms with negligible SASA may connect otherwise separate exposed regions, inflating the largest cluster.
- **3D proximity is not surface connectivity:** Euclidean distance between atom centers does not guarantee that two exposed regions are connected along the molecular surface.
- **Cutoff sensitivity:** A 6 Å cutoff can merge distinct patches, especially with `min_samples=1`. Results depend on the chosen cutoff and atom selection.

## Recommended improvements
1. Select hydrophobic atoms explicitly and apply a solvent-exposure filter (e.g., minimum per-atom SASA, with a documented threshold).
2. Test sensitivity to `eps` values such as 3, 4, 5, and 6 Å; check whether patch rankings remain stable.
3. For a more physically faithful patch definition, cluster connected regions on a solvent-accessible molecular surface rather than atom centers.
4. Document the hydrophobicity definition, SASA algorithm, coordinate units, and whether SASA is computed on the isolated nanobody or within the complex.

## Interpretation
The current result is best described as **the maximum summed SASA of a spatially connected cluster of selected atoms**, not necessarily the true area of a contiguous hydrophobic surface patch. Validate the selection and clustering assumptions before using it to compare nanobody designs or infer solubility.
