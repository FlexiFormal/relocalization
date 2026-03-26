resource ForthelOpersEng = open SigArgsEng, CatEng, ParadigmsEng, ResEng, ConstructorsEng in {
    oper
        mkKind: CN -> Kind = \cn -> lin Kind {
            cn = cn;
            adv = lin Adv { s = "" };
        };

        mkKind2: CN -> Prep -> Kind2 = \cn, prep1 -> lin Kind2 {
            cn = cn;
            prep1 = prep1;
        };

        mkKind3: CN -> Prep -> Prep -> Kind3 = \cn, prep1, prep2 -> lin Kind3 {
            cn = cn;
            prep1 = prep1;
            prep2 = prep2;
        };

        mkProperty2 : AP -> Prep -> Property2 = \ap, prep1 -> lin Property2 {
            ap = ap;
            prep1 = prep1;
        };

        mkPredicate : VP -> Predicate = \vp -> vp;

        mkPredicate2 : VP -> Prep -> Predicate2 = \vp, prep1 -> lin Predicate2 {
            vp = vp;
            prep1 = prep1;
        };

        mkPredicate3 : VP -> Prep -> Prep -> Predicate3 = \vp, prep1, prep2 -> lin Predicate3 {
            vp = vp;
            prep1 = prep1;
            prep2 = prep2;
        };

        _compound_noun : N -> N -> N = \n1,n2 -> mkN (n1.s ! Sg ! Nom) n2;

        -- mkCN : N -> N -> CN = \n1,n2 -> mkCN (_compound_noun n1 n2);
        makeCN = overload {
            makeCN : A -> N -> CN = \a, n -> mkCN a n;
            makeCN : N -> CN = \n -> mkCN n;
            makeCN : N -> N -> CN = \n1, n2 -> mkCN (_compound_noun n1 n2)
        };

        of_Prep : Prep = mkPrep "of";
        to_Prep : Prep = mkPrep "to";
        from_Prep : Prep = mkPrep "from";
        under_Prep : Prep = mkPrep "under";
        noprep_Prep : Prep = mkPrep "";
        onto_Prep : Prep = mkPrep "onto";

}
