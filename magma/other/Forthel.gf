--# -path=../magma:../lexica

abstract Forthel = SigArgs ** {
    cat
        -- FORMULAE
        ForthelIdentifier;
        ForthelTerm;
        ForthelStmt;
        RestrictedIdentifier;   -- n∈N, k, ... (restriction is optional)
    
    fun
        bracketed_stmt: Statement -> Statement;

        -- SPECIFIC PHRASES
        the_thesis_holds_stmt : Statement;
        falsity_holds_stmt : Statement;

        -- FORMULAE
        cast_identifier : ForthelIdentifier -> Identifier;
        cast_term : ForthelTerm -> Term;
        cast_stmt : ForthelStmt -> Statement;
        identifier_term : ForthelIdentifier -> ForthelTerm;
        cast_restricted_identifier : ForthelIdentifier -> RestrictedIdentifier;
        restricted_identifier_to_named_kind : RestrictedIdentifier -> NamedKind;
}

