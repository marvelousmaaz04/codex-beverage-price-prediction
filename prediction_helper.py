import pandas as pd
import joblib
import numpy as np

# Load model and encoders
model_path = 'artifacts/model_data.joblib'
model_data = joblib.load(model_path)

model = model_data['model']
cols_to_oe = model_data['cols_to_oe']
cols_to_ohe = model_data['cols_to_ohe']
ordinal_encoder = model_data['ordinal_encoder']
one_hot_encoder = model_data['one_hot_encoder']
features = model_data['features']

def categorize_age(age):
    if age >= 18 and age <= 25:
        return "18-25"
    elif age >= 26 and age <= 35:
        return "26-35"
    elif age >= 36 and age <= 45:
        return "36-45"
    elif age >= 46 and age <= 55:
        return "46-55"
    elif age >= 56 and age <= 70:
        return "56-70"
    elif age > 70:
        return "70+"

def calc_cf_ab_score(data):
    frequency_score = 0
    awareness_score = 0

    if data['consume_frequency(weekly)'] == "0-2 times":
        frequency_score = 1
    elif data['consume_frequency(weekly)'] == "3-4 times":
        frequency_score = 2
    elif data['consume_frequency(weekly)'] == "5-7 times":
        frequency_score = 3

    if data['awareness_of_other_brands'] == "0 to 1":
        awareness_score = 1
    elif data['awareness_of_other_brands'] == "2 to 4":
        awareness_score = 2
    elif data['awareness_of_other_brands'] == "above 4":
        awareness_score = 3

    cf_ab_score = frequency_score/(awareness_score + frequency_score)

    return np.round(cf_ab_score,2)

def calc_zas(data):
    zone_score = 0
    income_score = 0

    if data["zone"] == "Rural":
        zone_score = 1
    elif data["zone"] == "Semi-Urban":
        zone_score = 2
    elif data["zone"] == "Urban":
        zone_score = 3
    elif data["zone"] == "Metro":
        zone_score = 4

    if data["income_levels"] == "<10L":
        income_score = 1
    elif data["income_levels"] == "10L - 15L":
        income_score = 2
    elif data["income_levels"] == "16L - 25L":
        income_score = 3
    elif data["income_levels"] == "26L - 35L":
        income_score = 4
    elif data["income_levels"] == "> 35L":
        income_score = 5
    elif data["income_levels"] == "Not Reported":
        income_score = 0

    zas_score = zone_score * income_score
    return zas_score

# Prepare the input DataFrame
def prepare_df(age, gender, zone, occupation,
               income_levels, consume_frequency, current_brand, preferable_consumption_size,
               awareness_of_other_brands, reasons_for_choosing_brands, flavor_preference, purchase_channel,
               packaging_preference, health_concerns, typical_consumption_situations):
    # Input data as a dictionary
    input_data = {
        'age': [age],
        'gender': [gender],
        'zone': [zone],
        'occupation': [occupation],
        'income_levels': [income_levels],
        'consume_frequency(weekly)': [consume_frequency],
        'current_brand': [current_brand],
        'preferable_consumption_size': [preferable_consumption_size],
        'awareness_of_other_brands': [awareness_of_other_brands],
        'reasons_for_choosing_brands': [reasons_for_choosing_brands],
        'flavor_preference': [flavor_preference],
        'purchase_channel': [purchase_channel],
        'packaging_preference': [packaging_preference],
        'health_concerns': [health_concerns],
        'typical_consumption_situations': [typical_consumption_situations],
    }

    # Create a DataFrame
    input_df = pd.DataFrame(input_data)

    # Categorize age into groups
    input_df.loc[:, 'age_group'] = input_df['age'].apply(categorize_age)

    # Drop age column
    input_df = input_df.drop('age', axis=1)

    # Calculate cf_ab_score
    input_df.loc[:, 'cf_ab_score'] = input_df.apply(calc_cf_ab_score, axis=1)

    # Calculate zas
    input_df.loc[:, 'zas_score'] = input_df[['zone', 'income_levels']].apply(calc_zas, axis=1)
    print(input_df)
    # Apply label encoding for specified columns

    input_df[cols_to_oe] = ordinal_encoder.transform(input_df[cols_to_oe])

    # Apply one-hot encoding for specified columns
    ohe_encoded = one_hot_encoder.transform(input_df[cols_to_ohe])
    ohe_columns = one_hot_encoder.get_feature_names_out(cols_to_ohe)
    ohe_df = pd.DataFrame(ohe_encoded, columns=ohe_columns, index=input_df.index)

    # Drop original columns and concatenate the one-hot encoded ones
    input_df = pd.concat([input_df.drop(columns=cols_to_ohe), ohe_df], axis=1)

    # Ensure column order matches the model's expected input
    input_df = input_df.reindex(columns=features, fill_value=0)

    return input_df


# Predict function
def predict(age, gender, zone, occupation,
            income_levels, consume_frequency, current_brand, preferable_consumption_size,
            awareness_of_other_brands, reasons_for_choosing_brands, flavor_preference, purchase_channel,
            packaging_preference, health_concerns, typical_consumption_situations):
    # Prepare the DataFrame
    input_df = prepare_df(age, gender, zone, occupation,
                          income_levels, consume_frequency, current_brand, preferable_consumption_size,
                          awareness_of_other_brands, reasons_for_choosing_brands, flavor_preference, purchase_channel,
                          packaging_preference, health_concerns, typical_consumption_situations)

    # Make a prediction
    prediction = model.predict(input_df)
    print(prediction)
    if prediction[0] == 0:
        return '50-100'
    elif prediction[0] == 1:
        return '100-150'
    elif prediction[0] == 2:
        return '150-200'
    elif prediction[0] == 3:
        return '200-250'

    return prediction
