suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
})

processed_path <- file.path("data", "processed", "ev_population_cleaned.csv")
asset_path     <- file.path("assets", "ggplot2_ev_density_facet.png")

run_ggplot2_pipeline <- function() {
  cat("[INFO] Executing R ggplot2 analytics pipeline...\n")
  
  if (!file.exists(processed_path)) {
    stop(paste("[ERROR] Processed dataset not found at", processed_path, ". Run python/data_loader.py first."))
  }
  
  df <- read.csv(processed_path, stringsAsFactors = FALSE)
  
  df_valid <- df %>% filter(`Electric.Range` > 0)
  
  top_makes <- df_valid %>%
    count(Make, sort = TRUE) %>%
    top_n(6, n) %>%
    pull(Make)
  
  df_top_makes <- df_valid %>% filter(Make %in% top_makes)
  
  p <- ggplot(df_top_makes, aes(x = Electric.Range, fill = Electric.Vehicle.Type)) +
    geom_density(alpha = 0.5) +
    facet_wrap(~ Make, scales = "free_y") +
    scale_fill_manual(values = c("BEV" = "#1f77b4", "PHEV" = "#ff7f0e")) +
    theme_minimal() +
    labs(
      title    = "EV Range Density Distributions Across Top Manufacturers",
      subtitle = "Grammar of Graphics Faceted Plot Engine (Native R ggplot2)",
      x        = "Electric Range (Miles)",
      y        = "Density",
      fill     = "Vehicle Type"
    ) +
    theme(
      plot.title      = element_text(size = 14, face = "bold"),
      legend.position = "bottom"
    )
  
  dir.create(dirname(asset_path), recursive = TRUE, showwarnings = FALSE)
  
  ggsave(
    filename = asset_path,
    plot     = p,
    width    = 10,
    height   = 6,
    dpi      = 300
  )
  
  cat(paste("[SUCCESS] ggplot2 visual asset generated at", asset_path, "\n"))
}

run_ggplot2_pipeline()