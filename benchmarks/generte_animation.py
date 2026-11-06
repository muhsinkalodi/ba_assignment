import os
import shutil
import subprocess
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import pandas as pd

PROCESSED_PATH = os.path.join("data", "processed", "ev_population_cleaned.csv")
ANIMATION_PATH = os.path.join("assets", "animated_plots.gif")


def render_terminal_preview(image_path):
    """Renders saved animation preview inside terminal if chafa is available."""
    print("\n--- Terminal Graphic Preview ---")
    if shutil.which("chafa"):
        subprocess.run(["chafa", image_path])
    else:
        print(
            "[NOTE] Install 'chafa' system package to preview GIF animations directly in the terminal."
        )


def generate_ev_animation():
    """Generates an animated historical EV registration trajectory using Matplotlib

    and exports an animated GIF asset.
    """
    print("[INFO] Initiating dynamic EV registration animation pipeline...")

    if not os.path.exists(PROCESSED_PATH):
        raise FileNotFoundError(
            f"[ERROR] Processed data not found at {PROCESSED_PATH}. Run python/data_loader.py first."
        )

    df = pd.read_csv(PROCESSED_PATH)

    # Aggregate vehicle counts by Model Year and Type (2011 to recent)
    df_filtered = df[(df["Model Year"] >= 2011) & (df["Model Year"] <= 2024)]
    yearly_counts = (
        df_filtered.groupby(["Model Year", "Electric Vehicle Type"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    years = yearly_counts["Model Year"].values
    bev_counts = (
        yearly_counts["BEV"].values
        if "BEV" in yearly_counts
        else [0] * len(years)
    )
    phev_counts = (
        yearly_counts["PHEV"].values
        if "PHEV" in yearly_counts
        else [0] * len(years)
    )

    # Set up animated figure canvas
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(2010, 2025)
    max_y = max(max(bev_counts, default=100), max(phev_counts, default=100))
    ax.set_ylim(0, max_y * 1.1)

    ax.set_title(
        "Cumulative EV Adoption Growth Trajectory (2011 - 2024)",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xlabel("Model Year", fontweight="bold")
    ax.set_ylabel("Annual Vehicle Registrations", fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.5)

    (line_bev,) = ax.plot(
        [], [], color="#1f77b4", marker="o", linewidth=2.5, label="BEV"
    )
    (line_phev,) = ax.plot(
        [], [], color="#ff7f0e", marker="s", linewidth=2.5, label="PHEV"
    )
    ax.legend(loc="upper left")

    year_text = ax.text(
        0.05,
        0.85,
        "",
        transform=ax.transAxes,
        fontsize=16,
        fontweight="bold",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    def init():
        line_bev.set_data([], [])
        line_phev.set_data([], [])
        year_text.set_text("")
        return line_bev, line_phev, year_text

    def update(frame):
        x = years[: frame + 1]
        y_bev = bev_counts[: frame + 1]
        y_phev = phev_counts[: frame + 1]

        line_bev.set_data(x, y_bev)
        line_phev.set_data(x, y_phev)
        year_text.set_text(f"Year: {years[frame]}")
        return line_bev, line_phev, year_text

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=len(years),
        init_func=init,
        blit=True,
        interval=400,
    )

    os.makedirs(os.path.dirname(ANIMATION_PATH), exist_ok=True)
    anim.save(ANIMATION_PATH, writer="pillow", fps=2.5)
    plt.close()

    print(f"[SUCCESS] Animated visual GIF asset generated at {ANIMATION_PATH}")
    render_terminal_preview(ANIMATION_PATH)


if __name__ == "__main__":
    generate_ev_animation()