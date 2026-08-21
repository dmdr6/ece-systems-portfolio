# State-Space Matrix Exponential Derivation

## Problem Statement

Given a continuous linear time-invariant (LTI) autonomous system governed by the continuous-time dynamic differential equation:

$$\dot{x}(t) = Ax(t), \quad x(0) = x_0$$

Where $x(t) in \mathbb{R}^n$ is the state vector and $A\ in \mathbb{R}^{n \times n}$ is the constant system matrix. Derive the exact closed-form solution $x(t)$.

---

## Step-by-Step Mathematical Derivation

### Step 1: Rearrange and Apply the Matrix Integrating Factor
Rearrange the differential equation to group all state terms on the left-hand side

$$\dot{x}(t) - Ax(t) = 0$$

Pre-multiply the entire equation from the left by the matrix integrating factor $e^{-At} in \mathbb{R}^{n \times n}$:

$$e^{-At}\dot{x}(t) - e^{-At}Ax(t) = 0$$

---
### Step 2: Reverse Product Rule Application
