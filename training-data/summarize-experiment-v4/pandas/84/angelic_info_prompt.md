Your task is to summarize the expected input and output values of a buggy function, following the example provided below.

## Example source code of the buggy function
```python
def calculate_total_cost(nights, rate_per_night):
    discount = 0.1  # 10% discount for stays longer than 7 nights
    if nights > 7:
        total_cost = nights * rate_per_night * (1 - discount)
    else:
        total_cost = nights * rate_per_night
    return total_cost
```

## Example expected value and type of variables during the failing test execution

### Expected case 1
#### Input parameter value and type
nights, value: `8`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `790`, type: `int`

### Expected case 2
#### Input parameter value and type
nights, value: `9`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `880`, type: `int`

### Expected Case 3
#### Input parameter value and type
nights, value: `7`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `700`, type: `int`

### Exptected Case 4
#### Input parameter value and type
nights, value: `10`, type: `int`
rate_per_night, value: `100`, type: `int`
#### Expected value and type of variables right before the buggy function's return
total_cost, value: `970`, type: `int`


## Example summary:
Case 1: Given the input parameters `nights=8` and `rate_per_night=100`, the function should return `790`. This might be calculated by `7 * 100 + 100 * 0.9 = 790`.

Case2: Given the input parameters `nights=9` and `rate_per_night=100`, the function should return `880`. This might be calculated by `7 * 100 + 2 * 100 * 0.9 = 880`.

Case3: Given the input parameters `nights=7` and `rate_per_night=100`, the function should return `700`. This might be calculated by `7 * 100 = 700`.

Case4: Given the input parameters `nights=10` and `rate_per_night=100`, the function should return `970`. This might be calculated by `7 * 100 + 3 * 100 * 0.9 = 970`.



## The source code of the buggy function

```python
def _unstack_multiple(data, clocs, fill_value=None):
    if len(clocs) == 0:
        return data

    # NOTE: This doesn't deal with hierarchical columns yet

    index = data.index

    clocs = [index._get_level_number(i) for i in clocs]

    rlocs = [i for i in range(index.nlevels) if i not in clocs]

    clevels = [index.levels[i] for i in clocs]
    ccodes = [index.codes[i] for i in clocs]
    cnames = [index.names[i] for i in clocs]
    rlevels = [index.levels[i] for i in rlocs]
    rcodes = [index.codes[i] for i in rlocs]
    rnames = [index.names[i] for i in rlocs]

    shape = [len(x) for x in clevels]
    group_index = get_group_index(ccodes, shape, sort=False, xnull=False)

    comp_ids, obs_ids = compress_group_index(group_index, sort=False)
    recons_codes = decons_obs_group_ids(comp_ids, obs_ids, shape, ccodes, xnull=False)

    if rlocs == []:
        # Everything is in clocs, so the dummy df has a regular index
        dummy_index = Index(obs_ids, name="__placeholder__")
    else:
        dummy_index = MultiIndex(
            levels=rlevels + [obs_ids],
            codes=rcodes + [comp_ids],
            names=rnames + ["__placeholder__"],
            verify_integrity=False,
        )

    if isinstance(data, Series):
        dummy = data.copy()
        dummy.index = dummy_index

        unstacked = dummy.unstack("__placeholder__", fill_value=fill_value)
        new_levels = clevels
        new_names = cnames
        new_codes = recons_codes
    else:
        if isinstance(data.columns, MultiIndex):
            result = data
            for i in range(len(clocs)):
                val = clocs[i]
                result = result.unstack(val, fill_value=fill_value)
                clocs = [v if i > v else v - 1 for v in clocs]

            return result

        dummy = data.copy()
        dummy.index = dummy_index

        unstacked = dummy.unstack("__placeholder__", fill_value=fill_value)
        if isinstance(unstacked, Series):
            unstcols = unstacked.index
        else:
            unstcols = unstacked.columns
        new_levels = [unstcols.levels[0]] + clevels
        new_names = [data.columns.name] + cnames

        new_codes = [unstcols.codes[0]]
        for rec in recons_codes:
            new_codes.append(rec.take(unstcols.codes[-1]))

    new_columns = MultiIndex(
        levels=new_levels, codes=new_codes, names=new_names, verify_integrity=False
    )

    if isinstance(unstacked, Series):
        unstacked.index = new_columns
    else:
        unstacked.columns = new_columns

    return unstacked

```

## Expected values and types of variables during the failing test execution
Each case below includes input parameter values and types, and the expected values and types of relevant variables at the function's return. If an input parameter is not reflected in the output, it is assumed to remain unchanged. A corrected function must satisfy all these cases.

### Expected case 1
#### The values and types of buggy function's parameters
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

#### Expected values and types of variables right before the buggy function's return
clocs, expected value: `[0, 1]`, type: `list`

index, expected value: `MultiIndex([('a', 1, 3),
            ('a', 1, 4),
            ('a', 2, 3),
            ('a', 2, 4),
            ('b', 1, 3),
            ('b', 1, 4),
            ('b', 2, 3),
            ('b', 2, 4)],
           names=[('A', 'a'), 'B', 'C'])`, type: `MultiIndex`

rlocs, expected value: `[2]`, type: `list`

index.nlevels, expected value: `3`, type: `int`

clevels, expected value: `[Index(['a', 'b'], dtype='object', name=('A', 'a')), Int64Index([1, 2], dtype='int64', name='B')]`, type: `list`

index.levels, expected value: `FrozenList([['a', 'b'], [1, 2], [3, 4]])`, type: `FrozenList`

ccodes, expected value: `[array([0, 0, 0, 0, 1, 1, 1, 1], dtype=int8), array([0, 0, 1, 1, 0, 0, 1, 1], dtype=int8)]`, type: `list`

index.codes, expected value: `FrozenList([[0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 0, 0, 1, 1], [0, 1, 0, 1, 0, 1, 0, 1]])`, type: `FrozenList`

cnames, expected value: `[('A', 'a'), 'B']`, type: `list`

index.names, expected value: `FrozenList([('A', 'a'), 'B', 'C'])`, type: `FrozenList`

rlevels, expected value: `[Int64Index([3, 4], dtype='int64', name='C')]`, type: `list`

rcodes, expected value: `[array([0, 1, 0, 1, 0, 1, 0, 1], dtype=int8)]`, type: `list`

rnames, expected value: `['C']`, type: `list`

shape, expected value: `[2, 2]`, type: `list`

group_index, expected value: `array([0, 0, 1, 1, 2, 2, 3, 3])`, type: `ndarray`

comp_ids, expected value: `array([0, 0, 1, 1, 2, 2, 3, 3])`, type: `ndarray`

obs_ids, expected value: `array([0, 1, 2, 3])`, type: `ndarray`

recons_codes, expected value: `[array([0, 0, 1, 1]), array([0, 1, 0, 1])]`, type: `list`

dummy_index, expected value: `MultiIndex([(3, 0),
            (4, 0),
            (3, 1),
            (4, 1),
            (3, 2),
            (4, 2),
            (3, 3),
            (4, 3)],
           names=['C', '__placeholder__'])`, type: `MultiIndex`

dummy, expected value: `                   d  e
C __placeholder__      
3 0                1  2
4 0                1  2
3 1                1  2
4 1                1  2
3 2                1  2
4 2                1  2
3 3                1  2
4 3                1  2`, type: `DataFrame`

dummy.index, expected value: `MultiIndex([(3, 0),
            (4, 0),
            (3, 1),
            (4, 1),
            (3, 2),
            (4, 2),
            (3, 3),
            (4, 3)],
           names=['C', '__placeholder__'])`, type: `MultiIndex`

unstacked, expected value: `            d           e         
('A', 'a')  a     b     a     b   
B           1  2  1  2  1  2  1  2
C                                 
3           1  1  1  1  2  2  2  2
4           1  1  1  1  2  2  2  2`, type: `DataFrame`

new_levels, expected value: `[Index(['d', 'e'], dtype='object'), Index(['a', 'b'], dtype='object', name=('A', 'a')), Int64Index([1, 2], dtype='int64', name='B')]`, type: `list`

new_names, expected value: `[None, ('A', 'a'), 'B']`, type: `list`

new_codes, expected value: `[array([0, 0, 0, 0, 1, 1, 1, 1], dtype=int8), array([0, 0, 1, 1, 0, 0, 1, 1]), array([0, 1, 0, 1, 0, 1, 0, 1])]`, type: `list`

unstcols, expected value: `MultiIndex([('d', 0),
            ('d', 1),
            ('d', 2),
            ('d', 3),
            ('e', 0),
            ('e', 1),
            ('e', 2),
            ('e', 3)],
           names=[None, '__placeholder__'])`, type: `MultiIndex`

unstacked.index, expected value: `Int64Index([3, 4], dtype='int64', name='C')`, type: `Int64Index`

unstacked.columns, expected value: `MultiIndex([('d', 'a', 1),
            ('d', 'a', 2),
            ('d', 'b', 1),
            ('d', 'b', 2),
            ('e', 'a', 1),
            ('e', 'a', 2),
            ('e', 'b', 1),
            ('e', 'b', 2)],
           names=[None, ('A', 'a'), 'B'])`, type: `MultiIndex`

unstcols.levels, expected value: `FrozenList([['d', 'e'], [0, 1, 2, 3]])`, type: `FrozenList`

unstcols.codes, expected value: `FrozenList([[0, 0, 0, 0, 1, 1, 1, 1], [0, 1, 2, 3, 0, 1, 2, 3]])`, type: `FrozenList`

rec, expected value: `array([0, 1, 0, 1])`, type: `ndarray`

new_columns, expected value: `MultiIndex([('d', 'a', 1),
            ('d', 'a', 2),
            ('d', 'b', 1),
            ('d', 'b', 2),
            ('e', 'a', 1),
            ('e', 'a', 2),
            ('e', 'b', 1),
            ('e', 'b', 2)],
           names=[None, ('A', 'a'), 'B'])`, type: `MultiIndex`

## Summary:

[Your summary here.]