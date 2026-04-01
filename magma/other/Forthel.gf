--# -path=../magma:../lexica

abstract Forthel = SigArgs ** {
    cat
        -- FORMULAE
        ForthelPlainIdentifier;
        ForthelTerm;
        ForthelStmt;
        ForthelIdentifier;   -- n∈N, k, ... (restriction is optional)
    
    fun
        bracketed_stmt: Statement -> Statement;

        -- SPECIFIC PHRASES
        the_thesis_holds_stmt : Statement;
        falsity_holds_stmt : Statement;

        -- FORMULAE
        cast_identifier : ForthelIdentifier -> Identifier;
        cast_term : ForthelTerm -> Term;
        cast_stmt : ForthelStmt -> Statement;
        identifier_term : ForthelPlainIdentifier -> ForthelTerm;
        cast_restricted_identifier : ForthelPlainIdentifier -> ForthelIdentifier;
        -- restricted_identifier_to_named_kind : ForthelIdentifier -> NamedKind;
}

