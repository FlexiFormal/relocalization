--# -path=../magma:../formulae:../lexica

concrete ForthelEng of Forthel = SigArgsEng ** open ParamX, SymbolicEng, Prelude, ResEng, GrammarEng, ParadigmsEng, ConstructorsEng in {
    oper
        simple_cn : Str -> CN = \s -> lin CN {s = table { a => table { b => s } }; g = Neutr};

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
}
