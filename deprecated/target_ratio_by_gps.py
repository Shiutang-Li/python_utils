#!/usr/bin/python
# -*- coding:utf-8 -*-

# description     : calculate terget column ratio
# author          : Shiu-Tang Li
# last update     : 03/19/2018
# python_version  : 3.5.2

import pandas as pd
import numpy as np
    
def division(a, b, precision):
    if b == 0:
        return 0
    else:
        return round((a*1.0) / b,  precision)
    
def target_ratio_by_gps(df, target_column, target_value, gp_column, value_list, mode, precision):
    
    # Input:
    # df:                target dataframe
    # target column:     the key column we'd like to investigate the ratio
    # target_value:      the value in the key column we're interested
    # gp_column:         the ratio of the target column is calculated for each group, group by 'gp_column'
    # mode:              1: group by the values of 'gp_column', values given in 'value_list'
    #                    2: group by the value range of of 'gp_column', values given in 'value_list'
    # value_list:        used to group the values in 'gp_column'
    # Output:            dataframe, showing statistics
    # Example:
    
    list_gps = []
    list_target_value_count = []
    list_count = []
    list_target_value_ratio = []

    if mode == 1:
        for i in range(0, len(value_list)):
            list_gps.append(value_list[i])
            cnt_taget_value = df[(df[target_column] == target_value) & (df[gp_column] == value_list[i])].shape[0]
            cnt = df[df[gp_column] == value_list[i]].shape[0]

            list_target_value_count.append(cnt_taget_value)
            list_count.append(cnt)
            list_target_value_ratio.append(division(cnt_taget_value, cnt, precision))

        return pd.DataFrame({gp_column : list_gps,
                            'target_count': list_target_value_count,
                            'count': list_count,
                            'ratio': list_target_value_ratio
                            })[[gp_column,'target_count','count','ratio']]
    elif mode == 2:
        for i in range(0, len(value_list)-1):
            list_gps.append(str(value_list[i])+' ≤ x < '+ str(value_list[i+1]))
            cnt_taget_value = df[(df[target_column] == target_value)
                                 & (df[gp_column] >= value_list[i])
                                 & (df[gp_column] < value_list[i+1])].shape[0]
            cnt = df[(df[gp_column] >= value_list[i])
                     & (df[gp_column] < value_list[i+1])].shape[0]
    
            list_target_value_count.append(cnt_taget_value)
            list_count.append(cnt);
            list_target_value_ratio.append(division(cnt_taget_value, cnt, precision))
        
        return pd.DataFrame({gp_column + ': x': list_gps,
                             'target_count': list_target_value_count,
                             'count': list_count,
                             'ratio': list_target_value_ratio
                            })[[gp_column + ': x','target_count','count','ratio']]
    
    else:
        print('invalid value for mode')
        return None
    
