def merge(S1, S2, S):
    i, j = 0, 0
    while i+j < len(S):
        if (j == len(S2)) or (i < len(S1) and S1[i] < S2[j]):
            S[i+j] = S1[i]
            i += 1
        else:
            S[i+j] = S2[j]
            j += 1

def merge_sort(S):
    n = len(S)
    if n < 2:
        return S
    mid = n//2
    S1 = S[:mid]
    S2 = S[mid:]
    merge_sort(S1)
    merge_sort(S2)
    merge(S1, S2, S)

def quick_sort(S):
    if len(S) < 2:
        return
    pivot = S[-1]
    lesser = []
    greater = []
    equal = []
    for element in S:
        if element < pivot:
            lesser.append(element)
        elif element == pivot:
            equal.append(element)
        else:
            greater.append(element)
    quick_sort(lesser)
    quick_sort(greater)
    return lesser + equal + greater

def count_winner(S):
    """Given a sequence of integers with duplicates, return the integer with
    the highest number of duplicates."""
    merge_sort(S)
    counts = {}
    for i in S:
        counts.setdefault(S[i], 0)
        counts[S[i]] += 1
    return max(S, key = lambda key: S[key])
