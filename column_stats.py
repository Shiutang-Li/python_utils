#!/usr/bin/python
# -*- coding:utf-8 -*-

# description     : enhanced value_counts(), including cumulated sum and percentage in the output dataframe
# author          : Shiu-Tang Li
# last update     : 05/01/2018

def column_stats(df, column, order='asc', precision=3):
   
   num_records = df.shape[0]
   table = pd.DataFrame(df[column].value_counts())
   table.columns = ['cnt']
   table['value'] = table.index
   
   if order == 'asc':
       table.sort_values(by = 'value', inplace = True)
   elif order == 'desc':
       table.sort_values(by = 'value', ascending = False, inplace = True)
   else:
       print('argument error for "order"')
       return None
   
   table['cum_cnt'] = table['cnt'].cumsum()
   table['percentage'] = table.apply(
       lambda x: round(x['cnt']*100.0 / num_records, precision), axis=1)
   table['cum_percentage'] = table.apply(
       lambda x: round(x['cum_cnt']*100.0 / num_records, precision), axis=1)
   table.reset_index(inplace = True)
   
   return table[['value', 'cnt',  'cum_cnt', 'percentage', 'cum_percentage']]
   
