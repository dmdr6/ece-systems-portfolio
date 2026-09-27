# Proof #6: $L_2$-Regularized Linear Regression (Ridge Regression)

## Problem Statement

Consider a linear regression problem with design matrix $X \in \mathbb{R}^{m \times n}$ and target vector $y \in \mathbb{R}^m$. The $L_2$-regularized linear regression objective function $J(w)$ (also known as **Ridge Regression**) is defined as:

$$J(w) = \|Xw - y\|_2^2 + \lambda \|w\|_2^2$$

where $w \in \mathbb{R}^n$ represents the weight vector and $\lambda > 0$ is the regularization parameter.

**Goal:** Derive the closed-form solution $w^\star = (X^T X + \lambda I)^{-1} X^T y$, prove strict convexity and invertibility of $(X^T X + \lambda I)$ for $\lambda > 0$, formulate the gradient descent update rule, and analyze weight shrinkage using Singular Value Decomposition (SVD).

---

## Part I: Gradient Derivation & Closed-Form Solution

### Step 1: Matrix Calculus Expansion

Using the $L_2$-norm identity $\|v\|_2^2 = v^T v$, expand the objective function $J(w)$:

$$
\begin{aligned}
J(w) &= (Xw - y)^T (Xw - y) + \lambda w^T w \\
&= (w^T X^T - y^T)(Xw - y) + \lambda w^T w \\
&= w^T X^T X w - w^T X^T y - y^T X w + y^T y + \lambda w^T w
\end{aligned}
$$

Since $w^T X^T y \in \mathbb{R}$ is a scalar, it equals its transpose: $(w^T X^T y)^T = y^T X w$. Combining these terms gives:

$$J(w) = w^T X^T X w - 2 y^T X w + y^T y + \lambda w^T w$$

### Step 2: First-Order Gradient Derivation

Apply matrix differentiation rules:
1. $\frac{\partial}{\partial w} (w^T A w) = (A + A^T) w$ (for symmetric $A = X^T X$, this equals $2 X^T X w$)
2. $\frac{\partial}{\partial w} (a^T w) = a$
3. $\frac{\partial}{\partial w} (w^T w) = 2 w$

Differentiating $J(w)$ with respect to $w$:

$$
\begin{aligned}
\nabla_w J(w) &= \frac{\partial}{\partial w} \left( w^T X^T X w - 2 y^T X w + y^T y + \lambda w^T w \right) \\
&= 2 X^T X w - 2 X^T y + 2 \lambda w \\
&= 2 \left( (X^T X + \lambda I) w - X^T y \right)
\end{aligned}
$$

### Step 3: Stationary Point & Invertibility Proof

To find the optimal weight vector $w^\star$, set the gradient to zero:

$$\nabla_w J(w^\star) = 0 \implies 2 \left( (X^T X + \lambda I) w^\star - X^T y \right) = 0$$

$$(X^T X + \lambda I) w^\star = X^T y$$

**Invertibility Proof:**
To solve for $w^\star$, the matrix $M = X^T X + \lambda I$ must be invertible. 

1. $X^T X$ is a real symmetric positive semi-definite matrix: for any $v \in \mathbb{R}^n, v \neq 0$, we have $v^T X^T X v = (Xv)^T (Xv) = \|Xv\|_2^2 \ge 0$.
2. $\lambda I$ is positive definite for $\lambda > 0$: $v^T (\lambda I) v = \lambda \|v\|_2^2 > 0$.
3. Thus, for any $v \neq 0$:

$$v^T (X^T X + \lambda I) v = \|Xv\|_2^2 + \lambda \|v\|_2^2 \ge \lambda \|v\|_2^2 > 0$$

Since $v^T M v > 0$ for all non-zero vectors $v$, $M = X^T X + \lambda I$ is strictly **positive definite**. Every strictly positive definite matrix has strictly positive eigenvalues ($\lambda_i(M) \ge \lambda > 0$), making it nonsingular and strictly invertible—even if $X^T X$ is singular (e.g., when $m < n$ or under extreme multicollinearity).

Multiplying both sides by $(X^T X + \lambda I)^{-1}$ yields the unique analytical closed-form solution:

$$w^\star = (X^T X + \lambda I)^{-1} X^T y$$

---

## Part II: Convexity & Invertibility Proof

### Step 1: Second-Order Derivative (Hessian Matrix)

Compute the Hessian matrix $\nabla^2 J(w)$ by taking the gradient of $\nabla J(w)$:

$$
\begin{aligned}
\nabla^2 J(w) &= \frac{\partial}{\partial w} \left( 2 X^T X w - 2 X^T y + 2 \lambda w \right) \\
&= 2 X^T X + 2 \lambda I \\
&= 2 (X^T X + \lambda I)
\end{aligned}
$$

### Step 2: Global Optimality via Strict Convexity

For any non-zero vector $z \in \mathbb{R}^n, z \neq 0$:

$$
\begin{aligned}
z^T \left( \nabla^2 J(w) \right) z &= z^T \left( 2 X^T X + 2 \lambda I \right) z \\
&= 2 \|Xz\|_2^2 + 2 \lambda \|z\|_2^2
\end{aligned}
$$

Since $\|Xz\|_2^2 \ge 0$ and $2 \lambda \|z\|_2^2 > 0$ for $\lambda > 0$ and $z \neq 0$:

$$z^T \left( \nabla^2 J(w) \right) z > 0 \implies \nabla^2 J(w) \succ 0$$

Because the Hessian matrix is strictly positive definite everywhere, $J(w)$ is **strictly convex**. Therefore, $w^\star$ is the unique global minimum of $J(w)$.

---

## Part III: Gradient Descent Update Rule & SVD Weight Shrinkage Analysis

### Step 1: Gradient Descent Formulation

Using step size (learning rate) $\alpha > 0$, the Gradient Descent update rule is defined as:

$$w_{k+1} = w_k - \alpha \nabla J(w_k)$$

Substituting $\nabla J(w_k) = 2 \left( (X^T X + \lambda I) w_k - X^T y \right)$:

$$w_{k+1} = w_k - 2\alpha \left( (X^T X + \lambda I) w_k - X^T y \right)$$

$$w_{k+1} = \left( I - 2\alpha (X^T X + \lambda I) \right) w_k + 2\alpha X^T y$$

For convergence to $w^\star$, the learning rate must satisfy:

$$0 < \alpha < \frac{1}{\lambda_{\max}(X^T X + \lambda I)} = \frac{1}{\sigma_{\max}^2(X) + \lambda}$$

### Step 2: SVD Analysis of Weight Shrinkage Dynamics

Let the Singular Value Decomposition (SVD) of $X \in \mathbb{R}^{m \times n}$ be:

$$X = U \Sigma V^T$$

where $U \in \mathbb{R}^{m \times m}$ and $V \in \mathbb{R}^{n \times n}$ are orthogonal matrices ($U^T U = I_m, V^T V = I_n$), and $\Sigma \in \mathbb{R}^{m \times n}$ contains singular values $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_r > 0$.

Compute $X^T X$:

$$X^T X = (U \Sigma V^T)^T (U \Sigma V^T) = V \Sigma^T U^T U \Sigma V^T = V \Sigma^T \Sigma V^T$$

Substitute $X = U \Sigma V^T$ and $X^T X = V \Sigma^T \Sigma V^T$ into the Ridge analytical formula:

$$
\begin{aligned}
w^\star &= (V \Sigma^T \Sigma V^T + \lambda I)^{-1} (U \Sigma V^T)^T y \\
&= (V (\Sigma^T \Sigma + \lambda I) V^T)^{-1} V \Sigma^T U^T y \\
&= V (\Sigma^T \Sigma + \lambda I)^{-1} V^T V \Sigma^T U^T y \\
&= V (\Sigma^T \Sigma + \lambda I)^{-1} \Sigma^T U^T y
\end{aligned}
$$

For coordinate axis $i$ corresponding to right singular vector $v_i$:

$$w^\star = \sum_{i=1}^r \left( \frac{\sigma_i}{\sigma_i^2 + \lambda} \right) (u_i^T y) v_i$$

Comparing this to unregularized Ordinary Least Squares (OLS) where $w_{\text{OLS}} = \sum_{i=1}^r \left( \frac{1}{\sigma_i} \right) (u_i^T y) v_i$:

$$w^\star = \sum_{i=1}^r \left( \frac{\sigma_i^2}{\sigma_i^2 + \lambda} \right) w_{\text{OLS}, i} v_i$$

### Shrinkage Factor Analysis:

The component shrinkage factor $f_i$ along singular vector $v_i$ is defined as:

$$f_i = \frac{\sigma_i^2}{\sigma_i^2 + \lambda}$$

1. **Large Singular Values ($\sigma_i^2 \gg \lambda$):** $f_i \approx 1$. Directions with high variance are preserved with negligible shrinkage.
2. **Small Singular Values ($\sigma_i^2 \ll \lambda$):** $f_i \approx \frac{\sigma_i^2}{\lambda} \to 0$. Directions corresponding to noise or severe multicollinearity are heavily suppressed.
3. **Condition Number Stabilization:** The Hessian condition number improves from $\kappa_{\text{OLS}} = \frac{\sigma_{\max}^2}{\sigma_{\min}^2}$ to $\kappa_{\text{Ridge}} = \frac{\sigma_{\max}^2 + \lambda}{\sigma_{\min}^2 + \lambda} < \kappa_{\text{OLS}}$, guaranteeing numerical stability.
