import math
from pymol import cmd

# helper function to computer distance between center of masses
def dist(com_1, com_2):
    if len(com_2) == 3:
        return math.sqrt((com_1[0] - com_2[0])**2 + (com_1[1] - com_2[1])**2 + (com_1[2] - com_2[2])**2)
    return 10000


def com_filter(key, threshold=5, path="~/CURIS/PyMol Sessions/"):

    threshold = float(threshold)
    # load in list of objects
    objlist = cmd.get_names("objects")
    print(objlist)
    # mod key and initialize af model com
    target_com = []
    target_name = None
    key = key.lower()

    # calculate com of af model, iterate just in case it isn't the first object
    for obj in objlist:
        if "af" in obj.lower():
            target_com = cmd.centerofmass(obj)
            target_name = obj
            print(target_com)

    # iterate through object list, calculate com of the object if it is of key id (either by BS or lig)
    for obj in objlist:
        if key in obj.lower():
            com = cmd.centerofmass(obj)
            print("com: ", obj, ": ", com)
            # if the distance is too far from the af model, remove the ligand/BS pair
            if dist(com, target_com) > threshold:
                cmd.remove(obj)
                obj_pair = obj.replace('BS', 'lig') if key == 'bs' else obj.replace('lig', 'BS')
                cmd.remove(obj_pair)
                print("disabled: ", obj)
    # save pymol session with key and threshold noted
    filename = (path + "Filtered_" + target_name[0:8] + key.upper() + "_" + str(threshold).replace('.', '-') + ".pse")
    print("saved to", filename)
    cmd.save(filename)


cmd.extend("com_filter", com_filter)
