import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional, List

def generate_ill_conditioned_data(
    m: int = 100, 
    n: int = 20, 
    condition_number: float = 1e6, 
    seed: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Generates synthetic ill-conditioned design matrix and target vector."""
    np.random.seed(seed)
    X_raw = np.random.randn(m, n)
    U, S, Vt = np.linalg.svd(X_raw, full_matrices=False)
    
    # Construct exponentially decaying singular values to induce high ill-conditioning
    S_new = np.logspace(0, -np.log10(condition_number), num=min(m, n))
    X = U @ np.diag(S_new) @ Vt
    
    true_w = np.random.randn(n)
    y = X @ true_w + 0.1 * np.random.randn(m)
    return X, y, true_w, S_new

def ridge_closed_form(X: np.ndarray, y: np.ndarray, lmbda: float) -> np.ndarray:
    """Computes the analytical Ridge closed-form solution using numerically stable solve."""
    m, n = X.shape
    A = X.T @ X + lmbda * np.eye(n)
    b = X.T @ y
    return np.linalg.solve(A, b)

def ridge_gradient_descent(
    X: np.ndarray, 
    y: np.ndarray, 
    lmbda: float, 
    alpha: Optional[float] = None, 
    max_iters: int = 5000, 
    tol: float = 1e-8
) -> Tuple[np.ndarray, List[float]]:
    """Optimizes Ridge regression objective using Gradient Descent from scratch."""
    m, n = X.shape
    w = np.zeros(n)
    cost_history = []
    
    # Calculate adaptive learning rate based on Lipschitz constant if not provided
    if alpha is None:
        max_eig = np.linalg.eigvalsh(2 * (X.T @ X + lmbda * np.eye(n)))[-1]
        alpha = 0.9 / max_eig
        
    for k in range(max_iters):
        grad = 2 * (X.T @ X @ w - X.T @ y + lmbda * w)
        w = w - alpha * grad
        
        cost = np.linalg.norm(X @ w - y)**2 + lmbda * np.linalg.norm(w)**2
        cost_history.append(cost)
        
        if k > 0 and abs(cost_history[-2] - cost_history[-1]) < tol:
            break
    else:
        print(f"Warning: Gradient descent for lambda={lmbda} reached max_iters without full convergence.")
            
    return w, cost_history

def compute_metrics(
    X: np.ndarray, 
    y: np.ndarray, 
    w: np.ndarray, 
    lmbda: float
) -> Tuple[float, float, float, float]:
    """Calculates key performance metrics: MSE, L2 norm, objective value, and Hessian condition number."""
    m, n = X.shape
    mse = float(np.mean((X @ w - y)**2))
    l2_norm = float(np.linalg.norm(w))
    obj_val = float(np.linalg.norm(X @ w - y)**2 + lmbda * (l2_norm**2))
    
    Hessian = 2 * (X.T @ X + lmbda * np.eye(n))
    eigvals = np.linalg.eigvalsh(Hessian)
    cond_num = float(eigvals[-1] / eigvals[0])
    
    return mse, l2_norm, obj_val, cond_num

def main() -> None:
    m, n = 100, 20
    X, y, true_w, S_vals = generate_ill_conditioned_data(m=m, n=n, condition_number=1e5)
    
    lambdas = [0.0, 1e-2, 1.0, 100.0, 10000.0]
    
    print("=" * 85)
    print("PROOF #6 NUMERICAL VERIFICATION: CLOSED-FORM VS GRADIENT DESCENT RIDGE REGRESSION")
    print("=" * 85)
    
    print(f"{'Lambda':<10} | {'Method':<15} | {'MSE':<10} | {'||w||_2':<10} | {'Obj J(w)':<12} | {'Max L2 Diff':<12} | {'Hessian Cond#':<12}")
    print("-" * 85)
    
    gd_histories = {}
    
    for lmbda in lambdas:
        w_cf = ridge_closed_form(X, y, lmbda)
        mse_cf, l2_cf, obj_cf, cond_cf = compute_metrics(X, y, w_cf, lmbda)
        
        w_gd, cost_hist = ridge_gradient_descent(X, y, lmbda, max_iters=5000)
        mse_gd, l2_gd, obj_gd, _ = compute_metrics(X, y, w_gd, lmbda)
        gd_histories[lmbda] = cost_hist
        
        diff = float(np.max(np.abs(w_cf - w_gd)))
        
        print(f"{lmbda:<10.2e} | {'Closed-Form':<15} | {mse_cf:<10.4f} | {l2_cf:<10.4f} | {obj_cf:<12.4f} | {'N/A':<12} | {cond_cf:<12.2e}")
        print(f"{'':<10} | {'Grad Descent':<15} | {mse_gd:<10.4f} | {l2_gd:<10.4f} | {obj_gd:<12.4f} | {diff:<12.2e} | {'N/A':<12}")
        print("-" * 85)
        
    dense_lambdas = np.logspace(-3, 5, 200)
    weights_path = []
    
    for lmb in dense_lambdas:
        w_l = ridge_closed_form(X, y, lmb)
        weights_path.append(w_l)
        
    weights_path = np.array(weights_path)
    
    plt.figure(figsize=(18, 5))
    
    plt.subplot(1, 3, 1)
    for i in range(n):
        plt.plot(dense_lambdas, weights_path[:, i], alpha=0.7)
    plt.xscale('log')
    plt.xlabel('Regularization Strength lambda (log scale)')
    plt.ylabel('Weight Coefficients w_i')
    plt.title('Ridge Trace: Weight Shrinkage Path')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.subplot(1, 3, 2)
    for lmbda in lambdas[1:]:
        hist = gd_histories[lmbda]
        plt.plot(hist[:200], label=f'lambda={lmbda}')
    plt.yscale('log')
    plt.xlabel('Iteration k')
    plt.ylabel('Objective Value J(w_k) (log scale)')
    plt.title('Gradient Descent Convergence')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.subplot(1, 3, 3)
    mses = [compute_metrics(X, y, ridge_closed_form(X, y, lmb), lmb)[0] for lmb in dense_lambdas]
    l2_norms = [compute_metrics(X, y, ridge_closed_form(X, y, lmb), lmb)[1] for lmb in dense_lambdas]
    
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    
    l1 = ax1.plot(dense_lambdas, mses, 'b-', label='MSE (Prediction Error)')
    l2 = ax2.plot(dense_lambdas, l2_norms, 'r--', label='||w||_2 (Weight Norm)')
    
    ax1.set_xscale('log')
    ax1.set_xlabel('Regularization Strength lambda')
    ax1.set_ylabel('Mean Squared Error', color='b')
    ax2.set_ylabel('L2 Norm ||w||_2', color='r')
    plt.title('Trade-off Spectrum: MSE vs Weight Norm')
    
    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center left')
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
