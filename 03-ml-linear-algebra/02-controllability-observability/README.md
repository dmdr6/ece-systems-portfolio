# Controllability & Observability Rank Conditions Derivation

## Problem Statement

Given a continuous linear time-invariant (LTI) system governed by the state-space dynamic equations:

$$\dot{x}(t) = Ax(t) + Bu(t), \quad x(t) \in \mathbb{R}^n, \, u(t) \in \mathbb{R}^m$$
$$y(t) = Cx(t) + Du(t), \quad y(t) \in \mathbb{R}^p$$

Where $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$, and $D \in \mathbb{R}^{p \times m}$. Prove that the algebraic rank conditions $\text{rank}(\mathcal{C}) = n$ and $\text{rank}(\mathcal{O}) = n$ are necessary and sufficient for full controllability and observability, where:

$$\mathcal{C} = \begin{bmatrix} B & AB & A^2B & \dots & A^{n-1}B \end{bmatrix} \in \mathbb{R}^{n \times nm}$$
$$\mathcal{O} = \begin{bmatrix} C \\ CA \\ CA^2 \\ \vdots \\ CA^{n-1} \end{bmatrix} \in \mathbb{R}^{np \times n}$$

---

## Part I: Controllability Rank Condition Derivation

### Step 1: Solution to the Non-Homogeneous State Equation
The closed-form trajectory solution for the continuous LTI system evaluated at time $t_f > 0$ is given by:

$$x(t_f) = e^{A t_f} x(0) + \int_{0}^{t_f} e^{A(t_f - \tau)} B u(\tau) \, d\tau$$

Rearrange the expression to isolate the contribution of the control input $u(\tau)$ on the target state displacement:

$$x(t_f) - e^{A t_f} x(0) = \int_{0}^{t_f} e^{A(t_f - \tau)} B u(\tau) \, d\tau$$

---

### Step 2: Cayley-Hamilton Theorem Expansion
By the Cayley-Hamilton Theorem, every square matrix $A \in \mathbb{R}^{n \times n}$ satisfies its own characteristic polynomial $p(\lambda) = \det(\lambda I - A) = 0$. Consequently, high-order matrix powers $A^k$ for $k \ge n$ can be expressed as a finite linear combination of matrix powers of degree less than $n$:

$$A^k = \sum_{i=0}^{n-1} \alpha_i(k) A^i$$

Applying this property to the infinite matrix exponential power series yields:

$$e^{A(t_f - \tau)} = \sum_{k=0}^{\infty} \frac{(t_f - \tau)^k}{k!} A^k = \sum_{i=0}^{n-1} \psi_i(\tau) A^i$$

Where $\psi_i(\tau)$ are continuous scalar functions of time.

---

### Step 3: Integral Factorization & Matrix Block Construction
Substitute the finite series expansion of $e^{A(t_f - \tau)}$ back into the state displacement equation:

$$x(t_f) - e^{A t_f} x(0) = \int_{0}^{t_f} \left( \sum_{i=0}^{n-1} \psi_i(\tau) A^i \right) B u(\tau) \, d\tau$$

Factor out the constant matrix terms $A^i B$ from the scalar integral:

$$x(t_f) - e^{A t_f} x(0) = \sum_{i=0}^{n-1} A^i B \left( \int_{0}^{t_f} \psi_i(\tau) u(\tau) \, d\tau \right)$$

Define the vector integral coefficients $v_i \in \mathbb{R}^m$ as:

$$v_i = \int_{0}^{t_f} \psi_i(\tau) u(\tau) \, d\tau$$

Rewrite the finite sum as a block matrix multiplication:

$$x(t_f) - e^{A t_f} x(0) = B v_0 + AB v_1 + A^2 B v_2 + \dots + A^{n-1}B v_{n-1}$$

$$x(t_f) - e^{A t_f} x(0) = \begin{bmatrix} B & AB & A^2B & \dots & A^{n-1}B \end{bmatrix} \begin{bmatrix} v_0 \\ v_1 \\ v_2 \\ \vdots \\ v_{n-1} \end{bmatrix} = \mathcal{C} \, \mathbf{v}$$

To steer $x(0)$ to any arbitrary target state $x(t_f) \in \mathbb{R}^n$, the linear system $\mathcal{C} \mathbf{v} = d$ must yield a valid vector $\mathbf{v}$ for any $d \in \mathbb{R}^n$. This holds if and only if:

$$\text{rank}(\mathcal{C}) = n \quad \blacksquare$$

---

## Part II: Observability Rank Condition Derivation

### Step 1: Zero-Input Output Response
Without loss of generality, evaluate the zero-input system dynamic response ($u(t) = 0$) to isolate the effect of initial state $x(0) = x_0$ on the output vector $y(t)$:

$$y(t) = C e^{At} x_0$$

---

### Step 2: Cayley-Hamilton Expansion of Output Trajectory
Apply the Cayley-Hamilton reduction to the matrix exponential term $e^{At}$:

$$e^{At} = \sum_{i=0}^{n-1} \phi_i(t) A^i$$

Substitute this expansion directly into the output equation:

$$y(t) = C \left( \sum_{i=0}^{n-1} \phi_i(t) A^i \right) x_0 = \sum_{i=0}^{n-1} \phi_i(t) C A^i x_0$$

---

### Step 3: Successive Output Derivatives at $t = 0$
Evaluate successive temporal derivatives of the output vector $y(t)$ at the initial instant $t = 0$:

$$y(0) = C x_0$$
$$\dot{y}(0) = CA x_0$$
$$\ddot{y}(0) = CA^2 x_0$$
$$\vdots$$
$$y^{(n-1)}(0) = CA^{n-1} x_0$$

---

### Step 4: System Stacking & Full-Rank Mapping
Stack the $n-1$ derivatives into a single extended vector equation:

$$\begin{bmatrix} y(0) \\ \dot{y}(0) \\ \ddot{y}(0) \\ \vdots \\ y^{(n-1)}(0) \end{bmatrix} = \begin{bmatrix} C \\ CA \\ CA^2 \\ \vdots \\ CA^{n-1} \end{bmatrix} x_0 \implies Y_{0:n-1} = \mathcal{O} \, x_0$$

To uniquely solve for the initial state vector $x_0 \in \mathbb{R}^n$ given output measurement history, the linear transformation $\mathcal{O}$ must have a trivial nullspace ($\ker(\mathcal{O}) = \{0\}$). This holds if and only if $\mathcal{O}$ has full column rank:

$$\text{rank}(\mathcal{O}) = n \quad \blacksquare$$
