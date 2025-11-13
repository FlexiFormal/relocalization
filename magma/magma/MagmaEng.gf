concrete MagmaEng of Magma = MagmaFunctor with 
        (MagmaUtils = MagmaUtilsEng), (Syntax=SyntaxEng), (Grammar=GrammarEng), (Symbolic=SymbolicEng), (Extend=ExtendEng)
** open ParadigmsEng, ResEng, Prelude, StructuralEng, MorphoEng in {
    oper
        _call_V2 : V2 = mkV2 (mkV "call");
        _say_V2 : V2 = mkV2 (mkV "say" "said" "said");

        -- mergeAdv a b = lin Adv {s = a.s ++ b.s};

    lin
        negative_pol = lin Pol {s = [] ; p = CNeg True};
        negative_pol_v1 = lin Pol {s = [] ; p = CNeg False};

        iff_conj = lin Conjunction _iff_conj;
        iff_conj_v1 = lin Conjunction _iff_conj_v1;
        if_conj = lin Conjunction _if_conj;
        
        such_that_named_kind nk s = {cn = mkCN nk.cn (lin Adv {s = "such that" ++ s.s}); num = nk.num};
        such_that_named_kind_v1 nk s = {cn = mkCN nk.cn (lin Adv {s = "where" ++ s.s}); num = nk.num};
        such_that_named_kind_v2 nk s = {cn = mkCN nk.cn (lin Adv {s = "with" ++ s.s}); num = nk.num};


        existential_quantification_v1 = mkQuantification someSg_Det aPl_Det;
        universal_quantification = mkQuantification every_Det all_Det;
        universal_quantification_v1 = mkQuantification all_Det all_Det;

        stmt_for_term stmt term = lin S {s = stmt.s ++ (PrepNP (mkPrep "for") term).s};

        -- definitions
        define_nkind_as_nkind_v1 nk1 nk2 = mkS (mkCl (DetCN (indefart nk1.num) nk1.cn) (mkVP (passiveVP _call_V2) (term_to_adv (DetCN (indefart nk2.num) nk2.cn))));

        define_nkind_prop nk p = mkS (mkCl (SyntaxEng.mkNP (indefart nk.num) nk.cn) (mkVP (passiveVP _call_V2) (property_to_adv p)));
        define_nkind_prop_v1 nk p = mkS (mkCl (SyntaxEng.mkNP (indefart nk.num) nk.cn) (mkVP (passiveVP _say_V2) (str_adv (infVP VVInf (mkVP p) False Simul CPos (agrP3 Sg)))));
        define_nkind_prop_v2 nk p = mkS (mkCl (SyntaxEng.mkNP (indefart nk.num) nk.cn) p);

        -- for the following: TODO: support plural (probably rarely needed)
        define_ident_prop id p = mkS (mkCl (symb id.s) (mkVP (passiveVP _call_V2) (property_to_adv p)));
        define_ident_prop_v1 id p = mkS (mkCl (symb id.s) (mkVP (passiveVP _say_V2) (str_adv (infVP VVInf (mkVP p) False Simul CPos (agrP3 Sg)))));
        define_ident_prop_v2 id p = mkS (mkCl (symb id.s) p);
}
