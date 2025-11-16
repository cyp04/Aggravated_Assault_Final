import streamlit as st
import pandas as pd

# Load raw Excel
@st.cache_data
def load_raw():
    return pd.read_excel("ENG-220 Final project Spreadsheet.xlsx", sheet_name="Sheet1", header=None)

raw = load_raw()

# Section headers
HEADERS = [
    "victim age", "offender sex", "Victim sex", "Offender race",
    "Offender ethnicity", "Victim race", "Victim ethnicity",
    "Victim relationship to offender", "Weapon used for assult",
    "Location Type", "dates and report numbers"
]

def find_header_indices(df, headers):
    idx = {}
    for i in range(len(df)):
        cell = str(df.iloc[i, 0]).strip()
        if cell in headers:
            idx[cell] = i
    return idx

def read_section(df, start_row, next_row):
    labels, counts = [], []
    for r in range(start_row + 1, next_row):
        label = df.iloc[r, 0]
        val = df.iloc[r, 1] if df.shape[1] > 1 else None
        if isinstance(label, str) and label.strip() in HEADERS:
            break
        if pd.isna(label):
            continue
        labels.append(str(label).strip())
        counts.append(pd.to_numeric(val, errors="coerce"))
    return pd.DataFrame({"Label": labels, "Count": counts}).dropna()

header_idx = find_header_indices(raw, HEADERS)

def get_section(name):
    start = header_idx.get(name, None)
    if start is None:
        return pd.DataFrame(columns=["Label", "Count"])
    following = [v for k, v in header_idx.items() if v > start]
    next_row = min(following) if following else len(raw)
    return read_section(raw, start, next_row)

# Extract sections
victim_age = get_section("victim age")
offender_sex = get_section("offender sex")
victim_sex = get_section("Victim sex")
offender_race = get_section("Offender race")
offender_eth = get_section("Offender ethnicity")
victim_race = get_section("Victim race")
victim_eth = get_section("Victim ethnicity")
relationship = get_section("Victim relationship to offender")
weapons = get_section("Weapon used for assult")
locations = get_section("Location Type")

# Time series
dates_start = header_idx.get("dates and report numbers", None)
time_series = pd.DataFrame(columns=["Date", "Reports"])
if dates_start is not None:
    dates, counts = [], []
    for r in range(dates_start + 1, len(raw)):
        d = raw.iloc[r, 0]
        c = raw.iloc[r, 1] if raw.shape[1] > 1 else None
        if isinstance(d, str) and d.strip() in HEADERS:
            break
        dt = pd.to_datetime(d, errors="coerce")
        if pd.isna(dt):
            break
        dates.append(dt)
        counts.append(pd.to_numeric(c, errors="coerce"))
    time_series = pd.DataFrame({"Date": dates, "Reports": counts}).dropna()

# --- Streamlit UI ---
st.title("Crime Data Explorer (Cleaned)")
st.markdown("This app automatically restructures the messy Excel into tidy tables for visualization.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Victim Demographics", "Offender Demographics",
    "Weapons & Relationships", "Locations", "Time Series"
])

with tab1:
    st.subheader("Victim Age")
    st.bar_chart(victim_age.set_index("Label"))
    st.subheader("Victim Sex")
    st.bar_chart(victim_sex.set_index("Label"))
    st.subheader("Victim Race")
    st.bar_chart(victim_race.set_index("Label"))
    st.subheader("Victim Ethnicity")
    st.bar_chart(victim_eth.set_index("Label"))

with tab2:
    st.subheader("Offender Sex")
    st.bar_chart(offender_sex.set_index("Label"))
    st.subheader("Offender Race")
    st.bar_chart(offender_race.set_index("Label"))
    st.subheader("Offender Ethnicity")
    st.bar_chart(offender_eth.set_index("Label"))

with tab3:
    st.subheader("Relationships")
    st.bar_chart(relationship.set_index("Label"))
    st.subheader("Weapons")
    st.bar_chart(weapons.set_index("Label"))

with tab4:
    st.subheader("Locations")
    st.bar_chart(locations.set_index("Label"))

with tab5:
    st.subheader("Reports Over Time")
    if not time_series.empty:
        st.line_chart(time_series.set_index("Date"))
    else:
        st.info("No time series detected.")

# Download cleaned sections
st.sidebar.header("Download Cleaned Data")
bundle = {
    "victim_age": victim_age, "victim_sex": victim_sex, "victim_race": victim_race,
    "victim_ethnicity": victim_eth, "offender_sex": offender_sex,
    "offender_race": offender_race, "offender_ethnicity": offender_eth,
    "relationship": relationship, "weapons": weapons, "locations": locations
}
export = pd.concat([df.assign(Section=name) for name, df in bundle.items()], ignore_index=True)
csv = export.to_csv(index=False).encode("utf-8")
st.sidebar.download_button("Download Cleaned CSV", data=csv, file_name="crime_data_cleaned.csv", mime="text/csv")

