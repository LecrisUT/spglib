---
name: Report incorrect results
about: Found a bug resulting in incorrect symettries
title: ''
labels: bug
assignees: ''

---

<!-- Note to author: Please format your input using the  -->

## Input structure:
```yaml
lattice:
  - [ 1.0, 0.0, 0.0 ]  # a_x, b_x, c_x
  - [ 0.0, 1.0, 0.0 ]  # a_y, b_y, c_y
  - [ 0.0, 0.0, 1.0 ]  # a_z, b_z, c_z
points:  # all atoms
  - number: 1
    coordinates: [ 0.0, 0.0, 0.0 ]  # x, y, z
# Symmetry tolerance. Can keep it as `null` if you are using the default
symprec: null
angle_tolerance: null
mag_symprec: null 
```

Command run
```console

```

## Expected result
```yaml
```

## Actual output
```yaml
```
