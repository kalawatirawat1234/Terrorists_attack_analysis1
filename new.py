import pandas as pd
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# Title
st.title("COVID Prediction App 🤒")

# Load the data
df = pd.read_csv(r'C:\Users\rawat\PycharmProjects\PythonProject\covid_toy.csv')

# Handle missing values
df['fever'].fillna(df['fever'].mean(), inplace=True)

# Label Encoding
le_gender = LabelEncoder()
le_city = LabelEncoder()
le_cough = LabelEncoder()
le_has_covid = LabelEncoder()

df['gender'] = le_gender.fit_transform(df['gender'])
df['city'] = le_city.fit_transform(df['city'])
df['cough'] = le_cough.fit_transform(df['cough'])
df['has_covid'] = le_has_covid.fit_transform(df['has_covid'])

# Prepare data
X = df[['age', 'gender', 'fever', 'cough', 'city']]
y = df['has_covid']

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(x_train, y_train)

# Sidebar input
st.sidebar.header("Enter Patient Data:")

age = st.sidebar.slider("Age", 1, 100, 25)
gender = st.sidebar.selectbox("Gender", le_gender.classes_)
fever = st.sidebar.slider("Fever (in °F)", 95.0, 105.0, 101.0)
cough = st.sidebar.selectbox("Cough Strength", le_cough.classes_)
city = st.sidebar.selectbox("City", le_city.classes_)

# Convert input to model format
input_data = pd.DataFrame([[age,
                            le_gender.transform([gender])[0],
                            fever,
                            le_cough.transform([cough])[0],
                            le_city.transform([city])[0]]],
                          columns=['age', 'gender', 'fever', 'cough', 'city'])

# Predict
if st.sidebar.button("Predict"):
    prediction = model.predict(input_data)[0]
    result = le_has_covid.inverse_transform([prediction])[0]

    st.subheader("Prediction Result:")
    if result == 'Yes':
        st.error("⚠️ The patient is likely to have COVID.")
    else:
        st.success("✅ The patient is unlikely to have COVID.")

# Model accuracy
st.sidebar.markdown("---")
st.sidebar.write("**Model Accuracy**")
y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
st.sidebar.write(f"{accuracy * 100:.2f}%")

