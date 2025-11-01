import numpy as np
import pandas as pd

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
initial_portfolio = 4_000_000

# --- Helper functions ---
def mortgage_payment(principal, rate, years):
    monthly_rate = rate / 12
    n_payments = years * 12
    payment = principal * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)
    return payment

def future_value(principal, rate, years):
    return principal * ((1 + rate) ** years)

def calculate_remaining_balance(principal, rate, term_years, years_passed):
    """Calculate remaining mortgage balance after years_passed"""
    if years_passed >= term_years:
        return 0
    monthly_rate = rate / 12
    n_total = term_years * 12
    n_passed = years_passed * 12
    remaining = principal * ((1 + monthly_rate)**n_total - (1 + monthly_rate)**n_passed) / ((1 + monthly_rate)**n_total - 1)
    return remaining

def calculate_interest_paid(principal, rate, term_years, years_passed):
    """Calculate total interest paid over years_passed"""
    monthly_rate = rate / 12
    monthly_payment = mortgage_payment(principal, rate, term_years)
    n_payments = min(years_passed * 12, term_years * 12)
    
    total_paid = monthly_payment * n_payments
    principal_paid = principal - calculate_remaining_balance(principal, rate, term_years, years_passed)
    interest_paid = total_paid - principal_paid
    return interest_paid

def gross_sale_needed(net_cash_needed, tax_rate):
    """Return (gross sale, tax paid, net cash) required to net net_cash_needed from taxable investments."""
    if net_cash_needed <= 0:
        return 0.0, 0.0, 0.0
    gross_sale = net_cash_needed / (1 - tax_rate)
    tax_paid = gross_sale * tax_rate
    net_cash = gross_sale - tax_paid
    return gross_sale, tax_paid, net_cash

def simulate_scenario(price, mortgage_rate, term, investment_return, housing_return, duration, mode):
    """mode = 'cash', 'full', 'hybrid'"""
    if mode == 'cash':
        # Cash purchase: sell stocks to buy house outright (minus down payment)
        net_cash_needed = price - down_payment
        gross_sale, tax_cost, _ = gross_sale_needed(net_cash_needed, capital_gains_tax)
        
        # Remaining investments grow
        remaining_investments = initial_portfolio - gross_sale
        invested_balance = future_value(remaining_investments, investment_return, duration)
        
        # Home appreciates
        home_value = price * ((1 + housing_return) ** duration)
        
        net_worth = invested_balance + home_value
        
        # Total cost = taxes paid + opportunity cost of investments sold
        opportunity_cost = future_value(gross_sale, investment_return, duration) - gross_sale
        total_cost = tax_cost + opportunity_cost
        
        return net_worth, total_cost

    elif mode == 'full':
        # Full mortgage: borrow (price - down_payment), pay down_payment from stocks
        principal = price - down_payment
        down_payment_sale, down_payment_tax, _ = gross_sale_needed(down_payment, capital_gains_tax)
        
        # Monthly mortgage payment
        monthly_payment = mortgage_payment(principal, mortgage_rate, term)
        
        # Calculate interest paid and remaining balance
        interest_paid = calculate_interest_paid(principal, mortgage_rate, term, duration)
        remaining_balance = calculate_remaining_balance(principal, mortgage_rate, term, duration)
        
        # Tax deduction on mortgage interest
        interest_deduction = interest_paid * income_tax_rate
        net_interest = interest_paid - interest_deduction
        
        # Investments grow, but reduced by monthly mortgage payments
        # Assume mortgage payments come from cash flow, not investments
        # Investments = initial - down_payment_sale, then grow
        invested_balance = future_value(initial_portfolio - down_payment_sale, investment_return, duration)
        
        # Home appreciates
        home_value = price * ((1 + housing_return) ** duration)
        
        # Net worth = investments + home equity - remaining mortgage
        home_equity = home_value - remaining_balance
        net_worth = invested_balance + home_equity
        
        # Total cost = net interest paid + down payment tax + opportunity cost of down payment
        opportunity_cost_dp = future_value(down_payment_sale, investment_return, duration) - down_payment_sale
        total_cost = net_interest + down_payment_tax + opportunity_cost_dp
        
        return net_worth, total_cost

    elif mode == 'hybrid':
        # Hybrid: some mortgage (price * LTV), rest from stocks (minus down payment)
        principal = price * loan_to_value_hybrid
        stock_sale_needed = price - principal - down_payment
        net_cash_from_sales = down_payment + max(stock_sale_needed, 0)
        
        # Total stock sale includes down payment
        total_stock_sale, tax_cost, _ = gross_sale_needed(net_cash_from_sales, capital_gains_tax)
        
        # Monthly mortgage payment
        monthly_payment = mortgage_payment(principal, mortgage_rate, term)
        
        # Calculate interest paid and remaining balance
        interest_paid = calculate_interest_paid(principal, mortgage_rate, term, duration)
        remaining_balance = calculate_remaining_balance(principal, mortgage_rate, term, duration)
        
        # Tax deduction on mortgage interest
        interest_deduction = interest_paid * income_tax_rate
        net_interest = interest_paid - interest_deduction
        
        # Investments grow
        invested_balance = future_value(initial_portfolio - total_stock_sale, investment_return, duration)
        
        # Home appreciates
        home_value = price * ((1 + housing_return) ** duration)
        
        # Net worth = investments + home equity - remaining mortgage
        home_equity = home_value - remaining_balance
        net_worth = invested_balance + home_equity
        
        # Total cost = net interest + taxes + opportunity cost of stock sale
        opportunity_cost = future_value(total_stock_sale, investment_return, duration) - total_stock_sale
        total_cost = net_interest + tax_cost + opportunity_cost
        
        return net_worth, total_cost

def run_simulation():
    records = []

    for price in purchase_prices:
        for duration in years:
            for ret_case, inv_return in investment_returns.items():
                for house_case, house_return in housing_returns.items():
                    # Cash scenario calculation
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
    return df


def plot_expected_case(df):
    import matplotlib.pyplot as plt

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


if __name__ == '__main__':
    df = run_simulation()
    plot_expected_case(df)