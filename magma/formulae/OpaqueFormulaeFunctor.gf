--# -path=../magma
incomplete concrete OpaqueFormulaeFunctor of OpaqueFormulae = MagmaFunctor ** open Syntax, Grammar, Symbolic, Extend in {
    lincat
        Formula = {
            s: Str;
        };

    lin
        formula_ident m = {s = m.s; num = Sg};
        formula_term m = symb m;
        formula_stmt m = lin S {s = m.s};
}
