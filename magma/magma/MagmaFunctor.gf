incomplete concrete MagmaFunctor of Magma = open MagmaUtils, Syntax, Grammar, Symbolic, Extend, ParamX in {
    lincat
        Conjunction = Syntax.Conj;
        Subjunction = Syntax.Subj;
        Quantification = _Quantification;
        Statement = S;
        TopStatement = Utt;
        FurthermoreMarker = {s: Str};
        Polarity = Pol;
        Definition = S;
        DefCore = S;
        Sentence = {s: Str};
        Kind = _Kind;
        NamedKind = _NamedKind;
        Term = {np: NP; just_formula: Bool};
        Property = AP;
        Predicate = Grammar.VP;

        -- identifiers
        Identifier = _Ident;
        Identifiers = _Ident;   -- can reuse type
        IdentifierList = {tail: Str; head: Str };   

        -- declarations
        Declaration = Utt;
        DeclarationList = {head: Str; tail: Str };

    lin
        -- polarities
        positive_pol = positivePol;
        negative_pol = negativePol;

        -- conjunctions/subjunctions
        and_conj = and_Conj;
        or_conj = or_Conj;

        if_subj = if_Subj;

        -- identifiers
        no_idents_sg = {s = ""; num = Sg};
        no_idents_pl = {s = ""; num = Pl};
        BaseIdentifierList id1 id2 = {head = id1.s; tail = id2.s};
        ConsIdentifierList id il = {head = id.s; tail = il.tail ++ "," ++ il.head};
        finalizeIdentifierList il = {
            s = il.tail ++ _and_str ++ il.head;
            num = Pl  -- lists are always plural
        };
        finalizeIdentifierList_v1 il = { s = il.tail ++ "," ++ il.head; num = Pl };
        single_identifier id = {s = id.s; num = id.num};

        -- kinds/named kinds
        name_kind k i = {cn = mkCN (mkCN k.cn (symb i.s)) k.adv; num = i.num};
        nkind_that_is_property nk pol pp = {cn = mkCN nk.cn (mkRS pol (mkRCl IdRP pp)); num = nk.num};

        -- terms
        quantified_nkind q nk = {
            np = DetCN ( case nk.num of { Sg => q.sg; Pl => q.pl }) nk.cn;
            just_formula = False
        };
        it_term = {np = it_NP; just_formula = False};

        -- quantifications
        existential_quantification = mkQuantification aSg_Det aPl_Det;

        -- universal_quantification_sg = ;

        -- properties

        -- predicates

        -- definitions
        define_nkind_as_nkind_v2 nk1 nk2 = mkS (mkCl (indef_nk nk1) (indef_nk nk2));

        plain_defcore dc = dc;
        defcore_iff_stmt dc s = my_ssubjs dc _iff_subj s;
        defcore_iff_stmt_v1 dc s = my_ssubjs dc _iff_subj_v1 s;
        defcore_if_stmt dc s = my_ssubjs dc _if_subj s;

        -- statements
        conj_stmt c s1 s2 = mkS c s1 s2;
        subj_stmt ssubj s1 s2 = my_ssubjs s1 ssubj s2;

        exists_nkind nk = mkS (mkCl (indef_nk nk));
        exists_nkind_v1 nk = mkS (ExistsNP (indef_nk nk));

        term_has_nkind_stmt t nk = mkS (mkCl t.np have_V2 (indef_nk nk));
        term_is_property_stmt t p = mkS (mkCl t.np p);
        term_is_term_stmt t1 t2 = mkS (mkCl t1.np t2.np);
        term_predicate_stmt t pred = mkS (mkCl t.np pred);

        -- declarations
        let_kind_decl i nk = ImpP3 (symb i.s) (mkVP (Syntax.mkNP (indefart nk.num) nk.cn));
        let_kind_def_decl i nk = ImpP3 (symb i.s) (mkVP (Syntax.mkNP (defart nk.num) nk.cn));
        let_property_decl i p = ImpP3 (symb i.s) (mkVP p);
        BaseDeclarationList d1 d2 = {head = d1.s; tail = d2.s};
        ConsDeclarationList d dl = {head = d.s; tail = dl.tail ++ "," ++ d.s};
        ConsDeclarationList_v1 d dl = {head = d.s; tail = dl.tail ++ _and_str ++ d.s};
        furthermore_decl marker d = lin Utt {s = marker.s ++ d.s};

        -- sentences
        stmt_sentence s = {s = {- CAPIT ++ -} (mkUtt s).s ++ "."};
        def_sentence d = {s = {- CAPIT ++ -} (mkUtt d).s ++ "."};
        declaration_sentence a = {s = {- CAPIT ++ -} a.s ++ "."};
        declaration_list_sentence dl = {s = dl.tail ++ _and_str ++ dl.head ++ "."};
        declaration_list_sentence_v2 dl = {s = dl.tail ++ "," ++ dl.head ++ "."};
        topstmt_sentence ts = {s = (mkUtt ts).s ++ "."};
}
