--# -path=../magma
concrete OpaqueFormulaeGer of OpaqueFormulae = MagmaGer ** OpaqueFormulaeFunctor with 
        (Syntax=SyntaxGer), (Grammar=GrammarGer), (Symbolic=SymbolicGer), (Extend=ExtendGer) 
            ** open ParadigmsGer, ResGer, Prelude, StructuralGer, MorphoGer in {

--     oper
--         simple_cn : Str -> CN = \s -> lin CN {s = table { a => table { b => s } }; g = Neutr};
-- 
--     lin
--         formula_named_kind m = { cn = simple_cn m.s; num = Sg };

        lin
            formula_stmt m = lin S {s = table { _ => m.s } };
}
