Case 1
Input: 
columns: (1, 2)
aggfunc: 'mean'
data: 1  2  v
        0  1  1  4
        1  2  2  5
        2  3  3  6
values: 'v'
margins: False
dropna: True
margins_name: 'All'
observed: False

Output: 
columns: [1, 2]
table: 1  1  2  3
        2  1  2  3
        v  4  5  6

Case 2
Input: 
columns: ('a', 'b')
aggfunc: 'mean'
data: a  b  v
        0  1  1  4
        1  2  2  5
        2  3  3  6
values: 'v'
margins: False
dropna: True
margins_name: 'All'
observed: False

Output:
columns: ['a', 'b']
table: a  1  2  3
        b  1  2  3
        v  4  5  6

Case 3
Input: 
columns: (1, 'b')
aggfunc: 'mean'
data: 1  b  v
        0  1  1  4
        1  2  2  5
        2  3  3  6
values: 'v'
margins: False
dropna: True
margins_name: 'All'
observed: False

Output:
columns: [1, 'b']
table: 1  1  2  3
        b  1  2  3
        v  4  5  6

Case 4
Input: 
columns: ('a', 1)
aggfunc: 'mean'
data: a  1  v
        0  1  1  4
        1  2  2  5
        2  3  3  6
values: 'v'
margins: False
dropna: True
margins_name: 'All'
observed: False

Output:
columns: ['a', 1]
table: a  1  2  3
        1  1  2  3
        v  4  5  6