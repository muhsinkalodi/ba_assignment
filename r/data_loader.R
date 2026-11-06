suppressPackageStartupMessages({
  library(dplyr)
})

raw_path       <- file.path("data", "raw", "Electric_Vehicle_Population_Data.csv")
processed_path <- file.path("data", "processed", "ev_population_cleaned.csv")

clean_ev_data_r <- function() {
  cat("[INFO] Initiating dataset cleaning in R...\n")
  
  if (!file.exists(raw_path)) {
    csv_files <- list.files("data", pattern = "\\.csv$", full.names = TRUE)
    if (length(csv_files) > 0) {
      raw_path <- csv_files[1]
    } else {
      stop("[ERROR] No raw CSV file found in data/ directory!")
    }
  }
  
  df <- read.csv(raw_path, stringsAsFactors = FALSE)
  
  df_cleaned <- df %>%
    select(any_of(c("Model.Year", "Make", "Model", "Electric.Vehicle.Type", "Electric.Range", "County"))) %>%
    filter(!is.na(Electric.Range), !is.na(Make), !is.na(Model.Year)) %>%
    mutate(
      Electric.Vehicle.Type = ifelse(
        Electric.Vehicle.Type == "Battery Electric Vehicle (BEV)", "BEV",
        ifelse(Electric.Vehicle.Type == "Plug-in Hybrid Electric Vehicle (PHEV)", "PHEV", Electric.Vehicle.Type)
      )
    )
  
  dir.create(dirname(processed_path), recursive = TRUE, showwarnings = FALSE)
  write.csv(df_cleaned, processed_path, row.names = FALSE)
  
  cat(paste("[SUCCESS] R Cleaned dataset saved to", processed_path, "(", nrow(df_cleaned), "records)\n"))
}

clean_ev_data_r()