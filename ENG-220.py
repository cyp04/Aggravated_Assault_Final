
📊 Streamlit App Code
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Excel file
@st.cache_data
def load_data():
    df = pd.read_excel("ENG-220 Final project Spreadsheet.xlsx", sheet_name="Sheet1", header=None)
    return df

df = load_data()

st.title("ENG-220 Final Project: Crime Data Explorer")
st.markdown("Interactive dashboard for exploring victim and offender statistics, weapons, relationships, and crime trends.")

# Tabs for organization
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Victim Demographics", 
    "Offender Demographics", 
    "Weapons & Relationships", 
    "Locations", 
    "Time Series"
])

# --- Victim Demographics ---
with tab1:
    st.header("Victim Age Distribution")
    victim_age_labels = df.iloc[1:12, 0].values
    victim_age_counts = df.iloc[1:12, 1].values
    st.bar_chart(pd.DataFrame({"Age Group": victim_age_labels, "Count": victim_age_counts}).set_index("Age Group"))

    st.header("Victim Sex")
    victim_sex_labels = df.iloc[18:22, 0].values
    victim_sex_counts = df.iloc[18:22, 1].values
    fig, ax = plt.subplots()
    ax.pie(victim_sex_counts, labels=victim_sex_labels, autopct='%1.1f%%')
    st.pyplot(fig)

    st.header("Victim Race")
    victim_race_labels = df.iloc[45:54, 0].values
    victim_race_counts = df.iloc[45:54, 1].values
    st.bar_chart(pd.DataFrame({"Race": victim_race_labels, "Count": victim_race_counts}).set_index("Race"))

# --- Offender Demographics ---
with tab2:
    st.header("Offender Sex")
    offender_sex_labels = df.iloc[13:17, 0].values
    offender_sex_counts = df.iloc[13:17, 1].values
    st.bar_chart(pd.DataFrame({"Sex": offender_sex_labels, "Count": offender_sex_counts}).set_index("Sex"))

    st.header("Offender Race")
    offender_race_labels = df.iloc[21:30, 0].values
    offender_race_counts = df.iloc[21:30, 1].values
    st.bar_chart(pd.DataFrame({"Race": offender_race_labels, "Count": offender_race_counts}).set_index("Race"))

    st.header("Offender Ethnicity")
    offender_eth_labels = df.iloc[31:36, 0].values
    offender_eth_counts = df.iloc[31:36, 1].values
    st.bar_chart(pd.DataFrame({"Ethnicity": offender_eth_labels, "Count": offender_eth_counts}).set_index("Ethnicity"))

# --- Weapons & Relationships ---
with tab3:
    st.header("Victim-Offender Relationship")
    relationship_labels = df.iloc[200:220, 0].values
    relationship_counts = df.iloc[200:220, 1].values
    st.bar_chart(pd.DataFrame({"Relationship": relationship_labels, "Count": relationship_counts}).set_index("Relationship"))

    st.header("Weapons Used")
    weapon_labels = df.iloc[220:240, 0].values
    weapon_counts = df.iloc[220:240, 1].values
    st.bar_chart(pd.DataFrame({"Weapon": weapon_labels, "Count": weapon_counts}).set_index("Weapon"))

# --- Locations ---
with tab4:
    st.header("Location Types")
    location_labels = df.iloc[240:280, 0].values
    location_counts = df.iloc[240:280, 1].values
    st.bar_chart(pd.DataFrame({"Location": location_labels, "Count": location_counts}).set_index("Location"))

# --- Time Series ---
with tab5:
    st.header("Crime Reports Over Time")
    dates = pd.to_datetime(df.iloc[66:156, 0].values, errors="coerce")
    reports = df.iloc[66:156, 1].values
    time_df = pd.DataFrame({"Date": dates, "Reports": reports}).dropna()
    st.line_chart(time_df.set_index("Date"))

# --- Download Option ---
st.sidebar.header("Download Data")
csv = df.to_csv(index=False, header=False).encode("utf-8")
st.sidebar.download_button("Download Full Dataset as CSV", data=csv, file_name="crime_data_full.csv", mime="text/csv")
