--# -path=../magma
abstract OpaqueFormulae = Magma ** {
    cat
        -- formulae can only be constructed in MAGMa extensions
        Formula;
    
    fun
        formula_ident : Formula -> Identifier;
        formula_named_kind : Formula -> NamedKind;    -- as in "iff there is some n∈N such that ..."
        formula_term : Formula -> Term;
        formula_stmt : Formula -> Statement;
}
