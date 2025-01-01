def add_polynomials(polynomial1, polynomial2):
    return polynomial1.symmetric_difference(polynomial2)

def multiply_polynomials(polynomial1, polynomial2):
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
    terms = []

    for i, var in enumerate(variables):
        if (monomial & (1 << i)) != 0: 
            terms.append(var)
    if not terms:
        return "1"
    return "*".join(terms)

def zhegalkin_poly_to_str(polynomial, variables):
    if not polynomial:
        return "0"
    terms = [monomial_to_str(m, variables) for m in polynomial]
    
    return ' + '.join(terms)
