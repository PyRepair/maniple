You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

    def build(self, input_shape):
        for cell in self.cells:
            if isinstance(cell, Layer):
                cell.build(input_shape)
            if hasattr(cell.state_size, '__len__'):
                output_dim = cell.state_size[0]
            else:
                output_dim = cell.state_size
            input_shape = (input_shape[0], input_shape[1], output_dim)
        self.built = True



The test source code is following:

        def build(self, input_shape):
            # no time axis in the input shape passed to RNN cells
            assert len(input_shape) == 2

            self.kernel = self.add_weight(shape=(input_shape[-1], self.units),
                                          initializer='uniform',
                                          name='kernel')
            self.recurrent_kernel = self.add_weight(
                shape=(self.units, self.units),
                initializer='uniform',
                name='recurrent_kernel')
            self.built = True


