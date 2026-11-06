import os
import shutil
import subprocess
import pandas as pd
from plotnine import (
    ggplot,
    aes,
    geom_density,
    facet_wrap,
    scale_fill_manual,
    theme_minimal,
    labs,
    theme,
    element_text,
)

PROCESSED_PATH = os.path.join("data", "processed", "ev_population_cleaned.csv")
ASSET_PATH = os.path.join("assets", "plotnine_ev_density_facet.png")


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


def run_plotnine_pipeline():
    print("[INFO] Executing plotnine analytics pipeline...")

    if not os.path.exists(PROCESSED_PATH):
        raise FileNotFoundError(
            f"[ERROR] Processed data not found at {PROCESSED_PATH}. Run python/data_loader.py first."
        )

    df = pd.read_csv(PROCESSED_PATH)
    df_valid_range = df[df["Electric Range"] > 0]

    top_makes = df_valid_range["Make"].value_counts().head(6).index
    df_top_makes = df_valid_range[df_valid_range["Make"].isin(top_makes)]

    plot = (
        ggplot(
            df_top_makes,
            aes(x="Electric Range", fill="Electric Vehicle Type"),
        )
        + geom_density(alpha=0.5)
        + facet_wrap("~ Make", scales="free_y")
        + scale_fill_manual(values=["#1f77b4", "#ff7f0e"])
        + theme_minimal()
        + labs(
            title="EV Range Density Distributions Across Top Manufacturers",
            subtitle="Grammar of Graphics Faceted Plot Engine (plotnine in Python)",
            x="Electric Range (Miles)",
            y="Density",
            fill="Vehicle Type",
        )
        + theme(
            plot_title=element_text(size=14, weight="bold"),
            legend_position="bottom",
        )
    )

    os.makedirs(os.path.dirname(ASSET_PATH), exist_ok=True)
    plot.save(ASSET_PATH, width=10, height=6, dpi=300)

    print(f"[SUCCESS] plotnine visual asset generated at {ASSET_PATH}")
    render_terminal_preview(ASSET_PATH)


if __name__ == "__main__":
    run_plotnine_pipeline()