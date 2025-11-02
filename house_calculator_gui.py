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
        self.numeric_inputs = {}
        self._updating_control = False
        self._pending_calc = None
        self._pending_chart = None
        
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
        self.calculate(silent=True)
    
    def create_input_panel(self, parent):
        # Create outer frame for the input panel
        input_outer = ttk.LabelFrame(parent, text="Input Parameters", padding="10")
        input_outer.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Create canvas for scrolling
        canvas = tk.Canvas(input_outer, highlightthickness=0)
        scrollbar = ttk.Scrollbar(input_outer, orient="vertical", command=canvas.yview)
        
        # Create scrollable frame
        input_frame = ttk.Frame(canvas)
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        canvas_frame = canvas.create_window((0, 0), window=input_frame, anchor="nw")
        
        # Configure scroll region when frame changes size
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Also update the canvas window width to match canvas width
            canvas.itemconfig(canvas_frame, width=canvas.winfo_width())
        
        input_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_frame, width=e.width))
        
        # Bind mousewheel to scroll
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        row = 0

        row = self.add_numeric_input(input_frame, "Purchase Price 1 ($):", "price1", 500000, 100000, 2000000, 5000, row, kind="currency")
        row = self.add_numeric_input(input_frame, "Purchase Price 2 ($):", "price2", 600000, 100000, 2000000, 5000, row, kind="currency")
        row = self.add_numeric_input(input_frame, "Down Payment ($):", "down_payment", 200000, 0, 2000000, 5000, row, kind="currency")
        row = self.add_numeric_input(input_frame, "Initial Investment ($):", "initial_investment", 4000000, 100000, 10000000, 10000, row, kind="currency")
        row = self.add_numeric_input(input_frame, "Mortgage Rate (%):", "mortgage_rate", 6.3, 0.0, 15.0, 0.05, row, kind="percent")
        row = self.add_numeric_input(input_frame, "Expected Investment Return (%):", "inv_return_expected", 7.0, -10.0, 20.0, 0.1, row, kind="percent")
        row = self.add_numeric_input(input_frame, "Downside Investment Return (%):", "inv_return_downside", 4.0, -10.0, 20.0, 0.1, row, kind="percent")
        row = self.add_numeric_input(input_frame, "Expected Housing Return (%):", "house_return_expected", 2.0, -10.0, 10.0, 0.1, row, kind="percent")
        row = self.add_numeric_input(input_frame, "Downside Housing Return (%):", "house_return_downside", -2.0, -10.0, 10.0, 0.1, row, kind="percent")
        row = self.add_numeric_input(input_frame, "Capital Gains Tax (%):", "capital_gains_tax", 20.0, 0.0, 50.0, 0.1, row, kind="percent")
        row = self.add_numeric_input(input_frame, "Income Tax Rate (%):", "income_tax", 24.0, 0.0, 50.0, 0.1, row, kind="percent")
        row = self.add_numeric_input(input_frame, "Investment Cost Basis (%):", "cost_basis_ratio", 60.0, 0.0, 100.0, 1.0, row, kind="percent")
        row = self.add_numeric_input(input_frame, "Hybrid LTV Ratio (%):", "ltv_ratio", 50.0, 0.0, 100.0, 0.5, row, kind="percent")
        row = self.add_numeric_input(input_frame, "Monthly Cash Flow ($):", "monthly_cash_flow", 5000, 0, 20000, 100, row, kind="currency")
        row = self.add_numeric_input(input_frame, "Property Tax Rate (%):", "property_tax_rate", 1.2, 0.0, 5.0, 0.1, row, kind="percent")
        row = self.add_numeric_input(input_frame, "Home Insurance Rate (%):", "home_insurance_rate", 0.5, 0.0, 3.0, 0.1, row, kind="percent")
        row = self.add_numeric_input(input_frame, "Closing Cost Rate (%):", "closing_cost_rate", 3.0, 0.0, 10.0, 0.1, row, kind="percent")

        ttk.Label(input_frame, text="Time Horizons (years, comma-separated):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.years_var = tk.StringVar(value="3,5,10")
        years_entry = ttk.Entry(input_frame, textvariable=self.years_var, width=15)
        years_entry.grid(row=row, column=1, pady=5)
        self.years_var.trace_add('write', lambda *args: self.schedule_recalculate())
        row += 1

        ttk.Label(input_frame, text="Mortgage Terms (years, comma-separated):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.terms_var = tk.StringVar(value="15,30")
        terms_entry = ttk.Entry(input_frame, textvariable=self.terms_var, width=15)
        terms_entry.grid(row=row, column=1, pady=5)
        self.terms_var.trace_add('write', lambda *args: self.schedule_recalculate())
        row += 1

        calc_button = ttk.Button(input_frame, text="Calculate", command=lambda: self.calculate(silent=False))
        calc_button.grid(row=row, column=0, columnspan=2, pady=20)
        row += 1

        ttk.Label(input_frame, text="Chart Settings:", font=('TkDefaultFont', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        row += 1

        ttk.Label(input_frame, text="Price for Chart ($):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.chart_price_var = tk.StringVar(value="600000")
        chart_price_entry = ttk.Entry(input_frame, textvariable=self.chart_price_var, width=15)
        chart_price_entry.grid(row=row, column=1, pady=5)
        self.chart_price_var.trace_add('write', lambda *args: self.schedule_chart_update())
        row += 1

        ttk.Label(input_frame, text="Return Scenario:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.return_scenario_var = tk.StringVar(value="expected")
        return_combo = ttk.Combobox(input_frame, textvariable=self.return_scenario_var,
                                     values=["expected", "downside"], state="readonly", width=12)
        return_combo.grid(row=row, column=1, pady=5)
        return_combo.bind('<<ComboboxSelected>>', lambda _event: self.schedule_chart_update())
        row += 1

        ttk.Label(input_frame, text="Housing Scenario:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.housing_scenario_var = tk.StringVar(value="expected")
        housing_combo = ttk.Combobox(input_frame, textvariable=self.housing_scenario_var,
                                      values=["expected", "downside"], state="readonly", width=12)
        housing_combo.grid(row=row, column=1, pady=5)
        housing_combo.bind('<<ComboboxSelected>>', lambda _event: self.schedule_chart_update())
        row += 1

        update_button = ttk.Button(input_frame, text="Update Chart", command=self.update_chart)
        update_button.grid(row=row, column=0, columnspan=2, pady=10)
    
    def add_numeric_input(self, parent, label, name, default, minimum, maximum, resolution, row, kind="float"):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=5)
        entry_var = tk.StringVar(value=self.format_numeric(kind, default))
        entry = ttk.Entry(parent, textvariable=entry_var, width=15)
        entry.grid(row=row, column=1, pady=5)

        scale_var = tk.DoubleVar(value=default)
        scale = ttk.Scale(parent, variable=scale_var, from_=minimum, to=maximum, orient=tk.HORIZONTAL,
                          command=lambda val, n=name: self.on_slider_change(n, float(val)))
        scale.grid(row=row + 1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)

        self.numeric_inputs[name] = {
            "entry_var": entry_var,
            "scale_var": scale_var,
            "kind": kind,
            "min": minimum,
            "max": maximum,
            "resolution": resolution,
            "scale": scale,
        }

        entry_var.trace_add('write', lambda *args, n=name: self.on_entry_change(n))
        entry.bind('<FocusOut>', lambda _event, n=name: self.on_entry_commit(n))
        entry.bind('<Return>', lambda _event, n=name: self.on_entry_commit(n))
        # Ensure slider reflects default exactly
        scale.set(default)

        return row + 2

    def format_numeric(self, kind, value):
        if kind == "currency":
            return f"{round(value):.0f}"
        if kind == "percent":
            return f"{value:.2f}"
        return f"{value}"

    def parse_numeric(self, kind, text):
        cleaned = text.replace(',', '').strip()
        if not cleaned:
            return None
        try:
            return float(cleaned)
        except ValueError:
            return None

    def round_to_resolution(self, value, resolution):
        if not resolution:
            return value
        return round(value / resolution) * resolution

    def clamp(self, value, minimum, maximum):
        return max(minimum, min(maximum, value))

    def on_slider_change(self, name, value):
        config = self.numeric_inputs.get(name)
        if not config:
            return
        if config['resolution']:
            value = self.round_to_resolution(value, config['resolution'])
        value = self.clamp(value, config['min'], config['max'])
        if self._updating_control:
            return
        self._updating_control = True
        config['scale_var'].set(value)
        config['entry_var'].set(self.format_numeric(config['kind'], value))
        self._updating_control = False
        self.schedule_recalculate()

    def on_entry_change(self, name):
        if self._updating_control:
            return
        config = self.numeric_inputs.get(name)
        if not config:
            return
        value = self.parse_numeric(config['kind'], config['entry_var'].get())
        if value is None:
            return
        value = self.clamp(value, config['min'], config['max'])
        if config['resolution']:
            value = self.round_to_resolution(value, config['resolution'])
        self._updating_control = True
        config['scale_var'].set(value)
        self._updating_control = False
        self.schedule_recalculate()

    def on_entry_commit(self, name):
        config = self.numeric_inputs.get(name)
        if not config:
            return
        value = self.parse_numeric(config['kind'], config['entry_var'].get())
        if value is None:
            value = config['scale_var'].get()
        value = self.clamp(value, config['min'], config['max'])
        if config['resolution']:
            value = self.round_to_resolution(value, config['resolution'])
        self._updating_control = True
        config['scale_var'].set(value)
        config['entry_var'].set(self.format_numeric(config['kind'], value))
        self._updating_control = False
        self.schedule_recalculate()

    def schedule_recalculate(self, delay=250):
        if self._pending_calc is not None:
            self.root.after_cancel(self._pending_calc)
        self._pending_calc = self.root.after(delay, self._run_scheduled_calculate)

    def schedule_chart_update(self, delay=250):
        if self._pending_chart is not None:
            self.root.after_cancel(self._pending_chart)
        self._pending_chart = self.root.after(delay, self._run_scheduled_chart_update)

    def _run_scheduled_calculate(self):
        self._pending_calc = None
        self.calculate(silent=True)

    def _run_scheduled_chart_update(self):
        self._pending_chart = None
        self.update_chart()

    def get_numeric_value(self, name):
        config = self.numeric_inputs.get(name)
        if not config:
            raise ValueError(f"Unknown input: {name}")
        return float(config['scale_var'].get())

    def get_percent_value(self, name):
        return self.get_numeric_value(name) / 100.0

    def parse_int_list(self, text):
        parts = [part.strip() for part in text.split(',') if part.strip()]
        if not parts:
            raise ValueError("List of values cannot be empty")
        values = []
        for part in parts:
            values.append(int(part))
        return values

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
    
    def future_value_annuity(self, monthly_payment, annual_rate, years):
        """Calculate future value of monthly payments invested at annual_rate"""
        if monthly_payment == 0 or annual_rate == 0:
            return monthly_payment * years * 12
        monthly_rate = (1 + annual_rate) ** (1/12) - 1
        n_months = years * 12
        return monthly_payment * (((1 + monthly_rate)**n_months - 1) / monthly_rate)
    
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
    
    def gross_sale_needed(self, net_cash_needed, tax_rate, cost_basis_ratio):
        """
        Return (gross sale, tax paid, net cash) required to net net_cash_needed from taxable investments.
        
        Args:
            net_cash_needed: The amount of cash needed after taxes
            tax_rate: Capital gains tax rate
            cost_basis_ratio: Fraction of investment value that is original principal (not taxable)
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
        
        # Net cash = gross_sale - tax_paid
        net_cash = gross_sale - tax_paid
        
        return gross_sale, tax_paid, net_cash

    def simulate_scenario(self, price, down_payment, mortgage_rate, term, investment_return, 
                          housing_return, duration, mode, ltv, cap_gains_tax, income_tax, 
                          initial_investment, monthly_cash_flow, cost_basis_ratio,
                          property_tax_rate, home_insurance_rate, closing_cost_rate):
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
            gross_sale, tax_cost, _ = self.gross_sale_needed(net_cash_needed, cap_gains_tax, cost_basis_ratio)

            remaining_investments = initial_investment - gross_sale
            invested_balance = self.future_value(remaining_investments, investment_return, duration)

            # BENEFIT: No mortgage payment, but still pay property tax & insurance
            # Invest cash flow remaining after ownership costs
            cash_flow_to_invest = max(0, monthly_cash_flow - monthly_ownership_costs)
            invested_cash_flow = self.future_value_annuity(cash_flow_to_invest, investment_return, duration)

            home_value = price * ((1 + housing_return) ** duration)

            net_worth = invested_balance + invested_cash_flow + home_value

            opportunity_cost = self.future_value(gross_sale, investment_return, duration) - gross_sale
            total_cost = tax_cost + opportunity_cost + closing_costs

            return net_worth, total_cost

        elif mode == 'full':
            # Full mortgage: borrow (price - down_payment), pay down_payment + closing costs from stocks
            principal = price - down_payment
            net_cash_needed = down_payment + closing_costs
            down_payment_sale, down_payment_tax, _ = self.gross_sale_needed(net_cash_needed, cap_gains_tax, cost_basis_ratio)
            
            # Calculate mortgage payment
            monthly_pmt = self.mortgage_payment(principal, mortgage_rate, term)
            
            # Calculate interest paid and remaining balance
            interest_paid = self.calculate_interest_paid(principal, mortgage_rate, term, duration)
            remaining_balance = self.calculate_remaining_balance(principal, mortgage_rate, term, duration)
            
            # Tax deduction on mortgage interest
            interest_deduction = interest_paid * income_tax
            net_interest = interest_paid - interest_deduction
            
            # Investments grow (only down payment + closing costs come from portfolio)
            invested_balance = self.future_value(initial_investment - down_payment_sale, investment_return, duration)
            
            # Total monthly housing costs = mortgage + property tax + insurance
            total_monthly_housing = monthly_pmt + monthly_ownership_costs
            
            # Excess cash flow (if any) after all housing costs gets invested
            excess_cash_flow = max(0, monthly_cash_flow - total_monthly_housing)
            invested_excess = self.future_value_annuity(excess_cash_flow, investment_return, duration)
            
            # Home appreciates
            home_value = price * ((1 + housing_return) ** duration)
            
            # Net worth = investments + invested excess cash flow + home equity - remaining mortgage
            home_equity = home_value - remaining_balance
            net_worth = invested_balance + invested_excess + home_equity
            
            # Total cost = net interest paid + down payment tax + opportunity cost of down payment + closing costs
            opportunity_cost_dp = self.future_value(down_payment_sale, investment_return, duration) - down_payment_sale
            total_cost = net_interest + down_payment_tax + opportunity_cost_dp + closing_costs
            
            return net_worth, total_cost

        elif mode == 'hybrid':
            # Hybrid: some mortgage (price * LTV), rest from stocks + closing costs
            principal = price * ltv
            
            # Cash needed from stocks = price - borrowed amount + closing costs
            cash_from_stocks = price - principal + closing_costs
            total_stock_sale, tax_cost, _ = self.gross_sale_needed(cash_from_stocks, cap_gains_tax, cost_basis_ratio)
            
            # Calculate mortgage payment
            monthly_pmt = self.mortgage_payment(principal, mortgage_rate, term)
            
            # Calculate interest paid and remaining balance
            interest_paid = self.calculate_interest_paid(principal, mortgage_rate, term, duration)
            remaining_balance = self.calculate_remaining_balance(principal, mortgage_rate, term, duration)
            
            # Tax deduction on mortgage interest
            interest_deduction = interest_paid * income_tax
            net_interest = interest_paid - interest_deduction
            
            # Investments grow
            invested_balance = self.future_value(initial_investment - total_stock_sale, investment_return, duration)
            
            # Total monthly housing costs = mortgage + property tax + insurance
            total_monthly_housing = monthly_pmt + monthly_ownership_costs
            
            # Excess cash flow (if any) after all housing costs gets invested
            excess_cash_flow = max(0, monthly_cash_flow - total_monthly_housing)
            invested_excess = self.future_value_annuity(excess_cash_flow, investment_return, duration)
            
            # Home appreciates
            home_value = price * ((1 + housing_return) ** duration)
            
            # Net worth = investments + invested excess cash flow + home equity - remaining mortgage
            home_equity = home_value - remaining_balance
            net_worth = invested_balance + invested_excess + home_equity
            
            # Total cost = net interest + taxes + opportunity cost of stock sale + closing costs
            opportunity_cost = self.future_value(total_stock_sale, investment_return, duration) - total_stock_sale
            total_cost = net_interest + tax_cost + opportunity_cost + closing_costs
            
            return net_worth, total_cost
    
    def calculate(self, silent=False):
        if self._pending_calc is not None:
            self.root.after_cancel(self._pending_calc)
            self._pending_calc = None
        try:
            price1 = self.get_numeric_value('price1')
            price2 = self.get_numeric_value('price2')
            down_payment = self.get_numeric_value('down_payment')
            initial_investment = self.get_numeric_value('initial_investment')
            mortgage_rate = self.get_percent_value('mortgage_rate')

            inv_return_exp = self.get_percent_value('inv_return_expected')
            inv_return_down = self.get_percent_value('inv_return_downside')
            house_return_exp = self.get_percent_value('house_return_expected')
            house_return_down = self.get_percent_value('house_return_downside')

            cap_gains_tax = self.get_percent_value('capital_gains_tax')
            income_tax = self.get_percent_value('income_tax')
            cost_basis_ratio = self.get_percent_value('cost_basis_ratio')
            ltv = self.get_percent_value('ltv_ratio')
            monthly_cash_flow = self.get_numeric_value('monthly_cash_flow')
            property_tax_rate = self.get_percent_value('property_tax_rate')
            home_insurance_rate = self.get_percent_value('home_insurance_rate')
            closing_cost_rate = self.get_percent_value('closing_cost_rate')

            years = self.parse_int_list(self.years_var.get())
            terms = self.parse_int_list(self.terms_var.get())

            purchase_prices = [price1, price2]
            investment_returns = {"expected": inv_return_exp, "downside": inv_return_down}
            housing_returns = {"expected": house_return_exp, "downside": house_return_down}

            records = []

            for price in purchase_prices:
                for duration in years:
                    for ret_case, inv_return in investment_returns.items():
                        for house_case, house_return in housing_returns.items():
                            nw, cost = self.simulate_scenario(price, down_payment, 0, 0, inv_return,
                                                              house_return, duration, 'cash', ltv,
                                                              cap_gains_tax, income_tax, initial_investment, 
                                                              monthly_cash_flow, cost_basis_ratio,
                                                              property_tax_rate, home_insurance_rate, closing_cost_rate)
                            records.append([price, duration, ret_case, house_case, 'Cash',
                                            np.round(nw, 2), np.round(cost, 2)])

                            for term in terms:
                                nw_full, cost_full = self.simulate_scenario(price, down_payment, mortgage_rate, term,
                                                                            inv_return, house_return, duration, 'full',
                                                                            ltv, cap_gains_tax, income_tax, initial_investment,
                                                                            monthly_cash_flow, cost_basis_ratio,
                                                                            property_tax_rate, home_insurance_rate, closing_cost_rate)
                                records.append([price, duration, ret_case, house_case, f'Full {term}y',
                                                np.round(nw_full, 2), np.round(cost_full, 2)])

                            for term in terms:
                                nw_hybrid, cost_hybrid = self.simulate_scenario(price, down_payment, mortgage_rate, term,
                                                                                inv_return, house_return, duration, 'hybrid',
                                                                                ltv, cap_gains_tax, income_tax, initial_investment,
                                                                                monthly_cash_flow, cost_basis_ratio,
                                                                                property_tax_rate, home_insurance_rate, closing_cost_rate)
                                records.append([price, duration, ret_case, house_case, f'Hybrid {term}y',
                                                np.round(nw_hybrid, 2), np.round(cost_hybrid, 2)])

            self.df = pd.DataFrame(records, columns=['Price', 'Years', 'Return Case', 'Housing Case',
                                                     'Scenario', 'Net Worth', 'Total Cost'])

            self.update_table()
            self.update_chart()
            self.update_best_options()

        except Exception as exc:
            if silent:
                return
            messagebox.showerror("Error", f"Calculation error: {str(exc)}")
    
    def update_table(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not hasattr(self, 'df') or self.df.empty:
            self.tree['columns'] = []
            self.tree['show'] = ''
            return

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
        if self._pending_chart is not None:
            self.root.after_cancel(self._pending_chart)
            self._pending_chart = None

        if not hasattr(self, 'df') or self.df.empty:
            self.ax.clear()
            self.canvas.draw()
            return

        text_value = self.chart_price_var.get().replace(',', '').strip()
        try:
            chart_price = float(text_value)
        except ValueError:
            return

        return_case = self.return_scenario_var.get()
        housing_case = self.housing_scenario_var.get()

        self.ax.clear()

        scenarios = self.df['Scenario'].unique()
        plotted = False

        for scenario in scenarios:
            subset = self.df[(np.isclose(self.df['Price'], chart_price)) &
                             (self.df['Scenario'] == scenario) &
                             (self.df['Return Case'] == return_case) &
                             (self.df['Housing Case'] == housing_case)]

            if not subset.empty:
                subset = subset.sort_values('Years')
                self.ax.plot(subset['Years'], subset['Net Worth'], marker='o', label=scenario)
                plotted = True

        title_price = chart_price
        self.ax.set_title(f"Net Worth Over Time - ${title_price:,.0f} Home\n({return_case.title()} Investment, {housing_case.title()} Housing)")
        self.ax.set_xlabel("Years")
        self.ax.set_ylabel("Net Worth ($)")

        if plotted:
            self.ax.legend()
        else:
            self.ax.text(0.5, 0.5, "No data for selected inputs", transform=self.ax.transAxes,
                         ha='center', va='center')

        self.ax.grid(True, alpha=0.3)
        self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _pos: f'${x/1e6:.2f}M'))

        self.figure.tight_layout()
        self.canvas.draw()
    
    def update_best_options(self):
        self.best_text.delete(1.0, tk.END)

        if not hasattr(self, 'df') or self.df.empty:
            self.best_text.insert(1.0, "No data available. Adjust inputs to run the simulation.")
            return

        output = []

        output.append("=" * 80)
        output.append("BEST OPTIONS ANALYSIS")
        output.append("=" * 80)
        output.append("")

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
