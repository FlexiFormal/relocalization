concrete MagmaGer of Magma = MagmaFunctor with 
        (MagmaUtils = MagmaUtilsGer), (Syntax=SyntaxGer), (Grammar=GrammarGer), (Symbolic=SymbolicGer), (Extend=ExtendGer)
** open ParadigmsGer, ResGer, Prelude, StructuralGer, MorphoGer in {

    lin
        iff_subj = lin Subjunction _iff_subj;
        iff_subj_v1 = lin Subjunction _iff_subj_v1;

        let_ident_decl id = lin Utt { s = "sei " ++ id.s } ;
}
