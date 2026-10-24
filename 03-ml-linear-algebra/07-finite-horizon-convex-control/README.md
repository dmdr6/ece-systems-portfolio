# Proof #7: Finite-Horizon Convex Control & Model Predictive Control (MPC)

## Problem Statement

Consider a discrete-time Linear Time-Invariant (LTI) system with state $x_k \in \mathbb{R}^n$ and control input $u_k \in \mathbb{R}^m$:

$$x_{k+1} = A x_k + B u_k, \quad k = 0, 1, \dots, N-1$$

where $A \in \mathbb{R}^{n \times n}$ and $B \in \mathbb{R}^{n \times m}$. The finite-horizon optimal control problem minimizes a quadratic cost function subject to state dynamics and physical actuator constraints:

$$\min_{u_0, \dots, u_{N-1}} J = x_N^T P x_N + \sum_{k=0}^{N-1} \left( x_k^T Q x_k + u_k^T R u_k \right)$$

subject to:
1. $x_{k+1} = A x_k + B u_k, \quad \forall k \in \{0, \dots, N-1\}$
2. $u_{\min} \le u_k \le u_{\max}, \quad \forall k \in \{0, \dots, N-1\}$

where $Q \succeq 0$ is the state cost matrix, $R \succ 0$ is the control cost matrix, and $P \succeq 0$ is the terminal cost matrix.

**Goal:** Formulate the trajectory optimization problem as a standard Quadratic Program (QP), prove strict convexity, derive the condensed horizon matrix representation, and establish the Model Predictive Control (MPC) receding horizon framework.

---

## Part I: Condensed QP Trajectory Optimization Reformulation

### Step 1: State Evolution Expansion

By recursive substitution of the system dynamics $x_{k+1} = A x_k + B u_k$ starting from initial state $x_0$, any future state $x_k$ can be expressed as an explicit linear function of $x_0$ and the control sequence $U = [u_0^T, u_1^T, \dots, u_{N-1}^T]^T$:

$$
\begin{aligned}
x_1 &= A x_0 + B u_0 \\
x_2 &= A(A x_0 + B u_0) + B u_1 = A^2 x_0 + A B u_0 + B u_1 \\
&\;\;\vdots \\
x_k &= A^k x_0 + \sum_{j=0}^{k-1} A^{k-1-j} B u_j
\end{aligned}
$$

### Step 2: Matrix Stacking (Batch Form)

Stacking all states $X = [x_0^T, x_1^T, \dots, x_N^T]^T \in \mathbb{R}^{(N+1)n}$ into a single vector yields the linear batch equation:

$$X = \mathcal{S}_x x_0 + \mathcal{S}_u U$$

where the transition matrices $\mathcal{S}_x \in \mathbb{R}^{(N+1)n \times n}$ and $\mathcal{S}_u \in \mathbb{R}^{(N+1)n \times Nm}$ are defined as:

$$\mathcal{S}_x = \begin{bmatrix} I \\ A \\ A^2 \\ \vdots \\ A^N \end{bmatrix}, \quad \mathcal{S}_u = \begin{bmatrix} 
0 & 0 & \cdots & 0 \\
B & 0 & \cdots & 0 \\
AB & B & \cdots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
A^{N-1}B & A^{N-2}B & \cdots & B 
\end{bmatrix}$$

### Step 3: Quadratic Program (QP) Cost Expansion

Substituting $X = \mathcal{S}_x x_0 + \mathcal{S}_u U$ into the objective function $J$:

$$J(U) = X^T \mathcal{Q}_{\text{batch}} X + U^T \mathcal{R}_{\text{batch}} U$$

where $\mathcal{Q}_{\text{batch}} = \text{blockdiag}(Q, Q, \dots, Q, P)$ and $\mathcal{R}_{\text{batch}} = \text{blockdiag}(R, R, \dots, R)$. Expanding this yields a standard Quadratic Program in vector form:

$$J(U) = \frac{1}{2} U^T H U + f^T U + c$$

where:
- $H = \mathcal{S}_u^T \mathcal{Q}_{\text{batch}} \mathcal{S}_u + \mathcal{R}_{\text{batch}}$
- $f = \mathcal{S}_u^T \mathcal{Q}_{\text{batch}} \mathcal{S}_x x_0$
- $c = x_0^T \mathcal{S}_x^T \mathcal{Q}_{\text{batch}} \mathcal{S}_x x_0$

---

## Part II: Convexity & Optimality Proof

### Step 1: Hessian Positive-Definiteness

The Hessian matrix $\nabla_U^2 J(U)$ of the objective function with respect to the control sequence $U$ is:

$$\nabla_U^2 J(U) = H = \mathcal{S}_u^T \mathcal{Q}_{\text{batch}} \mathcal{S}_u + \mathcal{R}_{\text{batch}}$$

1. Since $Q \succeq 0$ and $P \succeq 0$, the block-diagonal matrix $\mathcal{Q}_{\text{batch}}$ is positive semi-definite ($\mathcal{Q}_{\text{batch}} \succeq 0$). Thus, $\mathcal{S}_u^T \mathcal{Q}_{\text{batch}} \mathcal{S}_u \succeq 0$.
2. Since $R \succ 0$ for all control inputs, $\mathcal{R}_{\text{batch}}$ is strictly positive definite ($\mathcal{R}_{\text{batch}} \succ 0$).
3. The sum of a positive semi-definite matrix and a strictly positive definite matrix is strictly positive definite:

$$H \succ 0$$

### Step 2: Global Optimality

Because the Hessian $H \succ 0$ everywhere and the box constraints $U_{\min} \le U \le U_{\max}$ define a convex polyhedron, the constrained finite-horizon control problem is a **strictly convex Quadratic Program**. 

Therefore, a unique global optimal control sequence $U^\star = [u_0^\star, u_1^\star, \dots, u_{N-1}^\star]^T$ exists and can be efficiently solved in polynomial time via interior-point methods.

---

## Part III: Model Predictive Control (MPC) Receding Horizon Framework

### The Receding Horizon Algorithm:

1. **Measure State:** At current time step $t$, obtain the system state $x(t)$.
2. **Solve QP:** Solve the finite-horizon optimal control problem over horizon $N$ to obtain the optimal control sequence $U^\star(t) = \{u_0^\star, u_1^\star, \dots, u_{N-1}^\star\}$.
3. **Apply Control:** Apply only the first control action to the plant:
   $$u(t) = u_0^\star(t)$$
4. **Advance Time:** Increment $t \leftarrow t + 1$, observe new state $x(t+1)$, and repeat the optimization loop.

This closed-loop feedback mechanism provides robustness against external disturbances, unmodeled dynamics, and actuator saturation limits.
