import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime

@st.cache_data
def fetch_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sairam@123",
        database="astro"
    )
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT a.id, a.name, a.absolute_magnitude_h, a.estimated_diameter_min_km,
               a.estimated_diameter_max_km, a.is_potentially_hazardous_asteroid,
               c.close_approach_date, c.relative_velocity_kmph, c.astronomical,
               c.miss_distance_km, c.miss_distance_lunar, c.orbiting_body
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
    """
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return pd.DataFrame(data)


def main():
    st.set_page_config(page_title="NASA Asteroid Tracker 🔭", page_icon=":rocket:", layout="wide")

    st.sidebar.title("🌌 Asteroid Approaches")
    page = st.sidebar.radio("Menu", ["Filter Criteria", "Queries"])

    with st.spinner('Fetching asteroid data...'):
        df = fetch_data()
        df['close_approach_date'] = pd.to_datetime(df['close_approach_date'])

    st.title("🚀 NASA Asteroid Tracker")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Asteroids", f"{df.shape[0]}")
    col2.metric("Average Magnitude", f"{df['absolute_magnitude_h'].mean():.2f}")
    col3.metric("Avg Diameter (km)", f"{(df['estimated_diameter_min_km'].mean() + df['estimated_diameter_max_km'].mean()) / 2:.4f}")

    st.markdown("---")

    if page == "Filter Criteria":
        st.subheader("🔍 Filter Asteroids")

        with st.form("filters"):
            col1, col2 = st.columns(2)
            with col1:
                min_mag, max_mag = st.slider(
                    "Magnitude Range",
                    float(df['absolute_magnitude_h'].min()),
                    float(df['absolute_magnitude_h'].max()),
                    (float(df['absolute_magnitude_h'].min()), float(df['absolute_magnitude_h'].max()))
                )

                min_dia, max_dia = st.slider(
                    "Min Estimated Diameter (km)",
                    float(df['estimated_diameter_min_km'].min()),
                    float(df['estimated_diameter_min_km'].max()),
                    (float(df['estimated_diameter_min_km'].min()), float(df['estimated_diameter_min_km'].max()))
                )

                max_dia_min, max_dia_max = st.slider(
                    "Max Estimated Diameter (km)",
                    float(df['estimated_diameter_max_km'].min()),
                    float(df['estimated_diameter_max_km'].max()),
                    (float(df['estimated_diameter_max_km'].min()), float(df['estimated_diameter_max_km'].max()))
                )

            with col2:
                vel_min, vel_max = st.slider(
                    "Relative Velocity (km/h)",
                    float(df['relative_velocity_kmph'].min()),
                    float(df['relative_velocity_kmph'].max()),
                    (float(df['relative_velocity_kmph'].min()), float(df['relative_velocity_kmph'].max()))
                )

                astro_min, astro_max = st.slider(
                    "Astronomical Unit Range",
                    float(df['astronomical'].min()),
                    float(df['astronomical'].max()),
                    (float(df['astronomical'].min()), float(df['astronomical'].max()))
                )

                start_date = st.date_input("Start Date", df['close_approach_date'].min().date())
                end_date = st.date_input("End Date", df['close_approach_date'].max().date())

                hazardous = st.selectbox(
                    "Potentially Hazardous?",
                    options=[0, 1],
                    format_func=lambda x: "Yes" if x == 1 else "No"
                )

            submit_button = st.form_submit_button("Apply Filters 🚀")

        if submit_button:
            with st.spinner('Filtering asteroids...'):
                mask = (
                    (df['absolute_magnitude_h'].between(min_mag, max_mag)) &
                    (df['estimated_diameter_min_km'].between(min_dia, max_dia)) &
                    (df['estimated_diameter_max_km'].between(max_dia_min, max_dia_max)) &
                    (df['relative_velocity_kmph'].between(vel_min, vel_max)) &
                    (df['astronomical'].between(astro_min, astro_max)) &
                    (df['close_approach_date'].dt.date >= start_date) &
                    (df['close_approach_date'].dt.date <= end_date) &
                    (df['is_potentially_hazardous_asteroid'] == hazardous)
                )

                filtered_df = df[mask]

                st.success(f"✅ Found {filtered_df.shape[0]} asteroids matching your filters!")
                st.markdown("### 🛰️ Filtered Asteroids")
                st.dataframe(filtered_df, use_container_width=True)

    else:
        st.subheader("📋 Pre-built Queries")
        st.write("Select a query to get instant answers about asteroids!")

        query_options = {
            "Top 5 Largest Asteroids": """
                SELECT id, name, estimated_diameter_max_km 
                FROM asteroids 
                ORDER BY estimated_diameter_max_km DESC 
                LIMIT 5
            """,
            "Top 5 Fastest Asteroids": """
                SELECT a.id, a.name, c.relative_velocity_kmph 
                FROM asteroids a
                JOIN close_approach c ON a.id = c.neo_reference_id
                ORDER BY c.relative_velocity_kmph DESC
                LIMIT 5
            """,
            "Potentially Hazardous Asteroids": """
                SELECT id, name, is_potentially_hazardous_asteroid 
                FROM asteroids 
                WHERE is_potentially_hazardous_asteroid = 1
            """,
            "Closest to Earth Asteroids (Min Astronomical Unit)": """
                SELECT a.id, a.name, c.astronomical
                FROM asteroids a
                JOIN close_approach c ON a.id = c.neo_reference_id
                ORDER BY c.astronomical ASC
                LIMIT 5
            """
        }

        selected_query_name = st.selectbox("Choose a Query:", list(query_options.keys()))

        if st.button("Run Query 🚀"):
            query = query_options[selected_query_name]

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Sairam@123",
                database="astro"
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()

            if results:
                df_query = pd.DataFrame(results)
                st.success(f"✅ Results for: {selected_query_name}")
                st.dataframe(df_query, use_container_width=True)
            else:
                st.warning("⚠️ No data found for this query.")


# Run App
if __name__ == "__main__":
    main()
