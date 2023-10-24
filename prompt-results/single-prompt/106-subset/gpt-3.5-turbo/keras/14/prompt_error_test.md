You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

def sparse_top_k_categorical_accuracy(y_true, y_pred, k=5):
    return K.mean(K.in_top_k(y_pred, K.cast(K.max(y_true, axis=-1), 'int32'), k),
                  axis=-1)



The test error on command line is following:

=================================================== test session starts ===================================================
platform darwin -- Python 3.7.9, pytest-5.4.3, py-1.8.1, pluggy-0.13.1 -- /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:14/venv/bin/python3.7
cachedir: .pytest_cache
rootdir: /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:14, inifile: pytest.ini
plugins: timeout-2.1.0, cov-4.1.0, mock-3.11.1, flaky-3.6.1, forked-1.1.3, xdist-1.32.0
timeout: 60.0s
timeout method: signal
timeout func_only: False
[gw0] darwin Python 3.7.9 cwd: /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:14
[gw1] darwin Python 3.7.9 cwd: /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:14
[gw0] Python 3.7.9 (v3.7.9:13c94747c7, Aug 15 2020, 01:31:08)  -- [Clang 6.0 (clang-600.0.57)]
[gw1] Python 3.7.9 (v3.7.9:13c94747c7, Aug 15 2020, 01:31:08)  -- [Clang 6.0 (clang-600.0.57)]
gw0 [1] / gw1 [1]
scheduling tests via LoadScheduling

tests/keras/metrics_test.py::test_sparse_top_k_categorical_accuracy[y_pred1-y_true1] 
[gw0] [100%] FAILED tests/keras/metrics_test.py::test_sparse_top_k_categorical_accuracy[y_pred1-y_true1] 

======================================================== FAILURES =========================================================
_________________________________ test_sparse_top_k_categorical_accuracy[y_pred1-y_true1] _________________________________
[gw0] darwin -- Python 3.7.9 /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:14/venv/bin/python3.7

graph = <tensorflow.python.framework.ops.Graph object at 0x7fc42f2b1650>
node_def = name: "in_top_k/InTopKV2"
op: "InTopKV2"
attr {
  key: "T"
  value {
    type: DT_INT32
  }
}

inputs = [<tf.Tensor 'Variable/read:0' shape=(2, 3) dtype=float32>, <tf.Tensor 'Cast:0' shape=() dtype=int32>, <tf.Tensor 'in_top_k/InTopKV2/k:0' shape=() dtype=int32>]
control_inputs = []

    def _create_c_op(graph, node_def, inputs, control_inputs):
      """Creates a TF_Operation.
    
      Args:
        graph: a `Graph`.
        node_def: `node_def_pb2.NodeDef` for the operation to create.
        inputs: A list of `Tensor`s (corresponding to scalar inputs) and lists of
          `Tensor`s (corresponding to sequence inputs, e.g. "int64 * N",
          "list(int64)"). The length of the list should be equal to the number of
          inputs specified by this operation's op def.
        control_inputs: A list of `Operation`s to set as control dependencies.
    
      Returns:
        A wrapped TF_Operation*.
      """
      # pylint: disable=protected-access
      op_desc = c_api.TF_NewOperation(graph._c_graph, compat.as_str(node_def.op),
                                      compat.as_str(node_def.name))
      if node_def.device:
        c_api.TF_SetDevice(op_desc, compat.as_str(node_def.device))
      # Add inputs
      for op_input in inputs:
        if isinstance(op_input, (list, tuple)):
          c_api.TF_AddInputList(op_desc, [t._as_tf_output() for t in op_input])
        else:
          c_api.TF_AddInput(op_desc, op_input._as_tf_output())
    
      # Add control inputs
      for control_input in control_inputs:
        c_api.TF_AddControlInput(op_desc, control_input._c_op)
      # pylint: enable=protected-access
    
      # Add attrs
      for name, attr_value in node_def.attr.items():
        serialized = attr_value.SerializeToString()
        # TODO(skyewm): this creates and deletes a new TF_Status for every attr.
        # It might be worth creating a convenient way to re-use the same status.
        c_api.TF_SetAttrValueProto(op_desc, compat.as_str(name), serialized)
    
      try:
>       c_op = c_api.TF_FinishOperation(op_desc)
E       tensorflow.python.framework.errors_impl.InvalidArgumentError: Shape must be rank 1 but is rank 0 for 'in_top_k/InTopKV2' (op: 'InTopKV2') with input shapes: [2,3], [], [].

venv/lib/python3.7/site-packages/tensorflow_core/python/framework/ops.py:1607: InvalidArgumentError

During handling of the above exception, another exception occurred:

y_pred = <tf.Variable 'Variable:0' shape=(2, 3) dtype=float32_ref>
y_true = <tf.Variable 'Variable_1:0' shape=(2,) dtype=float32_ref>

    @pytest.mark.skipif((K.backend() == 'cntk'),
                        reason='CNTK backend does not support top_k yet')
    @pytest.mark.parametrize('y_pred, y_true', [
        # Test correctness if the shape of y_true is (num_samples, 1)
        (np.array([[0.3, 0.2, 0.1], [0.1, 0.2, 0.7]]), np.array([[1], [0]])),
        # Test correctness if the shape of y_true is (num_samples,)
        (np.array([[0.3, 0.2, 0.1], [0.1, 0.2, 0.7]]), np.array([1, 0])),
    ])
    def test_sparse_top_k_categorical_accuracy(y_pred, y_true):
        y_pred = K.variable(y_pred)
        y_true = K.variable(y_true)
        success_result = K.eval(
>           metrics.sparse_top_k_categorical_accuracy(y_true, y_pred, k=3))

tests/keras/metrics_test.py:109: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
keras/metrics.py:48: in sparse_top_k_categorical_accuracy
    return K.mean(K.in_top_k(y_pred, K.cast(K.max(y_true, axis=-1), 'int32'), k),
keras/backend/tensorflow_backend.py:3446: in in_top_k
    return tf.nn.in_top_k(predictions, targets, k)
venv/lib/python3.7/site-packages/tensorflow_core/python/ops/nn_ops.py:4843: in in_top_k
    return gen_nn_ops.in_top_kv2(predictions, targets, k, name=name)
venv/lib/python3.7/site-packages/tensorflow_core/python/ops/gen_nn_ops.py:5042: in in_top_kv2
    "InTopKV2", predictions=predictions, targets=targets, k=k, name=name)
venv/lib/python3.7/site-packages/tensorflow_core/python/framework/op_def_library.py:794: in _apply_op_helper
    op_def=op_def)
venv/lib/python3.7/site-packages/tensorflow_core/python/util/deprecation.py:507: in new_func
    return func(*args, **kwargs)
venv/lib/python3.7/site-packages/tensorflow_core/python/framework/ops.py:3357: in create_op
    attrs, op_def, compute_device)
venv/lib/python3.7/site-packages/tensorflow_core/python/framework/ops.py:3426: in _create_op_internal
    op_def=op_def)
venv/lib/python3.7/site-packages/tensorflow_core/python/framework/ops.py:1770: in __init__
    control_input_ops)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

graph = <tensorflow.python.framework.ops.Graph object at 0x7fc42f2b1650>
node_def = name: "in_top_k/InTopKV2"
op: "InTopKV2"
attr {
  key: "T"
  value {
    type: DT_INT32
  }
}

inputs = [<tf.Tensor 'Variable/read:0' shape=(2, 3) dtype=float32>, <tf.Tensor 'Cast:0' shape=() dtype=int32>, <tf.Tensor 'in_top_k/InTopKV2/k:0' shape=() dtype=int32>]
control_inputs = []

    def _create_c_op(graph, node_def, inputs, control_inputs):
      """Creates a TF_Operation.
    
      Args:
        graph: a `Graph`.
        node_def: `node_def_pb2.NodeDef` for the operation to create.
        inputs: A list of `Tensor`s (corresponding to scalar inputs) and lists of
          `Tensor`s (corresponding to sequence inputs, e.g. "int64 * N",
          "list(int64)"). The length of the list should be equal to the number of
          inputs specified by this operation's op def.
        control_inputs: A list of `Operation`s to set as control dependencies.
    
      Returns:
        A wrapped TF_Operation*.
      """
      # pylint: disable=protected-access
      op_desc = c_api.TF_NewOperation(graph._c_graph, compat.as_str(node_def.op),
                                      compat.as_str(node_def.name))
      if node_def.device:
        c_api.TF_SetDevice(op_desc, compat.as_str(node_def.device))
      # Add inputs
      for op_input in inputs:
        if isinstance(op_input, (list, tuple)):
          c_api.TF_AddInputList(op_desc, [t._as_tf_output() for t in op_input])
        else:
          c_api.TF_AddInput(op_desc, op_input._as_tf_output())
    
      # Add control inputs
      for control_input in control_inputs:
        c_api.TF_AddControlInput(op_desc, control_input._c_op)
      # pylint: enable=protected-access
    
      # Add attrs
      for name, attr_value in node_def.attr.items():
        serialized = attr_value.SerializeToString()
        # TODO(skyewm): this creates and deletes a new TF_Status for every attr.
        # It might be worth creating a convenient way to re-use the same status.
        c_api.TF_SetAttrValueProto(op_desc, compat.as_str(name), serialized)
    
      try:
        c_op = c_api.TF_FinishOperation(op_desc)
      except errors.InvalidArgumentError as e:
        # Convert to ValueError for backwards compatibility.
>       raise ValueError(str(e))
E       ValueError: Shape must be rank 1 but is rank 0 for 'in_top_k/InTopKV2' (op: 'InTopKV2') with input shapes: [2,3], [], [].

venv/lib/python3.7/site-packages/tensorflow_core/python/framework/ops.py:1610: ValueError
------------------------------------------------ Captured stderr teardown -------------------------------------------------
WARNING:tensorflow:From /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:14/keras/backend/tensorflow_backend.py:95: The name tf.reset_default_graph is deprecated. Please use tf.compat.v1.reset_default_graph instead.

WARNING:tensorflow:From /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:14/keras/backend/tensorflow_backend.py:98: The name tf.placeholder_with_default is deprecated. Please use tf.compat.v1.placeholder_with_default instead.

WARNING:tensorflow:From /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:14/keras/backend/tensorflow_backend.py:102: The name tf.get_default_graph is deprecated. Please use tf.compat.v1.get_default_graph instead.

-------------------------------------------------- Captured log teardown --------------------------------------------------
WARNING  tensorflow:module_wrapper.py:139 From /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:14/keras/backend/tensorflow_backend.py:95: The name tf.reset_default_graph is deprecated. Please use tf.compat.v1.reset_default_graph instead.

WARNING  tensorflow:module_wrapper.py:139 From /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:14/keras/backend/tensorflow_backend.py:98: The name tf.placeholder_with_default is deprecated. Please use tf.compat.v1.placeholder_with_default instead.

WARNING  tensorflow:module_wrapper.py:139 From /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:14/keras/backend/tensorflow_backend.py:102: The name tf.get_default_graph is deprecated. Please use tf.compat.v1.get_default_graph instead.
==================================================== warnings summary =====================================================
venv/lib/python3.7/site-packages/tensorflow_core/python/framework/tensor_util.py:521
venv/lib/python3.7/site-packages/tensorflow_core/python/framework/tensor_util.py:521
  /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:14/venv/lib/python3.7/site-packages/tensorflow_core/python/framework/tensor_util.py:521: DeprecationWarning: tostring() is deprecated. Use tobytes() instead.
    tensor_proto.tensor_content = nparray.tostring()

venv/lib/python3.7/site-packages/tensorflow_core/contrib/learn/python/learn/learn_io/generator_io.py:26
  /Users/jerry/Documents/GitHub/PyRepair/benchmarks/BugsInPy_Cloned_Repos/keras:14/venv/lib/python3.7/site-packages/tensorflow_core/contrib/learn/python/learn/learn_io/generator_io.py:26: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated since Python 3.3,and in 3.9 it will stop working
    from collections import Container

-- Docs: https://docs.pytest.org/en/latest/warnings.html
================================================ slowest 20 test durations ================================================
0.01s call     tests/keras/metrics_test.py::test_sparse_top_k_categorical_accuracy[y_pred1-y_true1]

(0.00 durations hidden.  Use -vv to show these durations.)
================================================= short test summary info =================================================
FAILED tests/keras/metrics_test.py::test_sparse_top_k_categorical_accuracy[y_pred1-y_true1] - ValueError: Shape must be ...
============================================== 1 failed, 3 warnings in 6.56s ==============================================
Using TensorFlow backend.



The test source code is following:

@pytest.mark.skipif((K.backend() == 'cntk'),
                    reason='CNTK backend does not support top_k yet')
@pytest.mark.parametrize('y_pred, y_true', [
    # Test correctness if the shape of y_true is (num_samples, 1)
    (np.array([[0.3, 0.2, 0.1], [0.1, 0.2, 0.7]]), np.array([[1], [0]])),
    # Test correctness if the shape of y_true is (num_samples,)
    (np.array([[0.3, 0.2, 0.1], [0.1, 0.2, 0.7]]), np.array([1, 0])),
])
def test_sparse_top_k_categorical_accuracy(y_pred, y_true):
    y_pred = K.variable(y_pred)
    y_true = K.variable(y_true)
    success_result = K.eval(
        metrics.sparse_top_k_categorical_accuracy(y_true, y_pred, k=3))

    assert success_result == 1
    partial_result = K.eval(
        metrics.sparse_top_k_categorical_accuracy(y_true, y_pred, k=2))
    assert partial_result == 0.5
    failure_result = K.eval(
        metrics.sparse_top_k_categorical_accuracy(y_true, y_pred, k=1))
    assert failure_result == 0

