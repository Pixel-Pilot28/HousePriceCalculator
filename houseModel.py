import numpy as np
import pandas as pd

# --- Input parameters ---
purchase_prices = [550_000, 600_000]
down_payment = 200_000
mortgage_rates = [0.057]  # 5.7%
terms = [15, 30]
investment_returns = {"expected": 0.07, "downside": 0.04}
housing_returns = {"expected": 0.02, "downside": -0.02}
capital_gains_tax = 0.20
loan_to_value_hybrid = 0.5  # 50% LTV hybrid scenario
income_tax_rate = 0.24
property_tax_rate = 0.012  # 1.2% of home value annually
home_insurance_rate = 0.005  # 0.5% of home value annually
closing_cost_rate = 0.03  # 3% of purchase price (one-time)
monthly_cash_flow = 5_000  # Monthly amount available for mortgage payments or investments
investment_cost_basis_ratio = 0.6  # 60% of investment value is cost basis (original principal), 40% is gains

# Bear market simulator
bear_market_enabled = False  # Set to True to simulate a temporary market downturn
bear_market_year = 2  # Year when bear market occurs (e.g., 2 means after 2 years)
bear_market_drop = 0.30  # Percentage drop (e.g., 0.30 = 30% decrease)
bear_market_recovery_years = 2  # Years to recover to normal trajectory

years = [3, 5, 7, 10]
initial_portfolio = 4_000_000

# --- Helper functions ---
def mortgage_payment(principal, rate, years):
    """Return monthly payment; handle zero-rate loans explicitly."""
    if rate == 0:
        return principal / (years * 12)
    monthly_rate = rate / 12
    n_payments = years * 12
    payment = principal * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)
    return payment

def future_value(principal, rate, years):
    return principal * ((1 + rate) ** years)

def future_value_with_bear_market(principal, rate, years, bear_enabled, bear_year, bear_drop, bear_recovery_years):
    """
    Calculate future value with optional bear market scenario.
    
    Args:
        principal: Initial investment amount
        rate: Annual rate of return
        years: Total years to project
        bear_enabled: Whether to simulate a bear market
        bear_year: Year when bear market occurs
        bear_drop: Percentage drop (e.g., 0.30 for 30% decline)
        bear_recovery_years: Years to recover to normal trajectory
    
    Returns:
        Future value after accounting for bear market
    """
    if principal <= 0:
        return 0.0
    if not bear_enabled or bear_year < 0 or bear_year >= years or bear_drop <= 0:
        # No bear market or it happens after our time horizon
        return future_value(principal, rate, years)
    
    # Grow until bear market
    value_before_crash = principal * ((1 + rate) ** bear_year)
    
    # Calculate remaining years and recovery
    remaining_years = years - bear_year
    
    return _recover_after_crash(value_before_crash, rate, remaining_years, bear_drop, bear_recovery_years)


def _recover_after_crash(pre_crash_value, rate, years_after_crash, bear_drop, bear_recovery_years):
    """
    Grow a balance through a crash with partial recovery.
    
    Model: After crash, portfolio grows at normal rate but never fully recovers
    to original trajectory. This represents market "scarring" effects where
    bear markets have permanent wealth impacts.
    """
    if pre_crash_value <= 0:
        return 0.0

    post_crash_value = pre_crash_value * (1 - bear_drop)

    if years_after_crash <= 0:
        return post_crash_value

    if bear_drop <= 0:
        return pre_crash_value * ((1 + rate) ** years_after_crash)

    if bear_recovery_years <= 0:
        # No recovery period specified - grow from crashed value at normal rate
        return post_crash_value * ((1 + rate) ** years_after_crash)

    # Calculate what crashed value would grow to at normal rate
    crashed_final = post_crash_value * ((1 + rate) ** years_after_crash)
    
    # Calculate what original trajectory would be
    normal_final = pre_crash_value * ((1 + rate) ** years_after_crash)
    
    # During recovery period, interpolate between crashed path and partial recovery
    # Recovery closes the gap by a fraction, not 100%
    if years_after_crash <= bear_recovery_years:
        # Partial recovery during recovery window
        recovery_fraction = years_after_crash / bear_recovery_years
        # Close 70% of the gap to normal trajectory
        recovery_factor = 0.70
        return crashed_final + (normal_final - crashed_final) * recovery_fraction * recovery_factor
    else:
        # After recovery period ends, maintain 70% gap closure
        recovery_factor = 0.70
        final_gap = (normal_final - crashed_final) * recovery_factor
        return crashed_final + final_gap

def future_value_annuity(monthly_payment, annual_rate, years):
    """Calculate future value of monthly payments invested at annual_rate"""
    if monthly_payment == 0 or annual_rate == 0:
        return monthly_payment * years * 12
    monthly_rate = (1 + annual_rate) ** (1/12) - 1
    n_months = years * 12
    return monthly_payment * (((1 + monthly_rate)**n_months - 1) / monthly_rate)

def future_value_annuity_with_bear_market(monthly_payment, annual_rate, years, bear_enabled, bear_year, bear_drop, bear_recovery_years):
    """
    Calculate future value of monthly contributions with optional bear market.
    
    Contributions made before bear market are affected by the downturn.
    Contributions made during/after bear market grow normally from their contribution date.
    """
    if not bear_enabled or bear_year >= years:
        return future_value_annuity(monthly_payment, annual_rate, years)
    
    # Calculate value of contributions made before bear market
    pre_bear_contributions = future_value_annuity(monthly_payment, annual_rate, bear_year)
    remaining_years = years - bear_year

    pre_bear_final = _recover_after_crash(pre_bear_contributions, annual_rate, remaining_years, bear_drop, bear_recovery_years)
    
    # Calculate contributions made after bear market (these grow normally)
    post_bear_contributions = future_value_annuity(monthly_payment, annual_rate, remaining_years)
    
    return pre_bear_final + post_bear_contributions

def calculate_remaining_balance(principal, rate, term_years, years_passed):
    """Calculate remaining mortgage balance after years_passed"""
    if years_passed >= term_years:
        return 0
    if rate == 0:
        paid_fraction = min(1.0, years_passed / term_years)
        return principal * (1 - paid_fraction)
    monthly_rate = rate / 12
    n_total = term_years * 12
    n_passed = years_passed * 12
    remaining = principal * ((1 + monthly_rate)**n_total - (1 + monthly_rate)**n_passed) / ((1 + monthly_rate)**n_total - 1)
    return remaining

def calculate_interest_paid(principal, rate, term_years, years_passed):
    """Calculate total interest paid over years_passed"""
    if rate == 0:
        return 0.0
    monthly_payment = mortgage_payment(principal, rate, term_years)
    n_payments = min(years_passed * 12, term_years * 12)
    
    total_paid = monthly_payment * n_payments
    principal_paid = principal - calculate_remaining_balance(principal, rate, term_years, years_passed)
    interest_paid = total_paid - principal_paid
    return interest_paid

def gross_sale_needed(net_cash_needed, tax_rate, cost_basis_ratio):
    """
    Return (gross sale, tax paid, net cash) required to net net_cash_needed from taxable investments.
    
    Args:
        net_cash_needed: The amount of cash needed after taxes
        tax_rate: Capital gains tax rate
        cost_basis_ratio: Fraction of investment value that is original principal (not taxable)
                         e.g., 0.6 means 60% is cost basis, 40% is gains
    
    Example:
        If you need $100k and cost_basis_ratio=0.6:
        - You sell $X
        - Cost basis = $X * 0.6 (not taxed)
        - Gains = $X * 0.4 (taxed at tax_rate)
        - Net cash = $X - ($X * 0.4 * tax_rate)
        - Solve: $X = net_cash_needed / (1 - (1 - cost_basis_ratio) * tax_rate)
    """
    if net_cash_needed <= 0:
        return 0.0, 0.0, 0.0
    
    # Calculate taxable portion (gains)
    taxable_portion = 1 - cost_basis_ratio
    
    # Gross sale needed after accounting for tax on gains only
    gross_sale = net_cash_needed / (1 - (taxable_portion * tax_rate))
    
    # Tax is only on the gains portion
    gains = gross_sale * taxable_portion
    tax_paid = gains * tax_rate
    
    # Verify: net cash should equal gross_sale - tax_paid
    net_cash = gross_sale - tax_paid
    
    return gross_sale, tax_paid, net_cash

def simulate_scenario(price, mortgage_rate, term, investment_return, housing_return, duration, mode):
    """mode = 'cash', 'full', 'hybrid'"""
    # Calculate one-time closing costs
    closing_costs = price * closing_cost_rate
    
    # Calculate ongoing monthly ownership costs (property tax + insurance)
    annual_property_tax = price * property_tax_rate
    annual_insurance = price * home_insurance_rate
    monthly_ownership_costs = (annual_property_tax + annual_insurance) / 12
    
    if mode == 'cash':
        # Cash purchase: sell stocks to buy house outright + closing costs
        net_cash_needed = price + closing_costs
        gross_sale, tax_cost, _ = gross_sale_needed(net_cash_needed, capital_gains_tax, investment_cost_basis_ratio)
        
        # Remaining investments grow (with optional bear market)
        remaining_investments = initial_portfolio - gross_sale
        if remaining_investments < -1e-9:
            raise ValueError("Initial portfolio is insufficient for a cash purchase at this price")
        remaining_investments = max(0.0, remaining_investments)
        invested_balance = future_value_with_bear_market(remaining_investments, investment_return, duration,
                                                         bear_market_enabled, bear_market_year, 
                                                         bear_market_drop, bear_market_recovery_years)
        
        # BENEFIT: No mortgage payment, but still pay property tax & insurance
        # Invest cash flow remaining after ownership costs
        cash_flow_to_invest = max(0, monthly_cash_flow - monthly_ownership_costs)
        invested_cash_flow = future_value_annuity_with_bear_market(cash_flow_to_invest, investment_return, duration,
                                                                   bear_market_enabled, bear_market_year,
                                                                   bear_market_drop, bear_market_recovery_years)
        
        # Home appreciates
        home_value = price * ((1 + housing_return) ** duration)
        
        net_worth = invested_balance + invested_cash_flow + home_value
        
        # Out-of-pocket cost = taxes + closing costs (NO opportunity cost - already in net worth)
        out_of_pocket_cost = tax_cost + closing_costs
        
        return net_worth, out_of_pocket_cost

    elif mode == 'full':
        # Full mortgage: borrow (price - down_payment), pay down_payment + closing costs from stocks
        principal = price - down_payment
        net_cash_needed = down_payment + closing_costs
        down_payment_sale, down_payment_tax, _ = gross_sale_needed(net_cash_needed, capital_gains_tax, investment_cost_basis_ratio)
        
        # Calculate mortgage payment
        monthly_pmt = mortgage_payment(principal, mortgage_rate, term)
        
        # Calculate interest paid and remaining balance
        interest_paid = calculate_interest_paid(principal, mortgage_rate, term, duration)
        remaining_balance = calculate_remaining_balance(principal, mortgage_rate, term, duration)
        
        # Tax deduction on mortgage interest
        interest_deduction = interest_paid * income_tax_rate
        net_interest = interest_paid - interest_deduction
        
        # Investments grow (only down payment + closing costs come from portfolio)
        # Monthly mortgage payments come from cash flow
        remaining_portfolio = initial_portfolio - down_payment_sale
        if remaining_portfolio < -1e-9:
            raise ValueError("Initial portfolio is insufficient to cover down payment and closing costs")
        remaining_portfolio = max(0.0, remaining_portfolio)
        invested_balance = future_value_with_bear_market(remaining_portfolio, investment_return, duration,
                                                         bear_market_enabled, bear_market_year,
                                                         bear_market_drop, bear_market_recovery_years)
        
        # Total monthly housing costs = mortgage + property tax + insurance
        total_monthly_housing = monthly_pmt + monthly_ownership_costs
        
        # Excess cash flow (if any) after all housing costs gets invested
        excess_cash_flow = max(0, monthly_cash_flow - total_monthly_housing)
        invested_excess = future_value_annuity_with_bear_market(excess_cash_flow, investment_return, duration,
                                                                bear_market_enabled, bear_market_year,
                                                                bear_market_drop, bear_market_recovery_years)
        
        # Home appreciates
        home_value = price * ((1 + housing_return) ** duration)
        
        # Net worth = investments + invested excess cash flow + home equity - remaining mortgage
        home_equity = home_value - remaining_balance
        net_worth = invested_balance + invested_excess + home_equity
        
        # Out-of-pocket cost = net interest + taxes + closing costs (NO opportunity cost - already in net worth)
        out_of_pocket_cost = net_interest + down_payment_tax + closing_costs
        
        return net_worth, out_of_pocket_cost

    elif mode == 'hybrid':
        # Hybrid: some mortgage (price * LTV), rest from stocks + closing costs
        # The down payment comes from stocks, and we borrow up to LTV of the price
        principal = price * loan_to_value_hybrid
        
        # Cash needed from stocks = price - borrowed amount + closing costs
        cash_from_stocks = price - principal + closing_costs
        total_stock_sale, tax_cost, _ = gross_sale_needed(cash_from_stocks, capital_gains_tax, investment_cost_basis_ratio)
        
        # Calculate mortgage payment
        monthly_pmt = mortgage_payment(principal, mortgage_rate, term)
        
        # Calculate interest paid and remaining balance
        interest_paid = calculate_interest_paid(principal, mortgage_rate, term, duration)
        remaining_balance = calculate_remaining_balance(principal, mortgage_rate, term, duration)
        
        # Tax deduction on mortgage interest
        interest_deduction = interest_paid * income_tax_rate
        net_interest = interest_paid - interest_deduction
        
        # Investments grow
        remaining_portfolio = initial_portfolio - total_stock_sale
        if remaining_portfolio < -1e-9:
            raise ValueError("Initial portfolio is insufficient for the hybrid scenario cash requirement")
        remaining_portfolio = max(0.0, remaining_portfolio)
        invested_balance = future_value_with_bear_market(remaining_portfolio, investment_return, duration,
                                                         bear_market_enabled, bear_market_year,
                                                         bear_market_drop, bear_market_recovery_years)
        
        # Total monthly housing costs = mortgage + property tax + insurance
        total_monthly_housing = monthly_pmt + monthly_ownership_costs
        
        # Excess cash flow (if any) after all housing costs gets invested
        excess_cash_flow = max(0, monthly_cash_flow - total_monthly_housing)
        invested_excess = future_value_annuity_with_bear_market(excess_cash_flow, investment_return, duration,
                                                                bear_market_enabled, bear_market_year,
                                                                bear_market_drop, bear_market_recovery_years)
        
        # Home appreciates
        home_value = price * ((1 + housing_return) ** duration)
        
        # Net worth = investments + invested excess cash flow + home equity - remaining mortgage
        home_equity = home_value - remaining_balance
        net_worth = invested_balance + invested_excess + home_equity
        
        # Out-of-pocket cost = net interest + taxes + closing costs (NO opportunity cost - already in net worth)
        out_of_pocket_cost = net_interest + tax_cost + closing_costs
        
        return net_worth, out_of_pocket_cost

def run_simulation():
    records = []

    for price in purchase_prices:
        for duration in years:
            for ret_case, inv_return in investment_returns.items():
                for house_case, house_return in housing_returns.items():
                    # Cash scenario calculation
                    nw, cost = simulate_scenario(price, 0, 0, inv_return, house_return, duration, 'cash')
                    records.append([price, duration, ret_case, house_case, 'Cash', np.round(nw, 2), np.round(cost, 2)])

                    for mort_rate in mortgage_rates:
                        # Full mortgage scenarios
                        for term in terms:
                            nw, cost = simulate_scenario(price, mort_rate, term, inv_return, house_return, duration, 'full')
                            scenario_label = f'Full {term}y' if len(mortgage_rates) == 1 else f'Full {term}y @{mort_rate:.3f}'
                            records.append([price, duration, ret_case, house_case, scenario_label, np.round(nw, 2), np.round(cost, 2)])

                        # Hybrid scenarios
                        for term in terms:
                            nw, cost = simulate_scenario(price, mort_rate, term, inv_return, house_return, duration, 'hybrid')
                            scenario_label = f'Hybrid {term}y' if len(mortgage_rates) == 1 else f'Hybrid {term}y @{mort_rate:.3f}'
                            records.append([price, duration, ret_case, house_case, scenario_label, np.round(nw, 2), np.round(cost, 2)])

    df = pd.DataFrame(records, columns=['Price', 'Years', 'Return Case', 'Housing Case', 'Scenario', 'Net Worth', 'Out-of-Pocket Cost'])
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