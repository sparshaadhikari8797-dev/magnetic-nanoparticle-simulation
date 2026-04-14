# =============================================================
# Comparison — Bulk vs Near-Wall Model
# Author: Sparsha Adhikari
# =============================================================

import numpy as np
import matplotlib.pyplot as plt

L = 500.0
H = 100.0
dt = 0.1
n_steps = 10000
n_particles = 30
noise = 0.5
x_magnet = 250.0
y_magnet = 0.0
r_capture = 5.0

def flow_velocity(y, U_max):
    return U_max * 4 * y * (H - y) / H**2

def wall_correction(y):
    dist_to_wall = max(min(y, H - y), 0.1)
    return 1.0 + (r_capture / dist_to_wall)

def run_bulk(mag_force, U_max):
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

def run_near_wall(mag_force, U_max):
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
            wc = wall_correction(y)
            vx += np.random.normal(0, noise / wc)
            vy += np.random.normal(0, noise / wc)
            vx /= wc
            vy /= wc
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

# sweep magnetic force
mag_values = [0.05, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0]
U_fixed = 2.0

bulk_eff = []
nw_eff = []

print("Running comparison sweep...")
for mag in mag_values:
    b = np.mean([run_bulk(mag, U_fixed) for _ in range(3)])
    n = np.mean([run_near_wall(mag, U_fixed) for _ in range(3)])
    bulk_eff.append(b)
    nw_eff.append(n)
    print(f"mag={mag:.2f} → bulk={b:.2%} | near-wall={n:.2%}")

# plot comparison
plt.figure(figsize=(9, 5))
plt.plot(mag_values, bulk_eff, marker='o', linewidth=2,
         color='darkblue', label='Bulk model')
plt.plot(mag_values, nw_eff, marker='s', linewidth=2,
         color='darkred', label='Near-wall corrected')
plt.xlabel('Magnetic force strength')
plt.ylabel('Capture efficiency')
plt.title('Figure 5 — Bulk vs Near-Wall Model Comparison\n'
          f'U_max={U_fixed}, noise={noise}, n_particles=30')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figure5_comparison.png', dpi=300)
plt.show()
print("Done. figure5_comparison.png saved.")