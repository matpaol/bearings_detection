"""Plotting helpers, kept separate from any data logic.

These functions only draw: they never modify the signals they receive.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_signal(
    signal: np.ndarray,
    sampling_frequency: int,
    title: str | None = None,
    seconds: float | None = None,
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Plot a signal against time.

    Parameters
    ----------
    signal : np.ndarray
        One-dimensional signal.
    sampling_frequency : int
        Sampling frequency of the signal, in Hz.
    title : str, optional
        Title of the plot.
    seconds : float, optional
        If given, only the first `seconds` of the signal are shown.
    ax : matplotlib Axes, optional
        Axes to draw on; a new figure is created if omitted.

    Returns
    -------
    matplotlib Axes
        The axes the signal was drawn on.
    """
    signal = np.asarray(signal).ravel()
    if seconds is not None:
        signal = signal[: int(seconds * sampling_frequency)]
    time = np.arange(signal.size) / sampling_frequency
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 3))
    ax.plot(time, signal, linewidth=0.6)
    ax.set_xlabel("time [s]")
    ax.set_ylabel("amplitude")
    if title:
        ax.set_title(title)
    return ax
