import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Monthly Expense Dashboard", layout="wide")

st.title("📊 Monthly Expense Manager")

# Salary input
salary = st.number_input("Enter your Monthly Net Salary (₹)", min_value=1000, value=49200, step=500)

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file (monthly expenses)", type=["xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    if 'Expenses' in xls.sheet_names:
        df_raw = xls.parse('Expenses')
        df = df_raw.iloc[1:, [0, 1]]
        df.columns = ['Category', 'Amount']
        df = df.dropna()
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df = df.dropna()

        # User-defined classification
        st.sidebar.title("📂 Categorize Your Expenses")
        unique_cats = df['Category'].unique()
        category_map = {}
        for cat in unique_cats:
            category_map[cat] = st.sidebar.selectbox(f"{cat}", ['Need', 'Want', 'Investment/Savings'], key=cat)

        df['Type'] = df['Category'].map(category_map)

        # Grouped summary
        summary = df.groupby('Type')['Amount'].sum().reset_index()
        total_spent = df['Amount'].sum()
        summary.loc[len(summary.index)] = ['Unallocated', salary - total_spent]

        # Layout
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("💡 Expense Breakdown")
            st.dataframe(df)

        with col2:
            st.subheader("🧮 Summary by Type")
            st.dataframe(summary)

            # Pie chart
            fig, ax = plt.subplots()
            ax.pie(summary['Amount'], labels=summary['Type'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

        st.success(f"Total Spent: ₹{total_spent:,.0f} | Remaining: ₹{salary - total_spent:,.0f}")

    else:
        st.error("The uploaded Excel file does not contain a sheet named 'Expenses'.")
else:
    st.info("Please upload your monthly expenses Excel file to begin.")
