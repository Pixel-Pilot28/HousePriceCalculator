import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Input parameters ---
purchase_prices = [500_000, 600_000]
down_payment = 200_000
mortgage_rates = [0.063]  # 6.3%
terms = [15, 30]
investment_returns = {"expected": 0.07, "downside": 0.04}
housing_returns = {"expected": 0.02, "downside": -0.02}
capital_gains_tax = 0.20
loan_to_value_hybrid = 0.5  # 50% LTV hybrid scenario
income_tax_rate = 0.24

years = [3, 5, 10]

# --- Helper functions ---
def mortgage_payment(principal, rate, years):
    monthly_rate = rate / 12
    n_payments = years * 12
    payment = principal * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)
    return payment

def future_value(principal, rate, years):
    return principal * ((1 + rate) ** years)

def simulate_scenario(price, mortgage_rate, term, investment_return, housing_return, duration, mode):
    """mode = 'cash', 'full', 'hybrid'"""
    if mode == 'cash':
        stock_sale_needed = price - down_payment
        tax_cost = stock_sale_needed * capital_gains_tax
        total_cash_out = price + tax_cost
        home_value = price * ((1 + housing_return) ** duration)
        invested_balance = future_value(4_000_000 - stock_sale_needed, investment_return, duration)
        net_worth = invested_balance + home_value
        total_cost = total_cash_out - (price - home_value)
        return net_worth, total_cost

    elif mode == 'full':
        principal = price - down_payment
        payment = mortgage_payment(principal, mortgage_rate, term)
        total_paid = payment * 12 * duration
        interest_paid = total_paid - (principal * min(1, duration / term))
        interest_deduction = interest_paid * income_tax_rate
        net_interest = interest_paid - interest_deduction
        invested_balance = future_value(4_000_000 - 0, investment_return, duration)
        home_value = price * ((1 + housing_return) ** duration)
        remaining_principal = principal * ((1 + mortgage_rate/12)**(term*12) - (1 + mortgage_rate/12)**(duration*12)) / ((1 + mortgage_rate/12)**(term*12) - 1)
        net_worth = invested_balance + home_value - remaining_principal
        total_cost = net_interest
        return net_worth, total_cost

    elif mode == 'hybrid':
        principal = price * loan_to_value_hybrid
        stock_sale_needed = price - principal - down_payment
        tax_cost = stock_sale_needed * capital_gains_tax
        payment = mortgage_payment(principal, mortgage_rate, term)
        total_paid = payment * 12 * duration
        interest_paid = total_paid - (principal * min(1, duration / term))
        interest_deduction = interest_paid * income_tax_rate
        net_interest = interest_paid - interest_deduction
        invested_balance = future_value(4_000_000 - stock_sale_needed, investment_return, duration)
        home_value = price * ((1 + housing_return) ** duration)
        remaining_principal = principal * ((1 + mortgage_rate/12)**(term*12) - (1 + mortgage_rate/12)**(duration*12)) / ((1 + mortgage_rate/12)**(term*12) - 1)
        net_worth = invested_balance + home_value - remaining_principal
        total_cost = net_interest + tax_cost
        return net_worth, total_cost

# --- Run simulations ---
records = []

for price in purchase_prices:
    for duration in years:
        for ret_case, inv_return in investment_returns.items():
            for house_case, house_return in housing_returns.items():
                # Cash
                nw, cost = simulate_scenario(price, 0, 0, inv_return, house_return, duration, 'cash')
                records.append([price, duration, ret_case, house_case, 'Cash', np.round(nw, 2), np.round(cost, 2)])

                # Full mortgage 15y and 30y
                for term in terms:
                    nw, cost = simulate_scenario(price, 0.063, term, inv_return, house_return, duration, 'full')
                    records.append([price, duration, ret_case, house_case, f'Full {term}y', np.round(nw, 2), np.round(cost, 2)])

                # Hybrid
                for term in terms:
                    nw, cost = simulate_scenario(price, 0.063, term, inv_return, house_return, duration, 'hybrid')
                    records.append([price, duration, ret_case, house_case, f'Hybrid {term}y', np.round(nw, 2), np.round(cost, 2)])

df = pd.DataFrame(records, columns=['Price', 'Years', 'Return Case', 'Housing Case', 'Scenario', 'Net Worth', 'Total Cost'])

# --- Visualization: Risk-adjusted Net Worth Over Time ---
plt.figure(figsize=(12, 6))
for scenario in ['Cash', 'Full 30y', 'Hybrid 30y']:
    subset = df[(df['Price'] == 600_000) & (df['Scenario'] == scenario) & (df['Return Case'] == 'expected') & (df['Housing Case'] == 'expected')]
    plt.plot(subset['Years'], subset['Net Worth'], marker='o', label=scenario)

plt.title("Risk-Adjusted Net Worth Over Time – $600K Home (Expected Case)")
plt.xlabel("Years")
plt.ylabel("Net Worth ($)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# import caas_jupyter_tools
# caas_jupyter_tools.display_dataframe_to_user("Home Purchase Scenario Analysis", df)
