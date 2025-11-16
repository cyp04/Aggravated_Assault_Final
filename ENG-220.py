import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Crime Statistics Dashboard", layout="wide", page_icon="📊")

# Title
st.title("📊 Crime Statistics Dashboard")
st.markdown("FBI Crime Data Analysis and Visualization")

# Parse the CSV file manually to handle the multi-section format
def parse_crime_data():
    with open('crime_statistics_complete_final.csv', 'r') as f:
        lines = f.readlines()
    
    # Time series data
    time_data = []
    in_time_series = False
    
    for i, line in enumerate(lines):
        if 'TIME SERIES DATA' in line:
            in_time_series = True
            continue
        if in_time_series and line.strip() and ',' in line:
            parts = [p.strip() for p in line.split(',')]
            if parts[0] and parts[1] and parts[0] != 'Month':
                try:
                    time_data.append({
                        'Month': parts[0],
                        'Total_Reports': int(parts[1]),
                        'Clearances': int(parts[2])
                    })
                except:
                    pass
    
    return pd.DataFrame(time_data)

# Load data
ts_df = parse_crime_data()

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Time Series", 
    "👥 Demographics", 
    "🔫 Weapons & Locations",
    "🤝 Relationships"
])

# Tab 1: Time Series
with tab1:
    st.header("Crime Reports Over Time (2014-2025)")
    
    # Create line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ts_df['Month'], 
        y=ts_df['Total_Reports'],
        mode='lines+markers', 
        name='Total Reports',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=4)
    ))
    fig.add_trace(go.Scatter(
        x=ts_df['Month'], 
        y=ts_df['Clearances'],
        mode='lines+markers', 
        name='Clearances',
        line=dict(color='#2ca02c', width=3),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Reports",
        hovermode='x unified',
        height=500,
        showlegend=True
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
        st.metric("Clearance Rate", f"{clearance_rate:.1f}%")
    with col4:
        st.metric("Peak Reports", f"{ts_df['Total_Reports'].max():,}")
    
    # Show recent trend
    st.subheader("Recent Trend (Last 12 Months)")
    recent_df = ts_df.tail(12)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=recent_df['Month'],
        y=recent_df['Total_Reports'],
        name='Reports',
        marker_color='#1f77b4'
    ))
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

# Tab 2: Demographics
with tab2:
    st.header("Demographic Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Victim Age Distribution")
        victim_age = pd.DataFrame({
            'Age Range': ['20-29', '30-39', '40-49', '10-19', '50-59', '60-69', '0-9', '70-79', '80-89', '90+', 'Unknown'],
            'Count': [1425782, 1250901, 798971, 706876, 502769, 239066, 214102, 69725, 16637, 4581, 67614]
        })
        fig = px.bar(victim_age, x='Age Range', y='Count',
                    color='Count', color_continuous_scale='Blues')
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
            go.Bar(name='Victims', x=sex_data['Category'], y=sex_data['Victims'], marker_color='#ff7f0e'),
            go.Bar(name='Offenders', x=sex_data['Category'], y=sex_data['Offenders'], marker_color='#2ca02c')
        ])
        fig.update_layout(barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Race Distribution Comparison")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Victim Race**")
        victim_race = pd.DataFrame({
            'Race': ['White', 'Black/African American', 'Unknown', 'Asian', 'American Indian', 'Pacific Islander'],
            'Count': [2920862, 2025321, 194234, 71280, 69802, 15525]
        })
        fig = px.pie(victim_race, values='Count', names='Race', hole=0.4,
                    color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Offender Race**")
        offender_race = pd.DataFrame({
            'Race': ['White', 'Black/African American', 'Unknown', 'Asian', 'American Indian', 'Pacific Islander'],
            'Count': [2231378, 1893694, 775354, 50759, 68793, 14674]
        })
        fig = px.pie(offender_race, values='Count', names='Race', hole=0.4,
                    color_discrete_sequence=px.colors.sequential.RdBu)
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
        weapons = weapons.sort_values('Count', ascending=True)
        fig = px.bar(weapons, x='Count', y='Weapon', orientation='h',
                    color='Count', color_continuous_scale='Reds')
        fig.update_layout(height=500, showlegend=False)
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
        locations = locations.sort_values('Count', ascending=True)
        fig = px.bar(locations, x='Count', y='Location', orientation='h',
                    color='Count', color_continuous_scale='Greens')
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Percentage breakdown
    st.subheader("Location Type Breakdown")
    fig = px.pie(locations.sort_values('Count', ascending=False), 
                values='Count', names='Location',
                color_discrete_sequence=px.colors.sequential.Greens)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# Tab 4: Relationships
with tab4:
    st.header("Victim-Offender Relationships")
    
    relationships = pd.DataFrame({
        'Relationship': ['Unknown', 'Stranger', 'Acquaintance', 'Boyfriend/Girlfriend',
                       'Otherwise Known', 'Spouse', 'Child', 'Offender',
                       'Other Family', 'Parent', 'Friend', 'Sibling',
                       'Neighbor', 'Ex-Relationship'],
        'Count': [1362601, 992889, 744947, 722262, 517922, 235791,
                 180525, 142041, 140496, 133268, 127337, 125890,
                 117318, 114346]
    })
    
    # Treemap
    fig = px.treemap(relationships, path=['Relationship'], values='Count',
                    color='Count', color_continuous_scale='Viridis',
                    title="Relationship Treemap (Size = Number of Incidents)")
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Bar chart for top relationships
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Top Relationships")
        fig = px.bar(relationships.head(10), x='Count', y='Relationship',
                    orientation='h', color='Count',
                    color_continuous_scale='Plasma')
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Key Statistics")
        st.metric("Most Common", "Unknown")
        st.metric("Count", f"{1362601:,}")
        st.metric("% of Total", f"{(1362601/relationships['Count'].sum()*100):.1f}%")
        
        known_relationships = relationships[relationships['Relationship'] != 'Unknown']['Count'].sum()
        st.metric("Known Relationships", f"{known_relationships:,}")

# Sidebar
with st.sidebar:
    st.header("📊 Dashboard Info")
    st.info("""
    **Crime Statistics Dashboard**
    
    Visualizing FBI crime data from 2014-2025
    """)
    
    st.header("📈 Data Sections")
    st.markdown("""
    - **Time Series**: Monthly trends
    - **Demographics**: Age, sex, race
    - **Weapons & Locations**: Incident details
    - **Relationships**: Victim-offender connections
    """)
    
    st.header("💾 Data Source")
    st.markdown("Data: `crime_statistics_complete_final.csv`")
    
    # Download button
    with open('crime_statistics_complete_final.csv', 'r') as f:
        st.download_button(
            label="📥 Download CSV",
            data=f.read(),
            file_name="crime_statistics.csv",
            mime="text/csv"
        )
