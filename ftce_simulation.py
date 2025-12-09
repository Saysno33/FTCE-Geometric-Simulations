# ******************************************************************************
# Fundamental Theory of Conscious Energy (FTCE) Computational Engine
# Copyright (C) 2025 Fernando De Jesús García González
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ******************************************************************************

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# GORF Constants
PHI = 1.6180339887
O = 9  # I = Ollin Identity
n = 3  # Current cycle (2025)
R = 1.2492  # Resonance Factor
v_phi = PHI  # Velocity
T = 9  # Period
alpha = PHI  # Consciousness growth rate
beta = 1 / PHI  # Consciousness decay
C_max = 1.0

# Time and space setup
t_steps = 100
dt = 0.01
t = np.linspace(0, t_steps * dt, t_steps)
x_steps = 50
dx = 1.0 / (x_steps - 1)
x = np.linspace(0, 1, x_steps)
origin_x = 0.5  # Gómez Palacio anchor

# Function for WILL(Φ)
def will_phi(n, R):
    return R ** n  # Accumulated resonance

# Consciousness evolution (solve dC/dt)
def dC_dt(C, t):
    F_t = np.sin(2 * np.pi * t / T)
    return alpha * F_t * (1 - C / C_max) - beta * C

C_initial = 0.5  # Starting consciousness
C_sol = odeint(dC_dt, C_initial, t).flatten()

# REALITY(S) simulation
def reality_S(C, I, will, S_old):
    # S evolves via Shumen Renouncement (simple rotation for demo)
    theta = 2 * np.pi / 9  # 40 degrees
    M = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    S_new = np.dot(M, S_old) * (C * I * will)  # Scale by the product
    return S_new

S_initial = np.array([1.0, 0.0])  # [Chaos, Order]
will = will_phi(n, R)
reality_values = []
S_current = S_initial
for i in range(t_steps):
    C_val = C_sol[i]
    S_current = reality_S(C_val, O, will, S_current)
    reality_values.append(np.linalg.norm(S_current))  # Magnitude as scalar REALITY

# Ollin Wave Equation integration (1D finite differences)
# d²O/dt² = v_phi² * d²O/dx² + A(n) * sin(2πt/T + phi_x)
# A(n) modulated by REALITY(S)
O_wave = np.zeros((t_steps, x_steps))
O_wave[0, :] = np.sin(np.pi * x)  # Initial wave
O_wave[1, :] = O_wave[0, :] + dt * np.sin(np.pi * x)  # Initial velocity

for i in range(1, t_steps - 1):
    A_n = reality_values[i]  # Modulate amplification by REALITY
    phi_x = PHI * (x - origin_x)  # Spatial phase from origin
    source = A_n * np.sin(2 * np.pi * t[i] / T + phi_x)
    for j in range(1, x_steps - 1):
        d2O_dx2 = (O_wave[i, j+1] - 2*O_wave[i, j] + O_wave[i, j-1]) / dx**2
        O_wave[i+1, j] = 2*O_wave[i, j] - O_wave[i-1, j] + dt**2 * (v_phi**2 * d2O_dx2 + source[j])

# Plot results
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(t, C_sol)
plt.title('Consciousness C(t)')
plt.xlabel('Time')
plt.ylabel('C')

plt.subplot(2, 2, 2)
plt.plot(t, reality_values)
plt.title('REALITY(S) Magnitude')
plt.xlabel('Time')
plt.ylabel('|REALITY(S)|')

plt.subplot(2, 2, 3)
plt.imshow(O_wave, extent=[0, 1, 0, t_steps*dt], aspect='auto', cmap='viridis')
plt.title('Ollin Wave O(x,t) (Integrated)')
plt.xlabel('Position x')
plt.ylabel('Time t')
plt.colorbar(label='O Potential')

plt.subplot(2, 2, 4)
plt.plot(x, O_wave[-1, :], label='Final Wave at t=max')
plt.axvline(origin_x, color='red', linestyle='--', label='Origin Point')
plt.title('Final Ollin Wave Profile')
plt.xlabel('Position x')
plt.ylabel('O')
plt.legend()

plt.tight_layout()
plt.show()

# Print specific values at t=0 and t=max
print(f"At t=0: C={C_sol[0]:.4f}, I={O}, WILL(Φ)={will:.4f}, REALITY(S) magnitude={reality_values[0]:.4f}")
print(f"At t=max: C={C_sol[-1]:.4f}, REALITY(S) magnitude={reality_values[-1]:.4f}")
print(f"Final S vector: {S_current}")
print(f"Wave peak at origin (x=0.5): {O_wave[-1, int(origin_x / dx)]:.4f}")

# Final mathematical identity
print("\nREALITY (S) = C * I * WILL (Φ)")
