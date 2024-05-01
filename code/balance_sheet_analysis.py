import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

def read_balance_sheet_data(file_name):
    '''
    Convert active sheet of Screener.in file to csv file to obtain values
    
    Also delete the extra total row in the csv file to remove data consistency issues
    '''
    df = pd.read_csv(file_name) 
    df = df.transpose()
    df.columns = df.iloc[0]
    df = df[1:]
    for col in df.columns:
        df[col] = df[col].str.replace(',','').astype(float)
    dates = df.index.tolist()    
    dates_with_year = [f"{int(date.split('-')[0]) + 2000}-03-01" for date in dates]
    index = pd.to_datetime(dates_with_year, format='%Y-%m-%d')   
    df.index = index
    return df    

def read_profit_loss_data(filename):
    '''
    Convert active sheet of Screener.in file to csv file to obtain values
    '''
    df = pd.read_csv(filename)
    df = df.transpose()
    df.columns = df.iloc[0]
    df = df[1:]
    for col in df.columns:
        if col not in ("Price Dividend","Dividend Payout","OPM"):
            df[col] = df[col].str.replace(',','').astype(float)
        else:
            df[col] = df[col].str.replace('%','').astype(float) / 100
    dates = df.index.tolist()    
    dates_with_year = [f"{int(date.split('-')[0]) + 2000}-03-01" for date in dates]
    index = pd.to_datetime(dates_with_year, format='%Y-%m-%d')   
    df.index = index
    return df

def visualize_debt_to_equity_ratio(df):
    '''
    
    The debt-to-equity ratio is a financial metric used to evaluate a company's financial leverage.
    
    It compares a company's total debt to its total equity, representing the proportion of financing 
    that is provided by creditors (debt) versus shareholders (equity). 
    
    It is calculated by dividing total debt by total equity.
    
    A high debt-to-equity ratio indicates that the company relies more on debt financing, which can increase financial risk due to higher interest payments and potential default. 
    On the other hand, a low debt-to-equity ratio suggests that the company relies more on equity financing, which may indicate a lower risk of financial distress but could also limit growth opportunities.
    
    So Debt To Equity Ratio = Borrowings / (Equity Share Capital + Reserves)
    
    Borrowings: This represents the amount of debt the company owes to external sources, such as loans or bonds. It includes both short-term and long-term debt obligations.
    
    Equity Share Capital: This represents the amount of capital contributed by shareholders in exchange for ownership shares in the company.
    
    Reserves: Reserves represent accumulated profits that have not been distributed to shareholders as dividends.
    
    For RIL, we can see from the graph that there is a
    decrease in the debt-to-equity ratio from 0.8 to 0.45 over a 10-year period 
    generally indicates a reduction in the company's reliance on debt financing 
    relative to equity financing.
    
    This means that A decrease in the debt-to-equity ratio may also indicate 
    that the company is funding its growth initiatives through retained earnings 
    or equity financing rather than debt.
    
    Declining debt-to-equity ratio may signal that the company is managing its financial risk more prudently by reducing its leverage. 
    Lower leverage reduces the company's exposure to the risk of default and bankruptcy
    
    
    '''
    df['debt_to_equity_ratio'] = df['Borrowings'] / (df['Equity Share Capital'] + df['Reserves'])
    # Set the style
    sns.set_style("whitegrid")

    # Plotting
    plt.figure(figsize=(12, 6))
    # Sales
    sns.lineplot(data=df, x=df.index, y='debt_to_equity_ratio', marker='o', color='royalblue', linewidth=2, label='Debt To Equity Ratio')

    # Formatting
    plt.title('Debt To Equity Ratio: Reliance Industries', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Debt To Equity Ratio', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()
    
def visualize_return_on_equity(df):
    '''
    Return on Equity (ROE) is a financial ratio that measures the profitability of a company's equity shareholders' investment. 
    It indicates how effectively the company is generating profits from the shareholders' equity capital.
    
    By dividing net profit by the sum of equity share capital and reserves, the formula calculates the return
    generated for each unit of equity capital invested by shareholders.
    
    A higher ROE indicates that the company is generating more profit
    relative to the equity capital invested by shareholders, which is generally favorable.
    
    A lower ROE may indicate less efficient use of equity capital or lower profitability relative to the equity invested.
    
    Return On Equity = Net Profit / (Equity Share Capital + Reserves)
    
    For RIL, a declining Return on Equity (ROE) can indicate several underlying trends or issues 
    within a company. 
    
    Decreasing Profitability: A decline in ROE may be due to decreasing profitability,
    meaning the company is generating lower profits relative to the equity capital 
    invested by shareholders.

    Changes in the company's capital structure, such as increased debt levels, can impact ROE. 
    If the company's profitability  doesn't increase sufficiently to offset the 
    higher financial risk and interest costs, ROE may decline.
    
    '''
    df['return_on_equity'] = df['Net profit'] / (df['Equity Share Capital'] + df['Reserves'])
    # Set the style
    sns.set_style("whitegrid")

    # Plotting
    plt.figure(figsize=(12, 6))
    # Sales
    sns.lineplot(data=df, x=df.index, y='return_on_equity', marker='o', color='turquoise', linewidth=2, label='Return On Equity')

    # Formatting
    plt.title('Return On Equity: Reliance Industries', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Return On Equity', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()
    
def visualize_return_on_capital_employed(df):
    '''
    Return on Capital Employed (ROCE) is a financial ratio 
    that measures a company's profitability and efficiency in using its capital to generate earnings. 
    It indicates how effectively a company is utilizing its capital to generate profits 
    before considering the effects of taxes and financing costs.
    
    ROCE = Operating Profit / Capital Employed
    
    Capital Employed refers to the total capital invested in the business, 
    including both equity and debt components.
    
    Capital Employed = Reserves + Borrowings + Equity Share Capital
    
    Equity share capital represents the amount of capital 
    contributed by the shareholders of a company in exchange for ownership shares.
    
    Reserves, also known as retained earnings or accumulated profits, represent the portion of a company's profits that have been retained 
    and reinvested in the business rather than distributed to shareholders as dividends.
    
    Borrowings represent the funds borrowed by a company from external sources, 
    such as banks, financial institutions, or bondholders, to finance its operations, investments, or capital expenditures.
    
    An increasing ROCE often suggests that the company
    is becoming more efficient in generating profits from its capital investments.
    This can be attributed to factors such as improved cost management, 
    higher sales revenue, better asset utilization, or increased productivity. (RIL's case)
    
    Competitive Advantage: A rising ROCE relative to industry peers may indicate 
    that the company is gaining a competitive advantage, capturing market share, 
    or outperforming competitors in terms of profitability and efficiency.

    A decreasing ROCE signals a decline in profitability relative to the capital employed. This could result from factors 
    such as declining sales, rising costs, operational inefficiencies, or adverse market conditions.
    '''
    df['return_on_capital_employed'] = 0
    for i,val in enumerate(df.index):
        value = (df.iloc[i, df.columns.get_loc('Operating Profit')]) / (df.iloc[i, df.columns.get_loc('Equity Share Capital')] + df.iloc[i, df.columns.get_loc('Reserves')] + df.iloc[i, df.columns.get_loc('Borrowings')])
        df.at[val,'return_on_capital_employed'] = value
    # Set the style
    sns.set_style("whitegrid")

    # Plotting
    plt.figure(figsize=(12, 6))
    # Sales
    sns.lineplot(data=df, x=df.index, y='return_on_capital_employed', marker='o', color='purple', linewidth=2, label='Return On Capital Employed')

    # Formatting
    plt.title('Return On Capital Employed: Reliance Industries', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Return On Capital Employed', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()
    
def visualize_debtor_days(df):
    '''
    Debtor days is a financial metric that measures the average number of days
    it takes for a company to collect payment from its customers after making a sale.
    
    Debtors: This represents the total amount of money owed to the company by its customers for goods or services sold on credit. Debtors are also referred to as accounts receivable. 
    
    Sales: This represents the total value of goods sold or services rendered by the company during a specific period.
    
    365: This represents the number of days in a year. It is used to annualize the sales figure to calculate the average daily sales.
    
    By dividing the total amount of debtors by the average daily sales (sales divided by 365), the formula calculates the average number of days it takes for the company to collect payments from its debtors. This provides insight into the efficiency of the company's credit and collection policies and its ability to manage accounts receivable effectively.
    
    A lower debtor days value indicates that the company is collecting payments from its debtors more quickly, which is generally favorable as it improves cash flow and liquidity. Conversely, a higher debtor days value may indicate delays in collecting payments, 
    which could lead to cash flow challenges and increased credit risk.
    
    '''
    df['debtor_days'] = df['Debtors'] / (df['Sales'] / 365)
    # Set the style
    sns.set_style("whitegrid")

    # Plotting
    plt.figure(figsize=(12, 6))
    # Sales
    sns.lineplot(data=df, x=df.index, y='debtor_days', marker='o', color='#006400', linewidth=2, label='Debtor Days')

    # Formatting
    plt.title('Debtor Days: Reliance Industries', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Debtor Days', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()
    
def visualize_inventory_turnover(df):
    '''
    
    Inventory turnover is a financial ratio that measures 
    how efficiently a company manages its inventory by evaluating how many times 
    the company sells and replaces its inventory during a specific period, typically a year. 
    It indicates how quickly inventory is being sold and replaced within the business operations.
    
    Inventory Turnover = Sales / Inventory
    
    By dividing the total sales by the inventory value, 
    the formula calculates the inventory turnover ratio. 
    This ratio indicates how many times the company's inventory is sold and replaced during the period.
    
    Sales: This represents the total value of goods sold or services 
    rendered by the company during a specific period. It is typically obtained 
    from the company's income statement or profit and loss statement.

    Inventory: This represents the total value of inventory held by the company 
    at a particular point in time. It includes raw materials, work-in-progress, 
    and finished goods that are ready for sale. Inventory is usually reported as a 
    current asset on the balance sheet.

    A high inventory turnover ratio indicates that the company is selling 
    its inventory quickly and efficiently, which is generally favorable 
    as it minimizes the risk of obsolete or excess inventory and improves cash flow. 
    Conversely, a low inventory turnover ratio may suggest that the company is holding onto inventory 
    for too long, which can tie up capital and increase carrying costs.

    
    '''
    df['inventory_turnover'] = df['Sales'] / df['Inventory']
    # Set the style
    sns.set_style("whitegrid")

    # Plotting
    plt.figure(figsize=(12, 6))
    # Sales
    sns.lineplot(data=df, x=df.index, y='inventory_turnover', marker='o', color='teal', linewidth=2, label='Inventory Turnover')

    # Formatting
    plt.title('Inventory Turnover: Reliance Industries', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Inventory Turnover', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

def main():
    balance_sheet_file = os.path.join(os.path.join(os.path.dirname(os.getcwd()),'file'),'Reliance_Data_Balance_Sheet.csv')
    profit_loss_file = os.path.join(os.path.join(os.path.dirname(os.getcwd()),'file'),'Reliance_Data_Profit_Loss.csv')
    balance_sheet_df = read_balance_sheet_data(balance_sheet_file)
    profit_loss_df = read_profit_loss_data(profit_loss_file)
    combined_df = pd.merge(balance_sheet_df, profit_loss_df, left_index=True, right_index=True, how='inner')
    visualize_debt_to_equity_ratio(combined_df)
    visualize_return_on_equity(combined_df)
    visualize_return_on_capital_employed(combined_df)
    visualize_debtor_days(combined_df)
    visualize_inventory_turnover(combined_df)
    
if __name__ == "__main__":
    main()