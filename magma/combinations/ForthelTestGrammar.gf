--# -path=../magma:../formulae:../lexica

abstract ForthelTestGrammar = TestEngLex ** {
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

        -- MINI NOTATION LEXICON
        id_v0 : ForthelIdentifier;
        id_v1 : ForthelIdentifier;
        id_v2 : ForthelIdentifier;
        id_v3 : ForthelIdentifier;
        id_v4 : ForthelIdentifier;
        id_v5 : ForthelIdentifier;
        id_M : ForthelIdentifier;
        id_N : ForthelIdentifier;
        id_f : ForthelIdentifier;
        id_n : ForthelIdentifier;
        id_z : ForthelIdentifier;

        notation_times : ForthelTerm -> ForthelTerm -> ForthelTerm;
        notation_brackets_image : ForthelTerm -> ForthelTerm -> ForthelTerm;
        notation_bijection : ForthelTerm -> ForthelTerm -> ForthelTerm -> ForthelStmt; -- at least I think it's bijection

        -- language lexicon

        lex_set_difference: PreKind;
        lex_ordered_pair: PreKind;
}
