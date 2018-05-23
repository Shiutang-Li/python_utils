#!/usr/bin/python
# -*- coding:utf-8 -*-

# description     : enhanced value_counts(), including cumulated sum and percentage in the output dataframe
# author          : Shiu-Tang Li
# last update     : 05/22/2018

import pandas as pd
import numpy as np

def var_dist(value_list, var_name, order='asc', precision=3):
   
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
       print('argument error for "order"')
       return None
   
   table['cum_cnt'] = table['cnt'].cumsum()
   table['percentage'] = table.apply(
       lambda x: round(x['cnt']*100.0 / num_records, precision), axis=1)
   table['cum_percentage'] = table.apply(
       lambda x: round(x['cum_cnt']*100.0 / num_records, precision), axis=1)
   table.reset_index(inplace = True)
   
   return table 
   
