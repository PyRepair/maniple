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