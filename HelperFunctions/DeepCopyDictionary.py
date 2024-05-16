import HelperFunctions.Constants as C

def deep_copy_dict(dict_to_copy):
    dict_copy = {}
    for key in dict_to_copy:
        obj = dict_to_copy[key]
        dict_copy.update({key: C.ClassroomValue(obj.value, obj.cast_to_type)})
    return dict_copy
