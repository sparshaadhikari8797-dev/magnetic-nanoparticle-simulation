# =============================================================
# Experiment 1 — Capture Efficiency vs Magnetic Force Strength
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
U_max = 2.0
noise = 0.5
x_magnet = 250.0
y_magnet = 0.0
r_capture = 5.0

def flow_velocity(y):
    return U_max * 4 * y * (H - y) / H**2

def run_simulation(mag_force):
    captured = 0

    for p in range(n_particles):
        x = 0.0
        y = np.random.uniform(5, H - 5)

        for step in range(n_steps):
            vx = flow_velocity(y)
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

# magnetic force values to test
mag_force_values = [0.05, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0]
efficiencies = []

print("Running magnetic force sweep...")
for mag in mag_force_values:
    runs = [run_simulation(mag) for _ in range(3)]
    avg = np.mean(runs)
    efficiencies.append(avg)
    print(f"mag_force={mag:.2f} → efficiency={avg:.2%}")

# plot Figure 2
plt.figure(figsize=(8, 5))
plt.plot(mag_force_values, efficiencies, marker='o',
         linewidth=2, color='darkblue')
plt.xlabel('Magnetic force strength')
plt.ylabel('Capture efficiency')
plt.title('Figure 2 — Capture Efficiency vs Magnetic Force Strength\n'
          f'U_max={U_max}, noise={noise}, n_particles=50')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figure2_magnetic_sweep.png', dpi=300)
plt.show()
print("Done. figure2_magnetic_sweep.png saved.")