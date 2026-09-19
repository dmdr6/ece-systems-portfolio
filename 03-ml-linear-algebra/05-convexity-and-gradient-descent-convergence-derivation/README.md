# Proof #5: Convexity & Gradient Descent Convergence Derivation

## Problem Statement

Consider a general multidimensional quadratic objective function $f: \mathbb{R}^n \to \mathbb{R}$ defined as:

$$f(x) = \frac{1}{2} x^T Q x + b^T x + c$$

where:
* $x \in \mathbb{R}^n$ is the parameter vector,
* $Q \in \mathbb{R}^{n \times n}$ is a symmetric matrix ($Q = Q^T$),
* $b \in \mathbb{R}^n$ is a constant vector,
* $c \in \mathbb{R}$ is a scalar constant.

### Objectives
1. Derive the gradient $\nabla f(x)$ and the Hessian matrix $\nabla^2 f(x)$ using matrix calculus.
2. Prove the convexity of $f(x)$ under positive semi-definiteness ($Q \succeq 0$) and establish the global optimality condition $Q x^* = -b$.
3. Formulate the Gradient Descent error dynamics and derive the strict step-size bound for convergence:

$$0 < \alpha < \frac{2}{\lambda_{\max}(Q)}$$

---

## Part I: Gradient & Hessian Matrix Derivation

### Step 1: Derivative of the Quadratic Form
Expand the objective function using scalar index notation or differential matrix operator rules. Consider a small perturbation $dx$:

$$f(x + dx) = \frac{1}{2} (x + dx)^T Q (x + dx) + b^T (x + dx) + c$$

Expanding the quadratic term:

$$\frac{1}{2} (x + dx)^T Q (x + dx) = \frac{1}{2} \left( x^T Q x + x^T Q dx + (dx)^T Q x + (dx)^T Q dx \right)$$

Using the symmetry property $Q = Q^T$, the cross-term satisfies:

$$(dx)^T Q x = \left( (dx)^T Q x \right)^T = x^T Q^T dx = x^T Q dx$$

Thus, combining the linear differential terms:

$$\frac{1}{2} \left( x^T Q dx + x^T Q dx \right) = x^T Q dx$$
