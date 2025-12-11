class Node:
    def __init__(self, value):
        self.value = value
        self.childs = []
        self.puzzles = []


    def add_child(self, child):
        self.childs.append(Node(child))

    def add_puzzles(self, puzzle):
        self.puzzles.append(puzzle)

    def find(self, value):

        if value not in self:
            return None

        for child in self.childs:
            if value == child.value:
                return child

    def __contains__(self, value):
        return any(value == child.value for child in self.childs)

# Tree implementation
class Categories:
    def __init__(self):
        self.head = Node('')

    def add(self, tags: list, puzzle):
        Categories.add_sub_tree(self.head, tags, puzzle)

    @staticmethod
    def add_sub_tree(root: Node, tags: list, puzzle):
        
        if len(tags) == 0:
            root.add_puzzles(puzzle)
            return

        if tags[0] in root:
            Categories.add_sub_tree(root.find(tags[0]), tags[1:], puzzle)

        elif tags[0] not in root:
            root.add_child(tags[0])
            Categories.add_sub_tree(root.find(tags[0]), tags[1:], puzzle)

