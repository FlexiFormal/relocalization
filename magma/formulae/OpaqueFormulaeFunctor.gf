--# -path=../magma
incomplete concrete OpaqueFormulaeFunctor of OpaqueFormulae = MagmaFunctor ** open Syntax, Grammar, Symbolic, Extend in {
    lincat
        Formula = {
            s: Str;
        };

    lin
        formula_ident m = {s = m.s; num = Sg};
        formula_term m = {np = symb m; just_formula = True};
}
