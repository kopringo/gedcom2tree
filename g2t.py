#

class NodePerson:

    first_name = ''
    last_name = ''
    birth_year = None
    death_year = None

    parents = None
    families = []

    v_width = 1

    def get_father(self):
        return self.father

    def get_mother(self):
        return self.mother

    def get_families(self):
        return self.families

class NodeFamily:

    father = None
    mother = None
    children = []

    def get_father(self):
        return self.father

    def get_mother(self):
        return self.mother

    def get_children(self):
        return self.children

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

        # @todo

        self.build_tree()

    def load_raw_data(self, person_list, family_list):
        for person_id in person_list.keys():
            self.person_list[person_id] = NodePerson()

        for family_id in family_list:
            self.family_list[family_id] = NodeFamily()

            self.family_list[family_id].father = self.person_list[ family_list[family_id]['father_id'] ]
            self.family_list[family_id].mother = self.person_list[ family_list[family_id]['mother_id'] ]
            for children_id in family_list[family_id]['children_ids']:
                self.family_list[family_id].children.append( self.person_list[children_id] )

            if family_list[family_id]['father_id'] != None:
                self.person_list[ family_list[family_id]['father_id'] ].families.append( self.family_list[family_id] )
            if family_list[family_id]['mother_id'] != None:
                self.person_list[ family_list[family_id]['mother_id'] ].families.append( self.family_list[family_id] )

        self.build_tree()


    def clear_dfs(self):
        for p in self.person_list:
            p.visited = False
        for f in self.family_list:
            f.visited = False



    def build_tree(self):
        pass


    def _calc_tree(self, person):

        families = person.get_families()

        if families == []:
            person.v_width = 1
            return 1

        sum_all = 0

        # add spaces between families
        if len(families) > 0:
            sum_all = sum_all + len(families) - 1


        for family in families:
            children = family.get_children()
            v_sum = 0

            # add spaces between children
            if len(children) > 0:
                v_sum = v_sum + len(children) - 1

            # calculate width of child
            for child in children:
                self._calc_tree(child)
                v_sum = v_sum + child.v_width

            family.v_width = v_sum

            sum_all = sum_all + v_sum

        person.v_width = sum_all
        return sum_all

    def gen_tree(self, person_id):

        if not person_id in self.person_list.keys():
            raise 'person not found'

        person = self.person_list[person_id]
        while person.parents != None and person.parents.father != None:
            person = person.family.father

        self._calc_tree(person)