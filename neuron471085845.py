'''
Defines a class, Neuron471085845, of neurons from Allen Brain Institute's model 471085845

A demo is available by running:

    python -i mosinit.py
'''
class Neuron471085845:
    def __init__(self, name="Neuron471085845", x=0, y=0, z=0):
        '''Instantiate Neuron471085845.
        
        Parameters:
            x, y, z -- position offset
            
        Note: if name is not specified, Neuron471085845_instance is used instead
        '''
        
        # load the morphology
        from load_swc import load_swc
        load_swc('Pvalb-IRES-Cre_Ai14_IVSCC_-165874.04.02.01_464113242_m.swc', self,
                 use_axon=False, xshift=x, yshift=y, zshift=z)

        # custom axon (works because dropping axon during import)
        from neuron import h
        self.axon = [h.Section(cell=self, name='axon[0]'),
                     h.Section(cell=self, name='axon[1]')]
        for sec in self.axon:
            sec.L = 30
            sec.diam = 1
            sec.nseg = 1
        self.axon[0].connect(self.soma[0](0.5))
        self.axon[1].connect(self.axon[0](1))
        self.all += self.axon
        
        self._name = name
        self._insert_mechanisms()
        self._discretize_model()
        self._set_mechanism_parameters()
    
    def __str__(self):
        if self._name is not None:
            return self._name
        else:
            return "Neuron471085845_instance"
                
    def _insert_mechanisms(self):
        from neuron import h
        for sec in self.all:
            sec.insert("pas")
        for mech in [u'CaDynamics', u'Ca_HVA', u'Ca_LVA', u'Ih', u'Im_v2', u'K_T', u'Kd', u'Kv2like', u'Kv3_1', u'NaV', u'SK']:
            self.soma[0].insert(mech)
    
    def _set_mechanism_parameters(self):
        from neuron import h
        for sec in self.all:
            sec.Ra = 192.6
            sec.e_pas = -88.530632019
        
        for sec in self.axon:
            sec.cm = 1.15
            sec.g_pas = 0.000853481534938
        for sec in self.dend:
            sec.cm = 1.15
            sec.g_pas = 5.3397118226e-06
        for sec in self.soma:
            sec.cm = 1.15
            sec.ena = 53.0
            sec.ek = -107.0
            sec.gbar_Ih = 0.000203079
            sec.gbar_NaV = 0.0503524
            sec.gbar_Kd = 0
            sec.gbar_Kv2like = 0.00859707
            sec.gbar_Kv3_1 = 0.8032
            sec.gbar_K_T = 0.0185335
            sec.gbar_Im_v2 = 0.00745333
            sec.gbar_SK = 0.0166183
            sec.gbar_Ca_HVA = 0.000511448
            sec.gbar_Ca_LVA = 0.00976219
            sec.gamma_CaDynamics = 9.24734e-09
            sec.decay_CaDynamics = 233.08
            sec.g_pas = 6.41992e-05
    
    def _discretize_model(self):
        for sec in self.all:
            sec.nseg = 1 + 2 * int(sec.L / 40)

