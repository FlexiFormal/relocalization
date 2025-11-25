concrete SigTestLexiconGer of SigTestLexicon = SigArgsGer ** open MagmaUtilsGer, ConstructorsGer, ParadigmsGer, SyntaxGer, Prelude in {
    -- TODO: different prepositions for formula/non-formula arguments.
    -- (e.g. "Teilmenge der Menge" vs. "Teilmenge von S")
    -- or "Funtion von X nach Y" vs. "Funktion der Menge X in die Menge Y"
    oper
        mkKind2: CN -> (Bool => MiniPrep) -> Kind2 = \cn, prep1 -> lin Kind2 {
            cn = cn;
            prep1 = prep1
        };

        mkKind3: CN -> (Bool => MiniPrep) -> (Bool => MiniPrep) -> Kind3 = \cn, prep1, prep2 -> lin Kind3 {
            cn = cn;
            prep1 = prep1;
            prep2 = prep2
        };

        mkMP: Str -> Case -> MiniPrep = \s, c -> lin MiniPrep { s = s; c = c };
        mkMPTable : Str -> Case -> Str -> Case -> (Bool => MiniPrep) = \s1, c1, s2, c2 -> table {
            False => mkMP s1 c1;
            True  => mkMP s2 c2
        };

        gen_von_MP = mkMPTable "" genitive "von" dative;
        von_MP = mkMPTable "von" dative "von" dative;
        nach_MP = mkMPTable "in" dative "nach" dative;
    lin
        integer = mkKind (mkCN (mkA "ganz") (mkN "Zahl" feminine));
        subset = mkKind2 (mkCN (mkN "Teilmenge" feminine)) gen_von_MP;
        function = mkKind3 (mkCN (mkN "function")) von_MP nach_MP;
}
