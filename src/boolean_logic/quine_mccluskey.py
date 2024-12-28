def quine_mccluskey(minterms, num_vars, dont_cares=None):
    if dont_cares is None:
        dont_cares = []

    all_terms = minterms + dont_cares

    groups = {}
    for term in all_terms:
        ones = bin(term).count("1")
        groups.setdefault(ones, []).append(f"{term:0{num_vars}b}")

    prime_implicants = set()
    next_groups = groups

    while True:
        new_groups = {}
        checked = set()
        group_keys = sorted(next_groups.keys())
        for i in range(len(group_keys)-1):
            group1 = next_groups[group_keys[i]]
            group2 = next_groups[group_keys[i+1]]
            for term1 in group1:
                for term2 in group2:
                    diff = sum(c1 != c2 for c1, c2 in zip(term1, term2))
                    if diff == 1:
                        idx = next(idx for idx, (c1, c2) in enumerate(zip(term1, term2)) if c1 != c2)
                        combined = term1[:idx] + "-" + term1[idx+1:]
                        new_groups.setdefault(i, []).append(combined)
                        checked.add(term1)
                        checked.add(term2)

        leftover = []
        for group in next_groups.values():
            for term in group:
                if term not in checked:
                    leftover.append(term)
        prime_implicants.update(leftover)

        if not new_groups:
            break
        next_groups = {}
        unique_terms = set()
        for terms in new_groups.values():
            for term in terms:
                unique_terms.add(term)

        for term in unique_terms:
            ones = term.count("1")
            next_groups.setdefault(ones, []).append(term)

    essential_prime_implicants = find_essential_prime_implicants_with_dont_cares(prime_implicants, minterms, num_vars)
    return essential_prime_implicants

def find_essential_prime_implicants_with_dont_cares(prime_implicants, minterms, num_vars):
    def matches(prime_implicant, minterm):
        return all(pi == mt or pi == "-" for pi, mt in zip(prime_implicant, minterm))

    bin_minterms = [f'{m:0{num_vars}b}' for m in minterms]
    coverage = {}
    for pi in prime_implicants:
        coverage[pi] = [m for m in bin_minterms if matches(pi, m)]

    essential_pis = set()
    uncovered_minterms = set(bin_minterms)

    for m in bin_minterms:
        covering_pis = [pi for pi, covered in coverage.items() if m in covered]
        if len(covering_pis) == 1:
            essential_pis.add(covering_pis[0])

    for epi in essential_pis:
        for m in coverage[epi]:
            if m in uncovered_minterms:
                uncovered_minterms.remove(m)

    if not uncovered_minterms:
        return essential_pis

    remaining_pis = set(prime_implicants) - essential_pis
    uncovered_minterms = list(uncovered_minterms)

    def covers_all(selected_pis, minterms_to_cover):
        covered = set()
        for pi in selected_pis:
            covered.update(coverage[pi])
        return all(m in covered for m in minterms_to_cover)

    best_solution = None

    def backtrack(chosen, candidates):
        nonlocal best_solution

        if best_solution is not None and len(chosen) >= len(best_solution):
            return

        if covers_all(chosen, uncovered_minterms):
            if best_solution is None or len(chosen) < len(best_solution):
                best_solution = chosen[:]
            return

        if not candidates:
            return

        next_pi = candidates[0]
        chosen.append(next_pi)
        backtrack(chosen, candidates[1:])
        chosen.pop()
        backtrack(chosen, candidates[1:])

    backtrack([], list(remaining_pis))

    if best_solution is None:
        best_solution = list(remaining_pis)

    final_solution = essential_pis.union(best_solution)
    return final_solution

def matches(prime_implicant, minterm):
    return all(pi == mt or pi == "-" for pi, mt in zip(prime_implicant, minterm))