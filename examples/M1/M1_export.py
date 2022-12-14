import M1  # import parameters file
from netpyne import sim  # import netpyne sim module

np = M1.netParams
print("********************\n*\n*  Note: setting noise to 1, since noise can only be 0 or 1 in NeuroML export currently!\n*\n********************")
np.stimSourceParams['background_E']['noise'] = 1
np.stimSourceParams['background_I']['noise'] = 1

sim.createExportNeuroML2(netParams = np,
                       simConfig = M1.simConfig,
                       reference = 'M1',
                       connections=True,
                       stimulations=True)  # create and export network to NeuroML 2

###### Validate the NeuroML ######

from neuroml.utils import validate_neuroml2
validate_neuroml2('M1.net.nml')
