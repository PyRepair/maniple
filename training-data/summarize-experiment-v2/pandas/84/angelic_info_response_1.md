clocs = ([('A', 'a'), 0]
d = 
   d  e
0  1  2
1  1  2
2  1  2
3  1  2
4  1  2
5  1  2
6  1  2
7  1  2
data.index = MultiIndex
data.columns = Index

# Expected variables right before the buggy function's return
clocs = [0, 1]
index = MultiIndex
rlocs = [2]
index.nlevels = 3
clevels = [Index, Int64Index]
index.levels = FrozenList
ccodes = [array, array]
index.codes = FrozenList
cnames = [('A', 'a'), 'B']
index.names= FrozenList
rlevels = [Int64Index]
rcodes = [array]
rnames = ['C']
shape = [2, 2]
group_index = array
comp_ids = array
obs_ids = array
recons_codes = [array, array]
dummy_index = MultiIndex
dummy = DataFrame
dummy.index = MultiIndex
unstacked = DataFrame
new_levels = [Index, Index, Int64Index]
new_names = [None, ('A', 'a'), 'B']
new_codes = [array, array, array]
unstcols = MultiIndex
unstacked.index = Int64Index
unstacked.columns = MultiIndex
unstcols.levels = FrozenList
unstcols.codes = FrozenList
rec = array
new_columns = MultiIndex