import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = "ENG-220_cleaned.xlsx"
data = pd.read_excel(file_path, sheet_name="Sheet1", header=None)

st.title("Crime Data Explorer 📊")

st.sidebar.header("Filters")

# Example: Victim Age Distribution
st.subheader("Victim Age Distribution")
victim_age_labels = [
    "0-9","20-29","30-39","40-49","50-59","60-69",
    "70-79","80-89","90-Older","Unknown"
]
victim_age_counts = [
    1425782,1250901,798971,706876,502769,
    239066,214102,69725,67614,16637,4581
]

age_df = pd.DataFrame({"Age Group": victim_age_labels, "Count": victim_age_counts})
st.bar_chart(age_df.set_index("Age Group"))

# Example: Offender Sex
st.subheader("Offender Sex")
offender_sex_labels = ["Male","Female","Unknown","Not Specified"]
offender_sex_counts = [3388222,1035692,209326,401412]

sex_df = pd.DataFrame({"Sex": offender_sex_labels, "Count": offender_sex_counts})
st.bar_chart(sex_df.set_index("Sex"))

# Example: Victim Sex
st.subheader("Victim Sex")
victim_sex_labels = ["Male","Female","Unknown","Not Specified"]
victim_sex_counts = [2853063,2413675,30286,0]

victim_sex_df = pd.DataFrame({"Sex": victim_sex_labels, "Count": victim_sex_counts})
st.bar_chart(victim_sex_df.set_index("Sex"))

# Example: Weapon Used
st.subheader("Weapons Used in Assaults")
weapon_labels = [
    "Personal Weapons","Handgun","Knife/Cutting Instrument",
    "Firearm","Blunt Object","Motor Vehicle/Vessel","Asphyxiation","Other"
]
weapon_counts = [
    1073169,1054702,870805,626843,543908,301450,133729,494755
]

weapon_df = pd.DataFrame({"Weapon": weapon_labels, "Count": weapon_counts})
st.bar_chart(weapon_df.set_index("Weapon"))

# Example: Location Type
st.subheader("Top Locations of Assaults")
location_labels = ["Residence/Home","Highway/Street","Parking/Garage","Bar/Nightclub","School","Restaurant"]
location_counts = [2896668,1132859,304524,80796,52802,59464]

location_df = pd.DataFrame({"Location": location_labels, "Count": location_counts})
st.bar_chart(location_df.set_index("Location"))

st.write("Use the sidebar to add filters and expand this dashboard with more categories.")

