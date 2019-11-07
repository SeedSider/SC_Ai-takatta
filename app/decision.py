from .bayesian import BayesianNetwork

class DecisionNetwork(BayesianNetwork):

    def __init__(self, action, infer):
        super(DecisionNetwork, self).__init__()
        self.action = action
        self.infer = infer

    def best_action(self):
        return self.action

    def get_utility(self, action, state):
        raise NotImplementedError

    def get_expected_utility(self, action, evidence):
        u = 0.0
        prob_dist = self.infer(action, evidence, self).prob
        for item, _ in prob_dist.items():
            u += prob_dist[item] * self.get_utility(action, item)

        return u
