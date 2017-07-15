
"""
This script is responsible for the creation of The Brain from scratch using Genome data
"""

import json
import shutil
import errno
import datetime

import architect
import visualizer
import settings

settings.init()

# Backup the old brain
def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise

copyanything('../My_Brian', '../My_Brian_archive/My_Brain_'+str(datetime.datetime.now()).replace(' ', '_'))


# Read Genome data, reset connectome and build it up
data = settings.genome
blueprint = settings.cortical_list()

print("Here is the list of all defined cortical areas: %s " % blueprint)

# # Reset Connectume
for key in blueprint:
    file_name = 'connectome/'+key+'.json'
    with open(file_name, "w") as connectome:
        connectome.write(json.dumps({}))
        connectome.truncate()
    print("Cortical area %s is has been cleared." % key)

# Develop Neurons for various cortical areas defined in Genome
for key in blueprint:
    architect.three_dim_growth(key)
    print("Neuron Creation for Cortical area %s is now complete." % key)

# Build Synapses within all Cortical areas
for key in blueprint:
    architect.neighbor_builder(cortical_area=key, rule_id=data["blueprint"][key]["neighbor_locator_rule_id"],
                               rule_param=data["neighbor_locator_rule"][data["blueprint"][key]
                               ["neighbor_locator_rule_id"]][data["blueprint"][key]
                               ["neighbor_locator_rule_param_id"]],
                               connection_resistance=data["blueprint"][key]["connection_resistance"])
    print("Synapse Creation for Cortical area %s is now complete." % key)

# Build Synapses between various Cortical areas
for key in blueprint:
    for mapped_cortical_area in data["blueprint"][key]["cortical_mapping_dst"]:
        architect.neighbor_builder_ext(cortical_area_src=key,
                                       cortical_area_dst=mapped_cortical_area,
                                       rule=data["blueprint"][key]["cortical_mapping_dst"][mapped_cortical_area]
                                       ["neighbor_locator_rule_id"],
                                       rule_param=data["neighbor_locator_rule"][data["blueprint"][key]
                                       ["cortical_mapping_dst"][mapped_cortical_area]
                                       ["neighbor_locator_rule_id"]][data["blueprint"][key]["cortical_mapping_dst"]
                                       [mapped_cortical_area]["neighbor_locator_rule_param_id"]],
                                       connection_resistance=data["blueprint"][key]["connection_resistance"])
        print("Completed Synapse Creation between Cortical area %s and %s" % (key, mapped_cortical_area))
print("Neuronal mapping across all Cortical areas has been completed!!")

# Visualize Neurons and Synapses
if settings.vis_show:
    for key in blueprint:
        visualizer.connectome_visualizer(cortical_area=key, neighbor_show='true')

settings.save_brain_to_disk()