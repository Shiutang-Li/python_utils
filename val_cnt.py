#!/usr/bin/python
# -*- coding:utf-8 -*-

# description     : enhanced value_counts(), including cumulated sum and percentage in the output dataframe
# author          : Shiu-Tang Li
# last update     : 5/22/2018

import pandas as pd
import numpy as np

def val_cnt(value_list, details = True, var_name='value', order='asc', precision=3):
   
    # Input:
    # value_list:        The target list / np.array / pandas series that we would like to see distribution. 
    #                    If the input type is not pd.Series, type transfermation will be performed.  
    # details:           If False, then only the 'count' stats is displayed  
    # var_name:          User defined variable name
    # order:             Whether we'd like to see the stats in asc or desc order 
    # precision:         Number of digits to be displayed when calculating for percentages
    
    # Output:            distribution stats dataframe
   
   if isinstance(value_list, pd.Series) == False:
      value_list = pd.Series(value_list)

   num_records = len(value_list)
   stats = value_list.value_counts()
   table = pd.DataFrame({var_name: stats.index, 'cnt':stats.values})
   
   if details = False:
      return table
   
   if order == 'asc':
       table.sort_values(by = var_name, inplace = True)
   elif order == 'desc':
       table.sort_values(by = var_name, ascending = False, inplace = True)
   else:
       print('argument error for "order"')
       return table
   
   table['cum_cnt'] = table['cnt'].cumsum()
   table['percentage'] = table.apply(
       lambda x: round(x['cnt']*100.0 / num_records, precision), axis=1)
   table['cum_percentage'] = table.apply(
       lambda x: round(x['cum_cnt']*100.0 / num_records, precision), axis=1)
   table.reset_index(inplace = True)
   
   return table 
   
