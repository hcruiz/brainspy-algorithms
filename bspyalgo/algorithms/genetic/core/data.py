import numpy as np


class GAData:
    def __init__(self, inputs, targets, mask, hyperparams):  # , waveform_configs):
        assert len(inputs) == len(targets), f'No. of input data {len(inputs)} does not match no. of targets {len(targets)}'
        self.results = {}
        self.results['inputs'] = inputs
        self.results['targets'] = targets
        if mask is None or len(mask) <= 1:
            mask = np.ones(targets.shape[0], dtype=bool)
        self.results['mask'] = mask
        self.reset(hyperparams)

    def update(self, next_sate):
        gen = next_sate['generation']
        self.results['control_voltage_array'][gen, :, :] = next_sate['genes']
        self.results['output_current_array'][gen, :, :] = next_sate['outputs']
        self.results['fitness_array'][gen, :] = next_sate['fitness']

    def reset(self, hyperparams):
        # Define placeholders
        self.results['control_voltage_array'] = np.zeros((hyperparams['epochs'], hyperparams['genomes'],
                                                          hyperparams['genes']))
        self.results['output_current_array'] = np.zeros((hyperparams['epochs'], hyperparams['genomes']) + (len(self.results['inputs']), 1))
        self.results['fitness_array'] = -np.inf * np.ones((hyperparams['epochs'], hyperparams['genomes']))
        # return self.results['inputs'], self.results['targets']

    def judge(self):
        ind = np.unravel_index(np.argmax(self.results['fitness_array'], axis=None), self.results['fitness_array'].shape)
        self.results['best_output'] = self.results['output_current_array'][ind]
        self.results['control_voltages'] = self.results['control_voltage_array'][ind]
        self.results['best_performance'] = np.max(self.results['fitness_array'])
        self.print_results()

    def print_results(self):  # print(best_output.shape,self.target_wfm.shape)
        print(f'\n========================= BEST SOLUTION =======================')
        print('Max fitness: ', self.results['best_performance'])
        print(f"Best control voltages:\n {self.results['control_voltages']}")
        print('===============================================================')
