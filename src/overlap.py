def calculate_overlap(a: str, b: str) -> int:
    """
    Calculates an overlap between two strings using Knuth–Morris–Pratt algorithm
    """

    pi = [0] * (len(a) + len(b) + 1)
    string = b + '#' + a
    for i in range(len(string)):
        if i == 0:
            continue

        j = pi[i - 1]
        while j > 0 and string[i] != string[j]:
            j = pi[j - 1]
        if string[i] == string[j]:
            j += 1
        pi[i] = j

    return pi[-1]
