#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 23:48:55 2022

@author: alexander
"""

import pandas as pd
import plotly.express as px
import streamlit as st

#df = pd.read_csv(r'/Users/alexander/Downloads/sales_data_sample.csv', encoding = "ISO-8859-1")



st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="sales_data_sample.xlsx",
        engine="openpyxl",
        sheet_name="sales_data_sample",
        skiprows=0,
        usecols="A:Y",
        nrows=2824,
    )







# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
year = st.sidebar.multiselect(
    "Select Year:",
    options=df["YEAR_ID"].unique(),
    default=df["YEAR_ID"].unique(),
)

dealsize = st.sidebar.multiselect(
    "Select Deal size:",
    options=df["DEALSIZE"].unique(),
    default=df["DEALSIZE"].unique()
)

df_selection = df.query(
    "YEAR_ID == @year & DEALSIZE == @dealsize"
)

#st.dataframe(df_selection)



# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["SALES"].sum())
average_sale_by_transaction = round(df_selection["SALES"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")


# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["PRODUCTLINE"]).sum()[["SALES"]].sort_values(by="SALES")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="SALES",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by product line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_title="Sales", 
    yaxis_title="Product line"
)


# SALES BY Month [BAR CHART]
sales_by_month = df_selection.groupby(by=["MONTH_ID"]).sum()[["SALES"]]
fig_monthly_sales = px.bar(
    sales_by_month,
    x=sales_by_month.index,
    y="SALES",
    title="<b>Sales by month</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_month),
    template="plotly_white",
)
fig_monthly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
    xaxis_title="Month", 
    yaxis_title="Sales"
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_monthly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
#
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
