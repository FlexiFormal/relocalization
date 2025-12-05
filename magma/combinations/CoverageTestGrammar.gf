--# -path=../magma:../formulae:../lexica

abstract CoverageTestGrammar = TestCoverageLexicon, DollarMath ** {
    flags
        startcat = Sentence;

    fun
        -- arguments can also (sometimes) be prefixed, especially if they are formulae.
        -- example: "$n$-dimensional"
        -- It is always attached to the word that follows.
        -- So "$n$-dimensional space" is "($n$-dimensional) space", not "$n$-(dimensional space)".
        -- Here we have a quick implementation for that.
        -- While this is not the best place, it's specific to both the fact that we use opaque formulae and that don't have a fixed signature for words.

        prefix_arg_adj : Formula -> Adjective -> Adjective;
        prefix_arg_noun : Formula -> Noun -> Noun;
}
