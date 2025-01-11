from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

plt.rcParams["axes.xmargin"] = 0
plt.rcParams["axes.ymargin"] = 0
plt.rcParams["font.size"] = 24
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams["lines.linewidth"] = 4


@dataclass
class Plot:
    fig: Figure
    ax: Axes

    def __init__(self, fig_n_ax: tuple[Figure, Axes] | None = None):
        if fig_n_ax is None:
            fig, ax = plt.subplots(figsize=(16, 9))
            fig.tight_layout()
            ax.tick_params(axis="both", labelsize=32)
            ax.grid(which="both")
        else:
            fig, ax = fig_n_ax
        self.fig, self.ax = fig, ax

    def save(self, name: str):
        self.ax.legend(fontsize=30, loc="best")
        self.fig.savefig(f"{name}.png", bbox_inches="tight", pad_inches=0)
        self.fig.savefig(f"{name}.pdf", bbox_inches="tight", pad_inches=0)
        plt.close()
