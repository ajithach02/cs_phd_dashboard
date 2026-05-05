# app.py
# Main Streamlit dashboard for CS PhD Program Comparison
# Author: Ajitha Chittipothula

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# basic page setup — wide layout looks better for dashboards
st.set_page_config(page_title="CS PhD Program Dashboard", layout="wide")
st.title("🎓 CS PhD Program Comparison Dashboard")
st.markdown("Compare top CS PhD programs by rankings, stipends, research areas, and more.")

# load the CSV once and cache it so the app doesn't re-read it every time a filter changes
@st.cache_data
def load_data():
    df = pd.read_csv("data/phd_programs.csv")
    return df

df = load_data()

# sidebar filters — these control what shows up in all the charts below
st.sidebar.header("🔍 Filter Programs")

# let the user pick one or more research areas to focus on
all_areas = sorted(df["research_area"].unique())
selected_areas = st.sidebar.multiselect("Research Area", all_areas, default=all_areas)

# stipend slider — pulls the min and max directly from the data so it always stays accurate
min_stipend = int(df["stipend_monthly"].min())
max_stipend = int(df["stipend_monthly"].max())
stipend_range = st.sidebar.slider(
    "Monthly Stipend ($)", min_stipend, max_stipend, (min_stipend, max_stipend)
)

# acceptance rate slider — lower % means more selective schools
max_acceptance = st.sidebar.slider(
    "Max Acceptance Rate (%)", 1, 20, 20
)

# apply all three filters at once using boolean conditions chained together
filtered_df = df[
    (df["research_area"].isin(selected_areas)) &
    (df["stipend_monthly"] >= stipend_range[0]) &
    (df["stipend_monthly"] <= stipend_range[1]) &
    (df["acceptance_rate"] <= max_acceptance)
]

# show the user how many programs matched their filters
st.markdown(f"### Showing {len(filtered_df)} programs")

# split the dashboard into 4 tabs so it's not one giant scrollable page
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Rankings & Acceptance",
    "💰 Stipend Analysis",
    "🔬 Research Areas",
    "📋 Full Data Table"
])

# TAB 1 — Rankings and Acceptance Rates
with tab1:
    st.subheader("Top Programs by Rank")

    # sort by rank so the best programs show at the top
    fig, ax = plt.subplots(figsize=(10, 20))
    sorted_df = filtered_df.sort_values("rank")
    sns.barplot(data=sorted_df, x="rank", y="university", palette="Blues_r", ax=ax)
    ax.set_xlabel("Rank (lower is better)")
    ax.set_ylabel("University")
    ax.set_title("CS PhD Program Rankings")
    st.pyplot(fig)
    plt.close()  # close the figure so it doesn't bleed into the next chart

    st.subheader("Acceptance Rate by Program")

    # using the same sorted order so the schools line up consistently with the chart above
    fig2, ax2 = plt.subplots(figsize=(10, 20))
    sns.barplot(data=sorted_df, x="acceptance_rate", y="university", palette="Reds", ax=ax2)
    ax2.set_xlabel("Acceptance Rate (%)")
    ax2.set_ylabel("University")
    ax2.set_title("Acceptance Rates (lower = more selective)")
    st.pyplot(fig2)
    plt.close()

# TAB 2 — Stipend Analysis
with tab2:
    st.subheader("Monthly Stipend by Program")
    # sort highest to lowest so the best paying schools are at the top
    fig3, ax3 = plt.subplots(figsize=(8, 35))
    sorted_stip = filtered_df.sort_values("stipend_monthly", ascending=False)
    sns.barplot(data=sorted_stip, x="stipend_monthly", y="university", palette="Greens_r", ax=ax3)
    ax3.set_xlabel("Monthly Stipend ($)")
    ax3.set_ylabel("University")
    ax3.set_title("PhD Monthly Stipends")
    st.pyplot(fig3)
    plt.close()

    st.subheader("Stipend vs Cost of Living")
    # using plotly for interactive hover labels since there are 100 schools
    import plotly.express as px

    fig4 = px.scatter(
        filtered_df,
        x="cost_of_living_index",
        y="stipend_monthly",
        color="rank",
        hover_name="university",  # shows university name on hover
        hover_data=["research_area", "acceptance_rate", "stipend_monthly"],
        color_continuous_scale="RdYlGn_r",
        labels={
            "cost_of_living_index": "Cost of Living Index",
            "stipend_monthly": "Monthly Stipend ($)",
            "rank": "Rank"
        },
        title="Stipend vs Cost of Living (hover for details)"
    )
    st.plotly_chart(fig4, use_container_width=True)

# TAB 3 — Research Areas
with tab3:
    st.subheader("Programs by Research Area")

    # pie chart to show how programs are spread across different research fields
    area_counts = filtered_df["research_area"].value_counts()
    fig5, ax5 = plt.subplots(figsize=(7, 7))
    ax5.pie(area_counts, labels=area_counts.index, autopct="%1.0f%%", startangle=140)
    ax5.set_title("Distribution of Research Areas")
    st.pyplot(fig5)
    plt.close()

    st.subheader("Average Stipend by Research Area")

    # group by research area and average the stipends — useful for comparing fields
    fig6, ax6 = plt.subplots(figsize=(8, 5))
    area_stipend = filtered_df.groupby("research_area")["stipend_monthly"].mean().sort_values(ascending=False)
    sns.barplot(x=area_stipend.values, y=area_stipend.index, palette="viridis", ax=ax6)
    ax6.set_xlabel("Average Monthly Stipend ($)")
    ax6.set_ylabel("Research Area")
    ax6.set_title("Average Stipend by Research Area")
    st.pyplot(fig6)
    plt.close()

# TAB 4 — Full Data Table
with tab4:
    st.subheader("Full Program Data")

    # show the full filtered dataset as an interactive table
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

    # let the user download whatever they filtered as a CSV file
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download filtered data as CSV",
        data=csv,
        file_name="filtered_phd_programs.csv",
        mime="text/csv"
    )