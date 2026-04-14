# =============================================================
# Experiment 2 — Capture Efficiency vs Flow Velocity
# Author: Sparsha Adhikari
# =============================================================

import numpy as np
import matplotlib.pyplot as plt

# Channel geometry
L = 500.0
H = 100.0

# Simulation parameters
dt = 0.1
n_steps = 10000
n_particles = 50

# Fixed parameters for this experiment
mag_force = 0.4
noise = 0.5
x_magnet = 250.0
y_magnet = 0.0
r_capture = 5.0

def flow_velocity(y, U_max):
    return U_max * 4 * y * (H - y) / H**2

def run_simulation(U_max):
    captured = 0

    for p in range(n_particles):
        x = 0.0
        y = np.random.uniform(5, H - 5)

        for step in range(n_steps):
            vx = flow_velocity(y, U_max)
            vy = 0.0

            dx = x_magnet - x
            dy = y_magnet - y
            dist = max(np.sqrt(dx**2 + dy**2), r_capture)
            vx += mag_force * dx / dist
            vy += mag_force * dy / dist

            vx += np.random.normal(0, noise)
            vy += np.random.normal(0, noise)

            x += vx * dt
            y += vy * dt

            if y < 0: y = 0
            if y > H: y = H
            if x < 0: x = 0

            dist = np.sqrt((x - x_magnet)**2 + (y - y_magnet)**2)
            if dist < r_capture:
                captured += 1
                break

            if x > L:
                break

    return captured / n_particles

# flow velocity values to test
flow_values = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.0, 10.0]
efficiencies = []

print("Running flow velocity sweep...")
for U in flow_values:
    runs = [run_simulation(U) for _ in range(3)]
    avg = np.mean(runs)
    efficiencies.append(avg)
    print(f"U_max={U:.1f} → efficiency={avg:.2%}")

# plot Figure 3
plt.figure(figsize=(8, 5))
plt.plot(flow_values, efficiencies, marker='o',
         linewidth=2, color='darkred')
plt.xlabel('Flow velocity (U_max)')
plt.ylabel('Capture efficiency')
plt.title('Figure 3 — Capture Efficiency vs Flow Velocity\n'
          f'mag_force={mag_force}, noise={noise}, n_particles=50')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figure3_flow_sweep.png', dpi=300)
plt.show()
print("Done. figure3_flow_sweep.png saved.")