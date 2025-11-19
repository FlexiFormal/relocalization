concrete SigTestLexiconEng of SigTestLexicon = SigArgsEng ** open MagmaUtilsEng, ConstructorsEng, ParadigmsEng, SyntaxEng in {
    oper
        mkKind2: CN -> Prep -> Kind2 = \cn, prep1 -> lin Kind2 {
            cn = cn;
            prep1 = prep1;
        };

        mkKind3: CN -> Prep -> Prep -> Kind3 = \cn, prep1, prep2 -> lin Kind3 {
            cn = cn;
            prep1 = prep1;
            prep2 = prep2;
        };

        of_Prep : Prep = mkPrep "of";
    lin
        integer = mkKind (mkCN (mkN "integer"));
        subset = mkKind2 (mkCN (mkN "subset")) of_Prep;
        function = mkKind3 (mkCN (mkN "function")) from_Prep to_Prep;
}
