import math
import pandas as pd # Included for context, though logic is pure function

# --- Core Macronutrient Calculation Logic ---

def classify_bmi(weight_kg: float, height_m: float) -> str:
    """
    Calculates BMI (Body Mass Index) and returns the classification.
    """
    if height_m == 0:
        return "Invalid"
    
    bmi = weight_kg / (height_m * height_m)
    
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    elif bmi < 35:
        return "Obese Class 1"
    elif bmi < 40:
        return "Obese Class 2"
    else:
        return "Obese Class 3"

def calculate_macros(weight_kg: float, height_m: float, gender: str, bmi_class: str) -> dict:
    """
    Calculates personalized daily macronutrient recommendations (in grams) and calorie goals.
    This logic would be exposed via a Flask/REST API endpoint.
    (Age assumed 30 for consistency)
    """
    height_cm = height_m * 100
    
    # 1. Calculate BMR (Basal Metabolic Rate) using Mifflin-St Jeor formula (Gender Specific)
    bmr_kcal = (10 * weight_kg) + (6.25 * height_cm) - (5 * 30)
    if gender == 'Male':
        bmr_kcal += 5
    else: # Female
        bmr_kcal -= 161
    
    # 2. Calculate TDEE (Total Daily Energy Expenditure) 
    # Activity Factor (1.2) reflects sedentary nature of IT work (Activity-Based Nutrition Logic)
    ACTIVITY_FACTOR = 1.2 
    tdee_kcal = bmr_kcal * ACTIVITY_FACTOR
    
    # 3. Determine Goal and Calorie Target (Goal-Based Deficit/Surplus)
    calorie_goal = tdee_kcal
    
    if bmi_class == "Underweight":
        calorie_goal = tdee_kcal + 300 # Moderate surplus
        
    elif bmi_class == "Overweight" or bmi_class.startswith("Obese"):
        calorie_goal = tdee_kcal - 500 # Moderate deficit for safe weight loss

    # Constants for calorie conversion
    PROTEIN_CAL_PER_G = 4
    CARB_CAL_PER_G = 4
    FAT_CAL_PER_G = 9
    
    # 4. Determine Macro Ratios (The Personalized Strategy)
    if bmi_class == "Underweight":
        protein_g_per_kg = 1.5
        carbs_ratio = 0.60
        fats_ratio = 0.25
    elif bmi_class == "Normal":
        protein_g_per_kg = 1.2
        carbs_ratio = 0.50
        fats_ratio = 0.30
    else: # Overweight and Obese Classes - high protein for satiety
        protein_g_per_kg = 1.3 
        carbs_ratio = 0.35 
        fats_ratio = 0.35 
    
    # Calculate protein requirement first (as a fixed value per kg)
    protein_g = protein_g_per_kg * weight_kg
    protein_cal = protein_g * PROTEIN_CAL_PER_G
    
    # Allocate remaining calories to carbs and fats
    remaining_goal_calories = calorie_goal - protein_cal
    
    if remaining_goal_calories < 0:
        return None 

    # Distribute remaining calories based on the determined ratios
    total_ratio = carbs_ratio + fats_ratio
    adjusted_carbs_ratio = carbs_ratio / total_ratio
    adjusted_fats_ratio = fats_ratio / total_ratio

    carbs_cal = remaining_goal_calories * adjusted_carbs_ratio
    fats_cal = remaining_goal_calories * adjusted_fats_ratio
    
    carbohydrates_g = carbs_cal / CARB_CAL_PER_G
    fats_g = fats_cal / FAT_CAL_PER_G

    return {
        "Protein_g": round(protein_g),
        "Carbohydrates_g": round(carbohydrates_g),
        "Fats_g": round(fats_g),
        "Total_Calories": round(calorie_goal),
        "Goal": "Maintenance" if bmi_class == "Normal" else "Weight Loss" if bmi_class.startswith("Obese") or bmi_class == "Overweight" else "Weight Gain"
    }

if __name__ == '__main__':
    # Test block to verify the logic works (simulates API testing)
    test_weight = 85.0
    test_height = 1.75
    test_gender = 'Male'
    
    test_bmi_class = classify_bmi(test_weight, test_height)
    result = calculate_macros(test_weight, test_height, test_gender, test_bmi_class)
    
    print(f"--- Python Logic Test Complete ---")
    print(f"BMI Class: {test_bmi_class}")
    print(f"Goal: {result['Goal']}")
    print(f"Target Calories: {result['Total_Calories']} kcal")
    print(f"Macros (g): P={result['Protein_g']}, C={result['Carbohydrates_g']}, F={result['Fats_g']}")