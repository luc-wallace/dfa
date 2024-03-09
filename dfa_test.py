from dfa import DFA

D0 = DFA(
    {0, 1, 2, 3, 4, 5},
    {"a", "b"},
    {
        (0, "a"): 1,
        (0, "b"): 4,
        (1, "a"): 2,
        (1, "b"): 3,
        (2, "a"): 2,
        (2, "b"): 2,
        (3, "a"): 2,
        (3, "b"): 3,
        (4, "a"): 5,
        (4, "b"): 4,
        (5, "a"): 5,
        (5, "b"): 4,
    },
    0,
    {2, 3},
)

D0_min = D0.minimize()

strings = ("aba", "bba", "abbababaaab", "bbaaab", "bbbaab", "bbbbba", "bbb", "aaa")

for string in strings:
    print(f"D0: {D0.run(string)}, D0_min: {D0_min.run(string)} ({string}) ")
