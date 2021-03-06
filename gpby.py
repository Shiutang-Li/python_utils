#!/usr/bin/python
# -*- coding:utf-8 -*-

# description     : Custom group-by function
# author          : Shiu-Tang Li
# last update     : 05/22/2018
# python_version  : 3.5.2

import pandas as pd
import numpy as np
from bisect import bisect_right
from copy import deepcopy
    
def gpby(df, gp_feature, aggr_feature, aggr_func, join = True):
    
    # Input:
    # df:                target dataframe
    # gp_feature:        group by this feature
    # aggr_feature:      another feature for aggregation
    # aggr_func:         aggregation function: 'unique_count', 'mean', 'max', 'min', 'sum', 'list'
    # join:              True:   join the 'aggregation table' to original table
    #                    False:  return the 'aggregation table' only
    
    # Output:            resulting dataframe
    
    if aggr_func == 'mean':
        table  = df[[gp_feature, aggr_feature]].groupby(gp_feature).aggregate(np.mean)[aggr_feature]
    elif aggr_func == 'unique_count':
        table  = df[[gp_feature, aggr_feature]].drop_duplicates().groupby(gp_feature).aggregate('count')[aggr_feature]
    elif aggr_func == 'max':
        table  = df[[gp_feature, aggr_feature]].groupby(gp_feature).aggregate(np.max)[aggr_feature]        
    elif aggr_func == 'min':
        table  = df[[gp_feature, aggr_feature]].groupby(gp_feature).aggregate(np.min)[aggr_feature]          
    elif aggr_func == 'sum':
        table  = df[[gp_feature, aggr_feature]].groupby(gp_feature).aggregate(np.sum)[aggr_feature]  
    elif aggr_func == 'list':
        table  = df[[gp_feature, aggr_feature]].drop_duplicates().groupby(gp_feature)[aggr_feature].apply(list) 
    else:
        print('aggr function not available') 
        return None    
        
    table  = pd.DataFrame(table)
    table[gp_feature] = table.index
    
    if aggr_func != 'list':
        table  = pd.DataFrame({gp_feature:table[gp_feature].values,
                               aggr_func +': '+ aggr_feature: table[aggr_feature].values})
    else:
        table  = pd.DataFrame({gp_feature:table[gp_feature].values,
                               aggr_func +': '+ aggr_feature: 
                               [', '.join(str(e) for e in item) for item in table[aggr_feature].values]})
        
    if join == True:
        return df.join(table.set_index(gp_feature), on=gp_feature)
    else:
        return table

    
def position_to_range(i, range_list):
    if i == 0:
        return 'x < ' + str(range_list[i])
    elif i > 0 and i < len(range_list):
        return str(range_list[i-1]) + ' ≤ x < ' + str(range_list[i])
    else:
        return 'others'

    
def gpby_range(df, gp_feature, aggr_feature, aggr_func, range_list):
    
    # Input:
    # df:                target dataframe
    # gp_feature:        group by this feature
    # aggr_feature:      another feature for aggregation
    # aggr_func:         aggregation function: 'unique_count', 'count', 'mean', 'max', 'min', 'sum', 'list'
    # range_list:        the range of each group is based on range_list. Will be sorted in ascending order.
    
    # Output:            resulting dataframe
    
    if aggr_func not in ['unique_count', 'mean', 'max', 'min', 'sum', 'list']:
        print('aggr function not available')
        return None
    
    range_list.sort()
    df2 = deepcopy(df)
    df2['group_ID'] = df2.apply(lambda x: bisect_right(range_list, x[gp_feature]), axis = 1)
    table = gpby(df2, 'group_ID', aggr_feature, aggr_func, join = False).sort_values(by = 'group_ID')
    table[gp_feature + ': x'] = table.apply(lambda x: position_to_range(int(x['group_ID']), range_list), axis = 1)
    
    return table[[gp_feature + ': x', aggr_func +': '+ aggr_feature]]
