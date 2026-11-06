import os
import shutil
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROCESSED_PATH = os.path.join("data", "processed", "ev_population_clean.csv")
ASSET_PATH = os.path.join("assets", "seaborn_ev_distribution.png")


def render_terminal_preview(image_path):
    print("\n--- Terminal Graphic Preview ---")
    if shutil.which("chafa"):
        subprocess.run(["chafa", image_path])
    else:
        try:
            import climage

            output = climage.convert(image_path, width=80)
            print(output)
        except ImportError:
            print(
                "[NOTE] Terminal preview tool not found. Install 'chafa' or 'climage' for inline terminal previews."
            )


def run_seaborn_pipeline():
    print("[INFO] Executing Seaborn analytics pipeline...")

    if not os.path.exists(PROCESSED_PATH):
        raise FileNotFoundError(
            f"[ERROR] Processed data not found at {PROCESSED_PATH}. Run python/data_loader.py first."
        )

    df = pd.read_csv(PROCESSED_PATH)
    df_valid_range = df[df["Electric Range"] > 0]

    sns.set_theme(style="whitegrid", palette="muted")

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        "EV Statistical Distribution & Feature Relationships (Seaborn Ecosystem)",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )

    top_makes = df["Make"].value_counts().head(6).index
    df_top_makes = df_valid_range[df_valid_range["Make"].isin(top_makes)]

    sns.boxplot(
        data=df_top_makes,
        x="Make",
        y="Electric Range",
        hue="Electric Vehicle Type",
        palette="Set2",
        ax=axs[0, 0],
        showfliers=False,
    )
    sns.stripplot(
        data=df_top_makes,
        x="Make",
        y="Electric Range",
        hue="Electric Vehicle Type",
        dodge=True,
        alpha=0.3,
        palette="dark:black",
        ax=axs[0, 0],
        legend=False,
    )
    axs[0, 0].set_title("Range Distribution Across Top 6 Makes", fontweight="bold")
    axs[0, 0].set_xlabel("EV Manufacturer")
    axs[0, 0].set_ylabel("Electric Range (Miles)")

    sns.kdeplot(
        data=df_valid_range,
        x="Electric Range",
        hue="Electric Vehicle Type",
        fill=True,
        common_norm=False,
        palette="crest",
        alpha=0.5,
        linewidth=2,
        ax=axs[0, 1],
    )
    axs[0, 1].set_title("Electric Range Density Profiles (BEV vs PHEV)", fontweight="bold")
    axs[0, 1].set_xlabel("Electric Range (Miles)")
    axs[0, 1].set_ylabel("Density")

    sns.lineplot(
        data=df_valid_range,
        x="Model Year",
        y="Electric Range",
        hue="Electric Vehicle Type",
        style="Electric Vehicle Type",
        markers=True,
        dashes=False,
        err_style="band",
        palette="Set1",
        ax=axs[1, 0],
    )
    axs[1, 0].set_title("Historical Electric Range Trajectory with CI", fontweight="bold")
    axs[1, 0].set_xlabel("Model Year")
    axs[1, 0].set_ylabel("Electric Range (Miles)")

    numeric_cols = [col for col in ["Model Year", "Electric Range", "Base MSRP"] if col in df_valid_range.columns]
    numeric_df = df_valid_range[numeric_cols].corr()

    sns.heatmap(
        numeric_df,
        annot=True,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        fmt=".2f",
        square=True,
        ax=axs[1, 1],
    )
    axs[1, 1].set_title("Numeric Features Correlation Heatmap", fontweight="bold")

    os.makedirs(os.path.dirname(ASSET_PATH), exist_ok=True)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(ASSET_PATH, dpi=300)
    plt.close()

    print(f"[SUCCESS] Seaborn visual asset generated at {ASSET_PATH}")
    render_terminal_preview(ASSET_PATH)


if __name__ == "__main__":
    run_seaborn_pipeline()