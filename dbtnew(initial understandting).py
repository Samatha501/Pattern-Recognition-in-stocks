import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

data = pd.read_csv("C:\\Users\\sam\\Desktop\\TCS.csv")
data = data.iloc[998:1358,] # data from 19-11-19 to 23-04-21.
# print(data)



# print(data)
def get_max_min(prices1, smoothing1, window_range):
    smooth_prices = prices['Price'].rolling(window=smoothing).mean().dropna()
    local_max = argrelextrema(smooth_prices.values, np.greater)[0]
    local_min = argrelextrema(smooth_prices.values, np.less)[0]

    return local_max, local_min


smoothing = 1
window = 10
prices = data

min_max = get_max_min(prices, smoothing, window)
loc_max = min_max[0]
loc_min = min_max[1]




title1 = "p1 date1"
title8 = "p1 date2"
title2 = "p1 close"
title3 = "neck date"
title4 = "neck close"
title5 = "p2 date1"
title9 = "p2 date2"
title6 = "p2 close"
title7 = "type"
print("%-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s" % (title1,title8, title2, title3, title4, title5,title9, title6, title7))
#print(loc_max)
count = 0
# threshold = min(data['Low']) * 1.15
# print(loc_min)
# print(threshold)

count = 0

for i in loc_max:
    for j in loc_min:
        if(i+1==j):
            for k in loc_max:
                if(j+1==k):
                    if((data['Price'].iloc[i - 2] < data['Price'].iloc[i - 1])):
                        firstmin = i-2
                    else:
                        firstmin = i-1

                    if (data['Price'].iloc[i] > data['Price'].iloc[i+1]):
                        firstmax = i
                    else:
                        firstmax = i+1

                    if(data['Price'].iloc[j] < data['Price'].iloc[k]):
                        secondmin = j
                    # if(data['Price'].iloc[j] < data['Price'].iloc[k-1]):
                    #     secondmin = j



                    if(data['Price'].iloc[k] > data['Price'].iloc[k+1]):
                        secondmax = k

                    else:
                        secondmax = k+1
                    if(data['Price'].iloc[k] > data['Price'].iloc[k+2]):
                        secondmax = k
                    else:
                        secondmax = k+2
                    if(data['Price'].iloc[k+1] < data['Price'].iloc[k]):
                        lastmin = k+1

                    if(data['Price'].iloc[k+2] < data['Price'].iloc[k+1]):
                        lastmin = k+2
                    if ((data['Price'].iloc[firstmin] < data['Price'].iloc[firstmax] and data['Price'].iloc[firstmax] >
                         data['Price'].iloc[secondmin]) and data['Price'].iloc[secondmin] < data['Price'].iloc[secondmax] and
                            ( data['Price'].iloc[secondmax] > data['Price'].iloc[lastmin])):
                        if ((data['Price'].iloc[firstmin] <= data['Price'].iloc[secondmin]) and (data['Price'].iloc[lastmin] <= data['Price'].iloc[secondmin])):
                            #print("M")
                            count += 1
                            print("%-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s" % (data['Date'].iloc[firstmin],data['Date'].iloc[firstmax], data['Price'].iloc[firstmax], data['Date'].iloc[secondmin],data['Price'].iloc[secondmin],data['Date'].iloc[secondmax], data['Date'].iloc[lastmin], data['Price'].iloc[secondmax], "M"))
print("\nCount of double tops : ", count)

count = 0

for i in loc_min:
    for j in loc_max:
        if(i+1==j):
            for k in loc_min:
                if(j+1==k):
                    if((data['Price'].iloc[i - 2] > data['Price'].iloc[i - 1])):
                        firstmin = i-2
                    else:
                        firstmin = i-1

                    if (data['Price'].iloc[i] < data['Price'].iloc[i+1]):
                        firstmax = i
                    else:
                        firstmax = i+1

                    if(data['Price'].iloc[j] > data['Price'].iloc[k]):
                        secondmin = j
                    # if(data['Price'].iloc[j] < data['Price'].iloc[k-1]):
                    #     secondmin = j



                    if(data['Price'].iloc[k] < data['Price'].iloc[k+1]):
                        secondmax = k

                    else:
                        secondmax = k+1
                    if(data['Price'].iloc[k] < data['Price'].iloc[k+2]):
                        secondmax = k
                    else:
                        secondmax = k+2
                    if(data['Price'].iloc[k+1] > data['Price'].iloc[k]):
                        lastmin = k+1

                    if(data['Price'].iloc[k+2] > data['Price'].iloc[k+1]):
                        lastmin = k+2
                    if ((data['Price'].iloc[firstmin] > data['Price'].iloc[firstmax] and data['Price'].iloc[firstmax] <
                         data['Price'].iloc[secondmin]) and data['Price'].iloc[secondmin] > data['Price'].iloc[secondmax] and
                            ( data['Price'].iloc[secondmax] < data['Price'].iloc[lastmin])):
                        if ((data['Price'].iloc[firstmin] >= data['Price'].iloc[secondmin]) and (data['Price'].iloc[lastmin] >= data['Price'].iloc[secondmin])):
                            #print("W")
                            count += 1
                            print("%-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s" % (data['Date'].iloc[firstmin],data['Date'].iloc[firstmax], data['Price'].iloc[firstmax], data['Date'].iloc[secondmin],data['Price'].iloc[secondmin],data['Date'].iloc[secondmax], data['Date'].iloc[lastmin], data['Price'].iloc[secondmax], "W"))
print("\nCount of double bottoms : ", count)
