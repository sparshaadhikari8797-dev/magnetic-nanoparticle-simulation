# =============================================================
# Magnetic Nanoparticle Capture in Microfluidic Channel
# Author: Sparsha Adhikari
# Model: Bulk Langevin Dynamics — Baseline Simulation
# Units: Micrometers (length), dimensionless time
# Goal: Simulate nanoparticle transport and magnetic capture
#       in a 2D microfluidic channel for drug delivery research
# =============================================================

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# CHANNEL GEOMETRY
# -------------------------------------------------------------
L = 500.0    # channel length in micrometers
H = 100.0    # channel height in micrometers

# -------------------------------------------------------------
# SIMULATION PARAMETERS
# -------------------------------------------------------------
dt = 0.1          # timestep
n_steps = 10000   # maximum steps per particle
n_particles = 50  # number of particles to simulate

# -------------------------------------------------------------
# PHYSICS PARAMETERS
# tune these to study different capture regimes
# -------------------------------------------------------------
U_max = 2.0        # maximum flow velocity (parabolic profile)
mag_force = 0.4    # magnetic force strength — increase to capture more
noise = 0.5        # Brownian motion intensity — thermal random kicks
x_magnet = 250.0   # magnet x position (channel midpoint)
y_magnet = 0.0     # magnet at bottom wall
r_capture = 5.0    # capture radius in micrometers

# -------------------------------------------------------------
# PARABOLIC FLOW PROFILE (Poiseuille flow)
# velocity is zero at walls, maximum at channel center
# -------------------------------------------------------------
def flow_velocity(y):
    return U_max * 4 * y * (H - y) / H**2

# -------------------------------------------------------------
# MAIN SIMULATION LOOP
# each particle starts at inlet (x=0) at random y position
# forces acting: flow drag + magnetic attraction + Brownian noise
# particle stops when: captured by magnet OR exits channel
# -------------------------------------------------------------
def run_simulation():
    captured = 0
    trajectories = []

    for p in range(n_particles):
        # random starting position at channel inlet
        x = 0.0
        y = np.random.uniform(5, H - 5)

        x_traj = [x]
        y_traj = [y]

        for step in range(n_steps):

            # 1. flow velocity at current y position
            vx = flow_velocity(y)
            vy = 0.0

            # 2. magnetic force toward magnet position
            dx = x_magnet - x
            dy = y_magnet - y
            dist = max(np.sqrt(dx**2 + dy**2), r_capture)
            vx += mag_force * dx / dist
            vy += mag_force * dy / dist

            # 3. Brownian motion — random thermal kicks
            vx += np.random.normal(0, noise)
            vy += np.random.normal(0, noise)

            # 4. update particle position
            x += vx * dt
            y += vy * dt

            # 5. wall boundary conditions — particle cannot leave channel
            if y < 0: y = 0
            if y > H: y = H
            if x < 0: x = 0

            x_traj.append(x)
            y_traj.append(y)

            # 6. check if particle is captured by magnet
            dist = np.sqrt((x - x_magnet)**2 + (y - y_magnet)**2)
            if dist < r_capture:
                captured += 1
                break

            # 7. check if particle has exited the channel
            if x > L:
                break

        trajectories.append((x_traj, y_traj))

    efficiency = captured / n_particles
    return efficiency, trajectories

# -------------------------------------------------------------
# FIGURE 1 — PARTICLE TRAJECTORY VISUALIZATION
# shows path of each particle through the channel
# captured particles curve toward magnet
# escaped particles exit through the right side
# -------------------------------------------------------------
def plot_trajectories(trajectories):
    fig, ax = plt.subplots(figsize=(10, 4))

    for x_traj, y_traj in trajectories:
        ax.plot(x_traj, y_traj, alpha=0.4, linewidth=0.8)

    # channel walls
    ax.axhline(y=0, color='black', linewidth=2, label='Wall')
    ax.axhline(y=H, color='black', linewidth=2)

    # magnet position
    ax.scatter(x_magnet, y_magnet, color='red',
               zorder=5, s=150, label='Magnet')

    ax.set_xlabel('x position (micrometers)')
    ax.set_ylabel('y position (micrometers)')
    ax.set_title('Figure 1 — Nanoparticle Trajectories in Microfluidic Channel\n'
                 f'U_max={U_max}, mag_force={mag_force}, noise={noise}')
    ax.legend()
    plt.tight_layout()
    plt.savefig('figure1_trajectories.png', dpi=300)
    plt.show()

# -------------------------------------------------------------
# RUN
# -------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("Magnetic Nanoparticle Capture Simulation")
    print("Author: Sparsha Adhikari")
    print("=" * 50)
    print(f"Particles: {n_particles} | Steps: {n_steps} | dt: {dt}")
    print(f"U_max: {U_max} | mag_force: {mag_force} | noise: {noise}")
    print("-" * 50)
    print("Running simulation...")

    efficiency, trajectories = run_simulation()

    print(f"Capture efficiency: {efficiency:.2%}")
    print("-" * 50)
    print("Generating Figure 1...")
    plot_trajectories(trajectories)
    print("Done. figure1_trajectories.png saved.")
    print("=" * 50)