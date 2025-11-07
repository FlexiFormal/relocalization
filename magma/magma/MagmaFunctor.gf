incomplete concrete MagmaFunctor of Magma = MagmaFormulaConcr ** open Syntax, Grammar, Symbolic, Extend in {
    oper
        _Kind = {cn: CN; adv: Adv};   -- inspired by Aarne's new grammar
        _Ident = {s: Str; num: Number};

        mergeAdv : Adv -> Adv -> Adv = \a,b -> lin Adv {s = a.s ++ b.s};

        empty_Adv : Adv = lin Adv {s = ""};
        mkKind = overload {
            mkKind : CN -> _Kind = \cn -> {cn = cn; adv = empty_Adv};
            mkKind : N -> _Kind = \n -> {cn = mkCN n; adv = empty_Adv};
        };

        kind2CN : _Kind -> CN = \k -> mkCN k.cn k.adv;

        indefart : Number -> Det = \num -> case num of {
            Sg => a_Det;
            Pl => aPl_Det
        };

        mkQuantification : Det -> Det -> Quantification = \sgDet, plDet -> lin Quantification { sg = sgDet; pl = plDet };
    lincat
        Conj = Conj;
        Quantification = { sg: Det; pl: Det };    -- sg if it refers to singular object; can be "some (integer n)" or "all (integers n)"
        Stmt = S;
        Polarity = Pol;
        Def = S;
        DefCore = S;
        Formula = {s: Str};
        Sentence = {s: Str};
        PreKind = CN;
        Kind = _Kind;
        NamedKind = {cn: CN; num: Number};
        Term = NP;
        Ident = _Ident;
        Property = AP;
        ArgMarker = Prep;
        Predicate = VP;

    lin
        -- polarities
        positive_pol = positivePol;
        negative_pol = negativePol;

        -- conjunctions
        and_conj = and_Conj;
        or_conj = or_Conj;
        if_then_conj = if_then_Conj;

        -- identifiers
        no_ident = {s = ""; num = Sg};
        no_idents = {s = ""; num = Pl};
        math_ident m = {s = m.s; num = Sg};

        -- prekinds/kinds/named kinds
        prekind_to_kind pk = mkKind pk;
        name_kind k i = {cn = mkCN (mkCN k.cn (symb i.s)) k.adv; num = i.num};
        property_prekind pp pk = mkCN pp pk;
        kind_with_arg k am t = {
            cn = k.cn;
            adv = mergeAdv k.adv (PrepNP am t);
        };
        formula_named_kind m = { cn = lin CN {
            s = table { _ => table { _ => m.s } };
            g = Neutr
        }; num = Sg };
        nkind_that_is_property nk pol pp = {cn = mkCN nk.cn (mkRS pol (mkRCl IdRP pp)); num = nk.num};

        -- terms
        quantified_nkind q nk = DetCN (
            case nk.num of {
                Sg => q.sg;
                Pl => q.pl
            }
        ) nk.cn;
        math_term m = symb m.s;
        plural_term nk = DetCN aPl_Det nk.cn;

        -- quantifications
        existential_quantification = mkQuantification aSg_Det aPl_Det;

        -- universal_quantification_sg = ;

        -- properties
        property_with_arg p am t = AdvAP p (PrepNP am t);

        -- definitions
        define_nkind_as_nkind nk1 nk2 = mkS (mkCl (DetCN (indefart nk1.num) nk1.cn) (DetCN (indefart nk2.num) nk2.cn));

        plain_defcore dc = dc;
        defcore_iff_stmt dc s = mkS iff_conj dc s;
        defcore_iff_stmt_v1 dc s = mkS iff_conj_v1 dc s;
        defcore_if_stmt dc s = mkS if_conj dc s;

        -- statements
        conj_stmt c s1 s2 = mkS c s1 s2;

        formula_stmt m = lin S {s = m.s};
        exists_nkind nk = mkS (mkCl (DetCN (indefart nk.num) nk.cn));
        exists_nkind_v1 nk = mkS (ExistsNP (DetCN (indefart nk.num) nk.cn));

        term_has_nkind_stmt t nk = mkS (mkCl t have_V2 (DetCN (indefart nk.num) nk.cn));
        term_is_property_stmt t p = mkS (mkCl t p);
        term_is_term_stmt t1 t2 = mkS (mkCl t1 t2);
        term_predicate_stmt t pred = mkS (mkCl t pred);

        let_kind_stmt i nk = lin S { s = (ImpP3 (symb i.s) (mkVP (mkNP (indefart nk.num) nk.cn))).s };

        -- sentences
        fin_stmt s = {s = {- CAPIT ++ -} s.s ++ "."};
        def_sentence d = {s = {- CAPIT ++ -} d.s ++ "."};
}
