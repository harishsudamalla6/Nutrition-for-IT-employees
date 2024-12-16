getwd() 
setwd("C:/Users/DELL 5480/Downloads")
# Load required library
library(dplyr)

# Load the dataset
bmi_data <- read.csv("bmi.csv")

# Define a function for macronutrient recommendations based on weight and height
calculate_macros <- function(weight, height, bmi_class) {
  # Calculate Basal Metabolic Rate (BMR) as a base for macronutrient needs
  bmr <- 10 * weight + 6.25 * (height * 100) - 5 * 30  # Assuming age = 30 for simplicity
  if (bmi_class == "Underweight") {
    protein <- round(1.5 * weight, 1)  # 1.5g per kg body weight
    carbs <- round(0.6 * bmr, 1)       # 60% of BMR as carbs
    fats <- round(0.25 * bmr, 1)       # 25% of BMR as fats
  } else if (bmi_class == "Normal") {
    protein <- round(1.2 * weight, 1)  # 1.2g per kg body weight
    carbs <- round(0.5 * bmr, 1)       # 50% of BMR as carbs
    fats <- round(0.3 * bmr, 1)        # 30% of BMR as fats
  } else if (bmi_class == "Overweight") {
    protein <- round(1.0 * weight, 1)  # 1.0g per kg body weight
    carbs <- round(0.4 * bmr, 1)       # 40% of BMR as carbs
    fats <- round(0.35 * bmr, 1)       # 35% of BMR as fats
  } else if (bmi_class == "Obese Class 1" || bmi_class == "Obese Class 2" || bmi_class == "Obese Class 3") {
    protein <- round(1.2 * weight, 1)  # 1.2g per kg body weight
    carbs <- round(0.3 * bmr, 1)       # 30% of BMR as carbs
    fats <- round(0.4 * bmr, 1)        # 40% of BMR as fats
  } else {
    protein <- carbs <- fats <- NA     # Unknown case
  }
  return(c(protein = protein, carbs = carbs, fats = fats))
}

# Apply macronutrient recommendations based on weight, height, and BMI class
bmi_data <- bmi_data %>% 
  rowwise() %>% 
  mutate(
    Macros = list(calculate_macros(Weight, Height, BmiClass)),
    Protein_g = Macros["protein"],
    Carbohydrates_g = Macros["carbs"],
    Fats_g = Macros["fats"]
  ) %>% 
  select(-Macros)

# View the updated dataset
head(bmi_data)

# Save the recommendations to a new CSV file
write.csv(bmi_data, "bmi_with_diet_macros.csv", row.names = FALSE)

# Output message
cat("Diet macronutrient plans have been successfully added and saved to 'bmi_with_diet_macros.csv'.")


