# Proof 2: Controllability & Observability Rank Conditions

## Overview
This module derives and validates the algebraic conditions for controllability and observability in continuous Linear Time-Invariant (LTI) systems defined by:

$$
\dot{x}(t) = Ax(t) + Bu(t), \quad x(t) \in \mathbb{R}^n, \, u(t) \in \mathbb{R}^m
$$
$$
y(t) = Cx(t) + Du(t), \quad y(t) \in \mathbb{R}^p
$$

---

## Part 1: Controllability Rank Condition

### Definition & State Trajectory
A system is **controllable** if there exists an unconstrained control input $u(t)$ that transfers any initial state $x(0) = x_0$ to any final state $x(t_f) = x_f$ in finite time $t_f > 0$.

The analytical solution to the state-space dynamic equation is given by:

$$
x(t_f) = e^{A t_f} x_0 + \int_{0}^{t_f} e^{A(t_f - \tau)} B u(\tau) \, d\tau
$$

Rearranging terms yields the reachable state vector:

$$
x_f - e^{A t_f} x_0 = \int_{0}^{t_f} e^{A(t_f - \tau)} B u(\tau) \, d\tau
$$

---

### Application of Cayley-Hamilton Theorem
By the **Cayley-Hamilton Theorem**, every matrix $A \in \mathbb{R}^{n \times n}$ satisfies its own characteristic polynomial $p(\lambda) = \det(\lambda I - A) = 0$
