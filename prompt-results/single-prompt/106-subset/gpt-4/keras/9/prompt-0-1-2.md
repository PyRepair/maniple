You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

def process_list_block(docstring, starting_point, section_end,
                       leading_spaces, marker):
    ending_point = docstring.find('\n\n', starting_point)
    block = docstring[starting_point:(None if ending_point == -1 else
                                      ending_point - 1)]
    # Place marker for later reinjection.
    docstring_slice = docstring[starting_point:section_end].replace(block, marker)
    docstring = (docstring[:starting_point]
                 + docstring_slice
                 + docstring[section_end:])
    lines = block.split('\n')
    # Remove the computed number of leading white spaces from each line.
    lines = [re.sub('^' + ' ' * leading_spaces, '', line) for line in lines]
    # Usually lines have at least 4 additional leading spaces.
    # These have to be removed, but first the list roots have to be detected.
    top_level_regex = r'^    ([^\s\\\(]+):(.*)'
    top_level_replacement = r'- __\1__:\2'
    lines = [re.sub(top_level_regex, top_level_replacement, line) for line in lines]
    # All the other lines get simply the 4 leading space (if present) removed
    lines = [re.sub(r'^    ', '', line) for line in lines]
    # Fix text lines after lists
    indent = 0
    text_block = False
    for i in range(len(lines)):
        line = lines[i]
        spaces = re.search(r'\S', line)
        if spaces:
            # If it is a list element
            if line[spaces.start()] == '-':
                indent = spaces.start() + 1
                if text_block:
                    text_block = False
                    lines[i] = '\n' + line
            elif spaces.start() < indent:
                text_block = True
                indent = spaces.start()
                lines[i] = '\n' + line
        else:
            text_block = False
            indent = 0
    block = '\n'.join(lines)
    return docstring, block



The test error on command line is following:

=================================================== test session starts ===================================================
platform darwin -- Python 3.7.9, pytest-5.4.3, py-1.8.1, pluggy-0.13.1 -- /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:9/venv/bin/python3.7
cachedir: .pytest_cache
rootdir: /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:9, inifile: pytest.ini
plugins: timeout-2.1.0, cov-4.1.0, mock-3.11.1, flaky-3.6.1, forked-1.1.3, xdist-1.32.0
timeout: 60.0s
timeout method: signal
timeout func_only: False
[gw0] darwin Python 3.7.9 cwd: /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:9
[gw1] darwin Python 3.7.9 cwd: /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:9
[gw0] Python 3.7.9 (v3.7.9:13c94747c7, Aug 15 2020, 01:31:08)  -- [Clang 6.0 (clang-600.0.57)]
[gw1] Python 3.7.9 (v3.7.9:13c94747c7, Aug 15 2020, 01:31:08)  -- [Clang 6.0 (clang-600.0.57)]
gw0 [1] / gw1 [1]
scheduling tests via LoadScheduling

tests/test_doc_auto_generation.py::test_doc_lists[docs_descriptor1] 
[gw0] [100%] FAILED tests/test_doc_auto_generation.py::test_doc_lists[docs_descriptor1] 

======================================================== FAILURES =========================================================
____________________________________________ test_doc_lists[docs_descriptor1] _____________________________________________
[gw0] darwin -- Python 3.7.9 /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:9/venv/bin/python3.7

docs_descriptor = {'doc': 'Base class for recurrent layers.\n\n    # Arguments\n        return_sequences: Boolean. Whether to return the...r the full sequence.\n- __return_state__: Boolean. Whether to return the last state\n    in addition to the output.\n'}

    @pytest.mark.parametrize('docs_descriptor', [
        test_doc1,
        test_doc_with_arguments_as_last_block,
    ])
    def test_doc_lists(docs_descriptor):
        docstring = autogen.process_docstring(docs_descriptor['doc'])
>       assert markdown(docstring) == markdown(docs_descriptor['result'])
E       AssertionError: assert '<p>Base clas...e output.</p>' == '<p>Base clas....</li>\n</ul>'
E           <p>Base class for recurrent layers.</p>
E           <p><strong>Arguments</strong></p>
E         - <ul>
E         - <li><strong>return_sequences</strong>: Boolean. Whether to return the last output
E         ?  ^^^^^^^^^^                 ---------
E         + <p>return_sequences: Boolean. Whether to return the last output
E         ?  ^...
E         
E         ...Full output truncated (12 lines hidden), use '-vv' to show

tests/test_doc_auto_generation.py:355: AssertionError
------------------------------------------------ Captured stderr teardown -------------------------------------------------
WARNING:tensorflow:From /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:9/keras/backend/tensorflow_backend.py:95: The name tf.reset_default_graph is deprecated. Please use tf.compat.v1.reset_default_graph instead.

WARNING:tensorflow:From /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:9/keras/backend/tensorflow_backend.py:98: The name tf.placeholder_with_default is deprecated. Please use tf.compat.v1.placeholder_with_default instead.

WARNING:tensorflow:From /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:9/keras/backend/tensorflow_backend.py:102: The name tf.get_default_graph is deprecated. Please use tf.compat.v1.get_default_graph instead.

-------------------------------------------------- Captured log teardown --------------------------------------------------
WARNING  tensorflow:module_wrapper.py:139 From /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:9/keras/backend/tensorflow_backend.py:95: The name tf.reset_default_graph is deprecated. Please use tf.compat.v1.reset_default_graph instead.

WARNING  tensorflow:module_wrapper.py:139 From /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:9/keras/backend/tensorflow_backend.py:98: The name tf.placeholder_with_default is deprecated. Please use tf.compat.v1.placeholder_with_default instead.

WARNING  tensorflow:module_wrapper.py:139 From /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:9/keras/backend/tensorflow_backend.py:102: The name tf.get_default_graph is deprecated. Please use tf.compat.v1.get_default_graph instead.
==================================================== warnings summary =====================================================
venv/lib/python3.7/site-packages/tensorflow_core/contrib/learn/python/learn/learn_io/generator_io.py:26
  /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:9/venv/lib/python3.7/site-packages/tensorflow_core/contrib/learn/python/learn/learn_io/generator_io.py:26: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated since Python 3.3,and in 3.9 it will stop working
    from collections import Container

-- Docs: https://docs.pytest.org/en/latest/warnings.html
================================================ slowest 20 test durations ================================================
0.01s call     tests/test_doc_auto_generation.py::test_doc_lists[docs_descriptor1]

(0.00 durations hidden.  Use -vv to show these durations.)
================================================= short test summary info =================================================
FAILED tests/test_doc_auto_generation.py::test_doc_lists[docs_descriptor1] - AssertionError: assert '<p>Base clas...e ou...
============================================== 1 failed, 1 warning in 6.29s ===============================================
Using TensorFlow backend.



The test source code is following:


test_doc_with_arguments_as_last_block = {
    'doc': """Base class for recurrent layers.
    # Arguments
        return_sequences: Boolean. Whether to return the last output
            in the output sequence, or the full sequence.
        return_state: Boolean. Whether to return the last state
            in addition to the output.
    """,
    'result': '''Base class for recurrent layers.
__Arguments__
- __return_sequences__: Boolean. Whether to return the last output
    in the output sequence, or the full sequence.
- __return_state__: Boolean. Whether to return the last state
    in addition to the output.
'''}


@pytest.mark.parametrize('docs_descriptor', [
    test_doc1,
    test_doc_with_arguments_as_last_block,
])
def test_doc_lists(docs_descriptor):
    docstring = autogen.process_docstring(docs_descriptor['doc'])
    assert markdown(docstring) == markdown(docs_descriptor['result'])



The raised issue description for this bug is:
Callbacks documentation not showing bullet points correctly

The current documentation on callbacks isn't showing bullet points correctly under the "Arguments" section of a few models. Here's the example for ModelCheckpoint:

filepath: string, path to save the model file. monitor: quantity to monitor. verbose: verbosity mode, 0 or 1. save_best_only: if save_best_only=True, the latest best model according to the quantity monitored will not be overwritten. mode: one of {auto, min, max}. If save_best_only=True, the decision to overwrite the current save file is made based on either the maximization or the minimization of the monitored quantity. For val_acc, this should be max, for val_loss this should be min, etc. In auto mode, the direction is automatically inferred from the name of the monitored quantity. save_weights_only: if True, then only the model's weights will be saved (model.save_weights(filepath)), else the full model is saved (model.save(filepath)). period: Interval (number of epochs) between checkpoints.

Looking at the source code, the docstring seems to be organized correctly:
keras/keras/callbacks.py

Lines 371 to 390 in dc9e510

     # Arguments 
         filepath: string, path to save the model file. 
         monitor: quantity to monitor. 
         verbose: verbosity mode, 0 or 1. 
         save_best_only: if `save_best_only=True`, 
             the latest best model according to 
             the quantity monitored will not be overwritten. 
         mode: one of {auto, min, max}. 
             If `save_best_only=True`, the decision 
             to overwrite the current save file is made 
             based on either the maximization or the 
             minimization of the monitored quantity. For `val_acc`, 
             this should be `max`, for `val_loss` this should 
             be `min`, etc. In `auto` mode, the direction is 
             automatically inferred from the name of the monitored quantity. 
         save_weights_only: if True, then only the model's weights will be 
             saved (`model.save_weights(filepath)`), else the full model 
             is saved (`model.save(filepath)`). 
         period: Interval (number of epochs) between checkpoints. 
     """ 
It is however showing up correctly for other models, e.g. ProgbarLogger:

Arguments
count_mode: One of "steps" or "samples". Whether the progress bar should count samples seen or steps (batches) seen.
stateful_metrics: Iterable of string names of metrics that should not be averaged over an epoch. Metrics in this list will be logged as-is. All others will be averaged over time (e.g. loss, etc).
The raised issue description for this bug is:
EarlyStopping documentation with wrong format

EarlyStopping documentation has the wrong format. See here:
https://keras.io/callbacks/#earlystopping

The Arguments section is bugged.