import streamlit as st
import pandas as pd

# Load Excel file
@st.cache_data
def load_raw():
    return pd.read_excel("ENG-220 Final project Spreadsheet.xlsx", sheet_name="Sheet1", header=None)

raw = load_raw()

st.title("ENG-220 Final Project: Crime Data Explorer")
st.markdown("Dashboard parsing sections by headers to avoid brittle indexing.")

# Known headers in the sheet
HEADERS = [
    "victim age",
    "offender sex",
    "Victim sex",
    "Offender race",
    "Offender ethnicity",
    "Victim race",
    "Victim ethnicity",
    "dates and report numbers",
    "United States",
    "United States Clearances",
    "Victim relationship to offender",
    "Weapon used for assult",
    "Location Type",
]

def find_header_indices(df, headers):
    idx = {}
    for i in range(len(df)):
        cell = str(df.iloc[i, 0]).strip()
        if cell in headers:
            idx[cell] = i
    return idx

def read_section(df, start_row, next_row):
    labels = []
    counts = []
    for r in range(start_row + 1, next_row):
        label = df.iloc[r, 0]
        val = df.iloc[r, 1] if df.shape[1] > 1 else None
        # Stop if we hit another header-looking string
        if isinstance(label, str) and label.strip() in HEADERS:
            break
        # Skip empty lines
        if pd.isna(label):
            continue
        labels.append(str(label).strip())
        # Safely convert counts to numeric
        try:
            counts.append(pd.to_numeric(val, errors="coerce"))
        except Exception:
            counts.append(pd.NA)
    # Build DataFrame and drop NA counts
    df_out = pd.DataFrame({"Label": labels, "Count": counts})
    df_out = df_out.dropna(subset=["Count"])
    df_out["Count"] = df_out["Count"].astype(int)
    return df_out

# Locate headers
header_idx = find_header_indices(raw, HEADERS)

# Helper to get section by name
def get_section(name):
    start = header_idx.get(name, None)
    if start is None:
        return pd.DataFrame(columns=["Label", "Count"])
    # Determine next header row
    following = [v for k, v in header_idx.items() if v > start]
    next_row = min(following) if following else len(raw)
    return read_section(raw, start, next_row)

# Sections
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

# Dates + reports (time series)
dates_start = header_idx.get("dates and report numbers", None)
time_series = pd.DataFrame(columns=["Date", "Reports"])
if dates_start is not None:
    # Collect dates until we hit a numeric block; then collect corresponding counts
    # Strategy: first column contains dates (parseable), second column has counts
    # Build by walking forward until we hit non-date segments
    dates = []
    counts = []
    for r in range(dates_start + 1, len(raw)):
        d = raw.iloc[r, 0]
        c = raw.iloc[r, 1] if raw.shape[1] > 1 else None
        # Stop if we hit another known header
        if isinstance(d, str) and d.strip() in HEADERS:
            break
        # parse date (coerce)
        dt = pd.to_datetime(d, errors="coerce")
        if pd.isna(dt):
            # If not a date, likely we've reached numeric-only region; break
            break
        dates.append(dt)
        counts.append(pd.to_numeric(c, errors="coerce"))
    time_series = pd.DataFrame({"Date": dates, "Reports": counts}).dropna()

# Sidebar filters
st.sidebar.header("Filters")
age_sel = st.sidebar.multiselect("Victim age groups", victim_age["Label"].tolist(), default=victim_age["Label"].tolist())
victim_race_sel = st.sidebar.multiselect("Victim race", victim_race["Label"].tolist(), default=victim_race["Label"].tolist())
weapon_sel = st.sidebar.multiselect("Weapon types", weapons["Label"].tolist(), default=weapons["Label"].tolist())
location_sel = st.sidebar.multiselect("Locations", locations["Label"].tolist(), default=locations["Label"].tolist())

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Victim demographics",
    "Offender demographics",
    "Weapons & relationships",
    "Locations",
    "Time series",
])

with tab1:
    st.subheader("Victim age distribution")
    va = victim_age[victim_age["Label"].isin(age_sel)]
    st.bar_chart(va.set_index("Label"))

    st.subheader("Victim sex")
    st.bar_chart(victim_sex.set_index("Label"))

    st.subheader("Victim race")
    vr = victim_race[victim_race["Label"].isin(victim_race_sel)]
    st.bar_chart(vr.set_index("Label"))

    st.subheader("Victim ethnicity")
    st.bar_chart(victim_eth.set_index("Label"))

with tab2:
    st.subheader("Offender sex")
    st.bar_chart(offender_sex.set_index("Label"))

    st.subheader("Offender race")
    st.bar_chart(offender_race.set_index("Label"))

    st.subheader("Offender ethnicity")
    st.bar_chart(offender_eth.set_index("Label"))

with tab3:
    st.subheader("Victim-offender relationship")
    st.bar_chart(relationship.set_index("Label"))

    st.subheader("Weapons used")
    w = weapons[weapons["Label"].isin(weapon_sel)]
    st.bar_chart(w.set_index("Label"))

with tab4:
    st.subheader("Location types")
    loc = locations[locations["Label"].isin(location_sel)]
    st.bar_chart(loc.set_index("Label"))

with tab5:
    st.subheader("Crime reports over time")
    if len(time_series) > 0:
        st.line_chart(time_series.set_index("Date"))
    else:
        st.info("No time series detected from the sheet structure.")

# Download buttons
st.sidebar.header("Download")
# Full raw sheet
full_csv = raw.to_csv(index=False, header=False).encode("utf-8")
st.sidebar.download_button("Download raw sheet (CSV)", data=full_csv, file_name="crime_data_raw.csv", mime="text/csv")

# Cleaned sections bundle
bundle = {
    "victim_age": victim_age,
    "victim_sex": victim_sex,
    "victim_race": victim_race,
    "victim_ethnicity": victim_eth,
    "offender_sex": offender_sex,
    "offender_race": offender_race,
    "offender_ethnicity": offender_eth,
    "relationship": relationship,
    "weapons": weapons,
    "locations": locations,
}
# Concatenate with section label for export
export = pd.concat(
    [df.assign(Section=name) for name, df in bundle.items()],
    ignore_index=True
)
export_csv = export.to_csv(index=False).encode("utf-8")
st.sidebar.download_button("Download cleaned sections (CSV)", data=export_csv, file_name="crime_data_sections.csv", mime="text/csv")

