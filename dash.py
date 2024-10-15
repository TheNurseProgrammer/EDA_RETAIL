import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuración de la página de Streamlit
st.set_page_config(page_title="Sales Dashboard", layout="wide")


df = pd.read_csv('./data/output.csv')
df['Date'] = pd.to_datetime(df['Date'])

df_retail = df.groupby("RETAIL")["Sales"].sum()

df_ts = df.groupby("Date")['Sales'].sum().reset_index()

df['Month'] = df['Date'].dt.to_period('M') 
df_grouped = df.groupby('Month')["Sales"].sum().reset_index() 
df_grouped['Pct_Change'] = df_grouped['Sales'].pct_change() * 100  
df_grouped = df_grouped.fillna(0)
df_grouped['Pct_Change'] = df_grouped['Pct_Change'].astype(float)

# Título del Dashboard
st.title("Sales Dashboard")

# Sección 1: Comparación de Ventas por Retail y Series Temporales

st.header("Sales Overview")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Sales by Retail")
    st.plotly_chart(px.pie(df_retail, values='Sales', names=df_retail.index, 
                           title='Sales by Retail',color_discrete_sequence=px.colors.sequential.Inferno), use_container_width=True)
with col2:
    st.subheader("Sales Trend")
    st.plotly_chart(px.line(df_ts, x="Date", y="Sales", title="Sales Over Time"), use_container_width=True)

st.subheader("Monthly Sales and Percentage Change")

metrics_columns = st.columns(len(df_grouped))

for i, col in enumerate(metrics_columns):
    color = "off" if i == 0 else "normal"
    col.metric('Millions', f"{df_grouped['Sales'].iloc[i]/1000000:,.2f}", f"{df_grouped['Pct_Change'].iloc[i]:.2f}%", delta_color=color)

st.plotly_chart(px.line(df_grouped, x=df_grouped['Month'].astype(str), y='Pct_Change', 
                        title='Monthly Sales Variation', markers=True), use_container_width=True)

st.header("ROAS Analysis")

st.plotly_chart(px.bar(df, x='RETAIL', y='ROAS', color='CATEGORIA', 
                       barmode='group', title='ROAS by Retail and Category'), use_container_width=True)

# Sección 3: Correlaciones

st.header("Correlation Analysis")
cuantitativas = ['Impressions', 'Clicks', 'CTR', 'Unique Visitors', 'Frequency', 'Spend', 'Units', 'Sales', 'ROAS']
corr = df[cuantitativas].corr()
st.plotly_chart(px.imshow(corr, title='Correlation Matrix', text_auto=True, 
                          aspect="auto", color_continuous_scale='hot'), use_container_width=True)

# Sección 4: Relación Costo Unitario vs ROAS

st.header("Unit Cost vs ROAS")
st.plotly_chart(px.scatter(df, x='Unit Cost', y='ROAS', title='Unit Cost vs ROAS'), use_container_width=True)

# pie de página
st.markdown("""
    ---
    **Dashboard creado por Alexis Guzman**
""")
