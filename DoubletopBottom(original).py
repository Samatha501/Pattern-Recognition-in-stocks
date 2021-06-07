import numpy as np
import pandas as pd
from scipy.signal import argrelextrema


def find_local_min_max(data_frame, col_name):
    local_max = argrelextrema(data_frame[col_name].values, np.greater)[0]
    local_min = argrelextrema(data_frame[col_name].values, np.less)[0]

    data_frame['Local_min_max'] = ""

    data_frame.loc[local_min,'Local_min_max'] = "min"
    data_frame.loc[local_max,'Local_min_max'] = "max"

    return data_frame
    # print(data_frame.head(15))



data = pd.read_csv("C:\\Users\\sam\\Desktop\\TCS.csv")
data.rename(columns={'Unnamed: 0':'Index'}, inplace=True )
datafile = len(data)
# print(data)
# data = data.iloc[998:1358,] # data from 19-11-19 to 23-04-21.
df = find_local_min_max(data, 'Low')
# print(df)
df1 = df.replace('', np.nan)
local_min_max_df = df1.dropna(axis=0, how='any')
# local_min_max_df.set_index(['Date', 'Open', 'High', 'Low', 'Price', 'Volume', 'Local_min_max'])
# print(local_min_max_df.head())

local_min_max_df = local_min_max_df.reset_index(drop=True)
# local_min_max_df.reindex()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 4)
# print(local_min_max_df)

#IDENTIFYING W Pattern

max_range = len(local_min_max_df.index)
# print(max_range)
results_W_df = pd.DataFrame(columns=['p1_date', 'p1_close', 'p2_date', 'p2_close', 'p3_date', 'p3_close', 'p4_date',
                                     'p4_close', 'p5_date', 'p5_close', 'type', 'PnL', 'Exit_Date'])
count=0
for i in local_min_max_df.index:
    # print(i)
    if((i+4) < max_range):
        # print(local_min_max_df['Date'].loc[i])
        # print(i)
        if(local_min_max_df['Local_min_max'].loc[i]=='max'):

            if(local_min_max_df['Low'].iloc[i] > local_min_max_df['Low'].iloc[i+1] and
                local_min_max_df['Low'].iloc[i+1] < local_min_max_df['Low'].iloc[i+2] and
                local_min_max_df['Low'].iloc[i+2] > local_min_max_df['Low'].iloc[i+3] and
                local_min_max_df['Low'].iloc[i+3] < local_min_max_df['Low'].iloc[i+4]):

                if(((local_min_max_df['Low'].iloc[i] - local_min_max_df['Low'].iloc[i+2]) < (0.1*local_min_max_df['Low'].iloc[i+2]))
                        and local_min_max_df['Low'].iloc[i] >= local_min_max_df['Low'].iloc[i+2] and
                        local_min_max_df['Low'].iloc[i+2] <= local_min_max_df['Low'].iloc[i+4]):
                    diff = local_min_max_df['Price'].iloc[i+4] - local_min_max_df['Price'].iloc[i+2]
                    p5_value = diff + local_min_max_df['Price'].iloc[i+4]
                    profit_target = p5_value
                    stop_loss = local_min_max_df['Price'].iloc[i+2]
                    # print(profit_target)
                    next_point = local_min_max_df['Index'].iloc[i+4]+1
                    for n in range(next_point, datafile):
                        if(n < datafile):
                            if (data['Price'].iloc[n] >= profit_target and
                                    data['Price'].iloc[n] > stop_loss):

                                PnL = data['Price'].iloc[n] - local_min_max_df['Price'].iloc[i+4]

                                Exit_Date = data['Date'].iloc[n]

                                results_W_df = results_W_df.append({'p1_date': local_min_max_df['Date'].iloc[i], 'p1_close': local_min_max_df['Price'].iloc[i],
                                                                    'p2_date': local_min_max_df['Date'].iloc[i+1],'p2_close': local_min_max_df['Price'].iloc[i+1],
                                                                    'p3_date': local_min_max_df['Date'].iloc[i+2],'p3_close': local_min_max_df['Price'].iloc[i+2],
                                                                    'p4_date': local_min_max_df['Date'].iloc[i+3],'p4_close': local_min_max_df['Price'].iloc[i+3],
                                                                    'p5_date': local_min_max_df['Date'].iloc[i+4],'p5_close': local_min_max_df['Price'].iloc[i+4],
                                                                    'type': "W",'PnL': PnL, 'Exit_Date': Exit_Date,
                                                                    }, ignore_index=True)

                                break
                            elif((data['Price'].iloc[n] <= stop_loss)):

                                PnL = data['Price'].iloc[n] - local_min_max_df['Price'].iloc[i+4]

                                Exit_Date = data['Date'].iloc[n]


                                # print('p1: '+local_min_max_df['Date'].iloc[i],'p2:'+local_min_max_df['Date'].iloc[i+1],'p3: '
                                #    +local_min_max_df['Date'].iloc[i+2],'p4:'+local_min_max_df['Date'].iloc[i+3],'p5:'+local_min_max_df['Date'].iloc[i+4])


                                results_W_df = results_W_df.append({'p1_date': local_min_max_df['Date'].iloc[i], 'p1_close': local_min_max_df['Price'].iloc[i],
                                                                    'p2_date': local_min_max_df['Date'].iloc[i+1],'p2_close': local_min_max_df['Price'].iloc[i+1],
                                                                    'p3_date': local_min_max_df['Date'].iloc[i+2],'p3_close': local_min_max_df['Price'].iloc[i+2],
                                                                    'p4_date': local_min_max_df['Date'].iloc[i+3],'p4_close': local_min_max_df['Price'].iloc[i+3],
                                                                    'p5_date': local_min_max_df['Date'].iloc[i+4],'p5_close': local_min_max_df['Price'].iloc[i+4],
                                                                    'type': "W",'PnL': PnL, 'Exit_Date': Exit_Date,
                                                                    }, ignore_index=True)
                                break

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 4)
# print("no.of bottoms: ",count)
# print(results_W_df)

print("M Pattern DataFrame")

# IDENTIFYING M Pattern

df = find_local_min_max(data, 'High')
# print(df)
df1 = df.replace('', np.nan)
local_min_max_df = df1.dropna(axis=0, how='any')
# local_min_max_df.set_index(['Date', 'Open', 'High', 'Low', 'Price', 'Volume', 'Local_min_max'])
# print(local_min_max_df)
local_min_max_df = local_min_max_df.reset_index(drop=True)

max_range = len(local_min_max_df.index)
# print(max_range)
results_M_df = pd.DataFrame(columns=['p1_date', 'p1_close', 'p2_date', 'p2_close', 'p3_date', 'p3_close', 'p4_date',
                                     'p4_close', 'p5_date', 'p5_close', 'type', 'PnL', 'Exit_Date'])

count = 0
for i in local_min_max_df.index:
    # print(i)
    if((i+4) < max_range):
        if(local_min_max_df['Local_min_max'].loc[i]=='min'):
            if(local_min_max_df['High'].iloc[i] < local_min_max_df['High'].iloc[i+1] and
                    local_min_max_df['High'].iloc[i+1] > local_min_max_df['High'].iloc[i+2] and
                    local_min_max_df['High'].iloc[i+2] < local_min_max_df['High'].iloc[i+3] and
                    local_min_max_df['High'].iloc[i+3] > local_min_max_df['High'].iloc[i+4]):

                if(((local_min_max_df['High'].iloc[i] - local_min_max_df['High'].iloc[i+2]) < (0.1*local_min_max_df['High'].iloc[i+2])) and
                        local_min_max_df['High'].iloc[i] <= local_min_max_df['High'].iloc[i+2] and
                        local_min_max_df['High'].iloc[i+2] >= local_min_max_df['High'].iloc[i+4]):
                    diff = local_min_max_df['Price'].iloc[i+2] - local_min_max_df['Price'].iloc[i+4]
                    p5_value = diff + local_min_max_df['Price'].iloc[i+4]
                    profit_target = p5_value
                    stop_loss = local_min_max_df['Price'].iloc[i+2]
                    # print(profit_target)
                    next_point = local_min_max_df['Index'].iloc[i+4]+1
                    for n in range(next_point, datafile):
                        if(n < datafile):
                            if (data['Price'].iloc[n] <= profit_target and
                                    data['Price'].iloc[n] < stop_loss):

                                PnL = abs(local_min_max_df['Price'].iloc[i+4] - data['Price'].iloc[n])

                                Exit_Date = data['Date'].iloc[n]

                                results_M_df = results_M_df.append({'p1_date': local_min_max_df['Date'].iloc[i], 'p1_close': local_min_max_df['Price'].iloc[i],
                                                                    'p2_date': local_min_max_df['Date'].iloc[i+1],'p2_close': local_min_max_df['Price'].iloc[i+1],
                                                                    'p3_date': local_min_max_df['Date'].iloc[i+2],'p3_close': local_min_max_df['Price'].iloc[i+2],
                                                                    'p4_date': local_min_max_df['Date'].iloc[i+3],'p4_close': local_min_max_df['Price'].iloc[i+3],
                                                                    'p5_date': local_min_max_df['Date'].iloc[i+4],'p5_close': local_min_max_df['Price'].iloc[i+4],
                                                                    'type': "M",'PnL': PnL, 'Exit_Date': Exit_Date,
                                                                    }, ignore_index=True)

                                break
                            elif((data['Price'].iloc[n] >= stop_loss)):

                                PnL = local_min_max_df['Price'].iloc[i+4] - data['Price'].iloc[n]

                                Exit_Date = data['Date'].iloc[n]


                                # print('p1: '+local_min_max_df['Date'].iloc[i],'p2:'+local_min_max_df['Date'].iloc[i+1],'p3: '
                                #    +local_min_max_df['Date'].iloc[i+2],'p4:'+local_min_max_df['Date'].iloc[i+3],'p5:'+local_min_max_df['Date'].iloc[i+4])



                                results_M_df = results_M_df.append({'p1_date': local_min_max_df['Date'].iloc[i],'p1_close': local_min_max_df['Price'].iloc[i],
                                                        'p2_date': local_min_max_df['Date'].iloc[i+1],'p2_close': local_min_max_df['Price'].iloc[i+1],
                                                        'p3_date': local_min_max_df['Date'].iloc[i+2],'p3_close': local_min_max_df['Price'].iloc[i+2],
                                                        'p4_date': local_min_max_df['Date'].iloc[i+3],'p4_close': local_min_max_df['Price'].iloc[i+3],
                                                        'p5_date': local_min_max_df['Date'].iloc[i+4],'p5_close': local_min_max_df['Price'].iloc[i+4],
                                                    'type': "M", 'PnL': PnL, 'Exit_Date': Exit_Date }, ignore_index=True)

                                break

# print("no.of tops: ",count)
print(results_M_df)
results_df = pd.DataFrame()
results_df1 = pd.merge(results_W_df, results_M_df, how ='outer')
results_df1['p1_date'] = pd.to_datetime(results_df1['p1_date'])
results_df = results_df1.sort_values(by='p1_date', ignore_index=True)
# results_df.to_csv(r'C:\Users\sam\Desktop\fileMWnew.csv', index=False)
# print(results_df)
