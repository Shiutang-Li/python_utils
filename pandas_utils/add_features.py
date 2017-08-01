#!/usr/bin/python

# coding=utf8
# description     : Add mean, count, rank for a feature
# author          : Shiu-Tang Li
# last update     : 07/08/2017
# version         : 0.1
# python_version  : 3.5.2

import pandas as pd
import numpy as np
    
def add_features(df, feature, pred_feature, mean = True, count = True, rank = True):
    
    # Input:
    # df:                target dataframe
    # feature:           target column for group operations
    # pred_feature:      target numeric column
    # mean, count, rank: additional features to be added  
    
    # Output:            new dataframe
    
    # Example:
    # df     =  pd.DataFrame({'a':[1,1,2,2,3,3], 'b': [4,5,6,7,8,9]})
    # new_df =  add_features(df, 'a', 'b')    
    
    groups = df[[feature, pred_feature]].groupby(feature)
    table  = groups.aggregate(np.mean)[pred_feature]
    table  = pd.DataFrame(table)
    table[feature] = table.index
    table  = pd.DataFrame({feature:table[feature].values,
                           'mean_'+feature: table[pred_feature].values})

    table2  = groups.aggregate('count')[pred_feature]
    table2  = pd.DataFrame(table2)
    table2[feature] = table2.index
    table2  = pd.DataFrame({feature:      table2[feature].values,
                            'count_'+feature: table2[pred_feature].values})
    table = pd.merge(table, table2, on=feature)
    if rank == True:
        table[('rank_'+feature)] = table['mean_'+feature].rank(ascending=False).astype(int)
    if mean == False:
        del table['mean_'+feature]
    if count == False:
        del table['count_'+feature]
        
    df = df.join(table.set_index(feature), on=feature)
    return df
