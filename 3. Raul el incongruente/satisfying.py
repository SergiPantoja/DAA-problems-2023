from logic import logic

def unit_clause(formula):
    if formula is None:
        return []

    unit_clauses = []
    for clause in formula:
        if len(clause) == 1:
            unit_clauses.append(clause[0])

    if not unit_clauses:
        return []

    else:
        return unit_clauses

def satisfying_converter(formula):
    form = []
    for i in formula:
        f = []
        for j in i:
            x = False if(j.val) else True
            f.append([j.var, x])
        form.append(f)
    return satisfying_assignment(form)

def satisfying_assignment(formula):
    {}

    if formula == []:
        return {}

    if [] in formula:
        return None

    soln = {}
    unit_clauses = unit_clause(formula)

    while unit_clauses:
        for literal in unit_clauses:
            formula = help_update(formula, (literal[0], literal[1]))
            
            if [] in formula:
                return None

            soln.setdefault(literal[0], literal[1])
            
            if formula == []:
                return soln

        unit_clauses = unit_clause(formula)

    literal = formula[0][0]

    if literal[1] is True:
        switch_bool = False
    else:
        switch_bool = True

    nu_form = help_update(formula, literal)
    nu_form2 = help_update(formula, (literal[0], switch_bool))

    rec = satisfying_assignment(nu_form)
    if rec is not None:
        soln.update({literal[0]: literal[1]})
        return soln | rec

    rec2 = satisfying_assignment(nu_form2)
    if rec2 is not None:
        soln.update({literal[0]: switch_bool})
        return soln | rec2

    return None

def help_update(formula, literal):

    new_formula = []
    for chain in formula:
        new_chain = []
        literal_found = False
        for statement in chain:

            if literal in chain:
                literal_found = True

            elif statement[0] == literal[0]:
                continue

            new_chain.append(statement)

        if not literal_found:
            new_formula.append(new_chain)

    return new_formula