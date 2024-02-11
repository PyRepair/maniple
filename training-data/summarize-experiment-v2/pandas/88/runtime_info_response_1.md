Input:
columns: (1, 2)
aggfunc: 'mean'
data:  
   1  2  v
0  1  1  4
1  2  2  5
2  3  3  6
values: 'v'
margins: False
dropna: True
margins_name: 'All'
observed: False

Output:
index: []
columns: [1, 2]
keys: [1, 2]
table: 
     v
1 2   
1 1  4
2 2  5
3 3  6
values: ['v']
values_passed: True
values_multi: False
i: 'v'
to_filter: [1, 2, 'v']
x: 'v'
agged: 
     v
1 2   
1 1  4
2 2  5
3 3  6
agged.columns: Index(['v'], dtype='object')
v: 'v'
table.index: Index(['v'], dtype='object')
agged.index: MultiIndex([(1, 1),
            (2, 2),
            (3, 3)],
           names=[1, 2])
table.columns: MultiIndex([(1, 1),
            (2, 2),
            (3, 3)],
           names=[1, 2])
table.empty: False
table.T: 
     v
1 2   
1 1  4
2 2  5
3 3  6