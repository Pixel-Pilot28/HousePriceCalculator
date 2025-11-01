import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class HouseCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("House Purchase Calculator")
        self.root.geometry("1400x900")
        
        # Create main container
        main_container = ttk.Frame(root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Create input panel (left side)
        self.create_input_panel(main_container)
        
        # Create results panel (right side)
        self.create_results_panel(main_container)
        
        # Initialize with default calculation
        self.calculate()
    
    def create_input_panel(self, parent):
        input_frame = ttk.LabelFrame(parent, text="Input Parameters", padding="10")
        input_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        row = 0
        
        # Purchase Prices
        ttk.Label(input_frame, text="Purchase Price 1 ($):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.price1_var = tk.StringVar(value="500000")
        ttk.Entry(input_frame, textvariable=self.price1_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(input_frame, text="Purchase Price 2 ($):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.price2_var = tk.StringVar(value="600000")
        ttk.Entry(input_frame, textvariable=self.price2_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        # Down Payment
        ttk.Label(input_frame, text="Down Payment ($):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.down_payment_var = tk.StringVar(value="200000")
        ttk.Entry(input_frame, textvariable=self.down_payment_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        # Initial Investment Balance
        ttk.Label(input_frame, text="Initial Investment ($):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.initial_investment_var = tk.StringVar(value="4000000")
        ttk.Entry(input_frame, textvariable=self.initial_investment_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        # Mortgage Rate
        ttk.Label(input_frame, text="Mortgage Rate (%):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.mortgage_rate_var = tk.StringVar(value="6.3")
        ttk.Entry(input_frame, textvariable=self.mortgage_rate_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        # Investment Returns
        ttk.Label(input_frame, text="Expected Investment Return (%):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.inv_return_exp_var = tk.StringVar(value="7.0")
        ttk.Entry(input_frame, textvariable=self.inv_return_exp_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(input_frame, text="Downside Investment Return (%):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.inv_return_down_var = tk.StringVar(value="4.0")
        ttk.Entry(input_frame, textvariable=self.inv_return_down_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        # Housing Returns
        ttk.Label(input_frame, text="Expected Housing Return (%):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.house_return_exp_var = tk.StringVar(value="2.0")
        ttk.Entry(input_frame, textvariable=self.house_return_exp_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(input_frame, text="Downside Housing Return (%):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.house_return_down_var = tk.StringVar(value="-2.0")
        ttk.Entry(input_frame, textvariable=self.house_return_down_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        # Capital Gains Tax
        ttk.Label(input_frame, text="Capital Gains Tax (%):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.cap_gains_tax_var = tk.StringVar(value="20")
        ttk.Entry(input_frame, textvariable=self.cap_gains_tax_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        # Income Tax Rate
        ttk.Label(input_frame, text="Income Tax Rate (%):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.income_tax_var = tk.StringVar(value="24")
        ttk.Entry(input_frame, textvariable=self.income_tax_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        # Loan to Value for Hybrid
        ttk.Label(input_frame, text="Hybrid LTV Ratio (%):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.ltv_var = tk.StringVar(value="50")
        ttk.Entry(input_frame, textvariable=self.ltv_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        # Time Horizons
        ttk.Label(input_frame, text="Time Horizons (years, comma-separated):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.years_var = tk.StringVar(value="3,5,10")
        ttk.Entry(input_frame, textvariable=self.years_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        # Mortgage Terms
        ttk.Label(input_frame, text="Mortgage Terms (years, comma-separated):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.terms_var = tk.StringVar(value="15,30")
        ttk.Entry(input_frame, textvariable=self.terms_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        # Calculate button
        calc_button = ttk.Button(input_frame, text="Calculate", command=self.calculate)
        calc_button.grid(row=row, column=0, columnspan=2, pady=20)
        row += 1
        
        # Scenario selection for chart
        ttk.Label(input_frame, text="Chart Settings:", font=('TkDefaultFont', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        row += 1
        
        ttk.Label(input_frame, text="Price for Chart ($):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.chart_price_var = tk.StringVar(value="600000")
        ttk.Entry(input_frame, textvariable=self.chart_price_var, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(input_frame, text="Return Scenario:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.return_scenario_var = tk.StringVar(value="expected")
        return_combo = ttk.Combobox(input_frame, textvariable=self.return_scenario_var, 
                                     values=["expected", "downside"], state="readonly", width=12)
        return_combo.grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(input_frame, text="Housing Scenario:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.housing_scenario_var = tk.StringVar(value="expected")
        housing_combo = ttk.Combobox(input_frame, textvariable=self.housing_scenario_var, 
                                      values=["expected", "downside"], state="readonly", width=12)
        housing_combo.grid(row=row, column=1, pady=5)
        row += 1
        
        # Update chart button
        update_button = ttk.Button(input_frame, text="Update Chart", command=self.update_chart)
        update_button.grid(row=row, column=0, columnspan=2, pady=10)
    
    def create_results_panel(self, parent):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Chart tab
        chart_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(chart_frame, text="Chart")
        
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Table tab
        table_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(table_frame, text="Data Table")
        
        # Create treeview for data
        tree_scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        tree_scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        self.tree = ttk.Treeview(table_frame, 
                                  yscrollcommand=tree_scroll_y.set,
                                  xscrollcommand=tree_scroll_x.set)
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Best Options tab
        best_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(best_frame, text="Best Options")
        
        self.best_text = tk.Text(best_frame, wrap=tk.WORD, width=80, height=30)
        best_scroll = ttk.Scrollbar(best_frame, orient=tk.VERTICAL, command=self.best_text.yview)
        self.best_text.configure(yscrollcommand=best_scroll.set)
        
        self.best_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        best_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    def mortgage_payment(self, principal, rate, years):
        if rate == 0:
            return 0
        monthly_rate = rate / 12
        n_payments = years * 12
        payment = principal * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)
        return payment
    
    def future_value(self, principal, rate, years):
        return principal * ((1 + rate) ** years)
    
    def calculate_remaining_balance(self, principal, rate, term_years, years_passed):
        """Calculate remaining mortgage balance after years_passed"""
        if years_passed >= term_years:
            return 0
        monthly_rate = rate / 12
        n_total = term_years * 12
        n_passed = years_passed * 12
        remaining = principal * ((1 + monthly_rate)**n_total - (1 + monthly_rate)**n_passed) / ((1 + monthly_rate)**n_total - 1)
        return remaining
    
    def calculate_interest_paid(self, principal, rate, term_years, years_passed):
        """Calculate total interest paid over years_passed"""
        monthly_rate = rate / 12
        monthly_payment = self.mortgage_payment(principal, rate, term_years)
        n_payments = min(years_passed * 12, term_years * 12)
        
        total_paid = monthly_payment * n_payments
        principal_paid = principal - self.calculate_remaining_balance(principal, rate, term_years, years_passed)
        interest_paid = total_paid - principal_paid
        return interest_paid
    
    def simulate_scenario(self, price, down_payment, mortgage_rate, term, investment_return, 
                          housing_return, duration, mode, ltv, cap_gains_tax, income_tax, 
                          initial_investment):
        """mode = 'cash', 'full', 'hybrid'"""
        if mode == 'cash':
            # Cash purchase: sell stocks to buy house outright (minus down payment)
            stock_sale_needed = price - down_payment
            tax_cost = stock_sale_needed * cap_gains_tax
            
            # Remaining investments grow
            remaining_investments = initial_investment - stock_sale_needed
            invested_balance = self.future_value(remaining_investments, investment_return, duration)
            
            # Home appreciates
            home_value = price * ((1 + housing_return) ** duration)
            
            net_worth = invested_balance + home_value
            
            # Total cost = taxes paid + opportunity cost of investments sold
            opportunity_cost = self.future_value(stock_sale_needed, investment_return, duration) - stock_sale_needed
            total_cost = tax_cost + opportunity_cost
            
            return net_worth, total_cost

        elif mode == 'full':
            # Full mortgage: borrow (price - down_payment), pay down_payment from stocks
            principal = price - down_payment
            down_payment_sale = down_payment
            down_payment_tax = down_payment_sale * cap_gains_tax
            
            # Monthly mortgage payment
            monthly_payment = self.mortgage_payment(principal, mortgage_rate, term)
            
            # Calculate interest paid and remaining balance
            interest_paid = self.calculate_interest_paid(principal, mortgage_rate, term, duration)
            remaining_balance = self.calculate_remaining_balance(principal, mortgage_rate, term, duration)
            
            # Tax deduction on mortgage interest
            interest_deduction = interest_paid * income_tax
            net_interest = interest_paid - interest_deduction
            
            # Investments grow, but reduced by monthly mortgage payments
            # Assume mortgage payments come from cash flow, not investments
            # Investments = initial - down_payment_sale, then grow
            invested_balance = self.future_value(initial_investment - down_payment_sale, investment_return, duration)
            
            # Home appreciates
            home_value = price * ((1 + housing_return) ** duration)
            
            # Net worth = investments + home equity - remaining mortgage
            home_equity = home_value - remaining_balance
            net_worth = invested_balance + home_equity
            
            # Total cost = net interest paid + down payment tax + opportunity cost of down payment
            opportunity_cost_dp = self.future_value(down_payment_sale, investment_return, duration) - down_payment_sale
            total_cost = net_interest + down_payment_tax + opportunity_cost_dp
            
            return net_worth, total_cost

        elif mode == 'hybrid':
            # Hybrid: some mortgage (price * LTV), rest from stocks (minus down payment)
            principal = price * ltv
            stock_sale_needed = price - principal - down_payment
            
            # Total stock sale includes down payment
            total_stock_sale = stock_sale_needed + down_payment
            tax_cost = total_stock_sale * cap_gains_tax
            
            # Monthly mortgage payment
            monthly_payment = self.mortgage_payment(principal, mortgage_rate, term)
            
            # Calculate interest paid and remaining balance
            interest_paid = self.calculate_interest_paid(principal, mortgage_rate, term, duration)
            remaining_balance = self.calculate_remaining_balance(principal, mortgage_rate, term, duration)
            
            # Tax deduction on mortgage interest
            interest_deduction = interest_paid * income_tax
            net_interest = interest_paid - interest_deduction
            
            # Investments grow
            invested_balance = self.future_value(initial_investment - total_stock_sale, investment_return, duration)
            
            # Home appreciates
            home_value = price * ((1 + housing_return) ** duration)
            
            # Net worth = investments + home equity - remaining mortgage
            home_equity = home_value - remaining_balance
            net_worth = invested_balance + home_equity
            
            # Total cost = net interest + taxes + opportunity cost of stock sale
            opportunity_cost = self.future_value(total_stock_sale, investment_return, duration) - total_stock_sale
            total_cost = net_interest + tax_cost + opportunity_cost
            
            return net_worth, total_cost
    
    def calculate(self):
        try:
            # Get input values
            price1 = float(self.price1_var.get())
            price2 = float(self.price2_var.get())
            down_payment = float(self.down_payment_var.get())
            initial_investment = float(self.initial_investment_var.get())
            mortgage_rate = float(self.mortgage_rate_var.get()) / 100
            
            inv_return_exp = float(self.inv_return_exp_var.get()) / 100
            inv_return_down = float(self.inv_return_down_var.get()) / 100
            house_return_exp = float(self.house_return_exp_var.get()) / 100
            house_return_down = float(self.house_return_down_var.get()) / 100
            
            cap_gains_tax = float(self.cap_gains_tax_var.get()) / 100
            income_tax = float(self.income_tax_var.get()) / 100
            ltv = float(self.ltv_var.get()) / 100
            
            years = [int(y.strip()) for y in self.years_var.get().split(',')]
            terms = [int(t.strip()) for t in self.terms_var.get().split(',')]
            
            purchase_prices = [price1, price2]
            investment_returns = {"expected": inv_return_exp, "downside": inv_return_down}
            housing_returns = {"expected": house_return_exp, "downside": house_return_down}
            
            # Run simulations
            records = []
            
            for price in purchase_prices:
                for duration in years:
                    for ret_case, inv_return in investment_returns.items():
                        for house_case, house_return in housing_returns.items():
                            # Cash
                            nw, cost = self.simulate_scenario(price, down_payment, 0, 0, inv_return, 
                                                              house_return, duration, 'cash', ltv, 
                                                              cap_gains_tax, income_tax, initial_investment)
                            records.append([price, duration, ret_case, house_case, 'Cash', 
                                          np.round(nw, 2), np.round(cost, 2)])

                            # Full mortgage
                            for term in terms:
                                nw, cost = self.simulate_scenario(price, down_payment, mortgage_rate, term, 
                                                                  inv_return, house_return, duration, 'full', 
                                                                  ltv, cap_gains_tax, income_tax, initial_investment)
                                records.append([price, duration, ret_case, house_case, f'Full {term}y', 
                                              np.round(nw, 2), np.round(cost, 2)])

                            # Hybrid
                            for term in terms:
                                nw, cost = self.simulate_scenario(price, down_payment, mortgage_rate, term, 
                                                                  inv_return, house_return, duration, 'hybrid', 
                                                                  ltv, cap_gains_tax, income_tax, initial_investment)
                                records.append([price, duration, ret_case, house_case, f'Hybrid {term}y', 
                                              np.round(nw, 2), np.round(cost, 2)])
            
            self.df = pd.DataFrame(records, columns=['Price', 'Years', 'Return Case', 'Housing Case', 
                                                     'Scenario', 'Net Worth', 'Total Cost'])
            
            # Update table
            self.update_table()
            
            # Update chart
            self.update_chart()
            
            # Update best options
            self.update_best_options()
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def update_table(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Set columns
        columns = list(self.df.columns)
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'
        
        # Format columns
        for col in columns:
            self.tree.heading(col, text=col)
            if col in ['Net Worth', 'Total Cost', 'Price']:
                self.tree.column(col, width=120, anchor=tk.E)
            else:
                self.tree.column(col, width=100, anchor=tk.CENTER)
        
        # Add data
        for _, row in self.df.iterrows():
            values = []
            for col in columns:
                val = row[col]
                if col in ['Net Worth', 'Total Cost', 'Price']:
                    values.append(f"${val:,.0f}")
                else:
                    values.append(val)
            self.tree.insert('', tk.END, values=values)
    
    def update_chart(self):
        try:
            chart_price = float(self.chart_price_var.get())
            return_case = self.return_scenario_var.get()
            housing_case = self.housing_scenario_var.get()
            
            self.ax.clear()
            
            # Get unique scenarios
            scenarios = self.df['Scenario'].unique()
            
            for scenario in scenarios:
                subset = self.df[(self.df['Price'] == chart_price) & 
                                (self.df['Scenario'] == scenario) & 
                                (self.df['Return Case'] == return_case) & 
                                (self.df['Housing Case'] == housing_case)]
                
                if not subset.empty:
                    self.ax.plot(subset['Years'], subset['Net Worth'], marker='o', label=scenario)
            
            self.ax.set_title(f"Net Worth Over Time - ${chart_price:,.0f} Home\n({return_case.title()} Investment, {housing_case.title()} Housing)")
            self.ax.set_xlabel("Years")
            self.ax.set_ylabel("Net Worth ($)")
            self.ax.legend()
            self.ax.grid(True, alpha=0.3)
            self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.2f}M'))
            
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Chart update error: {str(e)}")
    
    def update_best_options(self):
        self.best_text.delete(1.0, tk.END)
        
        # Find best options by different criteria
        output = []
        
        output.append("=" * 80)
        output.append("BEST OPTIONS ANALYSIS")
        output.append("=" * 80)
        output.append("")
        
        # Group by price and timeframe
        for price in self.df['Price'].unique():
            output.append(f"\n{'='*80}")
            output.append(f"HOUSE PRICE: ${price:,.0f}")
            output.append(f"{'='*80}\n")
            
            for years in sorted(self.df['Years'].unique()):
                output.append(f"\n{'-'*80}")
                output.append(f"TIME HORIZON: {years} YEARS")
                output.append(f"{'-'*80}\n")
                
                for ret_case in ['expected', 'downside']:
                    for house_case in ['expected', 'downside']:
                        subset = self.df[(self.df['Price'] == price) & 
                                        (self.df['Years'] == years) & 
                                        (self.df['Return Case'] == ret_case) & 
                                        (self.df['Housing Case'] == house_case)]
                        
                        if not subset.empty:
                            output.append(f"\nScenario: {ret_case.title()} Investment Return, {house_case.title()} Housing Return")
                            
                            # Best by net worth
                            best_nw = subset.loc[subset['Net Worth'].idxmax()]
                            output.append(f"  Best Net Worth: {best_nw['Scenario']}")
                            output.append(f"    Net Worth: ${best_nw['Net Worth']:,.0f}")
                            output.append(f"    Total Cost: ${best_nw['Total Cost']:,.0f}")
                            
                            # Best by total cost (lowest)
                            best_cost = subset.loc[subset['Total Cost'].idxmin()]
                            output.append(f"  Lowest Total Cost: {best_cost['Scenario']}")
                            output.append(f"    Net Worth: ${best_cost['Net Worth']:,.0f}")
                            output.append(f"    Total Cost: ${best_cost['Total Cost']:,.0f}")
                            
                            output.append("")
        
        self.best_text.insert(1.0, "\n".join(output))

def main():
    root = tk.Tk()
    app = HouseCalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
