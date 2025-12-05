--# -path=../magma:../formulae:../lexica:../other

concrete CoverageTestGrammarEng of CoverageTestGrammar = DollarMathEng, TestCoverageLexiconEng ** open ParadigmsEng in {
    lin
        prefix_arg_adj f a = lin A {s = adj_table_prefix f.s a.s; isPre = a.isPre; isMost = a.isMost};
        prefix_arg_noun f n = mkN f.s n;

        statement_enum_placeholder = lin S {s = "STATEMENT_ENUM_PLACEHOLDER"};
}
