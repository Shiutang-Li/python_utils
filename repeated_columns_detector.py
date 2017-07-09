#!/usr/bin/python

# coding=utf8
# description     : Output a list of lists where each small list contains coulmns of the same value 
# author          : Shiu-Tang Li
# last update     : 07/09/2017
# version         : 0.1
# python_version  : 3.5.2

import pandas as pd
import numpy as np

def repeated_columns_detector(df, show_result = True):
    
    # Input:
    # df:                target dataframe
    # show_result:       print output if set to True
    
    # Output:            list of lists where each small list contains repeated coulmns 
    #                    (Won't include any column which doesn't repeat with other columns)
    
    # Example:
    # df     =  pd.DataFrame({'a':[1,2,3],'b':[4,5,6],'c':[4,5,6],'d':[1,2,3],'e':[4,5,6],'f':[7,8,9]})
    # repeated_columns_detector(df)    
    
    repeated_columns = []
    for column1 in df.columns:
        for column2 in df.columns:
            if df[column1].equals(df[column2]) and (column1 < column2):
                flag = 0 
                for item in repeated_columns:
                    if (column1 in item) and (column2 not in item):
                        item.append(column2)
                        flag = 1
                    elif (column1 in item) and (column2 in item):
                        flag = 1
                if flag == 0:
                    repeated_columns.append([column1, column2])
    print(repeated_columns)
    return df
