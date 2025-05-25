import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load and clean data
def load_data():
    df = pd.read_csv("U15554760_20250101_20250523.csv", skiprows=522, header=1)
    df.columns = [
        "Section", "Type", "Order", "Asset Class", "Currency", "Symbol",
        "DateTime", "Quantity", "Trade Price", "Close Price", "Proceeds",
        "Fee", "Basis", "Realized_PnL", "MTM_PnL", "Code", "Unknown"
    ]
    df["Date"] = pd.to_datetime(df["DateTime"], errors="coerce")
    df["Realized_PnL"] = pd.to_numeric(df["Realized_PnL"].astype(str).str.replace(',', ''), errors="coerce")
    df = df.dropna(subset=["Date", "Realized_PnL"])
    return df

df = load_data()

# Streamlit App
st.title("Trade Journal App")

symbol_filter = st.multiselect("Select symbols to display", options=df["Symbol"].unique(), default=df["Symbol"].unique())
filtered_df = df[df["Symbol"].isin(symbol_filter)]

# Cumulative PnL Chart
st.subheader("Cumulative Realized P/L")
cum_pnl = filtered_df.sort_values("Date").groupby("Date")["Realized_PnL"].sum().cumsum()
st.line_chart(cum_pnl)

# Table View
st.subheader("Trade Details")
st.dataframe(filtered_df[["Date", "Symbol", "Quantity", "Trade Price", "Proceeds", "Fee", "Realized_PnL"]])