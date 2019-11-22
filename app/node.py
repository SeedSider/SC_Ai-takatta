class Node:

    def __init__(self, X, parents, cpt):
        if isinstance(parents, str):
            parents = parents.split()

        if isinstance(cpt, (float, int)):
            cpt = {(): cpt}
        elif isinstance(cpt, dict):
            if cpt and isinstance(list(cpt.keys())[0], bool):
                cpt = {(v,): p for v, p in cpt.items()}

        assert isinstance(cpt, dict)
        for vs, p in cpt.items():
            # assert isinstance(vs, tuple) and len(vs) == len(parents)
            assert isinstance(vs, tuple)            
            assert all(isinstance(v, bool) for v in vs)
            assert 0 <= p <= 1

        self.variable = X
        self.parents = parents
        self.cpt = cpt
        self.children = []

    def p(self, value, event):
        assert isinstance(value, bool)
        ptrue = self.cpt[event_values(event, self.parents)]
        return ptrue if value else 1 - ptrue

    def sample(self, event):
        return probability(self.p(True, event))

    def __repr__(self):
        return repr((self.variable, ' '.join(self.parents)))
