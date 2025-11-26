incomplete concrete MagmaFunctor of Magma = open MagmaUtils, Syntax, Grammar, Symbolic, Extend, ParamX in {
    lincat
        Conjunction = Syntax.Conj;
        Subjunction = Syntax.Subj;
        Quantification = _Quantification;
        Statement = S;
        Polarity = Pol;
        Definition = S;
        DefCore = S;
        Declaration = Utt;
        Sentence = {s: Str};
        Kind = _Kind;
        NamedKind = {cn: CN; num: ParamX.Number};
        Term = {np: NP; just_formula: Bool};
        Identifier = _Ident;
        Property = AP;
        Predicate = Grammar.VP;

    lin
        -- polarities
        positive_pol = positivePol;
        negative_pol = negativePol;

        -- conjunctions/subjunctions
        and_conj = and_Conj;
        or_conj = or_Conj;

        if_subj = if_Subj;
        -- if_then_conj = if_then_Conj;

        -- identifiers
        no_ident = {s = ""; num = Sg};
        no_idents = {s = ""; num = Pl};

        -- kinds/named kinds
        name_kind k i = {cn = mkCN (mkCN k.cn (symb i.s)) k.adv; num = i.num};
        nkind_that_is_property nk pol pp = {cn = mkCN nk.cn (mkRS pol (mkRCl IdRP pp)); num = nk.num};

        -- terms
        quantified_nkind q nk = {
            np = DetCN ( case nk.num of { Sg => q.sg; Pl => q.pl }) nk.cn;
            just_formula = False
        };

        -- quantifications
        existential_quantification = mkQuantification aSg_Det aPl_Det;

        -- universal_quantification_sg = ;

        -- properties

        -- predicates

        -- definitions
        define_nkind_as_nkind nk1 nk2 = mkS (mkCl (DetCN (indefart nk1.num) nk1.cn) (DetCN (indefart nk2.num) nk2.cn));

        plain_defcore dc = dc;
        defcore_iff_stmt dc s = my_ssubjs dc _iff_subj s;
        defcore_iff_stmt_v1 dc s = my_ssubjs dc _iff_subj_v1 s;
        defcore_if_stmt dc s = my_ssubjs dc _if_subj s;

        -- statements
        conj_stmt c s1 s2 = mkS c s1 s2;
        subj_stmt ssubj s1 s2 = my_ssubjs s1 ssubj s2;

        exists_nkind nk = mkS (mkCl (DetCN (indefart nk.num) nk.cn));
        exists_nkind_v1 nk = mkS (ExistsNP (DetCN (indefart nk.num) nk.cn));

        term_has_nkind_stmt t nk = mkS (mkCl t.np have_V2 (DetCN (indefart nk.num) nk.cn));
        term_is_property_stmt t p = mkS (mkCl t.np p);
        term_is_term_stmt t1 t2 = mkS (mkCl t1.np t2.np);
        term_predicate_stmt t pred = mkS (mkCl t.np pred);

        -- declaration
        let_kind_decl i nk = ImpP3 (symb i.s) (mkVP (Syntax.mkNP (indefart nk.num) nk.cn));

        -- sentences
        stmt_sentence s = {s = {- CAPIT ++ -} (mkUtt s).s ++ "."};
        def_sentence d = {s = {- CAPIT ++ -} (mkUtt d).s ++ "."};
        declaration_sentence a = {s = {- CAPIT ++ -} a.s ++ "."};
}
