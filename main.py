import streamlit as st
from prediction_helper import predict

st.set_page_config(layout="wide")
# Dictionary of columns and their unique values
categorical_inputs = {
    'income_levels': ['<10L', '10L - 15L', '16L - 25L', '26L - 35L', '> 35L'],
    'consume_frequency(weekly)': ['0-2 times', '3-4 times', '5-7 times'],
    'preferable_consumption_size': ['Small (250 ml)', 'Medium (500 ml)', 'Large (1 L)'],
    'health_concerns': ['Low (Not very concerned)', 'Medium (Moderately health-conscious)', 'High (Very health-conscious)'],
    'gender': ['M', 'F'],
    'zone': ['Urban', 'Metro', 'Rural', 'Semi-Urban',],
    'occupation': ['Working Professional', 'Student', 'Entrepreneur', 'Retired'],
    'current_brand': ['Newcomer', 'Established'],
    'awareness_of_other_brands': ['0 to 1', '2 to 4', 'above 4'],
    'reasons_for_choosing_brands': ['Price', 'Quality', 'Availability', 'Brand Reputation'],
    'flavor_preference': ['Traditional', 'Exotic'],
    'purchase_channel': ['Online', 'Retail Store'],
    'packaging_preference': ['Simple', 'Premium', 'Eco-Friendly'],
    'typical_consumption_situations': ['Active (eg. Sports, gym)', 'Social (eg. Parties)', 'Casual (eg. At home)']
}

# Streamlit layout
st.markdown(
    "<h1 style='text-align: center;'>CodeX: Beverage Price Prediction</h1>",
    unsafe_allow_html=True
)

# Create rows with columns for inputs
row1 = st.columns(4)
row2 = st.columns(4)
row3 = st.columns(4)
row4 = st.columns(4)

# First row of inputs
with row1[0]:
    age = st.number_input('Age', min_value=18, max_value=100)
with row1[1]:
    gender = st.selectbox('Gender', categorical_inputs['gender'])
with row1[2]:
    zone = st.selectbox('Zone', categorical_inputs['zone'])
with row1[3]:
    occupation = st.selectbox('Occupation', categorical_inputs['occupation'])


# Second row of inputs
with row2[0]:
    income_levels = st.selectbox('Income Levels', categorical_inputs['income_levels'])
with row2[1]:
    consume_frequency = st.selectbox('Consume Frequency (weekly)', categorical_inputs['consume_frequency(weekly)'])
with row2[2]:
    current_brand = st.selectbox('Current Brand', categorical_inputs['current_brand'])
with row2[3]:
    preferable_consumption_size = st.selectbox('Preferable Consumption Size',
                                               categorical_inputs['preferable_consumption_size'])

# Third row of inputs
with row3[0]:
    awareness_of_other_brands = st.selectbox('Awareness of Other Brands', categorical_inputs['awareness_of_other_brands'])
with row3[1]:
    reasons_for_choosing_brands = st.selectbox('Reasons for Choosing Brands', categorical_inputs['reasons_for_choosing_brands'])
with row3[2]:
    flavor_preference = st.selectbox('Flavor Preference', categorical_inputs['flavor_preference'])
with row3[3]:
    purchase_channel = st.selectbox('Purchase Channel', categorical_inputs['purchase_channel'])



# Fourth row of inputs
with row4[0]:
    packaging_preference = st.selectbox('Packaging Preference', categorical_inputs['packaging_preference'])
with row4[1]:
    health_concerns = st.selectbox('Health Concerns', categorical_inputs['health_concerns'])
with row4[2]:
    typical_consumption_situations = st.selectbox('Typical Consumption Situations', categorical_inputs['typical_consumption_situations'])


if st.button('Calculate Price Range'):
    print('Calc...')
    price_range = predict(age, gender, zone, occupation,
            income_levels, consume_frequency, current_brand, preferable_consumption_size,
            awareness_of_other_brands, reasons_for_choosing_brands, flavor_preference, purchase_channel,
            packaging_preference, health_concerns, typical_consumption_situations)

    st.write(f"Price Range: {price_range} INR")


