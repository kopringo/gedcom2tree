#

class NodePerson:

    first_name = ''
    last_name = ''
    birth_year = None
    death_year = None

    parents = None
    families = []

    def get_father(self):
        pass

    def get_mother(self):
        pass

    def get_families(self):
        pass

class NodeFamily:

    def get_father(self):
        pass

    def get_mother(self):
        pass

    def get_children(self):
        pass

class Gedcom2Tree:
    """
    Usage:
    g = Gedcom2Tee(person_list, family_list)
    g.build_tree()
    g.to
    """

    person_list = {}
    family_list = {}

    def __init__(self):
        pass

    def load_gedcom(self, file_path):
        pass

    def load_raw_data(self, person_list, family_list):
        for person in person_list:
            self.person_list[person['id']] = person
            self.person_list[person['id']]['v'] = {
                'vx': None, # virtual x
                'vy': None, # virtual y
                'v_families': None,

            }
        for family in family_list:
            self.family_list[family['id']] = family


    def clear_dfs(self):
        for p in self.person_list:
            p.visited = False
        for f in self.family_list:
            f.visited = False



    def build_tree(self):
        pass

