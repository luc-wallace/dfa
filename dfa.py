class DFA:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q  # set of states
        self.Sigma = Sigma  # set of symbols
        self.delta = delta  # transition function as a dictionary
        self.q0 = q0  # initial state
        self.F = F  # set of final states

    def __repr__(self):
        return f"DFA({self.Q},\n\t{self.Sigma},\n\t{self.delta},\n\t{self.q0},\n\t{self.F})"

    def run(self, w):
        q = self.q0
        while w != "":
            try:
                q = self.delta[(q, w[0])]
            except KeyError:
                return False
            w = w[1:]
        return q in self.F

    def minimize(self):
        table = {}
        states = sorted(self.Q)
        for i in states[:-1]:
            for j in states[1:]:
                if i == j:
                    continue
                table[tuple(sorted([i, j]))] = False

        unknowns = []
        for i, j in table.keys():
            if (i in self.F and j not in self.F) or (j in self.F and i not in self.F):
                table[(i, j)] = True
                continue
            unknowns.append((i, j))

        potential = {(i, j): [] for i, j in unknowns}
        for i, j in unknowns:
            ijkey = tuple(sorted([i, j]))
            for symbol in self.Sigma:
                try:
                    p = self.delta[(i, symbol)]
                    q = self.delta[(j, symbol)]
                except KeyError:
                    raise Exception("DFA is incomplete")
                pqkey = tuple(sorted([p, q]))
                if p == q:
                    continue
                elif table[pqkey] == True:
                    table[ijkey] = True
                    pot = potential.get((i, j))
                    if pot is not None:
                        for a, b in pot:
                            table[tuple(sorted([a, b]))] = True
                    break
                potential[pqkey].append(ijkey)

        equals = []
        for pair, val in table.items():
            if not val:
                equals.append(pair)

        new_delta = {}
        for (old_state, symbol), new_state in self.delta.items():
            for pair in equals:
                if old_state in pair:
                    old_state = pair[0]
                if new_state in pair:
                    new_state = pair[0]
            new_delta[old_state, symbol] = new_state

        new_symbols = set([func[0] for func in new_delta])
        return DFA(
            new_symbols,
            self.Sigma,
            new_delta,
            self.q0,
            set(filter(lambda n: n in new_symbols, self.F)),
        )
