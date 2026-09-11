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
