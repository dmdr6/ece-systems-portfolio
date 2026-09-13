# Proof #4: LQR Optimality & Continuous Algebraic Riccati Equation (CARE) Derivation

## Problem Statement

Consider a continuous-time linear time-invariant (LTI) system defined by the state dynamics:

$$\dot{x}(t) = A x(t) + B u(t)$$

where $x(t) \in \mathbb{R}^n$ represents the state vector and $u(t) \in \mathbb{R}^m$ represents the control input vector.

We aim to minimize the infinite-horizon quadratic performance index:

$$J = \int_{0}^{\infty} \left( x(t)^T Q x(t) + u(t)^T R u(t) \right) dt$$

subject to state weighting matrix $Q \succeq 0$ (symmetric positive semi-definite) and control input weighting matrix $R \succ 0$ (symmetric positive definite).

**Goal:** Derive the optimal control law $u^*(t) = -K x(t)$ and show that the matrix $P \succ 0$ satisfies the Continuous Algebraic Riccati Equation (CARE).

---

## Part I: Value Function & Lyapunov Formulation

### Step 1: Candidate Value Function Definition
Assume an optimal value function (cost-to-go) that represents the minimal quadratic cost remaining from state $x(t)$ to infinity:

$$V(x) = x(t)^T P x(t)$$

where $P \in \mathbb{R}^{n \times n}$ is a constant, symmetric positive-definite matrix ($P = P^T \succ 0$).

### Step 2: Continuous-Time Lyapunov Energy Decay
By the definition of the cost functional $J$:

$$V(x(t)) = \int_{t}^{\infty} \left( x(\tau)^T Q x(\tau) + u(\tau)^T R u(\tau) \right) d\tau$$

Differentiating both sides with respect to time $t$ yields the foundational dynamic stability condition:

$$\dot{V}(x(t)) = -\left( x(t)^T Q x(t) + u(t)^T R u(t) \right)$$

$$\dot{V}(x) + x^T Q x + u^T R u = 0$$

---

## Part II: Minimization with Respect to Control Input $u$

### Step 3: Expanding the Time Derivative $\dot{V}(x)$
Applying the matrix chain rule to $\dot{V}(x) = \frac{d}{dt} \left( x^T P x \right)$:

$$\dot{V}(x) = \dot{x}^T P x + x^T P \dot{x}$$

Substituting system dynamics $\dot{x} = A x + B u$:

$$\dot{V}(x) = (A x + B u)^T P x + x^T P (A x + B u)$$

$$\dot{V}(x) = x^T A^T P x + u^T B^T P x + x^T P A x + x^T P B u$$

### Step 4: Constructing the Hamiltonian / HJB Function
Substitute $\dot{V}(x)$ into the energy dynamic equation:

$$H(x, u, P) = x^T A^T P x + u^T B^T P x + x^T P A x + x^T P B u + x^T Q x + u^T R u = 0$$

Note that since $P = P^T$, $u^T B^T P x$ is a scalar, meaning $u^T B^T P x = (u^T B^T P x)^T = x^T P B u$. Thus:

$$H(x, u, P) = x^T (A^T P + P A + Q) x + 2 x^T P B u + u^T R u = 0$$

### Step 5: Minimizing $H(x, u, P)$ with Respect to $u$
To find the optimal control input $u^*$, compute the partial derivative of $H(x, u, P)$ with respect to $u$ and set it to zero:

$$\frac{\partial H}{\partial u} = \frac{\partial}{\partial u} \left( 2 x^T P B u + u^T R u \right) = 0$$

Using standard matrix calculus identities $\frac{\partial}{\partial u}(a^T u) = a$ and $\frac{\partial}{\partial u}(u^T R u) = 2 R u$ (for symmetric $R$):

$$2 B^T P x + 2 R u^* = 0$$

Solving explicitly for $u^*$:

$$R u^* = -B^T P x \implies u^* = -R^{-1} B^T P x$$

This yields the linear state feedback law $u^* = -K x$, where the optimal feedback gain matrix $K$ is defined as:

$$K = R^{-1} B^T P$$

---

## Part III: Derivation of the Continuous Algebraic Riccati Equation (CARE)

### Step 6: Substituting Optimal Control Back into $H(x, u^*, P)$
Substitute $u^* = -R^{-1} B^T P x$ into the zero-Hamiltonian condition:

$$x^T (A^T P + P A + Q) x + 2 x^T P B (-R^{-1} B^T P x) + (-R^{-1} B^T P x)^T R (-R^{-1} B^T P x) = 0$$

Evaluate the third term using $(M N)^T = N^T M^T$ and $R^T = R$:

$$(-R^{-1} B^T P x)^T R (-R^{-1} B^T P x) = x^T P B R^{-1} R R^{-1} B^T P x = x^T P B R^{-1} B^T P x$$

Combine the second and third terms:

$$-2 x^T P B R^{-1} B^T P x + x^T P B R^{-1} B^T P x = -x^T P B R^{-1} B^T P x$$

### Step 7: Isolating the Quadratic Form
Grouping all terms under a single state-quadratic expression gives:

$$x(t)^T \left( A^T P + P A - P B R^{-1} B^T P + Q \right) x(t) = 0$$

Since this identity must hold for **all** non-trivial arbitrary trajectories $x(t) \neq 0$, the central matrix kernel must evaluate to zero identically.

$$\mathbf{A^T P + P A - P B R^{-1} B^T P + Q = 0} \quad \blacksquare$$

---

## Summary of Results

| Expression | Mathematical Definition |
|---|---|
| **CARE** | $A^T P + P A - P B R^{-1} B^T P + Q = 0$ |
| **Optimal Control Law** | $u^*(t) = -K x(t)$ |
| **Optimal Feedback Gain** | $K = R^{-1} B^T P$ |
| **Closed-Loop System Dynamics** | $\dot{x}(t) = (A - BK) x(t)$ |

