abstract TestEngLex = FreeArgs ** {
    fun
        lex_argmark_by : ArgMarker;
        lex_argmark_of : ArgMarker;
        lex_argmark_from : ArgMarker;
        lex_argmark_invis : ArgMarker;

        lex_integer : PreKind;
        lex_element : PreKind;
        lex_path : PreKind;
        lex_walk : PreKind;
        lex_sequence : PreKind;
        lex_edge : PreKind;
        lex_node : PreKind;
        lex_state : PreKind;
        lex_transition : PreKind;
        lex_pair : PreKind;
        lex_set : PreKind;
        lex_model : PreKind;
        lex_formula : PreKind;
        lex_proposition : PreKind;

        lex_finite : Property;
        lex_even : Property;
        lex_positive : Property;
        lex_divisible : Property;
        lex_countable : Property;
        lex_consistent : Property;
        lex_derivable : Property;

        lex_divide : Predicate;
}
