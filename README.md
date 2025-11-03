# House Purchase Calculator GUI

A comprehensive Python GUI application to analyze different house purchase scenarios and determine the optimal buying strategy based on various financial parameters.

## Recent Updates (November 2, 2025)

### Critical Accuracy Improvements

1. **Added Bear Market Simulator** (Latest):
   - **Enable/Disable Toggle**: Turn on/off bear market simulation
   - **Bear Market Year**: Set when the downturn occurs (default: year 2)
   - **Market Drop**: Percentage decline during bear market (default: 30%)
   - **Recovery Years**: Time to recover to normal trajectory (default: 2 years)
   - Models temporary market downturns and their impact on different buying strategies
   - Affects both existing investment balances and monthly contributions
   - Helps evaluate risk exposure across cash vs. mortgage scenarios

2. **Added Property Tax, Home Insurance, and Closing Costs**:
   - **Property Tax Rate**: Default 1.2% of home value annually
   - **Home Insurance Rate**: Default 0.5% of home value annually
   - **Closing Costs**: Default 3% of purchase price (one-time)
   - These costs now properly reduce investable cash flow and increase upfront costs
   - All three scenarios account for ongoing ownership costs (PITI = Principal, Interest, Taxes, Insurance)

2. **Added Monthly Cash Flow Parameter**: The model now includes a monthly cash flow input ($5,000 default) representing money available for mortgage payments or investments.

3. **Fixed Cash Scenario Calculation**: 
   - **Previously**: Cash scenario appeared artificially low because it didn't account for invested cash flow
   - **Now**: Correctly adds the future value of monthly cash flow that would have gone to mortgage payments
   - **Also**: Properly deducts property tax and insurance from investable cash flow

4. **Tax-Aware Stock Sales**: All scenarios use "gross-up" calculations to determine total stock sales needed to net specific cash amounts after capital gains taxes.

5. **Excess Cash Flow Investment**: Mortgage scenarios now properly invest any remaining cash flow after all housing costs (mortgage + property tax + insurance).

6. **Clarified Hybrid Scenario**: Simplified calculation - cash from stocks = price - borrowed amount + closing costs.

### Key Model Assumptions

- **Stock sales incur capital gains tax** (default 20%) on gains only
- **Investment cost basis ratio** (default 60%): Represents what portion of your investment is original principal vs. gains
  - Example: 60% cost basis = only 40% of sale proceeds are taxable gains
  - Higher ratio = less tax = more money stays invested
  - Adjust based on how long you've held investments and their growth
- **Closing costs** (default 3%) are paid upfront from stock sales
- **Property tax and home insurance** reduce monthly investable cash flow for all scenarios
  - Cash buyers: Pay property tax & insurance but no mortgage
  - Mortgage buyers: Pay mortgage + property tax + insurance (PITI)
- **Mortgage payments come from monthly cash flow**, not from selling investments
- **Excess cash flow is invested** at the expected investment return rate
- **Mortgage interest is tax-deductible** at your income tax rate
- **Investment returns compound annually**
- **Home appreciation compounds annually**

### Understanding Cost Basis

The **Investment Cost Basis Ratio** is crucial for accurate tax calculations:

- **100% cost basis**: No gains (break-even investments) - no capital gains tax
- **80% cost basis**: Your investments have grown 25% (original $800k → now $1M)
- **60% cost basis** (default): Investments have grown 67% (original $600k → now $1M)
- **50% cost basis**: Investments have doubled (original $500k → now $1M)
- **0% cost basis**: All proceeds are gains (unrealistic, but worst-case scenario)

**Example Impact**: If you need $500k cash with 20% capital gains tax:
- With 0% cost basis: Must sell $625k, pay $125k tax
- With 60% cost basis: Must sell $543k, pay $43k tax
- **Result**: Keep $81k more invested!

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

### Easy Method (Recommended)
Use the provided PowerShell scripts:

**To run the GUI:**
```powershell
.\run_gui.ps1
```

**To run the original model script:**
```powershell
.\run_model.ps1
```

### Manual Method
**To run the GUI application:**
```powershell
.\venv\Scripts\python.exe house_calculator_gui.py
```

**To run the original model script:**
```powershell
.\venv\Scripts\python.exe houseModel.py
```

**Or activate the virtual environment first:**
```powershell
.\venv\Scripts\Activate.ps1
python house_calculator_gui.py
# or
python houseModel.py
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
- **Investment Cost Basis**: Percentage of your portfolio that is original principal (default 60%)
- **Hybrid LTV Ratio**: Loan-to-value ratio for hybrid financing scenarios
- **Monthly Cash Flow**: Available monthly amount for housing costs or investments (default $5,000)
- **Property Tax Rate**: Annual property tax as percentage of home value (default 1.2%)
- **Home Insurance Rate**: Annual insurance premium as percentage of home value (default 0.5%)
- **Closing Cost Rate**: One-time closing costs as percentage of purchase price (default 3%)
- **Time Horizons**: Years to analyze (comma-separated)
- **Mortgage Terms**: Loan terms to compare (comma-separated)

### Purchase Scenarios Compared
The calculator analyzes three purchase strategies:

1. **Cash**: Buy outright by selling investments (incurs capital gains tax)
2. **Full Mortgage**: Finance the entire purchase minus down payment
3. **Hybrid**: Combination of cash and mortgage at specified LTV

For each strategy, it calculates:
- Net worth at each time horizon (with optional bear market impact)
- Total cost of the approach
- Risk exposure to market downturns

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
