import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import os

#extracting data

df=pd.read_excel("Adidas-new.xlsx")
st.set_page_config(layout="wide")
st.markdown("<style>div.block-container{padding-top:1rem}</style>",unsafe_allow_html=True)
image=Image.open("addidas.jpg")

col1,col2=st.columns([0.1,0.9])
with col1:
    st.image(image,width=100)

html_title="""
     <style>
     .title_test{
     font-weight:bold;
     padding:5px;
     border-radius:6px
     }
     </style>
     <center><h1 class="title-test">Adidas Interactive Sales Dashboard</h1></center>"""
with col2:
    st.markdown(html_title,unsafe_allow_html=True)
col3,col4,col5=st.columns([0.1,0.45,0.45])
with col3:
    box_date=str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by: \n {box_date}")
with col4:
    fig=px.bar(df,x="Retailer",y="Total Sales",labels={"Total Sales":"Total Sales {$}"},
               title="Total Sales by Retailer",hover_data=["Total Sales"],template="gridon",
               height=500)
    st.plotly_chart(fig,use_container_width=True)
__,view1,d1,view2,d2=st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander=st.expander("Retilaer wise Sales")
    data=df[["Retailer","Total Sales"]].groupby(by="Retailer")["Total Sales"].sum()
    expander.write(data)
with d1:
    st.download_button("Get Data",data=data.to_csv().encode("utf-8"),file_name="RetailerSales.csv",mime="text/csv")

df["Month_Year"]=df["Invoice Date"].dt.strftime("%b '%y")
result=df.groupby(by=df["Month_Year"])["Total Sales"].sum().reset_index()
with col5:
    fig=px.line(result,x="Month_Year",y="Total Sales",title="TotalSales over Time"
                ,template="gridon")
    st.plotly_chart(fig,use_container_width=True)
with view2:
    expander=st.expander("Monthly Sales")
    data=result
    expander.write(data)
with d2:
    st.download_button("Get Data",data=data.to_csv().encode("utf-8"),file_name="MonthlySales.csv",mime="text/csv")
st.divider()
result1=df.groupby(by="State")[["Total Sales","Units Sold"]].sum().reset_index()
fig3=go.Figure()
fig3.add_trace(go.Bar(x=result1["State"],y=result1["Total Sales"],name="Total-Sales"))
fig3.add_trace(go.Scatter(x=result1["State"],y=result1["Units Sold"],mode="lines",name="Units Sold",yaxis="y2"))
fig3.update_layout(
    title="Total Sales and Units Sold by State",xaxis=dict(title="State"),
    yaxis=dict(title="Total Sales",showgrid=False),
    yaxis2=dict(title="Units Sold",overlaying="y",side="right"),
    template="gridon",
    legend=dict(x=1,y=1)
)
_,col6=st.columns([0.1,1])
with col6:
    st.plotly_chart(fig3,use_container_width=True)
_,view3,dwn3=st.columns([0.5,0.45,0.45])
with view3:
    expander=st.expander("View data for Sales by units sold")
    expander.write(result1)
with dwn3:
    st.download_button("Get Data",data=result1.to_csv().encode("utf-8"),file_name="Sales_by_unitssold.csv",mime="text/csv")
st.divider()
_,col7=st.columns([0.1,1])
treemap=df[["Region","City","Total Sales"]].groupby(by=["Region","City"])["Total Sales"].sum().reset_index()
def format_values(value):
    if value>=0:
        return'{:.2f}Lakh'.format(value/1_000_00)
treemap["Total Sales(Formatted)"]=treemap["Total Sales"].apply(format_values)
    
fig4=px.treemap(treemap,path=["Region","City"],values="Total Sales",hover_name="Total Sales(Formatted)",
                hover_data="Total Sales(Formatted)",color="City",height=700,width=600)
fig4.update_traces(textinfo="label+value")
with col7:
    st.subheader(":point_right: Total Sales by Region and City in Treemap")
    st.plotly_chart(fig4,use_container_width=True)
_,view4,dwn4=st.columns([0.5,0.45,0.45])
with view4:
    result2=df[["Region","City","Total Sales"]].groupby(by=["Region","City"])["Total Sales"].sum()
    expander=st.expander("View data for Total Sales by Region and City")
    expander.write(result2)
with dwn4:
    st.download_button("Get Data",data=result2.to_csv().encode("utf-8"),file_name="Sales_by_regionandcity.csv",mime="text/csv")
_,view5,dwn5=st.columns([0.5,0.45,0.45])
with view5:
    expander=st.expander("View Sales raw data")
    expander.write(df)
with dwn5:
    st.download_button("Get Raw Data",data=df.to_csv().encode("utf-8"),file_name="Sales_Raw_data.csv",mime="text/csv")
st.divider()