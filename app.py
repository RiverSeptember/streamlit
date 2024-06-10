# -*- coding: utf-8 -*-

import streamlit as st
from utils import final_gain, calculate_return
import pandas as pd
import matplotlib.pyplot as plt

button_css = """
    <style>
    .center-button {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .btn {
        font-size: 20px;
        padding: 10px 20px;
        color: white;
        background-color: #4CAF50;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        text-align: center;
    }
    .btn:hover {
        background-color: #45a049;
    }
    </style>
"""

# Inject custom CSS
st.markdown(button_css, unsafe_allow_html=True)

def show_result(result):
    df = pd.DataFrame(list(result.items()), columns=['Metric', 'Value'])
    st.subheader("Net Gain/Loss")
    net_gain=result['net_gain']
    if net_gain >= 0:
        st.metric(label=" ", value=f"${net_gain:,.2f}", delta=f"+${net_gain:,.2f}", delta_color="normal")
    else:
        st.metric(label=" ", value=f"${net_gain:,.2f}", delta=f"${net_gain:,.2f}", delta_color="inverse")
    st.subheader("House Sold Price")
    house_price_sold=result['house_price_sold']
    st.metric(label=" ", value=f"${house_price_sold:,.2f}")
    st.subheader("Data Overview")
    st.dataframe(df)
    st.subheader("Bar Chart")
    fig, ax = plt.subplots()
    ax.bar(df['Metric'], df['Value'], color=['blue', 'green', 'red', 'purple', 'orange'])
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Value')
    plt.title('Financial Metrics')
    st.pyplot(fig)
    
st.title('Buy OR Rent? Ask AI!')



col1, col2 = st.columns(2)
with col1:
    house_price = st.number_input("Choose Your House Price", 0, 10000000, value=1000000)
    downpayment_ratio = st.number_input("Downpayment Ratio", 0, 100, value=15)
    mortgage_interest = st.number_input("Mortgage Interest Rate", 0.01, 20.0, value=4.0)
    property_tax_rate = st.number_input("Property Tax Rate", 0.0, 10.0, value=1.2)
    property_tax_rate_inflation_cap = st.number_input("Property Tax Inflation Cap in Your Region", 0, 10, value=1)
    rent = st.number_input("Substiture Rental Fee (Monthly)", 0, 100000, value=4000)
    
    for _ in range(4):
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    
with col2:
    rent_inflation = st.slider("Rental Annual Inflation Rate", 0, 20, value=3)
    investment_return = st.slider("What's your alternative investment annual return rate?", 0, 50, value=8)
    mortgage_year = st.slider("Mortgage Duration in Years", 0, 30, value=30)
    sell_commission = st.slider("Commission Rate to Agent When Sell", 0.0, 10.0, value=5.0)
    sell_fixed_cost = st.slider("One Time Miscallenous Cost When Sell", 0, 100000, value=10000)
    for _ in range(4):
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    

downpayment = house_price*downpayment_ratio/100
mortgage_months = mortgage_year*12           

with col1:
    st.header('Part 1: Calculate!')
    cashout_time_years = st.slider("When do you plan to sell it(Years from Purchase)?", 0, 30, value=5)
    cashout_time = cashout_time_years*12  
    house_inflation = st.number_input("Housing Price Annual Inflation Rate", 0.0, 50.0, value=1.8)
    
result1 = final_gain(house_price=house_price, 
    house_inflation=house_inflation, 
    rent_inflation=rent_inflation, 
    downpayment=downpayment, 
    mortgage_interest=mortgage_interest, 
    mortgage_months=mortgage_months,
    cashout_time=cashout_time, 
    rent=rent, 
    investment_return=investment_return, 
    sell_commission=sell_commission, 
    sell_fixed_cost=sell_fixed_cost, 
    property_tax_rate=property_tax_rate, 
    property_tax_rate_inflation_cap=property_tax_rate_inflation_cap,
    income_tax_rate=0)
with col1:
    st.subheader("Your Guessed House Inflation")
    if house_inflation >= 0:
        st.metric(label="Your Guessed House Inflation", value=f"{house_inflation:,.2f}")
    else:
        st.metric(label="Your Guessed House Inflation", value=f"{house_inflation:,.2f}")
    
    show_result(result1)

#trigger = st.button('See My Return', on_click=show_result(result1))


with col2:
    st.header('Part 2: Ask AI!')
    start = st.slider("Buy in Year", 1994, 2053, value=2024)
    end = st.slider("Sell in Year", start+1, 2054, value=start+5)
    
       

trend = pd.read_csv('trend_forecasted.csv', dtype = {'year': 'int64','ds': 'str','yhat': 'float64'})
trend=trend.set_index('year')
change_percent, annulized_change, change_lucky, annual_lucky, change_bad, annual_bad = calculate_return(trend, start, end)

cashout_time2 = (end-start)*12 
house_inflation2 = annulized_change*100

with col2:
    st.subheader("AI Predicted Annulized House Inflation")
    if house_inflation2 >= 0:
        st.metric(label="AI Predicted Annulized House Inflation", value=f"{house_inflation2:,.2f}")
    else:
        st.metric(label="AI Predicted Annulized House Inflation", value=f"{house_inflation2:,.2f}")

result2 = final_gain(house_price=house_price, 
    house_inflation=house_inflation2, 
    rent_inflation=rent_inflation, 
    downpayment=downpayment, 
    mortgage_interest=mortgage_interest, 
    mortgage_months=mortgage_months,
    cashout_time=cashout_time2, 
    rent=rent, 
    investment_return=investment_return, 
    sell_commission=sell_commission, 
    sell_fixed_cost=sell_fixed_cost, 
    property_tax_rate=property_tax_rate, 
    property_tax_rate_inflation_cap=property_tax_rate_inflation_cap,
    income_tax_rate=0)

#trigger = st.button('See AI Result', on_click=show_result(result2))
with col2:
    show_result(result2) 

house_inflation_lucky = annual_lucky*100
house_inflation_bad = annual_bad*100

result_lucky = final_gain(house_price=house_price, 
    house_inflation=house_inflation_lucky, 
    rent_inflation=rent_inflation, 
    downpayment=downpayment, 
    mortgage_interest=mortgage_interest, 
    mortgage_months=mortgage_months,
    cashout_time=cashout_time2, 
    rent=rent, 
    investment_return=investment_return, 
    sell_commission=sell_commission, 
    sell_fixed_cost=sell_fixed_cost, 
    property_tax_rate=property_tax_rate, 
    property_tax_rate_inflation_cap=property_tax_rate_inflation_cap,
    income_tax_rate=0)

result_bad = final_gain(house_price=house_price, 
    house_inflation=house_inflation_bad, 
    rent_inflation=rent_inflation, 
    downpayment=downpayment, 
    mortgage_interest=mortgage_interest, 
    mortgage_months=mortgage_months,
    cashout_time=cashout_time2, 
    rent=rent, 
    investment_return=investment_return, 
    sell_commission=sell_commission, 
    sell_fixed_cost=sell_fixed_cost, 
    property_tax_rate=property_tax_rate, 
    property_tax_rate_inflation_cap=property_tax_rate_inflation_cap,
    income_tax_rate=0)


if st.button("Want to know good time and bad time?"):
    with st.expander("Expanding Details"):
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("If Good Time")
            if house_inflation_lucky >= 0:
                st.metric(label="AI Predicted Annulized House Inflation", value=f"{house_inflation_lucky:,.2f}")
            else:
                st.metric(label="AI Predicted Annulized House Inflation", value=f"{house_inflation_lucky:,.2f}")
            show_result(result_lucky)
        with col4:
            st.subheader("If Bad Time")
            if house_inflation_bad >= 0:
                st.metric(label="AI Predicted Annulized House Inflation", value=f"{house_inflation_bad:,.2f}")
            else:
                st.metric(label="AI Predicted Annulized House Inflation", value=f"{house_inflation_bad:,.2f}")
            show_result(result_bad)


