concrete MagmaEng of Magma = MagmaFunctor - [term_is_not_property_stmt] with 
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

        not_ap_table : (Agr => Str) -> (Agr => Str) = \t -> table { a => "not" ++ t!a };


    lin
        negative_pol = lin Pol {s = [] ; p = CNeg True};
        negative_pol_v1 = lin Pol {s = [] ; p = CNeg False};

        iff_subj = lin Subjunction _iff_subj;
        iff_subj_v1 = lin Subjunction _iff_subj_v1;
        where_subj = lin Subjunction (mkSubj "where");
        where_subj_v1 = lin Subjunction (mkSubj ", where");
        where_subj_v2 = lin Subjunction (mkSubj "with");

        if_then_stmt s1 s2 = mkS (mkConj "if" ", then" singular) s1 s2;
        if_then_stmt_v1 s1 s2 = mkS (mkConj "if" "then" singular) s1 s2;
        if_then_stmt_v2 s1 s2 = mkS (mkConj "when" "," singular) s1 s2;
        if_then_stmt_v3 s1 s2 = mkS (mkConj "when" "" singular) s1 s2;
        if_then_stmt_v4 s1 s2 = mkS (mkConj "if" "," singular) s1 s2;

        statement_enum_as_stmt_v1 se = mkS (ParadigmsEng.mkAdv ":") se;  -- prepend colon - this is a bit of a hack, but works well (think "A = B iff: 1. ... 2. ...")

        -- oxford comma
        finalizeIdentifierList_v2 il = { s = il.tail ++ ", and" ++ il.head; num = Pl };
        
        such_that_named_kind nk s = {cn = mkCN nk.cn (lin Adv {s = "such that" ++ s.s}); num = nk.num};
        -- such_that_named_kind_v1 nk s = {cn = mkCN nk.cn (lin Adv {s = "where" ++ s.s}); num = nk.num};
        -- such_that_named_kind_v2 nk s = {cn = mkCN nk.cn (lin Adv {s = "with" ++ s.s}); num = nk.num};


        existential_quantification_v1 = mkQuantification someSg_Det aPl_Det;
        universal_quantification = mkQuantification every_Det all_Det;
        universal_quantification_v1 = mkQuantification all_Det all_Det;
        universal_quantification_v2 = mkQuantification (mkDeterminer singular "any") (mkDeterminer plural "any");
        universal_quantification_v3 = mkQuantification (mkDeterminer singular "each") all_Det;
        definite_quantification = mkQuantification theSg_Det thePl_Det;

        let_ident_decl id = lin Utt { s = "let" ++ id.s } ;
        let_such_that id stmt = lin Utt { s = "let" ++ id.s ++ "be such that" ++ stmt.s } ;
        let_such_that_v1 id stmt = lin Utt { s = "let" ++ id.s ++ "where" ++ stmt.s } ;
        let_such_that_v2 id stmt = lin Utt { s = "let" ++ id.s ++ "with" ++ stmt.s } ;
        fix_ident_decl id = lin Utt { s = "fix" ++ id.s } ;
        fix_nkind_decl nk = lin Utt { s = "fix" ++ (mkUtt (Syntax.mkNP (indefart nk.num) nk.cn)).s } ;

        
        term_is_not_property_stmt t p = mkS (mkCl t.np (lin AP {s = not_ap_table p.s; isPre = p.isPre}));
        term_is_not_property_stmt_v1 t p = mkS negativePol (mkCl t.np p);

        stmt_for_term stmt term = lin S {s = stmt.s ++ (PrepNP (mkPrep "for") term.np).s};
        stmt_for_term_v1 stmt term = lin S {s = (PrepNP (mkPrep "for") term.np).s ++ "," ++ stmt.s};

        therefore_stmt stmt = lin Utt {s = "therefore" ++ "," ++ stmt.s};
        therefore_stmt_v1 stmt = lin Utt {s = "therefore" ++ stmt.s};
        therefore_stmt_v2 stmt = lin Utt {s = "hence" ++ stmt.s};
        therefore_stmt_v3 stmt = lin Utt {s = "hence" ++ "," ++ stmt.s};
        therefore_stmt_v4 stmt = lin Utt {s = "it follows that" ++ stmt.s};
        therefore_stmt_v5 stmt = lin Utt {s = "thus" ++ stmt.s};
        therefore_stmt_v6 stmt = lin Utt {s = "thus" ++ "," ++ stmt.s};
        therefore_stmt_v7 stmt = lin Utt {s = "then" ++ stmt.s}; -- is it really semantically equivalent?
        therefore_stmt_v8 stmt = lin Utt {s = "then" ++ "," ++ stmt.s};
        therefore_stmt_v9 stmt = lin Utt {s = "as a consequence" ++ "," ++ stmt.s};

        specifically_stmt stmt = lin Utt {s = "specifically" ++ "," ++ stmt.s};
        specifically_stmt_v1 stmt = lin Utt {s = "in particular" ++ "," ++ stmt.s};
        more_precisely_stmt stmt = lin Utt {s = "more precisely" ++ "," ++ stmt.s};

        furthermore_stmt marker stmt = lin Utt {s = marker.s ++ stmt.s};

        furthermore_marker = {s = "furthermore" ++ "," ++ " "};
        furthermore_marker_v1 = {s = "in addition" ++ "," ++ " "};
        furthermore_marker_v2 = {s = "additionally" ++ "," ++ " "};
        furthermore_marker_v3 = {s = "moreover" ++ "," ++ " "};
        furthermore_marker_v4 = {s = "further" ++ "," ++ " "};

        indeed_stmt stmt = lin Utt {s = "indeed" ++ "," ++ stmt.s};
        indeed_stmt_v1 stmt = lin Utt {s = "in fact" ++ "," ++ stmt.s};

        assume_stmt stmt = lin Utt {s = "assume" ++ stmt.s};
        assume_stmt_v1 stmt = lin Utt {s = "suppose" ++ stmt.s};
        assume_stmt_v2 stmt = lin Utt {s = "assume that" ++ stmt.s};
        assume_stmt_v3 stmt = lin Utt {s = "suppose that" ++ stmt.s};

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

        define_ident_kind id k = mkS (mkCl we_NP (mkVP (mkVP _call_V2 (symb id.s)) (term_to_adv (mkNP (indefart id.num) (kind2CN  k)))));

        -- sentences
        declaration_list_sentence_v1 dl = {s = dl.tail ++ "," ++ "and" ++ dl.head ++ "."};
}
