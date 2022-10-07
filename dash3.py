import pandas as pd
import plotly.express as px
import streamlit as st
import openpyxl as op

df = pd.read_excel(
    io = "Scope_3_Data.xlsx",
    engine = "openpyxl",
    sheet_name = "data",
    skiprows = 0,
    usecols = "A:E",
    nrows = 500
)

st.set_page_config(page_title = "Scope 3 Dashboard",
                   page_icon = ":bar_chart:")

# --------- SIDEBAR --------- #

st.sidebar.header("Please filter here:")
industry = st.sidebar.multiselect(
    "Select Industry:",
    options = list(df["Industry"].unique()),
    default = "Agricultural Commodities"
)

rel_cat = st.sidebar.multiselect(
    "Select Relevant Category:",
    options = list(df["2021_Relevant_Scope_3_Categories"].unique()),
    default = "Other"
)

df_selection = df.query(
    "Industry == @industry & 2021_Relevant_Scope_3_Categories == @rel_cat"
)

#df = df.astype(str)
#st.dataframe(df_selection)

# --------- MAINPAGE --------- #

st.markdown("<h1 style='text-align: center; color: black;'>- Information Dashboard -</h1>", unsafe_allow_html=True)
st.markdown("##")

# KPI's
total_percentage = int((df_selection["Percentage_Makeup_Total_Emissions"]).sum())

st.markdown("<h2 style='text-align: center; color: grey;'>Selected 2021 Scope 3 Emissions Makeup (tonnes):</h2>", unsafe_allow_html=True)
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


st.markdown("---")


# Emission Pie Chart
scope_by_category = (
    df_selection.groupby(by=["2021_Relevant_Scope_3_Categories"]).sum()[["Percentage_Makeup_Total_Emissions"]].sort_values(by="Percentage_Makeup_Total_Emissions")
)
fig_sector = px.pie(
    scope_by_category,
    hole = 0.9,
    names = scope_by_category.index,
    values= "Percentage_Makeup_Total_Emissions",
    title = "<b>2019 Scope 3 Breakdown</b>"
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