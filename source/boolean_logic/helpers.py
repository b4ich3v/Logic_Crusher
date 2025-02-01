def add_polynomials(polynomial1, polynomial2):
    """
    Returns the XOR-based addition (symmetric difference)
    of two Zhegalkin polynomials.
    """
    return polynomial1.symmetric_difference(polynomial2)

def multiply_polynomials(polynomial1, polynomial2):
    """
    Returns the product of two Zhegalkin polynomials,
    where monomials are combined via XOR.
    """
    result = set()

    for m1 in polynomial1:
        for m2 in polynomial2:
            product_monom = m1 ^ m2

            if product_monom in result:
                result.remove(product_monom)
            else:
                result.add(product_monom)

    return result

def monomial_to_str(monomial, variables):
    """
    Convert a monomial bitmask into a string representation,
    e.g. 011 -> "A*B" if variables=['A','B','C'].
    """
    terms = []

    for i, var in enumerate(variables):
        if (monomial & (1 << i)) != 0: 
            terms.append(var)
    if not terms:
        return "1"
    return "*".join(terms)

def zhegalkin_polynomial_to_str(polynomial, variables):
    """
    Convert a Zhegalkin polynomial (set of monomial bitmasks)
    into a human-readable string using '+' for XOR.
    """
    if not polynomial:
        return "0"
    terms = [monomial_to_str(m, variables) for m in polynomial]
    
    return " + ".join(terms)
