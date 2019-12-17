class Node:
    def __init__(self, name):
        self.name = name
        self.children = set()
        self.parent = None

    def add_child(self, child):
        # child should also be a node
        assert isinstance(child, Node)

        self.children.add(child)
        
        assert child.parent is None or child.parent == self
        child.parent = self

    def n_children(self):
        return sum([
            child.n_children()
            for child in self.children
        ]) + len(self.children)

    def __repr__(self):
        return self.name

def n_ancestors(node):
    n = 0
    while node.parent is not None:
        n += 1
        node = node.parent

    return n

def rootpath(node):
    path = []
    while node.parent is not None:
        path.append(node.parent)
        node = node.parent
    
    return path

def find_lowest_common_ancestor(node1, node2):
    rootpath1 = list(reversed(path_to(node1, None)))
    rootpath2 = list(reversed(path_to(node2, None)))

    i = 0
    while rootpath1[i] == rootpath2[i]:
        i += 1

    return rootpath1[i-1]

def path_to(src, dest):
    if src == dest:
        return []

    path = []
    node = src
    while node.parent != dest:
        path.append(node.parent)
        node = node.parent

    return path

orbits = open('../data/input6').readlines()

# orbits = """COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
# K)YOU
# I)SAN""".split()

# build tree?
nodes = {}
nodes['COM'] = Node('COM')

for orbit in orbits:
    source, target = orbit.strip().split(')')

    if source not in nodes:
        nodes[source] = Node(source)
    if target not in nodes:
        nodes[target] = Node(target)

    # add relation
    nodes[source].add_child(nodes[target])

print(sum(n_ancestors(node) for node in nodes.values()))

# part 2
common_anc = find_lowest_common_ancestor(nodes['YOU'], nodes['SAN'])

ans2 = len(path_to(nodes['YOU'], common_anc)) + len(path_to(nodes['SAN'], common_anc))

print(ans2)