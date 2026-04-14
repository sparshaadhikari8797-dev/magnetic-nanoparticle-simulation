# =============================================================
# Near-Wall Corrected Model
# Author: Sparsha Adhikari
# Same as bulk model but adds wall correction factor
# =============================================================

import numpy as np
import matplotlib.pyplot as plt

L = 500.0
H = 100.0

dt = 0.1
n_steps = 10000
n_particles = 50

noise = 0.5
x_magnet = 250.0
y_magnet = 0.0
r_capture = 5.0

def flow_velocity(y, U_max):
    return U_max * 4 * y * (H - y) / H**2

def wall_correction(y):
    # distance to nearest wall
    dist_to_wall = min(y, H - y)
    dist_to_wall = max(dist_to_wall, 0.1)
    # correction factor — increases drag near wall
    return 1.0 + (r_capture / dist_to_wall)

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

            # near-wall correction
            wc = wall_correction(y)
            corrected_noise = noise / wc

            vx += np.random.normal(0, corrected_noise)
            vy += np.random.normal(0, corrected_noise)

            # slow down near wall
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

# test run
if __name__ == "__main__":
    print("Testing near-wall model...")
    eff = run_simulation(mag_force=0.4, U_max=2.0)
    print(f"Capture efficiency: {eff:.2%}")
    print("Near-wall model working.")