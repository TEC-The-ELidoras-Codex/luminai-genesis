"""Utility functions for physical resonance calculations.

These helpers provide simple, well-documented formulas for common
resonant systems:

- mass-spring natural frequency: f = (1/2pi) * sqrt(k/m)
- LC circuit resonant frequency: f = 1/(2pi*sqrt(L*C))
- energy <-> frequency via Planck's relation: E = h * f

The FFT helper is optional and requires numpy. It will raise a
clear ImportError with guidance if numpy isn't available.
"""

from __future__ import annotations

import math

# Physical constants
PLANCK_H = 6.62607015e-34  # Planck constant (J·s)


def mass_spring_natural_frequency(mass_kg: float, stiffness_n_per_m: float) -> float:
    """Return natural frequency in Hz for a simple mass-spring system.

    f_n = (1 / (2*pi)) * sqrt(k / m)

    Args:
        mass_kg: mass in kilograms (m > 0)
        stiffness_n_per_m: spring constant in N/m (k >= 0)

    Raises:
        ValueError: if mass_kg <= 0 or stiffness < 0
    """
    if mass_kg <= 0:
        raise ValueError("mass_kg must be > 0")
    if stiffness_n_per_m < 0:
        raise ValueError("stiffness_n_per_m must be >= 0")
    omega_n = math.sqrt(stiffness_n_per_m / mass_kg)
    return omega_n / (2 * math.pi)


def lc_resonant_frequency(inductance_h: float, capacitance_f: float) -> float:
    """Return resonant frequency in Hz for an LC circuit: f = 1/(2*pi*sqrt(L*C)).

    Args:
        inductance_h: Inductance in henries (L > 0)
        capacitance_f: Capacitance in farads (C > 0)
    """
    if inductance_h <= 0 or capacitance_f <= 0:
        raise ValueError("inductance_h and capacitance_f must be > 0")
    omega = 1.0 / math.sqrt(inductance_h * capacitance_f)
    return omega / (2 * math.pi)


def energy_from_frequency(freq_hz: float) -> float:
    """Return energy in joules corresponding to frequency via E = h * f."""
    if freq_hz < 0:
        raise ValueError("freq_hz must be >= 0")
    return PLANCK_H * freq_hz


def frequency_from_energy(energy_j: float) -> float:
    """Return frequency in Hz from energy in joules (f = E / h)."""
    if energy_j < 0:
        raise ValueError("energy_j must be >= 0")
    return energy_j / PLANCK_H


def dominant_frequencies_from_signal(
    signal: list[float],
    sample_rate: float,
    n_peaks: int = 3,
) -> list[tuple[float, float]]:
    """Return the top `n_peaks` dominant frequencies and their magnitudes from a
    time-series signal.

    This function requires numpy. It returns a list of tuples
    (frequency_hz, magnitude). If numpy isn't installed it will raise ImportError
    with guidance.
    """
    try:
        import numpy as np
    except ImportError as e:  # pragma: no cover - runtime dependency
        raise ImportError(
            "dominant_frequencies_from_signal requires numpy. "
            "Install it with `pip install numpy` to use this helper.",
        ) from e

    if sample_rate <= 0:
        raise ValueError("sample_rate must be > 0")

    x = np.asarray(signal)
    n = x.size
    if n == 0:
        return []

    # Compute FFT and power spectral density
    freqs = np.fft.rfftfreq(n, d=1.0 / sample_rate)
    spectrum = np.abs(np.fft.rfft(x))

    # Find top peaks by magnitude
    idx = np.argsort(spectrum)[-n_peaks:][::-1]
    result = [(float(freqs[i]), float(spectrum[i])) for i in idx]
    return result
