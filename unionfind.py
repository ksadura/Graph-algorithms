class UnionFind:
    def __init__(self, components_number):
        self.id = [x for x in range(components_number)]
        self.size = [1 for _ in range(components_number)]

    def root_of(self, component):
        while component != self.id[component]:
            # make every node in path point to its grandparent (thereby halving path length)
            self.id[component] = self.id[self.id[component]]
            component = self.id[component]
        return component

    def are_connected(self, p, q):
        return self.root_of(p) == self.root_of(q)

    def union(self, p, q):
        root_of_p = self.root_of(p)
        root_of_q = self.root_of(q)
        # self.id[p] = rootOfQ
        if root_of_p == root_of_q:
            return
        elif self.size[root_of_p] < self.size[root_of_q]:
            self.id[root_of_p] = root_of_q
            self.size[root_of_q] += self.size[root_of_p]
        else:
            self.id[root_of_q] = root_of_p
            self.size[root_of_p] += self.size[root_of_q]


