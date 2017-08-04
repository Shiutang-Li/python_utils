#!/usr/bin/python

# coding=utf8
# description     : count number of missing values  
# author          : Shiu-Tang Li
# last update     : 08/04/2017
# version         : 0.2
# python_version  : 3.5.2

import pandas as pd
import numpy as np
    
def structure(df, with_stat = False):
    
    # Input:
    # df:                target dataframe
    # with_stat:         an option that allows you to include additional statistics for numeric features
    
    # Output:            a dataframe that contains the following columns:
    #                        1. column_name:  column names of the original dataframe
    #                        2. type:  data types for each column (numeric data with NAs are set to float64)
    #                        3. num_of_non-NAs:  number of non-missing values in each column  
    #                        4. num_of_NAs:  number of missing values in each column  
    #                        5. num_of_unique_values:   number of unique values in each column. missing value 
    #                                                   is counted as a unique value
    #                    if with_stat = True, max, min, mean, std, 25%, 50%, 75% percentiles will be included,
    #                        and all missing values will be ignored when calculating statistics 
    
    missing_values = [df.isnull().sum(axis=0)[column] for column in df.columns] 
    output_df =  pd.DataFrame({'column_name':df.columns, 
                               'type': df.dtypes.values,
                               'num_of_NAs': missing_values},
                                index = np.arange(len(df.columns)))
    output_df['num_of_unique_values'] = output_df.column_name.apply(lambda x: len(df[x].unique()))
    output_df['num_of_non-NAs'] = df.shape[0] - output_df['num_of_NAs']
    output_df['num_of_zeros'] = output_df.column_name.apply(lambda x: sum(df[x] == 0))
    
    if with_stat:
        statistics = df.describe().T
        statistics['column_name'] = statistics.index
        del statistics['count'] 
        output_df = output_df.join(statistics.set_index("column_name"), on = "column_name")
    
        return output_df[['column_name', 
                          'type', 
                          'num_of_non-NAs', 
                          'num_of_NAs', 
                          'num_of_unique_values', 
                          'num_of_zeros',
                          'min', '25%', '50%', '75%', 'max','mean','std']]
    
    else:
         return output_df[['column_name', 
                          'type', 
                          'num_of_non-NAs', 
                          'num_of_NAs', 
                          'num_of_unique_values',
                          'num_of_zeros']]