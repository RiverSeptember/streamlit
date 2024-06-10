# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 21:43:22 2024

@author: Bing Hu
"""
import mortgage
from itertools import islice

def calculate_total_return_for_monthly_investment(monthly_investment, annual_interest_rate, inflation_rate, months):
    # Convert annual interest rate to a monthly interest rate
    monthly_interest_rate = annual_interest_rate / 12 / 100
    # Convert annual inflation rate to a monthly inflation rate
    annual_inflation_rate = inflation_rate / 100
    
    # Initialize total amount
    total_amount = 0
    current_monthly_investment = monthly_investment
    
    # Loop through each month and calculate the investment value
    for month in range(1, months + 1):
        # Calculate the amount for the current month
        total_amount = total_amount * (1 + monthly_interest_rate) + current_monthly_investment
        
        # Increase the monthly investment at the end of each year by the inflation rate
        if month % 12 == 0:
            current_monthly_investment *= (1 + annual_inflation_rate)
    
    total_amount = round(total_amount,2)
    return total_amount

def calculate_total_return_for_yearly_investment(annual_investment, annual_interest_rate, annual_inflation_rate, years):
    annual_interest_rate = annual_interest_rate / 100
    annual_inflation_rate = annual_inflation_rate / 100
    
    # Initialize total amount
    total_amount = 0
    current_annual_investment = annual_investment
    # Loop through each year and calculate the investment value
    for year in range(1, years + 1):
        # Calculate the amount for the current year
        total_amount = total_amount * (1 + annual_interest_rate) + current_annual_investment
        current_annual_investment *= (1 + annual_inflation_rate)
    total_amount = round(total_amount,2)
    return total_amount

def mortgage_calculator(interest, loan_amount, months, cashout_time, investment_return):
    m=mortgage.Mortgage(interest=interest/100, amount=loan_amount, months=months)
    payment =  float(m.monthly_payment())
    principle = float(sum(month[0] for month in islice(m.monthly_payment_schedule(), cashout_time)))
    remain_loan = loan_amount - principle
    payment_opp = calculate_total_return_for_monthly_investment(payment, investment_return, 0, cashout_time)
    
    return {'payment':payment, 'remain_loan':remain_loan, 'payment_opp':payment_opp}

def rental_calculator(rent, rent_inflation, investment_return, rent_time):
    rent_opp = calculate_total_return_for_monthly_investment(rent, investment_return, rent_inflation, rent_time)
    return {'rent_opp':rent_opp}


def final_gain(house_price=0, house_inflation=0, rent_inflation=0, downpayment=0, mortgage_interest=0, mortgage_months=0,
               cashout_time=0, rent=0, investment_return=0, sell_commission=6, sell_fixed_cost=10000, 
               property_tax_rate=1, property_tax_rate_inflation_cap=1,
               income_tax_rate=0):
    downpayment_opp = downpayment*((1+investment_return/100)**(cashout_time/12))
    property_tax = house_price*property_tax_rate/100
    property_tax_rate_inflation = min(property_tax_rate_inflation_cap, house_inflation)
    property_tax_opp = calculate_total_return_for_yearly_investment(property_tax, investment_return, property_tax_rate_inflation, int(cashout_time/12))
    #print('property_tax_opp',property_tax_opp)
    rent_opp = rental_calculator(rent, investment_return, rent_inflation, cashout_time)['rent_opp']
    loan_amount = house_price - downpayment
    mortgage_ = mortgage_calculator(mortgage_interest, loan_amount, mortgage_months, cashout_time, investment_return)
    monthly_mortgage_payment = mortgage_['payment']
    payment_opp = mortgage_['payment_opp']
    remain_loan = mortgage_['remain_loan']
    
    house_price_sold = house_price*((1+house_inflation/100)**(cashout_time/12))
    
    buy_cost = round(downpayment_opp + payment_opp + property_tax_opp, 2)
    
    sold_ending_amount = round(house_price_sold - remain_loan - house_price_sold*sell_commission/100 - sell_fixed_cost,2)
    
    nobuy_cost = round(rent_opp,2)
    
    net_gain = round(sold_ending_amount - buy_cost + nobuy_cost, 2)
    
    return {'buy_cost':buy_cost, 'sold_ending_amount':sold_ending_amount, 
            'rent_cost':nobuy_cost,'net_gain':net_gain,
            'monthly_mortgage_payment':monthly_mortgage_payment,
            'house_price_sold':house_price_sold}

def calculate_return(trend, start, end):
    y = (end-start)
    change_percent = (trend.loc[end]['yhat'] - trend.loc[start]['yhat'])/trend.loc[start]['yhat']
    annulized_change_rate = (trend.loc[end]['yhat']  / trend.loc[start]['yhat'] ) ** (1 / y) - 1
    #optimistic return
    change_percent_lucky = (trend.loc[end]['yhat_upper'] - trend.loc[start]['yhat'])/trend.loc[start]['yhat']
    annulized_change_rate_lucky = (trend.loc[end]['yhat_upper']  / trend.loc[start]['yhat'] ) ** (1 / y) - 1
    #pessimistic return
    change_percent_bad = (trend.loc[end]['yhat_lower'] - trend.loc[start]['yhat'])/trend.loc[start]['yhat']
    annulized_change_rate_bad = (trend.loc[end]['yhat_lower']  / trend.loc[start]['yhat'] ) ** (1 / y) - 1
    return [round(change_percent,4), round(annulized_change_rate,4),
           round(change_percent_lucky,4), round(annulized_change_rate_lucky,4),
           round(change_percent_bad,4), round(annulized_change_rate_bad,4)]
