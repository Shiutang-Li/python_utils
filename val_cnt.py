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
   
   if order == 'asc':
       table.sort_values(by = var_name, inplace = True)
   elif order == 'desc':
       table.sort_values(by = var_name, ascending = False, inplace = True)
   else:
       print('Argument error for "order". "desc" will be used.')
       table.sort_values(by = var_name, ascending = False, inplace = True)
      
   if details = False:
      return table
   
   table['cum_cnt'] = table['cnt'].cumsum()
   table['percentage'] = table.apply(
       lambda x: round(x['cnt']*100.0 / num_records, precision), axis=1)
   table['cum_percentage'] = table.apply(
       lambda x: round(x['cum_cnt']*100.0 / num_records, precision), axis=1)
   table.reset_index(inplace = True)
   
   return table 
   
def position_to_range_val_cnt(i, range_list):
    if i == 0:
        return 'x < ' + str(range_list[i])
    elif i > 0 and i < len(range_list):
        return str(range_list[i-1]) + ' ≤ x < ' + str(range_list[i])
    else:
        return 'others'
   
def val_cnt_range(value_list, range_list, details = True, var_name='value', order='asc', precision=3):
   
    # Input:
    # value_list:        The target list / np.array / pandas series that we would like to see distribution. 
    #                    If the input type is not pd.Series, type transfermation will be performed. 
    # range_list:        The list where the range of each group is based on. Will be sorted in ascending order
    # details:           If False, then only the 'count' stats is displayed  
    # var_name:          User defined variable name
    # order:             Whether we'd like to see the stats in asc or desc order 
    # precision:         Number of digits to be displayed when calculating for percentages
    
    # Output:            distribution stats dataframe
   
   if isinstance(value_list, pd.Series) == False:
      value_list = pd.Series(value_list)

   num_records = len(value_list)
   stats = value_list.value_counts()
   table = pd.DataFrame({var_name + ' :x': stats.index, 'cnt':stats.values})
   table['group_ID'] = table.apply(lambda x: bisect_right(range_list, x[var_name + ' :x']), axis = 1)
   
   if order == 'asc':
       table.sort_values(by = 'group_ID', inplace = True)
   elif order == 'desc':
       table.sort_values(by = 'group_ID', ascending = False, inplace = True)
   else:
       print('Argument error for "order". "desc" will be used.')
       table.sort_values(by = 'group_ID', ascending = False, inplace = True)
   
   table[var_name + ': x'] = table.apply(lambda x: position_to_range_val_cnt(int(x['group_ID']), range_list), axis = 1)
   del table['groupID']
   
   if details = False:
      return table
   
   table['cum_cnt'] = table['cnt'].cumsum()
   table['percentage'] = table.apply(
       lambda x: round(x['cnt']*100.0 / num_records, precision), axis=1)
   table['cum_percentage'] = table.apply(
       lambda x: round(x['cum_cnt']*100.0 / num_records, precision), axis=1)
   table.reset_index(inplace = True)
   
   return table 
