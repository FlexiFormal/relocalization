incomplete concrete MagmaFunctor of Magma = open MagmaUtils, Syntax, Grammar, Symbolic, Extend in {
    lincat
        Conj = Conj;
        Quantification = _Quantification;
        Stmt = S;
        Polarity = Pol;
        Def = S;
        Assumption = S;
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

        -- kinds/named kinds
        name_kind k i = {cn = mkCN (mkCN k.cn (symb i.s)) k.adv; num = i.num};
        nkind_that_is_property nk pol pp = {cn = mkCN nk.cn (mkRS pol (mkRCl IdRP pp)); num = nk.num};

        -- terms
        quantified_nkind q nk = DetCN (
            case nk.num of {
                Sg => q.sg;
                Pl => q.pl
            }
        ) nk.cn;
        plural_term nk = DetCN aPl_Det nk.cn;

        -- quantifications
        existential_quantification = mkQuantification aSg_Det aPl_Det;

        -- universal_quantification_sg = ;

        -- properties

        -- predicates

        -- definitions
        define_nkind_as_nkind nk1 nk2 = mkS (mkCl (DetCN (indefart nk1.num) nk1.cn) (DetCN (indefart nk2.num) nk2.cn));

        plain_defcore dc = dc;
        defcore_iff_stmt dc s = mkS iff_conj dc s;
        defcore_iff_stmt_v1 dc s = mkS iff_conj_v1 dc s;
        defcore_if_stmt dc s = mkS if_conj dc s;

        -- statements
        conj_stmt c s1 s2 = mkS c s1 s2;

        exists_nkind nk = mkS (mkCl (DetCN (indefart nk.num) nk.cn));
        exists_nkind_v1 nk = mkS (ExistsNP (DetCN (indefart nk.num) nk.cn));

        term_has_nkind_stmt t nk = mkS (mkCl t have_V2 (DetCN (indefart nk.num) nk.cn));
        term_is_property_stmt t p = mkS (mkCl t p);
        term_is_term_stmt t1 t2 = mkS (mkCl t1 t2);
        term_predicate_stmt t pred = mkS (mkCl t pred);

        -- declaration
        let_kind_decl i nk = lin S { s = (ImpP3 (symb i.s) (mkVP (mkNP (indefart nk.num) nk.cn))).s };

        -- sentences
        stmt_sentence s = {s = {- CAPIT ++ -} s.s ++ "."};
        def_sentence d = {s = {- CAPIT ++ -} d.s ++ "."};
        declaration_sentence a = {s = {- CAPIT ++ -} a.s ++ "."};
}
