def quine_mccluskey(minterms, num_vars, dont_cares=None):
    """
    Quine-McCluskey algorithm to find prime implicants for given minterms/don't cares.
    """
    if dont_cares is None:
        dont_cares = []

    all_terms = minterms + dont_cares
    groups = {}

    for term in all_terms:
        count_of_ones = bin(term).count("1")
        groups.setdefault(count_of_ones, []).append(f"{term:0{num_vars}b}")

    prime_implicants = set()
    current_groups = groups

    while True:
        new_groups = {}
        checked = set()
        group_keys = sorted(current_groups.keys())

        for group_index in range(len(group_keys)-1):
            group1 = current_groups[group_keys[group_index]]
            group2 = current_groups[group_keys[group_index+1]]

            for term1 in group1:
                for term2 in group2:
                    bit_difference = sum(c1 != c2 for c1, c2 in zip(term1, term2))

                    if bit_difference == 1:
                        bit_position = next(idx for idx, (c1, c2) in enumerate(zip(term1, term2)) if c1 != c2)
                        combined = term1[:bit_position] + "-" + term1[bit_position+1:]
                        new_groups.setdefault(group_index, []).append(combined)
                        checked.add(term1)
                        checked.add(term2)

        leftover_terms = []

        for group in current_groups.values():
            for term in group:
                if term not in checked:
                    leftover_terms.append(term)

        prime_implicants.update(leftover_terms)

        if not new_groups:
            break

        current_groups = {}
        unique_combined_terms = set()

        for terms in new_groups.values():
            for term in terms:
                unique_combined_terms.add(term)

        for term in unique_combined_terms:
            count_of_ones = term.count("1")
            current_groups.setdefault(count_of_ones, []).append(term)

    essential_prime_implicants = find_essential_prime_implicants_with_dont_cares(
        prime_implicants, minterms, num_vars
        )
    return essential_prime_implicants

def find_essential_prime_implicants_with_dont_cares(prime_implicants, minterms, num_vars):
    """
    Identify essential prime implicants, considering don't cares if any.
    """
    def matches_pattern(prime_implicant, minterm):
        return all(
            current_prime_implicant == minterm_bit_state or current_prime_implicant == "-" 
            for current_prime_implicant, minterm_bit_state in zip(prime_implicant, minterm)
        )

    bin_minterms = [f'{minterm_bin:0{num_vars}b}' for minterm_bin in minterms]
    coverage = {}

    for prime_implicant in prime_implicants:
        coverage[prime_implicant] = [
            minterm_bin for minterm_bin in bin_minterms
            if matches_pattern(prime_implicant, minterm_bin)
            ]

    essential_pis = set()
    uncovered_minterms = set(bin_minterms)

    for minterm_bin in bin_minterms:
        covering_pis = [
            current_prime_implicant for current_prime_implicant,
            covered in coverage.items() if minterm_bin in covered
            ]

        if len(covering_pis) == 1:
            essential_pis.add(covering_pis[0])

    for epi in essential_pis:
        for minterm_bin in coverage[epi]:

            if minterm_bin in uncovered_minterms:
                uncovered_minterms.remove(minterm_bin)

    if not uncovered_minterms:
        return essential_pis

    remaining_pis = set(prime_implicants) - essential_pis
    uncovered_minterms = list(uncovered_minterms)

    def covers_all(selected_pis, minterms_to_cover):
        covered = set()
        
        for prime_implicant in selected_pis:
            covered.update(coverage[prime_implicant])

        return all(minterm_bin in covered for minterm_bin in minterms_to_cover)

    best_solution = None

    def backtrack(selected_prime_implicants, candidates):
        nonlocal best_solution

        if best_solution is not None and len(selected_prime_implicants) >= len(best_solution):
            return

        if covers_all(selected_prime_implicants, uncovered_minterms):
            if best_solution is None or len(selected_prime_implicants) < len(best_solution):
                best_solution = selected_prime_implicants[:]
            return

        if not candidates:
            return

        next_prime_implicant = candidates[0]
        selected_prime_implicants.append(next_prime_implicant)
        backtrack(selected_prime_implicants, candidates[1:])
        selected_prime_implicants.pop()
        backtrack(selected_prime_implicants, candidates[1:])

    backtrack([], list(remaining_pis))

    if best_solution is None:
        best_solution = list(remaining_pis)

    final_solution = essential_pis.union(best_solution)
    return final_solution

def matches_pattern(prime_implicant, minterm):
    """
    Matches a prime implicant pattern against a minterm.
    """
    return all(
        current_prime_implicant == mt or current_prime_implicant == "-" 
        for current_prime_implicant, mt in zip(prime_implicant, minterm)
    )
