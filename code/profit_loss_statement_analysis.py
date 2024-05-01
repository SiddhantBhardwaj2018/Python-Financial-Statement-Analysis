import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

def read_data(file_name):
    '''
    Convert active sheet of Screener.in file to csv file to obtain values
    '''
    df = pd.read_csv(file_name) 
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

def generate_sales_vs_profit_lineplot(df):
    # Set the style
    sns.set_style("whitegrid")

    # Plotting
    plt.figure(figsize=(12, 6))
    # Sales
    sns.lineplot(data=df, x=df.index, y='Sales', marker='o', color='royalblue', linewidth=2, label='Sales')

    # EPS
    sns.lineplot(data=df, x=df.index, y='Operating Profit', marker='o', color='green', linewidth=2, label='Operating Profit')

    # EPS
    sns.lineplot(data=df, x=df.index, y='EPS', marker='o', color='orange', linewidth=2, label='EPS')

    # Formatting
    plt.title('Profit Vs Sales Vs EPS: Reliance Industries', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Amount (in Rupees)', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yscale('log')
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()
    
def generate_correlation_heatmap(df):
    selected_columns = ["Sales", "Profit before tax", "Operating Profit", "EPS"]
    selected_corr_matrix = df[selected_columns].corr()
    
    # Plot heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(selected_corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 10})
    plt.title('Correlation Heatmap of Financial Metrics', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.show()

def generate_operating_profit_margin(df):
    '''
    Operating profit margin is a financial metric that measures a company's profitability by expressing its operating income as a percentage of its revenue. It's calculated by dividing operating income by 
    revenue and then multiplying by 100 to get a percentage.
    
    The formula for operating profit margin is:
    
    Operating Profit Margin = (Operating Profit / Revenue) * 100
    
    A consistently high operating profit margin indicates that a company is effectively managing its costs and expenses relative to its revenue. This efficiency in operations can be a reflection of competitive advantages such as economies of scale, superior technology, 
    efficient production processes, or strong brand recognition.
    
    A high operating profit margin, especially when maintained over several periods, suggests that the company possesses qualities that allow it to outperform competitors and maintain its market position. This could be due to factors like unique intellectual property,
    proprietary technology, strong customer loyalty, or efficient supply chain management.
    
    In the case of Reliance Industries, a consistently rising operating profit margin is indicative of 
    a durable competitive advantage, which means that
    the company has a strong competitive position in its industry, 
    which can translate into stable earnings and potentially higher returns over time.
    '''
    df['operating_profit_margin'] = (df['Operating Profit'] / df['Sales']) * 100
     # Set the style
    sns.set_style("whitegrid")

    # Plotting
    plt.figure(figsize=(12, 6))
    # Sales
    sns.lineplot(data=df, x=df.index, y='operating_profit_margin', marker='o', color='royalblue', linewidth=2, label='Operating Profit Margin')

    # Formatting
    plt.title('Operating Profit Margin: Reliance Industries', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Operating Profit Margin (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

def visualize_depreciation(df):
    '''
    Depreciation is an accounting method used to allocate the cost of tangible assets 
    over their useful lives. When a company buys assets such as equipment, machinery, buildings, 
    or vehicles, these assets gradually lose value over time due to wear and tear, obsolescence, 
    or other factors. Depreciation 
    reflects this decrease in value by spreading the asset's cost over its expected useful life.
    
    When depreciation consistently increases for a company, 
    
    a) The company may be acquiring more assets over time, leading to a larger depreciation expense on its income statement.
    b) The company is using its assets more intensively, they might depreciate at a faster rate, leading to higher depreciation expenses.
    c) Increasing depreciation might signify that the company is investing in long-term assets with higher initial costs or shorter useful lives, resulting in higher depreciation expenses.
    
    Above Points for RIL
    '''
     # Set the style
    sns.set_style("whitegrid")

    # Plotting
    plt.figure(figsize=(12, 6))
    # Sales
    sns.lineplot(data=df, x=df.index, y='Depreciation', marker='o', color='#33FF57', linewidth=2, label='Depreciation')

    # Formatting
    plt.title('Depreciation: Reliance Industries', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Depreciation', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()


def visualize_interest_expense(df):
    '''
    Interest expense as a percentage of operating profit is a financial ratio that indicates the proportion of a company's operating profit that is being used to cover interest expenses.
    It's calculated using the formula:
    
    Interest Expense as Percent of Operating Profit = (Interest Expense / Operating Profit) * 100
    
    When this ratio is increasing, then
    
    a) A rising ratio suggests that a larger portion of the company's operating profit is being used to cover interest expenses. This could indicate higher financial risk, especially if the company is heavily reliant on debt financing.
    b) If the increase in interest expense outpaces the growth in operating profit, it may suggest that the company is facing challenges in generating sufficient cash flows to cover its debt obligations.
    
    When this ratio is decreasing, then 
    
    a) Improving Financial Health: A declining ratio indicates that interest expenses are becoming a smaller portion of operating profit. This suggests improved financial health, as the company may be generating more profit relative to its interest obligations.
    b) Better Debt Management: A decreasing ratio could also signify that the company has successfully refinanced its debt at lower interest rates or reduced its overall debt burden, leading to lower interest expenses.

    
    '''
    df['interest_expense'] = (df['Interest'] / df['Operating Profit']) * 100
    # Set the style
    sns.set_style("whitegrid")

    # Plotting
    plt.figure(figsize=(12, 6))
    # Sales
    sns.lineplot(data=df, x=df.index, y='interest_expense', marker='o', color='#33FFA8', linewidth=2, label='Interest')

    # Formatting
    plt.title('Interest Expense As Percent Of Operating Profit: Reliance Industries', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Interest Expense (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()
    
def visualize_net_profit_margin(df):
    '''
    The net profit to sales ratio, also known as the net profit margin or simply profit margin, is a financial ratio that measures the percentage of each sales dollar that translates into net profit after all expenses have been deducted. 
    It is calculated using the formula:
    
    Net Profit Margin = (Net Profit / Sales) * 100
    
    Where,
    
    Net Profit is the total profit earned by the company after deducting all expenses, 
    including operating expenses, interest, taxes, and other costs.
    
    Sales (or Revenue) is the total amount of money generated from selling goods or services.
    
    The net profit margin provides insight into a company's profitability and efficiency in generating profit from its sales.
    
    A High Net Profit Margin means - 
    
        a)  Efficient Operations: A high net profit margin indicates that the company is effectively managing its costs and expenses relative to its sales revenue.
        
        b) Competitive Advantage: Companies with high profit margins often have a competitive advantage, such as strong brand recognition, unique products or services, or a dominant market position.
        
    A Low Net Profit Margin means - 
    
        a) Profitability Challenges: A low net profit margin suggests that the company's profitability is constrained by various factors such as high operating expenses, low pricing power, or intense competition.
        
        b) Operating Inefficiencies: Companies with low profit margins may be facing challenges in managing costs or inefficient operations.
       
    For RIL, the last 10 years display a very volatile Net Profit Margin.
       
        a) Fluctuations in profitability could stem from various factors such as erratic sales patterns, unexpected changes in costs or expenses, or external economic conditions.
        
        b) Volatility in net profit margin may reflect the company's sensitivity to external factors such as changes in market demand, pricing pressures, or regulatory developments. Companies operating in highly cyclical industries or those with exposure to volatile commodity prices are particularly susceptible to fluctuations in profitability.
        
        c) Companies with volatile net profit margins may face challenges in managing risks effectively. Rapid fluctuations in profitability can make it difficult for management to plan and allocate resources, leading to potential disruptions in operations or financial performance.    
    
    '''
    df['net_profit_margin'] = ( df['Net profit'] / df['Sales'] ) * 100
    # Set the style
    sns.set_style("whitegrid")

    # Plotting
    plt.figure(figsize=(12, 6))
    # Sales
    sns.lineplot(data=df, x=df.index, y='net_profit_margin', marker='o', color='#B233FF', linewidth=2, label='Net Profit Margin')

    # Formatting
    plt.title('Net Profit Margin: Reliance Industries', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Net Profit Margin (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()
    
def visualize_EPS(df):
    '''
    EPS stands for Earnings Per Share. 
    It is a financial metric that represents the portion of a company's profit 
    allocated to each outstanding share of its common stock. 
    
    EPS is calculated by dividing the company's net income (after deducting preferred dividends) 
    by the average number of outstanding shares during a specific period. 
    
    The formula for calculating EPS is as follows:
    
    EPS  = (Net Income  - Preferred Dividends) / (Average Number of Shares Outstanding)
    
    Increasing EPS - 
    
        a) Profit Growth: An increasing EPS generally indicates that a company's profitability is improving over time
    
        b) Positive Investor Sentiment: Rising EPS is often viewed positively by investors and can lead to an increase in the company's stock price.
        
    Decreasing EPS - 
    
        a) Profit Decline: A decreasing EPS suggests that a company's profitability is declining. This could be due to factors such as declining revenues, rising costs, or deteriorating market conditions.
        
        b) Concerns for Investors: Declining EPS may raise concerns among investors about the company's financial health and future prospects.
    '''
    # Set the style
    sns.set_style("whitegrid")

    # Plotting
    plt.figure(figsize=(12, 6))
    # Sales
    sns.lineplot(data=df, x=df.index, y='EPS', marker='o', color='#B233FF', linewidth=2, label='Earnings Per Share')

    # Formatting
    plt.title('Earnings Per Share (EPS): Reliance Industries', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('EPS', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()
    
def main():
    profit_loss_file = os.path.join(os.path.join(os.path.dirname(os.getcwd()),'file'),'Reliance_Data_Profit_Loss.csv')
    df = read_data(profit_loss_file)
    generate_operating_profit_margin(df)
    visualize_depreciation(df)
    visualize_interest_expense(df)
    visualize_net_profit_margin(df)
    visualize_EPS(df)
         
if __name__ == "__main__":
    main()