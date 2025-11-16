import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Crime Statistics Dashboard", layout="wide", page_icon="📊")

# Title
st.title("📊 Crime Statistics Dashboard")
st.markdown("FBI Crime Data Analysis and Visualization")

# Load the data
@st.cache_data
def load_data():
    # Read the CSV file
    df = pd.read_csv('crime_statistics_complete_final.csv')
    return df

# Try to load data
try:
    data = load_data()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Time Series", 
        "👥 Demographics", 
        "🔫 Weapons & Locations",
        "🤝 Relationships",
        "📋 Raw Data"
    ])
    
    # Tab 1: Time Series
    with tab1:
        st.header("Crime Reports Over Time")
        
        # Parse time series data (starts after "TIME SERIES DATA - UNITED STATES REPORTS")
        time_data = []
        start_reading = False
        
        with open('crime_statistics_complete_final.csv', 'r') as f:
            for line in f:
                if 'TIME SERIES DATA' in line:
                    start_reading = True
                    next(f)  # Skip header line
                    continue
                if start_reading and line.strip() and ',' in line:
                    parts = line.strip().split(',')
                    if len(parts) >= 3 and parts[0] and parts[1]:
                        try:
                            time_data.append({
                                'Month': parts[0],
                                'Total_Reports': int(parts[1]),
                                'Clearances': int(parts[2])
                            })
                        except:
                            pass
        
        if time_data:
            ts_df = pd.DataFrame(time_data)
            
            # Create line chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=ts_df['Month'], y=ts_df['Total_Reports'],
                                    mode='lines', name='Total Reports',
                                    line=dict(color='#1f77b4', width=2)))
            fig.add_trace(go.Scatter(x=ts_df['Month'], y=ts_df['Clearances'],
                                    mode='lines', name='Clearances',
                                    line=dict(color='#2ca02c', width=2)))
            
            fig.update_layout(
                title="Crime Reports and Clearances Over Time (2014-2025)",
                xaxis_title="Month",
                yaxis_title="Number of Reports",
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Reports", f"{ts_df['Total_Reports'].sum():,}")
            with col2:
                st.metric("Total Clearances", f"{ts_df['Clearances'].sum():,}")
            with col3:
                clearance_rate = (ts_df['Clearances'].sum() / ts_df['Total_Reports'].sum() * 100)
                st.metric("Avg Clearance Rate", f"{clearance_rate:.1f}%")
            with col4:
                st.metric("Peak Month Reports", f"{ts_df['Total_Reports'].max():,}")
    
    # Tab 2: Demographics
    with tab2:
        st.header("Demographic Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Victim Age Distribution")
            victim_age = {
                '20-29': 1425782, '30-39': 1250901, '40-49': 798971,
                '10-19': 706876, '50-59': 502769, '60-69': 239066,
                '0-9': 214102, '70-79': 69725, '80-89': 16637,
                '90+': 4581, 'Unknown': 67614
            }
            fig = px.bar(x=list(victim_age.keys()), y=list(victim_age.values()),
                        labels={'x': 'Age Range', 'y': 'Count'},
                        color=list(victim_age.values()),
                        color_continuous_scale='Blues')
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Victim vs Offender Sex")
            sex_data = pd.DataFrame({
                'Category': ['Male', 'Female', 'Unknown'],
                'Victims': [2853063, 2413675, 30286],
                'Offenders': [3388222, 1035692, 209326]
            })
            fig = go.Figure(data=[
                go.Bar(name='Victims', x=sex_data['Category'], y=sex_data['Victims']),
                go.Bar(name='Offenders', x=sex_data['Category'], y=sex_data['Offenders'])
            ])
            fig.update_layout(barmode='group', height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Race Distribution")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Victim Race**")
            victim_race = pd.DataFrame({
                'Race': ['White', 'Black/African American', 'Asian', 
                        'American Indian/Alaska Native', 'Pacific Islander', 'Unknown'],
                'Count': [2920862, 2025321, 71280, 69802, 15525, 194234]
            })
            fig = px.pie(victim_race, values='Count', names='Race', hole=0.4)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Offender Race**")
            offender_race = pd.DataFrame({
                'Race': ['White', 'Black/African American', 'Asian',
                        'American Indian/Alaska Native', 'Pacific Islander', 'Unknown/Not Specified'],
                'Count': [2231378, 1893694, 50759, 68793, 14674, 775354]
            })
            fig = px.pie(offender_race, values='Count', names='Race', hole=0.4)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Weapons & Locations
    with tab3:
        st.header("Weapons and Locations Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 Weapons Used")
            weapons = pd.DataFrame({
                'Weapon': ['Personal Weapons', 'Handgun', 'Knife/Cutting', 'Firearm',
                          'Blunt Object', 'Other', 'Motor Vehicle', 'Asphyxiation',
                          'None', 'Unknown'],
                'Count': [1073169, 1054702, 870805, 626843, 543908, 494755, 
                         301450, 133729, 126954, 110675]
            })
            fig = px.bar(weapons, x='Count', y='Weapon', orientation='h',
                        color='Count', color_continuous_scale='Reds')
            fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Top 10 Crime Locations")
            locations = pd.DataFrame({
                'Location': ['Residence/Home', 'Highway/Street', 'Parking Lot', 
                            'Other/Unknown', 'Hotel/Motel', 'Bar/Nightclub',
                            'Convenience Store', 'Restaurant', 'Park/Playground',
                            'School'],
                'Count': [2896668, 1132859, 304524, 150187, 83456, 
                         80796, 63777, 59464, 55637, 52802]
            })
            fig = px.bar(locations, x='Count', y='Location', orientation='h',
                        color='Count', color_continuous_scale='Greens')
            fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: Relationships
    with tab4:
        st.header("Victim-Offender Relationships")
        
        relationships = pd.DataFrame({
            'Relationship': ['Unknown', 'Stranger', 'Acquaintance', 'Boyfriend/Girlfriend',
                           'Otherwise Known', 'Spouse', 'Child', 'Offender',
                           'Other Family', 'Parent', 'Friend', 'Sibling'],
            'Count': [1362601, 992889, 744947, 722262, 517922, 235791,
                     180525, 142041, 140496, 133268, 127337, 125890]
        })
        
        fig = px.treemap(relationships, path=['Relationship'], values='Count',
                        color='Count', color_continuous_scale='Viridis')
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top relationships table
        st.subheader("Top 15 Victim-Offender Relationships")
        st.dataframe(relationships.head(15), use_container_width=True)
    
    # Tab 5: Raw Data
    with tab5:
        st.header("Raw Data Explorer")
        st.info("Download the original CSV file to explore all data")
        
        with open('crime_statistics_complete_final.csv', 'r') as f:
            csv_content = f.read()
            st.download_button(
                label="📥 Download Complete Dataset",
                data=csv_content,
                file_name="crime_statistics_complete.csv",
                mime="text/csv"
            )
        
        st.subheader("Data Preview")
        st.text(csv_content[:2000] + "\n... (showing first 2000 characters)")

except FileNotFoundError:
    st.error("⚠️ Please upload 'crime_statistics_complete_final.csv' to the same directory as this script.")
    st.info("You can upload the file and run: `streamlit run app.py`")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please check your data file format.")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("""
    This dashboard visualizes FBI crime statistics including:
    - Time series trends (2014-2025)
    - Demographic breakdowns
    - Weapon and location analysis
    - Victim-offender relationships
    """)
    
    st.header("Instructions")
    st.markdown("""
    1. Place `crime_statistics_complete_final.csv` in the same folder
    2. Run: `streamlit run app.py`
    3. Explore different tabs for insights
    """)
