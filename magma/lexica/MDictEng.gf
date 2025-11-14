resource MDictEng = open SyntaxEng, ParadigmsEng in {
    oper
        dict_integer_N: N = mkN "integer";
        dict_element_N: N = mkN "element";
        dict_path_N: N = mkN "path";
        dict_walk_N: N = mkN "walk";
        dict_sequence_N: N = mkN "sequence";
        dict_edge_N: N = mkN "edge";
        dict_node_N: N = mkN "node";
        dict_state_N: N = mkN "state";
        dict_transition_N: N = mkN "transition";
        dict_pair_N: N = mkN "pair";
        dict_set_N: N = mkN "set";
        dict_model_N: N = mkN "model";
        dict_formula_N: N = mkN "formula";
        dict_proposition_N: N = mkN "proposition";
        dict_subset_N: N = mkN "subset";

        dict_positive_A: A = mkA "positive";
        dict_even_A: A = mkA "even";
        dict_finite_A: A = mkA "finite";
        dict_divisible_A: A = mkA "divisible";
        dict_countable_A: A = mkA "countable";
        dict_consistent_A: A = mkA "consistent";
        dict_derivable_A: A = mkA "derivable";

        dict_divide: V = mkV "divide";
}
