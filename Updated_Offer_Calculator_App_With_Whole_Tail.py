
import streamlit as st

# App Title
st.title("Real Estate Offer Calculator")

# Offer Type Selection
offer_type = st.selectbox("Select Offer Type", ["Straight Cash", "Novation Agreement", "Seller Financing"])

# Input Fields
arv = st.number_input("After Repair Value (ARV)", min_value=0.0, step=1000.0)
renovation_costs = st.number_input("Renovation Costs", min_value=0.0, step=1000.0)
taxes = st.number_input("Taxes (Annual)", min_value=0.0, step=100.0)
insurance = st.number_input("Insurance (6 months)", min_value=0.0, step=100.0, value=3000.0)
profit_target = st.number_input("Profit Target (12% of ARV)", value=arv * 0.12, format="%.2f")

# Additional Option for Seller Financing
whole_tail = False
if offer_type == "Seller Financing":
    whole_tail = st.checkbox("Whole Tail (3 months carrying costs)")

# Additional Inputs for Specific Offers
if offer_type == "Straight Cash":
    # Constants for Straight Cash Offer
    loan_interest = 0.11  # 11% annual interest
    loan_points = 0.02  # 2% loan points
    max_loan = arv * 0.7  # Maximum loan (70% of ARV)
    closing_costs = max_loan * 0.05 + 3000  # 5% of loan + $3000
    interest_cost = max_loan * loan_interest / 2  # 6-month carry
    realtor_fee = arv * 0.04  # 4% of ARV for realtor
    carrying_costs = taxes / 2 + insurance  # 6-month taxes + insurance

    # Total Costs for Straight Cash Offer
    total_costs = (
        renovation_costs +
        carrying_costs +
        interest_cost +
        closing_costs +
        profit_target +
        realtor_fee
    )

elif offer_type == "Novation Agreement":
    # Novation-specific Calculations
    interest_cost = renovation_costs * 0.11 / 2  # Interest only on reno costs for 6 months
    attorney_fees = 3000
    realtor_fee = arv * 0.04  # 4% of ARV
    carrying_costs = taxes / 2 + insurance  # 6-month taxes + insurance

    # Total Costs for Novation Agreement
    total_costs = (
        renovation_costs +
        carrying_costs +
        interest_cost +
        profit_target +
        attorney_fees +
        realtor_fee
    )

elif offer_type == "Seller Financing":
    # Seller Financing-specific Calculations
    down_payment = arv * 0.07  # 7% of ARV
    loan_amount = arv * 0.93  # Remaining 93% financed by seller
    interest_cost = loan_amount * 0.10 / 2  # 6-month interest at 10%
    title_fees = 5000  # Estimated title fees
    attorney_fees = 3000

    # Adjust carrying costs for Whole Tail
    if whole_tail:
        carrying_costs = taxes / 4 + insurance / 2  # 3-month taxes + insurance
    else:
        carrying_costs = taxes / 2 + insurance  # 6-month taxes + insurance

    # Total Costs for Seller Financing
    total_costs = (
        renovation_costs +
        carrying_costs +
        interest_cost +
        profit_target +
        title_fees +
        attorney_fees
    )

# Calculate MAO
mao = arv - total_costs

# Display Results
st.write(f"### Maximum Allowable Offer ({offer_type}): ${mao:,.2f}")
