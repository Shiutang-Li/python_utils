#!/usr/bin/python

# coding=utf8
# description     : Custom group-by function
# author          : Shiu-Tang Li
# last update     : 03/26/2018
# python_version  : 3.5.2

import pandas as pd
import numpy as np
    
def gpby(df, gp_feature, aggr_feature, aggr_func, join = True):
    
    # Input:
    # df:                target dataframe
    # gp_feature:        group by this feature
    # aggr_feature:      another feature for aggregation
    # aggr_func:         aggregation function: 'count', 'mean', 'max', 'min', 'sum', 'list'
    # join:              True:   join the 'aggregation table' to original table
    #                    False:  return the 'aggregation table' only
    
    # Output:            new dataframe
    
    # Example:
    # df     =  pd.DataFrame({'a':[1,1,2,2,3,3], 'b': [4,5,6,7,8,9]})
    # new_df =  gpby(df, 'a', 'b', 'mean')  
    
    if aggr_func == 'mean':
        table  = df[[gp_feature, aggr_feature]].groupby(gp_feature).aggregate(np.mean)[aggr_feature]
    elif aggr_func == 'count':
        table  = df[[gp_feature, aggr_feature]].groupby(gp_feature).aggregate('count')[aggr_feature]
    elif aggr_func == 'max':
        table  = df[[gp_feature, aggr_feature]].groupby(gp_feature).aggregate(np.max)[aggr_feature]        
    elif aggr_func == 'min':
        table  = df[[gp_feature, aggr_feature]].groupby(gp_feature).aggregate(np.min)[aggr_feature]          
    elif aggr_func == 'sum':
        table  = df[[gp_feature, aggr_feature]].groupby(gp_feature).aggregate(np.sum)[aggr_feature]  
    elif aggr_func == 'list':
        table  = df[[gp_feature, aggr_feature]].drop_duplicates().groupby(gp_feature)[aggr_feature].apply(list) 
    else:
        return 'aggr function not available'
        
        
    table  = pd.DataFrame(table)
    table[gp_feature] = table.index
    
    if aggr_func != 'list':
        table  = pd.DataFrame({gp_feature:table[gp_feature].values,
                               aggr_func +'_of_'+ aggr_feature +'_gp_by_'+ gp_feature: table[aggr_feature].values})
    else:
        table  = pd.DataFrame({gp_feature:table[gp_feature].values,
                               aggr_func +'_of_'+ aggr_feature +'_gp_by_'+ gp_feature: 
                               [', '.join(str(e) for e in item) for item in table[aggr_feature].values]})
        
    if join == True:
        return df.join(table.set_index(gp_feature), on=gp_feature)
    else:
        return table
