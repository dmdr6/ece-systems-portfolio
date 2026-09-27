import numpy as np
import matplotlib.pyplot as plt

def objective_function(x, Q, b, c):
    return 0.5 * x.T @ Q @ x + b.T @ x + c

def compute_gradient(x, Q, b):
    return Q @ x + b

def run_gradient_descent(x0, Q, b, c, alpha, max_iters=50):
    trajectory = [x0.copy()]
    costs = [objective_function(x0, Q, b, c)]
    gradients = [compute_gradient(x0, Q, b)]
    
    x = x0.copy()
    for _ in range(max_iters):
        grad = compute_gradient(x, Q, b)
        x = x - alpha * grad
        trajectory.append(x.copy())
        costs.append(objective_function(x, Q, b, c))
        gradients.append(compute_gradient(x, Q, b))
        if np.isnan(x).any() or np.isinf(x).any():
            break
            
    return np.array(trajectory), np.array(costs), np.array(gradients)

def main():
    np.random.seed(42)
    
    Q = np.array([[3.0, 1.0], 
                  [1.0, 2.0]])
    b = np.array([-2.0, -4.0])
    c = 1.5
    
    eigenvalues, eigenvectors = np.linalg.eig(Q)
    lambda_min = np.min(eigenvalues)
    lambda_max = np.max(eigenvalues)
    
    x_star = -np.linalg.inv(Q) @ b
    f_star = objective_function(x_star, Q, b, c)
    
    alpha_max = 2.0 / lambda_max
    alpha_opt = 2.0 / (lambda_min + lambda_max)
    
    learning_rates = {
        'Slow Rate': 0.05,
        'Optimal Rate': alpha_opt,
        'Oscillatory Rate': 0.42,
        'Divergent Rate': alpha_max * 1.05
    }
    
    print("=" * 60)
    print("PROOF #5 NUMERICAL VERIFICATION: QUADRATIC CONVEXITY & GD")
    print("=" * 60)
    print(f"Hessian Matrix Q:\n{Q}")
    print(f"Eigenvalues of Q: {eigenvalues}")
    print(f"Hessian Positive Definite: {np.all(eigenvalues > 0)}")
    print(f"Analytical Global Minimum (x*): {x_star}")
    print(f"Minimum Objective Value f(x*): {f_star:.6f}")
    print(f"Theoretical Upper Step-Size Bound (2 / lambda_max): {alpha_max:.6f}")
    print(f"Theoretical Optimal Step Size: {alpha_opt:.6f}")
    print("-" * 60)
    
    x0 = np.array([3.0, 3.0])
    max_iters = 30
    results = {}
    
    for label, alpha in learning_rates.items():
        traj, costs, grads = run_gradient_descent(x0, Q, b, c, alpha, max_iters)
        results[label] = (traj, costs, grads, alpha)
        final_x = traj[-1]
        final_err = np.linalg.norm(final_x - x_star) if not np.isnan(final_x).any() else np.inf
        print(f"[{label}] alpha = {alpha:.4f} | Final x: {np.round(final_x, 4)} | Distance to x*: {final_err:.6f}")
        
    fig = plt.figure(figsize=(16, 6))
    
    ax1 = fig.add_subplot(1, 2, 1)
    
    x1_vals = np.linspace(-1.0, 4.0, 200)
    x2_vals = np.linspace(-1.0, 4.0, 200)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)
    Z = np.zeros_like(X1)
    
    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):
            pt = np.array([X1[i, j], X2[i, j]])
            Z[i, j] = objective_function(pt, Q, b, c)
            
    ax1.contour(X1, X2, Z, levels=30, cmap='viridis', alpha=0.6)
    ax1.plot(x_star[0], x_star[1], 'r*', markersize=15, label='Global Min $x^*$')
    
    colors = {'Slow Rate': 'blue', 'Optimal Rate': 'green', 'Oscillatory Rate': 'orange', 'Divergent Rate': 'red'}
    
    for label, (traj, costs, grads, alpha) in results.items():
        if label == 'Divergent Rate':
            valid_traj = traj[:6]
        else:
            valid_traj = traj
            
        ax1.plot(valid_traj[:, 0], valid_traj[:, 1], 'o-', color=colors[label], label=f"{label} ($\\alpha$={alpha:.3f})", alpha=0.8, markersize=4)
        
        if label == 'Optimal Rate':
            for idx in range(0, min(5, len(valid_traj))):
                pt = valid_traj[idx]
                gr = grads[idx]
                ax1.quiver(pt[0], pt[1], -gr[0], -gr[1], color='black', angles='xy', scale_units='xy', scale=8, width=0.003, alpha=0.5)

    ax1.set_title('Optimization Trajectories & Contour Plot', fontsize=12, fontweight='bold')
    ax1.set_xlabel('$x_1$')
    ax1.set_ylabel('$x_2$')
    ax1.set_xlim([-1.0, 4.0])
    ax1.set_ylim([-1.0, 4.0])
    ax1.legend(loc='upper left', fontsize=9)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    ax2 = fig.add_subplot(1, 2, 2)
    
    for label, (traj, costs, grads, alpha) in results.items():
        iterations = np.arange(len(costs))
        ax2.plot(iterations, costs, 'o-', color=colors[label], label=f"{label} ($\\alpha$={alpha:.3f})", linewidth=1.5, markersize=3)
        
    ax2.axhline(f_star, color='black', linestyle=':', label='Min Cost $f(x^*)$')
    ax2.set_yscale('symlog')
    ax2.set_title('Objective Function Convergence $f(x_k)$ vs Iteration', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Iteration $k$')
    ax2.set_ylabel('Objective Value $f(x_k)$ (symlog scale)')
    ax2.set_xlim([0, max_iters])
    ax2.set_ylim([-5, 100])
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
