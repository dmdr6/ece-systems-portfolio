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

