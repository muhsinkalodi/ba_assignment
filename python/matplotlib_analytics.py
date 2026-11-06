import os
import matplotlib.pyplot as plt
import pandas as pd

PROCESSED_PATH = os.path.join("data", "processed", "data.csv")
ASSET_PATH = os.path.join("assets", "matplotlib_ev_trend.png")


def run_matplotlib_pipeline():
   
    print("[INFO] Executing Matplotlib analytics pipeline...")

    if not os.path.exists(PROCESSED_PATH):
        raise FileNotFoundError(
            f"[ERROR] Processed data not found at {PROCESSED_PATH}. Run python/data_loader.py first."
        )

    df = pd.read_csv(PROCESSED_PATH)

    df_valid_range = df[df["Electric Range"] > 0]

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        "EV Population & Performance Metrics (Matplotlib Ecosystem)",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )

    yearly_range = (
        df_valid_range.groupby("Model Year")["Electric Range"]
        .mean()
        .reset_index()
    )
    axs[0, 0].plot(
        yearly_range["Model Year"],
        yearly_range["Electric Range"],
        marker="o",
        color="#1f77b4",
        linewidth=2,
    )
    axs[0, 0].set_title("Mean Electric Range Evolution", fontweight="bold")
    axs[0, 0].set_xlabel("Model Year")
    axs[0, 0].set_ylabel("Average Range (Miles)")
    axs[0, 0].grid(True, linestyle="--", alpha=0.5)

    top_10_makes = df["Make"].value_counts().head(10)
    axs[0, 1].barh(
        top_10_makes.index[::-1],
        top_10_makes.values[::-1],
        color="#2ca02c",
        edgecolor="black",
        alpha=0.8,
    )
    axs[0, 1].set_title("Top 10 EV Manufacturers by Registrations", fontweight="bold")
    axs[0, 1].set_xlabel("Total Registrations")
    axs[0, 1].grid(True, axis="x", linestyle="--", alpha=0.5)

    bev_data = df_valid_range[df_valid_range["Electric Vehicle Type"] == "BEV"]
    phev_data = df_valid_range[df_valid_range["Electric Vehicle Type"] == "PHEV"]

    axs[1, 0].scatter(
        bev_data["Model Year"],
        bev_data["Electric Range"],
        alpha=0.4,
        c="#d62728",
        label="BEV",
        s=20,
    )
    axs[1, 0].scatter(
        phev_data["Model Year"],
        phev_data["Electric Range"],
        alpha=0.4,
        c="#9467bd",
        label="PHEV",
        s=20,
    )
    axs[1, 0].set_title("Electric Range Scatter by Vehicle Type", fontweight="bold")
    axs[1, 0].set_xlabel("Model Year")
    axs[1, 0].set_ylabel("Electric Range (Miles)")
    axs[1, 0].legend()
    axs[1, 0].grid(True, linestyle="--", alpha=0.5)

    type_counts = df["Electric Vehicle Type"].value_counts()
    axs[1, 1].pie(
        type_counts.values,
        labels=type_counts.index,
        autopct="%1.1f%%",
        colors=["#ff7f0e", "#17becf"],
        startangle=140,
        explode=(0.05, 0),
    )
    axs[1, 1].set_title("Fleet Composition Share (BEV vs PHEV)", fontweight="bold")

    os.makedirs(os.path.dirname(ASSET_PATH), exist_ok=True)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(ASSET_PATH, dpi=300)
    plt.close()

    print(f"[SUCCESS] Matplotlib visual asset generated at {ASSET_PATH}")


if __name__ == "__main__":
    run_matplotlib_pipeline()