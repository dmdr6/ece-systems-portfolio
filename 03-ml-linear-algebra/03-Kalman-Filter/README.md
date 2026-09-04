# Kalman Filter Gain & Covariance Update Derivation

## Problem Statement

Given a discrete-time linear dynamic system governed by the state and measurement equations:

$$x_k = A x_{k-1} + B u_{k-1} + w_{k-1}, \quad x_k \in \mathbb{R}^n, \, u_k \in \mathbb{R}^m$$
$$z_k = H x_k + v_k, \quad z_k \in \mathbb{R}^p$$

Where $x_k$ is the true state, $z_k$ is the measurement, $w_k \sim \mathcal{N}(0, Q)$ is zero-mean process noise, and $v_k \sim \mathcal{N}(0, R)$ is zero-mean measurement noise with positive-definite covariance matrix $R = \mathbb{E}[v_k v_k^T] \succ 0$.

Let $\hat{x}_k^-$ denote the prior state estimate, $P_k^-$ denote the prior error covariance, and $e_k^- = x_k - \hat{x}_k^-$ denote the prior estimation error. Assuming the linear state estimate update:

$$\hat{x}_k^+ = \hat{x}_k^- + K_k (z_k - H \hat{x}_k^-)$$

Prove that the optimal feedback matrix $K_k$ that minimizes the mean-squared error (MSE) trace objective $\text{tr}(P_k^+)$ and its corresponding posterior covariance update $P_k^+$ are given by:

$$K_k = P_k^- H^T \left( H P_k^- H^T + R \right)^{-1}$$
$$P_k^+ = (I - K_k H) P_k^-$$

---

## Part I: Posterior Estimation Error Expansion

### Step 1: Linear Estimator Structure
The posterior state estimate $\hat{x}_k^+$ incorporates the innovation residual $(z_k - H \hat{x}_k^-)$ weighted by the gain matrix $K_k \in \mathbb{R}^{n \times p}$:

$$\hat{x}_k^+ = \hat{x}_k^- + K_k (z_k - H \hat{x}_k^-)$$

Substitute the measurement equation $z_k = H x_k + v_k$ into the update formula:

$$\hat{x}_k^+ = \hat{x}_k^- + K_k (H x_k + v_k - H \hat{x}_k^-) = \hat{x}_k^- + K_k H (x_k - \hat{x}_k^-) + K_k v_k$$

---

### Step 2: Derivation of the Posterior Error Vector
Define the posterior estimation error $e_k^+$ as the difference between the true state $x_k$ and the posterior estimate $\hat{x}_k^+$:

$$e_k^+ = x_k - \hat{x}_k^+$$

Substitute the expanded expression for $\hat{x}_k^+$ into the error equation:

$$e_k^+ = x_k - \left( \hat{x}_k^- + K_k H (x_k - \hat{x}_k^-) + K_k v_k \right)$$

Group terms with respect to the prior estimation error $e_k^- = x_k - \hat{x}_k^-$:

$$e_k^+ = (x_k - \hat{x}_k^-) - K_k H (x_k - \hat{x}_k^-) - K_k v_k = (I - K_k H) e_k^- - K_k v_k$$

---

## Part II: General Posterior Covariance Derivation (Joseph Form)

### Step 1: Covariance Expectation Expansion
The posterior error covariance matrix $P_k^+$ is defined as the expected value of the outer product of the posterior error vector:

$$P_k^+ = \mathbb{E}\left[ e_k^+ (e_k^+)^T \right]$$

Substitute the posterior error expression derived in Part I:

$$P_k^+ = \mathbb{E}\left[ \left( (I - K_k H) e_k^- - K_k v_k \right) \left( (I - K_k H) e_k^- - K_k v_k \right)^T \right]$$

Apply the transpose identity $(A - B)^T = A^T - B^T$ and expand the terms:

$$P_k^+ = \mathbb{E}\left[ (I - K_k H) e_k^- (e_k^-)^T (I - K_k H)^T - (I - K_k H) e_k^- v_k^T K_k^T - K_k v_k (e_k^-)^T (I - K_k H)^T + K_k v_k v_k^T K_k^T \right]$$

---

### Step 2: Uncorrelated Noise Elimination & General Form
By assumption, the prior estimation error $e_k^-$ depends only on state and measurement histories up to step $k-1$, making it uncorrelated with the current measurement noise $v_k$:

$$\mathbb{E}[e_k^- v_k^T] = \mathbf{0}_{n \times p}, \quad \mathbb{E}[v_k (e_k^-)^T] = \mathbf{0}_{p \times n}$$

Linear cross-terms vanish under expectation. Substituting $P_k^- = \mathbb{E}[e_k^- (e_k^-)^T]$ and $R = \mathbb{E}[v_k v_k^T]$ yields the general Joseph form update:

$$P_k^+ = (I - K_k H) P_k^- (I - K_k H)^T + K_k R K_k^T$$

---

## Part III: Minimum Mean-Squared Error (MMSE) Trace Optimization

### Step 1: Define Trace Objective Function
The optimal Kalman filter minimizes the total mean-squared estimation error:

$$J(K_k) = \mathbb{E}\left[ \| e_k^+ \|_2^2 \right] = \mathbb{E}\left[ (e_k^+)^T e_k^+ \right] = \text{tr}\left( \mathbb{E}\left[ e_k^+ (e_k^+)^T \right] \right) = \text{tr}(P_k^+)$$

Expand the Joseph form equation for $P_k^+$ explicitly:

$$P_k^+ = P_k^- - K_k H P_k^- - P_k^- H^T K_k^T + K_k H P_k^- H^T K_k^T + K_k R K_k^T$$

$$P_k^+ = P_k^- - K_k H P_k^- - P_k^- H^T K_k^T + K_k \left( H P_k^- H^T + R \right) K_k^T$$

---

### Step 2: Matrix Differentiation & Stationary Point Condition
Apply the trace matrix calculus identities for differentiation with respect to $K_k$:

$$\frac{\partial}{\partial K} \text{tr}(K A) = A^T, \quad \frac{\partial}{\partial K} \text{tr}(A K^T) = A, \quad \frac{\partial}{\partial K} \text{tr}(K B K^T) = 2 K B \quad \text{(for symmetric } B\text{)}$$

Compute the gradient of $\text{tr}(P_k^+)$ with respect to $K_k$:

$$\frac{\partial \text{tr}(P_k^+)}{\partial K_k} = -2 P_k^- H^T + 2 K_k \left( H P_k^- H^T + R \right)$$

Set the matrix derivative equal to zero:

$$-2 P_k^- H^T + 2 K_k \left( H P_k^- H^T + R \right) = 0 \implies K_k \left( H P_k^- H^T + R \right) = P_k^- H^T$$

Isolate $K_k$ by post-multiplying by the inverse matrix $\left( H P_k^- H^T + R \right)^{-1}$:

$$K_k = P_k^- H^T \left( H P_k^- H^T + R \right)^{-1} \quad \blacksquare$$

---

## Part IV: Simplified Posterior Covariance Derivation

### Step 1: Substitution of Optimal Gain Condition
From the optimality condition derived in Part III, Step 2:

$$K_k \left( H P_k^- H^T + R \right) = P_k^- H^T$$

Substitute this identity into the expanded posterior covariance formula for $P_k^+$:

$$P_k^+ = P_k^- - K_k H P_k^- - P_k^- H^T K_k^T + \left[ K_k \left( H P_k^- H^T + R \right) \right] K_k^T$$

$$P_k^+ = P_k^- - K_k H P_k^- - P_k^- H^T K_k^T + \left( P_k^- H^T \right) K_k^T$$

---

### Step 2: Algebraic Cancellation & Canonical Form
Cancel out the identical positive and negative transposed terms:

$$P_k^+ = P_k^- - K_k H P_k^-$$

Factor $P_k^-$ out to obtain the final algebraic result:

$$P_k^+ = (I - K_k H) P_k^- \quad \blacksquare$$
