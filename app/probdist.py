class ProbDist:

    def __init__(self, var_name='?', freqs=None):
        self.prob = {}
        self.var_name = var_name
        self.values = []
        if freqs:
            for (v, p) in freqs.items():
                self[v] = p
            self.normalize()

    def __getitem__(self, val):
        try:
            return self.prob[val]
        except KeyError:
            return 0

    def __setitem__(self, val, p):
        if val not in self.values:
            self.values.append(val)
        self.prob[val] = p

    def normalize(self):
        total = sum(self.prob.values())
        if not isclose(total, 1.0):
            for val in self.prob:
                self.prob[val] /= total
        return self

    def show_approx(self, numfmt='{:.3g}'):
        return ', '.join([('{}: ' + numfmt).format(v, p) for (v, p) in sorted(self.prob.items())])

    def __repr__(self):
        return "P({})".format(self.var_name)

class JointProbDist(ProbDist):

    def __init__(self, variables):
        self.prob = {}
        self.variables = variables
        self.vals = defaultdict(list)

    def __getitem__(self, values):
        values = event_values(values, self.variables)
        return ProbDist.__getitem__(self, values)

    def __setitem__(self, values, p):
        values = event_values(values, self.variables)
        self.prob[values] = p
        for var, val in zip(self.variables, values):
            if val not in self.vals[var]:
                self.vals[var].append(val)

    def values(self, var):
        return self.vals[var]

    def __repr__(self):
        return "P({})".format(self.variables)