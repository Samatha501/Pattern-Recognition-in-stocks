import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from scipy.signal import argrelextrema
import os
from os.path import basename

files = glob.glob("C:\\Users\\sam\\Desktop\\csvfiles\\*.csv")
#files = pd.read_csv("C:/Users/Ashmita/Downloads/d-kite/d-kite/3MINDIA.csv")
title0 = "filename"
title1 = "p1 date"
title2 = "p1 close"
title3 = "neck date"
title4 = "neck close"
title5 = "p2 date"
title6 = "p2 close"
title7 = "type"


print("%-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s"  % (title0, title1, title2, title3, title4, title5, title6, title7))



def get_max_min(prices1, smoothing1, window_range):
    smooth_prices = prices['Price'].rolling(window=smoothing).mean().dropna()
    local_max = argrelextrema(smooth_prices.values, np.greater)[0]
    local_min = argrelextrema(smooth_prices.values, np.less)[0]
    return local_max, local_min
for file in files:
    data = pd.read_csv(file)
    base = os.path.basename(file)
    name = os.path.splitext(base)[0]

    smoothing = 1
    window = 10
    prices = data
    min_max = get_max_min(prices, smoothing, window)
    loc_min = min_max[1]
    loc_max = min_max[0]

    count = 0

    for i in loc_max:
        for j in loc_min:
            if(i+1==j):
                for k in loc_max:
                    if(j+1==k):
                        if((data['Price'].iloc[i - 1] < data['Price'].iloc[i - 2])):
                            firstmin = i-2
                        else:
                            firstmin = i-1

                        if((data['Price'].iloc[k+1] < data['Price'].iloc[k+2])):
                            lastmin = k+2
                        else:
                            lastmin = k+1

                        if ((data['Price'].iloc[firstmin] < data['Price'].iloc[i] and data['Price'].iloc[i] >
                             data['Price'].iloc[j]) and data['Price'].iloc[j] < data['Price'].iloc[k] and
                                ( data['Price'].iloc[k] > data['Price'].iloc[lastmin])):
                            if ((data['Price'].iloc[firstmin] <= data['Price'].iloc[j]) and(data['Price'].iloc[j] >= data['Price'].iloc[lastmin]) and (data['Price'].iloc[i] <= data['Price'].iloc[k])):
                                #print("W")
                                count += 1
                                print("%-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s" % (name,data['Date'].iloc[firstmin-1],data['Date'].iloc[i], data['Price'].iloc[i], data['Date'].iloc[j],data['Price'].iloc[j],data['Date'].iloc[k], data['Date'].iloc[lastmin], data['Price'].iloc[k], "M"))
    print("\nCount of double tops : ", count)

    print()
    for i in loc_min:
        for j in loc_max:
            if(i+1==j):
                for k in loc_min:
                    if(j+1==k):
                        if((data['Price'].iloc[i - 1] < data['Price'].iloc[i - 2])):
                            firstmin = i-2
                        else:
                            firstmin = i-1

                        if((data['Price'].iloc[k+1] < data['Price'].iloc[k+2])):
                            lastmin = k+2
                        else:
                            lastmin = k+1

                        if ((data['Price'].iloc[firstmin] > data['Price'].iloc[i] and data['Price'].iloc[i] <
                             data['Price'].iloc[j]) and data['Price'].iloc[j] > data['Price'].iloc[k] and
                                ( data['Price'].iloc[k] < data['Price'].iloc[lastmin])):
                            if ((data['Price'].iloc[firstmin] >= data['Price'].iloc[j]) and(data['Price'].iloc[j] <= data['Price'].iloc[lastmin])):
                                #print("W")
                                count += 1
                                print("%-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s %-15s" % (name,data['Date'].iloc[firstmin-1],data['Date'].iloc[i], data['Price'].iloc[i], data['Date'].iloc[j],data['Price'].iloc[j],data['Date'].iloc[k], data['Date'].iloc[lastmin-1], data['Price'].iloc[k], " W"))

    print("\nCount of double bottom : ", count)

    print()