## Expected case 1
### Input parameter value and type
clocs, value: `(('A', 'a'), 'B')`, type: `tuple`

data, value: `            d  e
(A, a) B C      
a      1 3  1  2
         4  1  2
       2 3  1  2
         4  1  2
b      1 3  1  2
         4  1  2
       2 3  1  2
         4  1  2`, type: `DataFrame`

data.index, value: `MultiIndex([('a', 1, 3),
            ('a', 1, 4),
            ('a', 2, 3),
            ('a', 2, 4),
            ('b', 1, 3),
            ('b', 1, 4),
            ('b', 2, 3),
            ('b', 2, 4)],
           names=[('A', 'a'), 'B', 'C'])`, type: `MultiIndex`

data.columns, value: `Index(['d', 'e'], dtype='object')`, type: `Index`

### Expected value and type of variables right before the buggy function's return
clocs, expected value: `[0, 1]`, type: `list`

index.nlevels, expected value: `3`, type: `int`

clevels, expected value: `[Index(['a', 'b'], dtype='object', name=('A', 'a')), Int64Index([1, 2], dtype='int64', name='B')]`, type: `list`

ccodes, expected value: `[array([0, 0, 0, 0, 1, 1, 1, 1], dtype=int8), array([0, 0, 1, 1, 0, 0, 1, 1], dtype=int8)]`, type: `list`

rlevels, expected value: `[Int64Index([3, 4], dtype='int64', name='C')]`, type: `list`

rcodes, expected value: `[array([0, 1, 0, 1, 0, 1, 0, 1], dtype=int8)]`, type: `list`

shape, expected value: `[2, 2]`, type: `list`

unstacked, expected value: `            d           e         
('A', 'a')  a     b     a     b   
B           1  2  1  2  1  2  1  2
C                                 
3           1  1  1  1  2  2  2  2
4           1  1  1  1  2  2  2  2`, type: `DataFrame`

unstacked.columns, expected value: `MultiIndex([('d', 'a', 1),
            ('d', 'a', 2),
            ('d', 'b', 1),
            ('d', 'b', 2),
            ('e', 'a', 1),
            ('e', 'a', 2),
            ('e', 'b', 1),
            ('e', 'b', 2)],
           names=[None, ('A', 'a'), 'B'])`, type: `MultiIndex`