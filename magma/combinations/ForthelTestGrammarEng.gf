--# -path=../magma:../formulae:../lexica

concrete ForthelTestGrammarEng of ForthelTestGrammar = TestEngLexConcr ** open ParamX, SymbolicEng, Prelude, ResEng, GrammarEng, ParadigmsEng, ConstructorsEng in {
    oper

        simple_cn : Str -> CN = \s -> lin CN {s = table { a => table { b => s } }; g = Neutr};
        compound_n : N -> N -> N = \n1,n2 -> mkN (n1.s ! Sg ! Nom) n2;

    lin
        formula_named_kind m = { cn = simple_cn m.s; num = Sg };
    lincat
        ForthelIdentifier = Str;
        ForthelTerm = Str;
        ForthelStmt = Str;
        RestrictedIdentifier = Str;
    lin
        bracketed_stmt stmt = lin S {s = "(" ++ stmt.s ++ ")"};

        the_thesis_holds_stmt = lin S {s = "the thesis holds"};
        falsity_holds_stmt = lin S {s = "falsity holds"};

        -- FORMULAE
        cast_identifier s = {s = s; num = Sg };
        cast_term s = {np = symb s; just_formula = True};
        cast_stmt s = lin S {s = s};
        identifier_term s = s;
        cast_restricted_identifier s = s;

        restricted_identifier_to_named_kind s = { cn = simple_cn s; num = Sg };

        id_v0 = "v0";
        id_v1 = "v1";
        id_v2 = "v2";
        id_v3 = "v3";
        id_v4 = "v4";
        id_v5 = "v5";
        id_M = "M";
        id_N = "N";
        id_f = "f";
        id_n = "n";
        id_z = "z";

        notation_times t1 t2 = t1 ++ "\\times" ++ t2;
        notation_brackets_image t1 t2 = t1 ++ "[" ++ t2 ++ "]";
        notation_bijection t1 t2 t3 = t1 ++ ":" ++ t2 ++ "\\leftrightarrow" ++ t3;

        lex_set_difference = compound_n lex_set lex_difference;
        lex_ordered_pair = mkCN (mkN "ordered pair");
}
