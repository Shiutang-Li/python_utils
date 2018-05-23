
```python
duplicate_columns(df) 
```

Input:
* df: target dataframe

Output:
* list of lists, each sublist is a group of columns with the same value (any column which doesn't repeat with other columns is not included) 

Example:    

df =   
![](imgs/gpby-1.png)   

Peforming 'mean' aggregation. Missing values will be ignored except when aggr function = 'list'. 
![](imgs/gpby-2.png)  

if join = True, then the resulting dataframe will be joined back to the original dataframe. 
![](imgs/gpby-3.png)  

by setting up value list, groups are split based on it. Missing values and Values outside of the range specified by value list will go to 'others' group.  Also, if no value exist in a group, that group will not be displayed.  
![](imgs/gpby-4.png)  
