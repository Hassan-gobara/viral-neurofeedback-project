"""
Module for exporting models as Python scripts

"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from builtins import open
from future import standard_library
standard_library.install_aliases()
from netpyne import __version__

def createPythonScript(fname, netParams, simConfig):
    """
    Function for/to <short description of `netpyne.conversion.pythonScript.createPythonScript`>

    Parameters
    ----------
    fname : <type>
        <Short description of fname>
        **Default:** *required*

    netParams : <type>
        <Short description of netParams>
        **Default:** *required*

    simConfig : <type>
        <Short description of simConfig>
        **Default:** *required*


    """


    import sys
    import json
    from netpyne import specs

    def replace(string):
        # convert bools and null from json to python
        return string.replace('true', 'True').replace('false', 'False').replace('null', '""')

    def remove(dictionary):
        # remove reserved keys such as __str__, __dict__
        if isinstance(dictionary, dict):
            for key, value in list(dictionary.items()):
                if key.startswith('__'):
                    dictionary.pop(key)
                else:
                    remove(value)

    def addAttrToScript(attr, value, obj_name, class_instance, file):
        # write line of netpyne code if is different from default value
        if not hasattr(class_instance, attr) or value!=getattr(class_instance, attr):
            file.write(obj_name + '.' + attr + ' = ' + replace(json.dumps(value, indent=4)) + '\n')

    def header(title, spacer='-'):
        # writes a header for the section
        return '\n# ' + title.upper() + ' ' + spacer*(77-len(title)) + '\n'

    if isinstance(netParams, specs.NetParams):
        # convert netpyne.specs.netParams class to dict class
        netParams = netParams.todict()
    if isinstance(simConfig, specs.SimConfig):
        simConfig = simConfig.todict()

    # remove reserved keys like __str__, __dict__
    remove(netParams)
    remove(simConfig)

    # network parameters
    params =  ['popParams' , 'cellParams', 'synMechParams']
    params += ['connParams', 'stimSourceParams', 'stimTargetParams']

    try :
        with open(fname if fname.endswith('.py') else fname+'.py', 'w') as file:
            file.write('from netpyne import specs, sim\n')
            file.write(header('documentation'))
            file.write("''' Please visit: https://www.netpyne.org '''\n")
            file.write("# Python script automatically generated by NetPyNE v%s from netParams and simConfig objects\n"%__version__)
            file.write(header('script', spacer='='))
            file.write('netParams = specs.NetParams()\n')
            file.write('simConfig = specs.SimConfig()\n')

            file.write(header('single valued attributes'))
            for key, value in list(netParams.items()):
                if key not in params:
                    addAttrToScript(key, value, 'netParams', specs.NetParams(), file)

            file.write(header('network attributes'))
            for param in params:
                for key, value in list(netParams[param].items()):
                    file.write("netParams." + param + "['" + key + "'] = " + replace(json.dumps(value, indent=4))+ '\n')

            file.write(header('network configuration'))
            for key, value in list(simConfig.items()):
                addAttrToScript(key, value, 'simConfig', specs.SimConfig(), file)

            file.write(header('create simulate analyze network'))
            file.write('import sys\n')
            file.write('if not "-neuroml" in sys.argv:\n')
            file.write('    sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)\n')
            file.write('else:\n')
            file.write('    nml_reference = "NetPyNENetwork" if not simConfig.filename else simConfig.filename\n')
            file.write('    sim.createExportNeuroML2(netParams=netParams, simConfig=simConfig, reference = nml_reference)\n')
            file.write(header('end script', spacer='='))

        print(("script saved on " + fname))

    except:
        print(('error saving file: %s' %(sys.exc_info()[1])))
