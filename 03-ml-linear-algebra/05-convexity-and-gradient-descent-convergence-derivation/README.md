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

### Step 2: Total First Differential
Collecting the first-order terms in $dx$:

$$df = f(x + dx) - f(x) = x^T Q dx + b^T dx + \mathcal{O}(\|dx\|^2)$$

$$df = (Q x + b)^T dx$$

By the definition of the gradient $\nabla f(x)$, where $df = \langle \nabla f(x), dx \rangle = (\nabla f(x))^T dx$:

$$\nabla f(x) = Q x + b$$

### Step 3: Hessian Matrix Derivation
The Hessian matrix $\nabla^2 f(x) \in \mathbb{R}^{n \times n}$ is defined as the Jacobian matrix of the gradient operator:

$$\nabla^2 f(x) = \frac{\partial}{\partial x} \left( \nabla f(x) \right) = \frac{\partial}{\partial x} (Q x + b)$$

Since $Q$ is constant with respect to $x$ and $b$ is independent of $x$:

$$\nabla^2 f(x) = Q$$

---

## Part II: Convexity Proof & Global Optimality

### Step 1: Second-Order Characterization of Convexity
A twice-continuously differentiable function $f: \mathbb{R}^n \to \mathbb{R}$ is convex if and only if its Hessian is positive semi-definite everywhere:

$$\nabla^2 f(x) \succeq 0 \quad \forall x \in \mathbb{R}^n$$

Since $\nabla^2 f(x) = Q$ is constant across $\mathbb{R}^n$, $f(x)$ is convex if and only if:

$$v^T Q v \ge 0 \quad \forall v \in \mathbb{R}^n$$

If $Q \succ 0$ (all eigenvalues $\lambda_i(Q) > 0$), $f(x)$ is **strictly convex**.

### Step 2: Global Minimum Condition
By first-order optimality conditions, $x^*$ is a stationary point if and only if the gradient vanishes:

$$\nabla f(x^*) = 0 \implies Q x^* + b = 0 \implies Q x^* = -b$$

If $Q \succ 0$, $Q$ is invertible, guaranteeing a unique global minimum:

$$x^* = -Q^{-1} b$$

---

## Part III: Gradient Descent Formulation & Convergence Analysis

### Step 1: First-Order Update Rule
The standard Gradient Descent (GD) iteration scheme with constant learning rate $\alpha > 0$ is defined as:

$$x_{k+1} = x_k - \alpha \nabla f(x_k)$$

Substituting the analytical gradient $\nabla f(x_k) = Q x_k + b$:

$$x_{k+1} = x_k - \alpha (Q x_k + b)$$

### Step 2: Error Dynamics
Define the parameter error vector at iteration $k$ as $e_k = x_k - x^*$. Since $Q x^* = -b$, we rewrite $b = -Q x^*$:

$$x_{k+1} = x_k - \alpha Q x_k - \alpha b$$
$$x_{k+1} = x_k - \alpha Q x_k + \alpha Q x^*$$

Subtracting $x^*$ from both sides:

$$x_{k+1} - x^* = (x_k - x^*) - \alpha Q (x_k - x^*)$$

$$e_{k+1} = (I - \alpha Q) e_k$$

By induction, the error after $k$ steps is given by matrix power iteration:

$$e_k = (I - \alpha Q)^k e_0$$

### Step 3: Spectral Step-Size Bound for Convergence
For the error to vanish as $k \to \infty$ ($e_k \to 0$), the iteration matrix $T = I - \alpha Q$ must be a contraction mapping. This requires its spectral radius $\rho(T)$ to be strictly less than $1$:

$$\rho(I - \alpha Q) = \max_i |1 - \alpha \lambda_i(Q)| < 1$$

For all eigenvalues $\lambda_i(Q) \in [\lambda_{\min}(Q), \lambda_{\max}(Q)]$:

