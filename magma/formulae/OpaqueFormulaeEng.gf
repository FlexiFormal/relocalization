--# -path=../magma
concrete OpaqueFormulaeEng of OpaqueFormulae = MagmaEng ** OpaqueFormulaeFunctor with 
        (Syntax=SyntaxEng), (Grammar=GrammarEng), (Symbolic=SymbolicEng), (Extend=ExtendEng) 
            ** open ParadigmsEng, ResEng, Prelude, StructuralEng, MorphoEng in {

    oper
        simple_cn : Str -> CN = \s -> lin CN {s = table { a => table { b => s } }; g = Neutr};

    lin
        formula_named_kind m = { cn = simple_cn m.s; num = Sg };
        formula_stmt m = lin S {s = m.s};
}
