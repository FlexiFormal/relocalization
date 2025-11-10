concrete TestEngLexConcr of TestEngLex = FreeArgsEng ** open MDictEng, ParadigmsEng, SyntaxEng, GrammarEng in {
    lin
        lex_argmark_by = mkPrep "by";
        lex_argmark_of = mkPrep "of";
        lex_argmark_from = mkPrep "from";
        lex_argmark_invis = mkPrep "";

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

        lex_finite = mkAP dict_finite_A;
        lex_even = mkAP dict_even_A;
        lex_positive = mkAP dict_positive_A;
        lex_divisible = mkAP dict_divisible_A;
        lex_countable = mkAP dict_countable_A;
        lex_consistent = mkAP dict_consistent_A;
        lex_derivable = mkAP dict_derivable_A;

        lex_divide = mkVP dict_divide;
}
