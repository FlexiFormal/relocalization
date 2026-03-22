abstract TestEngLex = FreeArgs ** {
    fun
        lex_argmark_by : ArgMarker;
        lex_argmark_of : ArgMarker;
        lex_argmark_from : ArgMarker;
        lex_argmark_to : ArgMarker;
        lex_argmark_onto : ArgMarker;
        lex_argmark_under : ArgMarker;
        -- lex_argmark_invis : ArgMarker;

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
        lex_subset : PreKind;
        lex_function : PreKind;
        lex_class : PreKind;
        lex_subclass : PreKind;
        lex_intersection : PreKind;
        lex_object : PreKind;
        lex_union : PreKind;
        lex_difference : PreKind;
        lex_family : PreKind;
        lex_map : PreKind;
        lex_domain : PreKind;
        lex_value : PreKind;
        lex_powerset : PreKind;

        lex_finite : Property;
        lex_even : Property;
        lex_positive : Property;
        lex_divisible : Property;
        lex_countable : Property;
        lex_consistent : Property;
        lex_derivable : Property;
        lex_equal : Property;
        lex_empty : Property;
        lex_disjoint : Property;

        lex_divide : PrePredicate;
        lex_map_V : PrePredicate;
        lex_surject : PrePredicate;
}
