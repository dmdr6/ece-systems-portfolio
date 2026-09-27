"""
Project 5: Sensor Calibration & Regression
Models a temperature sensor (V = a*T + b + noise), estimates parameters using 
OLS and Gradient Descent, evaluates robustness to outliers and regularization, 
and recovers temperature from held-out voltage test readings.
"""

import numpy as np
import matplotlib.pyplot as plt

# Set standard figure styling for clean outputs
plt.rcParams['figure.figsize'] = (8, 5)
plt.rcParams['axes.grid'] = True


# Helper Functions

def fit_ridge(X, V, lmbda):
    """
    Fits Ridge regression without penalizing the intercept parameter b.
    theta = (X^T * X + lambda * P)^(-1) * X^T * V
    """
    P = np.eye(X.shape[1])
    P[1, 1] = 0.0  # Do not penalize intercept b
    theta_ridge = np.linalg.inv(X.T @ X + lmbda * P) @ X.T @ V
    return theta_ridge


def gradient_descent(X, V, lr=1e-4, iterations=5000):
    """
    Manual Gradient Descent implementation for MSE loss.
    """
    n = len(V)
    theta = np.zeros(2)
    loss_history = []
    
    for _ in range(iterations):
        V_pred = X @ theta
        loss = (1 / n) * np.sum((V - V_pred) ** 2)
        loss_history.append(loss)
        
        gradient = - (2 / n) * X.T @ (V - V_pred)
        theta = theta - lr * gradient
        
    return theta, loss_history


def evaluate_metrics(V_true, V_pred, theta_est, theta_true):
    """
    Calculates MSE, RMSE, MAE, and L2 Parameter Error.
    """
    mse = np.mean((V_true - V_pred) ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(V_true - V_pred))
    param_err = np.linalg.norm(theta_est - theta_true)
    return mse, rmse, mae, param_err


# Main Execution Workflow

def main():
    print("==================================================")
    print("    PROJECT 5: SENSOR CALIBRATION & REGRESSION    ")
    print("==================================================\n")

    # Task 1: Generate Simulated Sensor Data
    print("--> Task 1: Generating Simulated Sensor Data...")
    np.random.seed(42)
    
    a_true = 0.05    # Sensitivity (Volts/°C)
    b_true = 0.5     # Offset / Intercept (Volts)
    noise_std = 0.1  # Gaussian noise standard deviation
    n_samples = 100

    T = np.linspace(0, 100, n_samples)
    epsilon = np.random.normal(0, noise_std, size=n_samples)
    
    V_true = a_true * T + b_true
    V_measured = V_true + epsilon

    # Design Matrix X (Column of Temperatures, Column of Ones)
    X = np.column_stack((T, np.ones(n_samples)))

    plt.figure()
    plt.scatter(T, V_measured, color='blue', alpha=0.6, label='Noisy Measured Voltage (V)')
    plt.plot(T, V_true, color='red', linewidth=2, label=f'True Relation ($V = {a_true}T + {b_true}$)')
    plt.xlabel('True Temperature T (°C)')
    plt.ylabel('Measured Voltage V (Volts)')
    plt.title('Task 1: Simulated Temperature Sensor')
    plt.legend()
    plt.show()


    # Task 2: Ordinary Least Squares (OLS) from Scratch
    print("\n--> Task 2: Fitting OLS via Closed-Form Solution...")
    
    # theta = (X^T * X)^(-1) * X^T * V
    theta_ols = np.linalg.inv(X.T @ X) @ X.T @ V_measured
    a_ols, b_ols = theta_ols[0], theta_ols[1]

    print(f"True Parameters:      a = {a_true:.5f}, b = {b_true:.5f}")
    print(f"Estimated (OLS):      a = {a_ols:.5f}, b = {b_ols:.5f}")
    print(f"Parameter Error (a):  {abs(a_ols - a_true):.5f}")
    print(f"Parameter Error (b):  {abs(b_ols - b_true):.5f}")


    # Task 3: Gradient Descent from Scratch
    print("\n--> Task 3: Running Gradient Descent...")
    
    learning_rates = [1e-5, 5e-5, 1e-4]
    iterations = 5000

    plt.figure()
    for lr in learning_rates:
        theta_gd, loss_hist = gradient_descent(X, V_measured, lr=lr, iterations=iterations)
        plt.plot(range(iterations), loss_hist, label=f'LR = {lr}')
        print(f"GD (lr={lr:.0e}): a = {theta_gd[0]:.5f}, b = {theta_gd[1]:.5f} | Final Loss = {loss_hist[-1]:.6f}")

    plt.xlabel('Iteration')
    plt.ylabel('MSE Loss J(θ)')
    plt.yscale('log')
    plt.title('Task 3: Gradient Descent Loss Convergence')
    plt.legend()
    plt.show()


    # Task 4: Outlier Experiment
    print("\n--> Task 4: Introducing Outliers & Evaluating Robustness...")
    
    n_outliers = int(0.10 * n_samples)  # 10% outliers
    outlier_idx = np.random.choice(n_samples, size=n_outliers, replace=False)

    V_corrupted = V_measured.copy()
    V_corrupted[outlier_idx] += np.random.uniform(1.5, 3.0, size=n_outliers)

    theta_corrupted = np.linalg.inv(X.T @ X) @ X.T @ V_corrupted
    a_out, b_out = theta_corrupted[0], theta_corrupted[1]

    rmse_clean = np.sqrt(np.mean((V_measured - X @ theta_ols) ** 2))
    rmse_corrupted = np.sqrt(np.mean((V_corrupted - X @ theta_corrupted) ** 2))

    print(f"Clean Data OLS:     a = {a_ols:.5f}, b = {b_ols:.5f} | RMSE = {rmse_clean:.5f}")
    print(f"Corrupted Data OLS: a = {a_out:.5f}, b = {b_out:.5f} | RMSE = {rmse_corrupted:.5f}")
    print(f"Parameter Shift:    Δa = {abs(a_out - a_ols):.5f}, Δb = {abs(b_out - b_ols):.5f}")

    plt.figure()
    plt.scatter(T, V_measured, color='blue', alpha=0.4, label='Clean Measurements')
    plt.scatter(T[outlier_idx], V_corrupted[outlier_idx], color='red', marker='x', s=80, label='Corrupted Outliers (10%)')
    plt.plot(T, X @ theta_ols, 'g--', linewidth=2, label=f'Clean OLS (a={a_ols:.4f})')
    plt.plot(T, X @ theta_corrupted, 'r-', linewidth=2, label=f'Corrupted OLS (a={a_out:.4f})')
    plt.xlabel('True Temperature T (°C)')
    plt.ylabel('Measured Voltage V (Volts)')
    plt.title('Task 4: OLS Sensitivity to Corrupted Outliers')
    plt.legend()
    plt.show()


    # Task 5: Ridge Regression
    print("\n--> Task 5: Ridge Regression Parameter Shrinkage...")
    
    lambdas = [0.0, 10.0, 100.0, 1000.0, 10000.0]
    slopes, intercepts = [], []

    print(f"{'Lambda (λ)':<12} | {'a (Slope)':<10} | {'b (Intercept)':<12} | {'Norm ||θ||':<10}")
    print("-" * 52)
    
    for lmb in lambdas:
        t_r = fit_ridge(X, V_measured, lmbda=lmb)
        slopes.append(t_r[0])
        intercepts.append(t_r[1])
        print(f"{lmb:<12.1f} | {t_r[0]:<10.5f} | {t_r[1]:<12.5f} | {np.linalg.norm(t_r):<10.5f}")

    plt.figure()
    plt.plot(lambdas, slopes, 'o-', color='darkorange', label='Slope (a)')
    plt.xscale('log')
    plt.xlabel('Regularization Strength λ (Log Scale)')
    plt.ylabel('Parameter Value')
    plt.title('Task 5: Parameter Shrinkage under Ridge Regression')
    plt.legend()
    plt.show()


    # Task 6: Model Evaluation Benchmark
    print("\n--> Task 6: Running Comprehensive Model Benchmark...")
    
    noise_levels = [0.05, 0.20]
    outlier_pcts = [0.0, 0.10]
    lambdas_eval = [0.0, 100.0]
    theta_true_vec = np.array([a_true, b_true])

    print(f"{'Noise':<6} | {'Outliers':<8} | {'λ':<6} | {'MSE':<8} | {'RMSE':<8} | {'MAE':<8} | {'Param Err':<10}")
    print("-" * 70)

    for n_std in noise_levels:
        for out_p in outlier_pcts:
            eps_exp = np.random.normal(0, n_std, size=n_samples)
            V_exp = a_true * T + b_true + eps_exp
            
            if out_p > 0:
                n_out_exp = int(out_p * n_samples)
                idx_exp = np.random.choice(n_samples, size=n_out_exp, replace=False)
                V_exp[idx_exp] += np.random.uniform(2.0, 4.0, size=n_out_exp)
                
            for lmb in lambdas_eval:
                t_est = fit_ridge(X, V_exp, lmbda=lmb)
                V_pred = X @ t_est
                mse, rmse, mae, perr = evaluate_metrics(V_true, V_pred, t_est, theta_true_vec)
                print(f"{n_std:<6.2f} | {out_p*100:<7.0f}% | {lmb:<6.0f} | {mse:<8.4f} | {rmse:<8.4f} | {mae:<8.4f} | {perr:<10.5f}")


    # Task 7: Final Calibration & Held-Out Test Recovery
    print("\n--> Task 7: Calibration on Unknown Sensor & Test Recovery...")
    
    np.random.seed(101)
    T_train = np.random.uniform(0, 100, size=80)
    T_test  = np.random.uniform(0, 100, size=20)

    V_train = a_true * T_train + b_true + np.random.normal(0, noise_std, size=80)
    V_test  = a_true * T_test  + b_true + np.random.normal(0, noise_std, size=20)

    # 1. Fit Calibration Parameters on Training Data
    X_train = np.column_stack((T_train, np.ones(len(T_train))))
    theta_cal = np.linalg.inv(X_train.T @ X_train) @ X_train.T @ V_train
    a_est, b_est = theta_cal[0], theta_cal[1]

    # 2. Temperature Inversion on Unseen Test Voltages: T_hat = (V - b) / a
    T_pred_test = (V_test - b_est) / a_est

    # 3. Evaluate Recovery Accuracy
    mae_temp = np.mean(np.abs(T_test - T_pred_test))
    rmse_temp = np.sqrt(np.mean((T_test - T_pred_test) ** 2))

    print(f"Calibrated Parameters:    a = {a_est:.5f} V/°C, b = {b_est:.5f} V")
    print(f"Test Set Temperature MAE:   {mae_temp:.3f} °C")
    print(f"Test Set Temperature RMSE:  {rmse_temp:.3f} °C")

    plt.figure()
    plt.scatter(T_test, T_pred_test, color='purple', s=60, label='Recovered Temperatures')
    plt.plot([0, 100], [0, 100], 'k--', label='Ideal 1:1 Calibration Line')
    plt.xlabel('True Held-Out Temperature (°C)')
    plt.ylabel('Recovered Estimated Temperature (°C)')
    plt.title('Task 7: Temperature Recovery on Unseen Test Readings')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
