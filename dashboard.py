import pandas as pd #pip install pandas openpyxl
import plotly.express as px # pip install plotly-express
import streamlit as st # pip install streamlit

#emojis: www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Data",
                    page_icon=":globe_with_meridians:",
                    layout="wide"
                    )

df = pd.read_excel(
io='PythonData.xlsx',
engine='openpyxl',
sheet_name='Data',
skiprows=0,
usecols="A:T",
nrows=9995,)



st.dataframe(df)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
City=st.sidebar.multiselect(
    "Select City:",
    options=df["City"].unique(),
    default=df["City"].unique()
    )

customer_Name=st.sidebar.multiselect(
    "Select Customer_Name:",
    options=df["Customer_Name"].unique(),
    default=df["Customer_Name"].unique()
    )

manufacturer = st.sidebar.multiselect(
    "Select the Manufacturer:",
    options=df["Manufacturer"].unique(),
    default=df["Manufacturer"].unique()
    ) 
            
df_selection = df.query(
    "City == @City & Customer_Name == @customer_Name & Manufacturer == @manufacturer"
    )

#---- MAINPAGE ----
st.title(":bar_chart: Sales Data")
st.markdown("##")

#top KPI's
total_sales = (df_selection["Sales"].sum())
average_discount =(df_selection["Discount"].mean(),1) #take average of Quantity, round with 1 decimal
average_quantity = (df_selection["Quantity"].mean(),1) 
average_sales_by_order = round(df_selection["Sales"].mean(),2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Revenue:")
    st.subheader(f"US$ {total_sales:,}") 
with middle_column:
    st.subheader("Order size:")
    st.subheader(f"{average_quantity}",1) 
with right_column:
    st.subheader("Average sales by order:")
    st.subheader(f"US ${average_sales_by_order}")

st.markdown("---") #divider

#Sales by product line [bar chart]
sales_by_product_name = (
    df_selection.groupby(by=["Product_Name"]).sum()[["Sales"]].sort_values(by="Sales")
    )
fig_product_sales = px.bar(
    sales_by_product_name,
    x="Sales",
    y=sales_by_product_name.index,
    orientation="h",
    title="<b>Sales by Product Name</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_name),
    template="plotly_white"
)

st.plotly_chart(fig_product_sales)

#SALES BY REGION [Bar chart]
sales_by_region = df_selection.groupby(by=["Region"]).sum()[["Total"]]
fig_regional_sales = px.bar(
    sales_by_region,
    x=sales_by_region.index,
    y="Sales",
    title="<b>Sales by region</b>",
    coloer_discrete_sequence=["#0083B8"] * len(sales_by_region),
    template="plotly_white",
)
fig_regional_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(howgrid=False)),
)

st.plotly_chart(fig_regional_sales)

