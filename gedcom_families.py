from gedcom import Gedcom

class GedcomFamilies:

    families: dict = None

    # gedcom file and object
    __gedcom: Gedcom = None
    __gedcom_file_path: str = None

    # all elements
    __individuals: list = None
    __families: list = None
    __files: list = None

    def __init__(self, gedcom_file_path):

        # load gedcom object
        self.__gedcom_file_path = gedcom_file_path
        self.__gedcom = Gedcom(gedcom_file_path)

        # load GEDCOM elements
        self.__load_gedcom_elements()

        # split the whole free into families
        self.__generate_familie_subtrees()

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

    def __generate_familie_subtrees(self):

        self.families = {}

        #
        for individual in self.__individuals:
            (firstname, lastname) = individual.get_name()
            if lastname:
                lastname_lower = lastname.lower()
                if lastname_lower not in self.families.keys():
                    self.families[lastname_lower] = []

                self.families[lastname_lower].append(individual)

        #print(self.families)
        #print('')
        #print(self.families.keys())

    def get_dot_graph(self):
        data = ''
        data += GedcomFamilies.__get_dot_graph_header()

        # prepare subgraphs for families
        for family_key in self.families:
            if len(self.families[family_key]) < 3:
                continue

            data += self.__get_subgraph_for_family(family_key)

        data += GedcomFamilies.__get_dot_graph_footer()

        return data

    @staticmethod
    def __get_dot_graph_header():
        return """digraph G {\n
\tgraph [fontname="fixed"];\n
\tnode [fontname="fixed"];\n
\tedge [fontname="fixed"];\n
\tmincross = 2.0;\n
\tratio = fill;\n"""

    @staticmethod
    def __get_dot_graph_footer():
        return """}\n"""

    def __get_subgraph_for_family(self, family_key):
        data = """subgraph cluster_%s {\n
label = "process %s";\n
""" % (family_key, family_key)

        for person in self.families[family_key]:
            data += u'\t_%s [shape=box, label="%s"];\n' % (
                person.get_pointer().replace('@', ''),
                (' '.join(person.get_name())).replace('"', '^')
            )

            for family in self.__gedcom.get_families(person):
                data += u'\t_%s -> _%s [weight=1];\n' % (person.get_pointer().replace('@', ''), family.get_pointer().replace('@', ''))

        data += "}\n"
        return data
