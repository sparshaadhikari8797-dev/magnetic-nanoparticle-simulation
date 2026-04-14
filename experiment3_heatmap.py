# =============================================================
# Experiment 3 — Capture Efficiency Heatmap
# Author: Sparsha Adhikari
# Sweeps both magnetic force and flow velocity simultaneously
# =============================================================

import numpy as np
import matplotlib.pyplot as plt

# Channel geometry
L = 500.0
H = 100.0

# Simulation parameters
dt = 0.1
n_steps = 10000
n_particles = 30

# Fixed parameters
noise = 0.5
x_magnet = 250.0
y_magnet = 0.0
r_capture = 5.0

def flow_velocity(y, U_max):
    return U_max * 4 * y * (H - y) / H**2

def run_simulation(mag_force, U_max):
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

# parameter ranges
mag_values  = [0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0]
flow_values = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.0]

results = np.zeros((len(mag_values), len(flow_values)))

print("Running heatmap sweep...")
for i, mag in enumerate(mag_values):
    for j, flow in enumerate(flow_values):
        eff = run_simulation(mag, flow)
        results[i, j] = eff
        print(f"mag={mag:.2f} flow={flow:.1f} → {eff:.2%}")

# plot Figure 4
plt.figure(figsize=(9, 6))
plt.imshow(results, origin='lower', aspect='auto',
           extent=[flow_values[0], flow_values[-1],
                   mag_values[0],  mag_values[-1]],
           cmap='viridis', vmin=0, vmax=1)
plt.colorbar(label='Capture efficiency')
plt.xlabel('Flow velocity (U_max)')
plt.ylabel('Magnetic force strength')
plt.title('Figure 4 — Capture Efficiency Heatmap\n'
          'Effect of flow velocity and magnetic strength')
plt.tight_layout()
plt.savefig('figure4_heatmap.png', dpi=300)
plt.show()
print("Done. figure4_heatmap.png saved.")