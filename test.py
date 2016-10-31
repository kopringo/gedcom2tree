# test

from g2t import Gedcom2Tree

person_list = {
    1: {},
    2: {},
    3: {},
    4: {},
    5: {},
    6: {},
    7: {},
    8: {},
    9: {},
    10: {},
    11: {},
    12: {},
    13: {},
    14: {},
    15: {},
    16: {},
    17: {},
    18: {},
    19: {},
    20: {},
    21: {},
    22: {},
    23: {},
    24: {},
    25: {},
    26: {},
    27: {},
    28: {},
}

family_list = {
    1: {'father_id': 1, 'mother_id': 2, 'children_ids': [3, 4]},
    2: {'father_id': 6, 'mother_id': 7, 'children_ids': [23, 24, 25, 26, 27]},
    3: {'father_id': 26, 'mother_id': 27, 'children_ids': [28]},
    4: {'father_id': 10, 'mother_id': 9, 'children_ids': [11, 12, 13]},
    5: {'father_id': 14, 'mother_id': 15, 'children_ids': [9, 8, 1, 2, 5, 6]},
    6: {'father_id': 10, 'mother_id': 20, 'children_ids': [14, 15, 16, 17, 18]},
    7: {'father_id': 21, 'mother_id': 22, 'children_ids': [19]},
}

g = Gedcom2Tree()
g.load_raw_data(person_list, family_list)
g.gen_tree(26)