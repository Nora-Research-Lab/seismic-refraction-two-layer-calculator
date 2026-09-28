import numpy as np
import matplotlib.pyplot as plt
import io
import math
import pandas as pd

def parse_distances_and_times(distance_str, time_str):
    """Parse comma-separated strings into arrays of floats. Raises ValueError."""
    if not distance_str or not time_str:
        raise ValueError("Both distance and time arrays must be provided.")
    distances = [float(x.strip()) for x in distance_str.split(',') if x.strip()]
    times = [float(x.strip()) for x in time_str.split(',') if x.strip()]

    if len(distances) != len(times):
        raise ValueError("Distance and time arrays must have the same length.")
    if len(distances) < 6:
        raise ValueError("At least 6 data points are required.")
    if any(d <= 0 for d in distances):
        raise ValueError("Distances must be positive.")
    if any(t < 0 for t in times):
        raise ValueError("Times must be non-negative.")

    # Sort by distance
    combined = sorted(zip(distances, times))
    distances, times = zip(*combined)
    return np.array(distances), np.array(times)

def compute_two_layer(distances, times, max_iter=10):
    """Two-layer refraction calculation using iterative intercept-time method."""
    N = len(distances)

    # Initial split: first 25% as direct
    split_idx = max(2, int(round(0.25 * N)))
    direct_mask = np.zeros(N, dtype=bool)
    direct_mask[:split_idx] = True

    prev_mask = None
    for _ in range(max_iter):
        if np.array_equal(direct_mask, prev_mask):
            break
        prev_mask = direct_mask.copy()

        # Fit direct arrivals
        idx_d = direct_mask
        idx_r = ~direct_mask
        if np.sum(idx_d) < 2 or np.sum(idx_r) < 2:
            raise ValueError("Not enough points in one of the subsets after iteration.")

        m1, b1 = np.polyfit(distances[idx_d], times[idx_d], 1)
        m2, b2 = np.polyfit(distances[idx_r], times[idx_r], 1)

        # Crossover distance
        if abs(m1 - m2) < 1e-12:
            raise ValueError("Slopes equal; cannot compute crossover distance.")

        Xc = (b2 - b1) / (m1 - m2)

        # Reassign: distances <= Xc -> direct; > Xc -> refracted
        new_mask = distances <= Xc
        # Ensure at least 2 points in each group
        if np.sum(new_mask) < 2 or np.sum(~new_mask) < 2:
            # Fall back to previous mask
            break
        direct_mask = new_mask

    # Final fit
    idx_d = direct_mask
    idx_r = ~direct_mask
    if np.sum(idx_d) < 2 or np.sum(idx_r) < 2:
        raise ValueError("Insufficient points in final direct or refracted subset.")

    m1, b1 = np.polyfit(distances[idx_d], times[idx_d], 1)
    m2, b2 = np.polyfit(distances[idx_r], times[idx_r], 1)

    Xc = (b2 - b1) / (m1 - m2)

    V1 = 1.0 / m1 if m1 != 0 else float('inf')  # km/s (times in ms, distances in m => m/ms)
    V2 = 1.0 / m2 if m2 != 0 else float('inf')

    # Convert to km/s: m/ms -> km/s (multiply by 1 because m/ms = km/s)
    # Actually 1 m/ms = 1 km/s, so V1 and V2 in m/ms are same numerical value in km/s
    # Keep as is
    ti = b2  # intercept time in ms

    # Depth calculation
    if V2 <= V1:
        depth = float('nan')
    else:
        depth = (ti * V1 * V2) / (2 * math.sqrt(V2**2 - V1**2))

    # Classification
    if V1 < 1.5:
        classification = "Unconsolidated soil"
    elif V1 <= 2.5:
        classification = "Weathered rock"
    else:
        classification = "Competent rock"

    # Fitted times for all points
    direct_fitted = m1 * distances + b1
    refracted_fitted = m2 * distances + b2

    return {
        'v1': V1,
        'v2': V2,
        'depth': depth,
        'crossover_distance': Xc,
        'intercept_time': ti,
        'classification': classification,
        'direct_times_fitted': direct_fitted,
        'refracted_times_fitted': refracted_fitted,
        'direct_mask': direct_mask
    }

def generate_csv(distances, times, direct_fitted, refracted_fitted):
    """Generate CSV string with distance, time, fitted direct, fitted refracted."""
    df = pd.DataFrame({
        'Distance (m)': distances,
        'Time (ms)': times,
        'Fitted direct time (ms)': direct_fitted,
        'Fitted refracted time (ms)': refracted_fitted
    })
    return df.to_csv(index=False)

def generate_plot(distances, times, direct_fitted, refracted_fitted, v1, v2, Xc):
    """Generate matplotlib figure for travel-time plot."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(distances, times, color='black', label='Observed arrivals', zorder=5)

    # Direct line (dashed)
    ax.plot(distances, direct_fitted, '--', color='blue', label=f'Direct (V1={v1:.2f} km/s)')
    # Refracted line (solid)
    ax.plot(distances, refracted_fitted, '-', color='red', label=f'Refracted (V2={v2:.2f} km/s)')

    # Mark crossover
    if not np.isnan(Xc):
        ax.axvline(x=Xc, color='green', linestyle=':', label=f'Xc≈{Xc:.1f} m')

    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Time (ms)')
    ax.set_title('Travel-Time Plot (Two-Layer Refraction)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig
