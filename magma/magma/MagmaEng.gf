concrete MagmaEng of Magma = MagmaFunctor with 
        (MagmaUtils = MagmaUtilsEng), (Syntax=SyntaxEng), (Grammar=GrammarEng), (Symbolic=SymbolicEng), (Extend=ExtendEng)
** open ParadigmsEng, ResEng, Prelude, StructuralEng, MorphoEng in {
    oper
        _call_V2 : V2 = mkV2 (mkV "call");
        _say_V : V = mkV "say" "said" "said";
        _say_V2 : V2 = mkV2 (_say_V);

        -- mergeAdv a b = lin Adv {s = a.s ++ b.s};

        called_an_nkind_vp : NamedKind -> VP = \nk -> mkVP (passiveVP _call_V2) (term_to_adv (indef_nk nk));
        said_vp_vp : VP -> VP = \vp -> mkVP (passiveVP _say_V2) (str_adv (infVP VVInf vp False Simul CPos (agrP3 Sg)));
        we_say_that : S -> S = \s -> mkS (mkCl we_NP (mkVS _say_V) s);


    lin
        negative_pol = lin Pol {s = [] ; p = CNeg True};
        negative_pol_v1 = lin Pol {s = [] ; p = CNeg False};

        iff_subj = lin Subjunction _iff_subj;
        iff_subj_v1 = lin Subjunction _iff_subj_v1;

        if_then_stmt s1 s2 = mkS (mkConj "if" ", then" singular) s1 s2;
        if_then_stmt_v1 s1 s2 = mkS (mkConj "if" "then" singular) s1 s2;

        -- oxford comma
        finalizeIdentifierList_v2 il = { s = il.tail ++ ", and" ++ il.head; num = Pl };
        
        such_that_named_kind nk s = {cn = mkCN nk.cn (lin Adv {s = "such that" ++ s.s}); num = nk.num};
        such_that_named_kind_v1 nk s = {cn = mkCN nk.cn (lin Adv {s = "where" ++ s.s}); num = nk.num};
        such_that_named_kind_v2 nk s = {cn = mkCN nk.cn (lin Adv {s = "with" ++ s.s}); num = nk.num};


        existential_quantification_v1 = mkQuantification someSg_Det aPl_Det;
        universal_quantification = mkQuantification every_Det all_Det;
        universal_quantification_v1 = mkQuantification all_Det all_Det;

        let_ident_decl id = lin Utt { s = "let" ++ id.s } ;
        let_such_that id stmt = lin Utt { s = "let" ++ id.s ++ "be such that" ++ stmt.s } ;
        let_such_that_v1 id stmt = lin Utt { s = "let" ++ id.s ++ "where" ++ stmt.s } ;
        let_such_that_v2 id stmt = lin Utt { s = "let" ++ id.s ++ "with" ++ stmt.s } ;


        stmt_for_term stmt term = lin S {s = stmt.s ++ (PrepNP (mkPrep "for") term.np).s};

        therefore_stmt stmt = lin Utt {s = "therefore" ++ "," ++ stmt.s};
        therefore_stmt_v1 stmt = lin Utt {s = "therefore" ++ stmt.s};
        therefore_stmt_v2 stmt = lin Utt {s = "hence" ++ stmt.s};
        therefore_stmt_v3 stmt = lin Utt {s = "hence" ++ "," ++ stmt.s};
        therefore_stmt_v4 stmt = lin Utt {s = "it follows that" ++ stmt.s};
        therefore_stmt_v5 stmt = lin Utt {s = "thus" ++ stmt.s};
        therefore_stmt_v6 stmt = lin Utt {s = "thus" ++ "," ++ stmt.s};
        therefore_stmt_v7 stmt = lin Utt {s = "then" ++ stmt.s}; -- is it really semantically equivalent?
        therefore_stmt_v8 stmt = lin Utt {s = "then" ++ "," ++ stmt.s};

        -- definitions
        define_nkind_as_nkind nk1 nk2 = mkS (mkCl (indef_nk nk1) (called_an_nkind_vp nk2));
        define_nkind_as_nkind_v1 nk1 nk2 = mkS (mkCl (indef_nk nk1) (said_vp_vp (mkVP (indef_nk nk2))));
        define_nkind_as_nkind_v3 nk1 nk2 = we_say_that (mkS (mkCl (indef_nk nk1) (indef_nk nk2)));

        define_nkind_prop nk p = mkS (mkCl (indef_nk nk) (mkVP (passiveVP _call_V2) (property_to_adv p)));
        define_nkind_prop_v1 nk p = mkS (mkCl (indef_nk nk) (said_vp_vp (mkVP p)));
        define_nkind_prop_v2 nk p = mkS (mkCl (indef_nk nk) p);
        define_nkind_prop_v3 nk p = we_say_that (mkS (mkCl (indef_nk nk) p));

        -- for the following: TODO: support plural (probably rarely needed)
        define_ident_prop id p = mkS (mkCl (symb id.s) (mkVP (passiveVP _call_V2) (property_to_adv p)));
        define_ident_prop_v1 id p = mkS (mkCl (symb id.s) (said_vp_vp (mkVP p)));
        define_ident_prop_v2 id p = mkS (mkCl (symb id.s) p);
        define_ident_prop_v3 id p = we_say_that (mkS (mkCl (symb id.s) p));

        define_ident_nkind id nk = mkS (mkCl (symb id.s) (called_an_nkind_vp nk));
        define_ident_nkind_v1 id nk = mkS (mkCl (symb id.s) (said_vp_vp (mkVP (indef_nk nk))));
        define_ident_nkind_v2 id nk = mkS (mkCl (symb id.s) (indef_nk nk));
        define_ident_nkind_v3 id nk = we_say_that (mkS (mkCl (symb id.s) (indef_nk nk)));

        -- sentences
        declaration_list_sentence_v1 dl = {s = dl.tail ++ "," ++ "and" ++ dl.head ++ "."};
}
