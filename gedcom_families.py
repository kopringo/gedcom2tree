from gedcom import Gedcom, GEDCOM_TAG_HUSBAND
from copy import copy

class GedcomFamilies:

    families: list = None
    single_individuals: list = None

    # gedcom file and object
    __gedcom: Gedcom = None
    __gedcom_file_path: str = None

    # all elements
    __individuals: list = None
    __families: list = None
    __files: list = None

    def __init__(self, gedcom_file_path, subtree_type=1):
        """
        @param gedcom_file_path path to the gedcom file
        @param subtree_type how to split tree into families:
               1 - split tree using father's surname
               2 - join related families into the same tree
        """

        # load gedcom object
        self.__gedcom_file_path = gedcom_file_path
        self.__gedcom = Gedcom(gedcom_file_path)

        # load GEDCOM elements
        self.__load_gedcom_elements()

        # split the whole free into families
        if subtree_type == 1:
            self.__generate_family_subtrees()
        if subtree_type == 2:
            self.__generate_subtrees()

    def __load_gedcom_elements(self):

        self.__individuals = []
        self.__families = []
        self.__files = []
        for element in self.__gedcom.get_root_child_elements():
            if element.is_individual():
                self.__individuals.append(element)
            if element.is_family():
                self.__families.append(element)
            if element.is_file():
                self.__files.append(element)

    def __generate_subtrees(self):

        self.families = []
        self.single_individuals = []

        # set all persons as unvisited
        for individual in self.__individuals:
            individual.visited = False
        
        self.__set_all_individuals_as_unvisited()

        # split them all
        for individual in self.__individuals:

            if individual.visited:
                continue

            new_family = []

            queue = []
            queue.append(individual)

            while len(queue) > 0:

                tmp_individual = queue.pop()
                if tmp_individual.visited:
                    continue
                
                tmp_individual.visited = True
                new_family.append(tmp_individual)

                tmp_families = self.__gedcom.get_families(tmp_individual, 'FAMC')
                tmp_families = tmp_families + self.__gedcom.get_families(tmp_individual, 'FAMS')

                for tmp_family in tmp_families:
                    for tmp_child in self.__gedcom.get_family_members(tmp_family):
                        queue.append(tmp_child)

            if len(new_family) == 1:
                self.single_individuals.append(new_family[0])
            else:
                self.families.append(copy(new_family))



    def __generate_family_subtrees(self):

        self.families = []
        self.single_individuals = []

        self.__set_all_individuals_as_unvisited()

        # split them all
        for individual in self.__individuals:

            if individual.visited:
                continue

            new_family = []
            tmp_indivdual_list = []

            # let's find the oldest ancestor of this family
            individual_pointer = individual
            stop = False
            while not stop:

                families = self.__gedcom.get_families(individual_pointer, 'FAMC')
                if len(families) == 0:
                    break

                for family in families:
                    fathers = self.__gedcom.get_family_members(family, GEDCOM_TAG_HUSBAND)
                    if len(fathers) > 0:
                        individual_pointer = fathers[0]
                    else:
                        stop = True
                    break

            # let's find all descendants
            tmp_indivdual_list.append(individual_pointer)
            while len(tmp_indivdual_list) > 0:
                individual2 = tmp_indivdual_list.pop()
                individual2.visited = True
                new_family.append(individual2)
                families = self.__gedcom.get_families(individual2, 'FAMS')
                for family in families:
                    fathers = self.__gedcom.get_family_members(family, GEDCOM_TAG_HUSBAND)
                    if len(fathers) > 0 and fathers[0] == individual2:
                        for individual3 in self.__gedcom.get_family_members(family, 'CHIL'):
                            tmp_indivdual_list.append(individual3)

            if len(new_family) == 1:
                self.single_individuals.append(individual_pointer)
            else:
                self.families.append(copy(new_family))





            """
            (firstname, lastname) = individual.get_name()
            if lastname:
                lastname_lower = lastname.lower()
                if lastname_lower not in self.families.keys():
                    self.families[lastname_lower] = []

                self.families[lastname_lower].append(individual)
            """

        #print(self.families)
        #print(len(self.families))
        #print('')
        #print(self.families.keys())

    def __set_all_individuals_as_unvisited(self):
        # set all persons as unvisited
        for individual in self.__individuals:
            individual.visited = False

    def get_dot_graph(self):
        data = ''
        data += GedcomFamilies.__get_dot_graph_header()

        # prepare subgraphs for families
        i = 0
        for family in self.families:
            if len(family) < 3:
                continue

            #if family_key == 'koperkiewicz':
            family_key = str(i)
            i = i + 1
            #if i == 3:
            data += self.__get_subgraph_for_family(family, family_key)

        data += GedcomFamilies.__get_dot_graph_footer()

        return data

    @staticmethod
    def __get_dot_graph_header():
        return """digraph G {
\tgraph [fontname="fixed"];
\tnode [fontname="fixed"];
\tedge [fontname="fixed"];
\tmincross = 2.0;splines=polyline;
\tratio = expand;\n"""

    @staticmethod
    def __get_dot_graph_footer():
        return """}\n"""

    def __get_subgraph_for_family(self, family, family_key):
        data = """subgraph cluster_%s {\n
label = "process %s";color=red;\n
""" % (family_key, family_key)

        # dict for people from family
        person_list_in_family = {}
        family_list_in_family = {}

        for person in family:
            data += u'\t_%s [shape=box, label="%s"];\n' % (
                person.get_pointer().replace('@', ''),
                (' '.join(person.get_name())).replace('"', '^')
            )
            person_list_in_family[person.get_pointer()] = person

        for person in family:
            for family in self.__gedcom.get_families(person):

                if family.get_pointer() in family_list_in_family.keys():
                    continue
                family_list_in_family[family.get_pointer()] = True

                data += u'\t_%s [label="M",height=.1,width=.1];' % family.get_pointer().replace('@', '')

                # data += u'\t_%s -> _%s [weight=1];\n' % (person.get_pointer().replace('@', ''), family.get_pointer().replace('@', ''))

                data += u'\t\tsubgraph cluster_family_%s {\ncolor=blue;\n' % family.get_pointer().replace('@', '')
                parents = self.__gedcom.get_family_members(family, 'PARENTS')
                for parent in parents:
                    data += u'\t\t\t_%s -> _%s [weight=50];\n' % (parent.get_pointer().replace('@', ''), family.get_pointer().replace('@', ''))
                data += u'\t\t}\n'

                children = self.__gedcom.get_family_members(family, 'CHIL')
                for child in children:
                    data += u'\t_%s -> _%s [weight=1];\n' % (family.get_pointer().replace('@', ''), child.get_pointer().replace('@', ''))
                    #for family2 in gedcom.get_families(child):
                    #    print('\t\tcluster_%s;' % family2.get_pointer().replace('@', ''))


        data += "}\n\n"
        return data
