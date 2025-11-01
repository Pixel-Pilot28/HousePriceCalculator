# House Purchase Calculator GUI

A comprehensive Python GUI application to analyze different house purchase scenarios and determine the optimal buying strategy based on various financial parameters.

## Setup

### 1. Virtual Environment
The virtual environment has been created in the `venv` folder. To activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Dependencies
All required packages are already installed:
- numpy
- pandas
- matplotlib

## Running the Application

To run the GUI application:

```powershell
.\venv\Scripts\python.exe house_calculator_gui.py
```

Or with the virtual environment activated:

```powershell
python house_calculator_gui.py
```

## Features

### Input Parameters (Left Panel)
The GUI allows you to customize all financial parameters:

- **Purchase Prices**: Two different house prices to compare
- **Down Payment**: Initial cash payment
- **Initial Investment**: Your starting investment balance (stocks/portfolio)
- **Mortgage Rate**: Interest rate for mortgage loans
- **Investment Returns**: Expected and downside scenarios for investment growth
- **Housing Returns**: Expected and downside scenarios for home appreciation
- **Capital Gains Tax**: Tax rate on stock sales
- **Income Tax Rate**: Your income tax bracket (for mortgage interest deduction)
- **Hybrid LTV Ratio**: Loan-to-value ratio for hybrid financing scenarios
- **Time Horizons**: Years to analyze (comma-separated)
- **Mortgage Terms**: Loan terms to compare (comma-separated)

### Purchase Scenarios Compared
The calculator analyzes three purchase strategies:

1. **Cash**: Buy outright by selling investments (incurs capital gains tax)
2. **Full Mortgage**: Finance the entire purchase minus down payment
3. **Hybrid**: Combination of cash and mortgage at specified LTV

For each strategy, it calculates:
- Net worth at each time horizon
- Total cost of the approach

### Output Tabs (Right Panel)

#### 1. Chart Tab
- Visual comparison of net worth over time
- Customizable by price, return scenario, and housing scenario
- Shows all purchase strategies on one graph

#### 2. Data Table Tab
- Complete results in tabular format
- All combinations of parameters and scenarios
- Sortable columns for easy analysis

#### 3. Best Options Tab
- Automated analysis of optimal strategies
- Grouped by price point and time horizon
- Shows best options for both net worth maximization and cost minimization
- Displays results for all scenario combinations (expected/downside)

## How to Use

1. **Modify Inputs**: Change any values in the left panel input fields
2. **Calculate**: Click the "Calculate" button to run all scenarios
3. **Review Results**: 
   - View the chart to see net worth trends
   - Check the data table for detailed numbers
   - Read the "Best Options" tab for recommendations
4. **Update Chart**: Adjust chart settings and click "Update Chart" to visualize different scenarios

## Understanding the Results

### Net Worth
Total value of your assets (investments + home equity) minus liabilities (remaining mortgage balance)

### Total Cost
The effective cost of the purchase strategy, including:
- Capital gains taxes (for cash and hybrid scenarios)
- Net mortgage interest (after tax deduction)

### Best Strategy Indicators
- **Highest Net Worth**: Strategy that maximizes wealth
- **Lowest Total Cost**: Strategy that minimizes out-of-pocket expenses

## Tips

- Compare scenarios under both expected and downside conditions to assess risk
- Consider both short-term (3-5 years) and long-term (10+ years) horizons
- Pay attention to how different mortgage terms affect outcomes
- Balance between net worth maximization and cash preservation based on your risk tolerance

## Original Script

The original calculation script is available in `houseModel.py` for reference or batch processing.
