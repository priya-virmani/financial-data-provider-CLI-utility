import requests, json
import ast
import pandas as pd

api_key = input("Enter your API Key: ")
company = input("Enter the company name: ");
api_endpoint = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=%s&apikey=%s' %(company, api_key)

print("\n")

# Getting data from API
response_data = requests.get(api_endpoint)
json_data = response_data.text

#Converting this data into table
val = ast.literal_eval(json_data)
val1 = json.loads(json.dumps(val))
val2 = val1['bestMatches']

#List of columns tobe displayed as a grid
columns_names = ['Symbol', 'Name', 'Type', 'Region', 'Market Open', 'Market Close', ' Timezone', 'Currency', 'Match Score']
new_col_list = []
for ele in val2:
    if isinstance(ele, dict):
        new_dict = dict(zip(columns_names, list(ele.values())))
        new_col_list.append(new_dict)    
df = pd.DataFrame(new_col_list)
print(df)

choice = input("\nEnter you company Symbol(Symbol is CASE SENSITIVE): ")

print("\nData of the Company\n")

for ele in new_col_list:
    if ele["Symbol"]==choice:
        print(pd.DataFrame([ele]))
        break
        
#display historical prices on specific timeframes:
while(True):
    prices_choice = int(input("\n\nEnter the option you want to see the Historical Prices: \n1. Intraday\n2. Daily\n3. Weekly\n4. Monthly\n\n"))
    if prices_choice==1:
        interval = input("Enter the time interval of the day: (1min, 5min, 10min, 15min, 30min)\n")
        interval_data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=%s&interval=%s&apikey=%s' %(choice, interval, api_key))       
        val = ast.literal_eval(interval_data.text)
        val1 = json.loads(json.dumps(val['Time Series (%s)' %interval]))
        df = pd.DataFrame.from_dict([val1])
        df_t = df.T
        print(df_t)
    elif prices_choice==2:
        interval_data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&apikey=%s' %(choice, api_key))       
        val = ast.literal_eval(interval_data.text)
        val1 = json.loads(json.dumps(val['Time Series (Daily)']))
        df = pd.DataFrame.from_dict([val1])
        df_t = df.T
        print(df_t)
    elif prices_choice==3:
        interval_data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=%s&apikey=%s' %(choice, api_key))       
        val = ast.literal_eval(interval_data.text)
        val1 = json.loads(json.dumps(val['Weekly Time Series']))
        df = pd.DataFrame.from_dict([val1])
        df_t = df.T
        print(df_t)
    elif prices_choice==4:
        interval_data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=%s&apikey=%s' %(choice, api_key))       
        val = ast.literal_eval(interval_data.text)
        val1 = json.loads(json.dumps(val['Monthly Time Series']))
        df = pd.DataFrame.from_dict([val1])
        df_t = df.T
        print(df_t)
    
    user_choice = input("Do you want to select again? (Y/N): ")
    if user_choice == 'N':
        break

#display current quote
print("\nGlobal Quote\n")
global_quote = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey=%s' %(choice, api_key))       
print(global_quote.text)

#indicator results for it in grid
interval_choice = input("Enter the time interval of the day: (1min, 5min, 10min, 15min, 30min, 60min, daily, weekly, monthly)\n")    
time_period = input("Enter the time interval of the day: (60, 200)\n")
series_type = input("Enter the time interval of the day: (close, open, high, low)\n")
sma_data = requests.get('https://www.alphavantage.co/query?function=SMA&symbol=%s&interval=%s&time_period=%s&series_type=%s&apikey=%s' %(choice, interval_choice, time_period, series_type, api_key))       
val = ast.literal_eval(sma_data.text)
val1 = json.loads(json.dumps(val["Technical Analysis: SMA"]))
df = pd.DataFrame.from_dict([val1])
df_t = df.T
print(df_t)