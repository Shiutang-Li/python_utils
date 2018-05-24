#!/usr/bin/python
# -*- coding:utf-8 -*-

# description     : customized 'join' function to make life easy 
# author          : Shiu-Tang Li
# last update     : 5/24/2018

import pandas as pd

# Input:
# df1, df2: pandas dataframe to be joined
# key:      the join key, a string

# Output:
# Pandas dataframe storing the joined result

# Only left_join, inner_join, and outer_join are available. Why do we even need right joins? 
      
def left_join(df1, df2, key):
    
    columns_1 = df1.columns.tolist()
    columns_2 = df2.columns.tolist()
    columns_1.remove(key)  
    columns_2.remove(key) 
    
    table = df1.join(df2.set_index(key), on = key, how = 'left')
    table.reset_index(inplace = True)
    
    return table[[key] + columns_1 + columns_2]

def inner_join(df1, df2, key):
    columns_1 = df1.columns.tolist()
    columns_2 = df2.columns.tolist()
    columns_1.remove(key)  
    columns_2.remove(key) 
    
    table = df1.join(df2.set_index(key), on = key, how = 'inner')
    table.reset_index(inplace = True)
    
    return table[[key] + columns_1 + columns_2]

def outer_join(df1, df2, key):
    
    columns_1 = df1.columns.tolist()
    columns_2 = df2.columns.tolist()
    columns_1.remove(key)  
    columns_2.remove(key) 
    
    table = df1.join(df2.set_index(key), on = key, how = 'outer')
    table.reset_index(inplace = True)
    
    return table[[key] + columns_1 + columns_2]
