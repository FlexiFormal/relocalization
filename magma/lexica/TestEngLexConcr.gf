concrete TestEngLexConcr of TestEngLex = FreeArgsEng ** open MDictEng, ParadigmsEng, SyntaxEng, GrammarEng in {
    lin
        lex_argmark_by = mkPrep "by";
        lex_argmark_of = mkPrep "of";
        lex_argmark_from = mkPrep "from";
        lex_argmark_to = mkPrep "to";
        lex_argmark_onto = mkPrep "onto";
        lex_argmark_under = mkPrep "under";
        -- lex_argmark_invis = mkPrep "";

        lex_integer = mkCN dict_integer_N;
        lex_element = mkCN dict_element_N;
        lex_path = mkCN dict_path_N;
        lex_walk = mkCN dict_walk_N;
        lex_sequence = mkCN dict_sequence_N;
        lex_edge = mkCN dict_edge_N;
        lex_node = mkCN dict_node_N;
        lex_state = mkCN dict_state_N;
        lex_transition = mkCN dict_transition_N;
        lex_pair = mkCN dict_pair_N;
        lex_set = mkCN dict_set_N;
        lex_model = mkCN dict_model_N;
        lex_formula = mkCN dict_formula_N;
        lex_proposition = mkCN dict_proposition_N;
        lex_subset = mkCN dict_subset_N;
        lex_function = mkCN dict_function_N;
        lex_class = mkCN dict_class_N;
        lex_subclass = mkCN dict_subclass_N;
        lex_intersection = mkCN dict_intersection_N;
        lex_object = mkCN dict_object_N;
        lex_union = mkCN dict_union_N;
        lex_difference = mkCN dict_difference_N;
        lex_family = mkCN dict_family_N;
        lex_map = mkCN dict_map_N;
        lex_domain = mkCN dict_domain_N;
        lex_value = mkCN dict_value_N;
        lex_powerset = mkCN dict_powerset_N;

        lex_finite = mkAP dict_finite_A;
        lex_even = mkAP dict_even_A;
        lex_positive = mkAP dict_positive_A;
        lex_divisible = mkAP dict_divisible_A;
        lex_countable = mkAP dict_countable_A;
        lex_consistent = mkAP dict_consistent_A;
        lex_derivable = mkAP dict_derivable_A;
        lex_equal = mkAP dict_equal_A;
        lex_empty = mkAP dict_empty_A;
        lex_disjoint = mkAP dict_disjoint_A;

        lex_divide = dict_divide_V;
        lex_map_V = dict_map_V;
        lex_surject = dict_surject_V;
}
