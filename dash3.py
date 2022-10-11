import pandas as pd
import plotly.express as px
import streamlit as st
import openpyxl as op
from PIL import Image

df = pd.read_excel(
    io = "Scope_3_Data.xlsx",
    engine = "openpyxl",
    sheet_name = "data",
    skiprows = 0,
    usecols = "A:E",
    nrows = 500
)
st.set_page_config(page_title = "Scope 3 Dashboard",
                   page_icon = "Geostreams_Final_Logo_White_Transparent.png")

# --------- SIDEBAR --------- #

st.sidebar.header("Please filter here:")
industry = st.sidebar.selectbox(
    "Select Industry:",
    options = list(df["Industry"].unique())
)

category = st.sidebar.multiselect(
    "Select Relevant Category:",
    options = list(df["Category"].unique()),
    default = "Other"
)

warning1 = st.sidebar.text(
    "*Please note that if a there is no data"
)

warning2 = st.sidebar.text(
    "on a selected category for your"
)

warning3 = st.sidebar.text(
    "specific industry, no changes are made"
)


df_selection = df.query(
    "Industry == @industry & Category == @category"
)

#df = df.astype(str)
#st.dataframe(df_selection)

# --------- MAINPAGE --------- #

img = Image.open("Geostreams_Final_Logo_White_Transparent.png")
st.image(img, use_column_width = "auto")

st.markdown("<h1 style='text-align: center; color: black;'>- Information Dashboard -</h1>", unsafe_allow_html=True)
st.markdown("##")

# KPI's
total_percentage = int((df_selection["Percentage"]).sum())

st.markdown("<h2 style='text-align: center; color: grey;'>Selected 2021 Scope 3 Emissions Makeup:</h2>", unsafe_allow_html=True)
st.subheader(f"{total_percentage:,}%")

st.markdown("---")


# Emission Bar chart
#emission_by_country = (
#    df_selection.groupby(by=["Country"]).sum()[["Total_GHG_Emissions"]].sort_values(by="Total_GHG_Emissions")
#)
#fig_emissions = px.bar(
#    emission_by_country,
#    x = "Total_GHG_Emissions",
#    y = emission_by_country.index,
#    orientation = "h",
#    title = "<b>2019 Emissions by Country</b>",
#    color_discrete_sequence = ["#339933"] * len(emission_by_country),
#    template = "plotly_white"
#)
#fig_emissions.update_layout(
#    plot_bgcolor = "rgba(0,0,0,0)",
#    xaxis = (dict(showgrid=False))
#)
#st.plotly_chart(fig_emissions)
#
#
#st.markdown("---")


# Emission Pie Chart
scope_by_category = (
    df_selection.groupby(by=["Category"]).sum()[["Percentage"]].sort_values(by="Percentage")
)
fig_sector = px.pie(
    scope_by_category,
    hole = 0.9,
    names = scope_by_category.index,
    values= "Percentage",
    title = "<b>2021 Scope 3 Breakdown</b>",
    color_discrete_sequence=px.colors.sequential.Purp
)
st.plotly_chart(fig_sector)



# Hide streamlit style
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
