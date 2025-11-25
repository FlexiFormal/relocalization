concrete SigArgsGer of SigArgs = MagmaGer ** SigArgsFunctor - [Kind2, Kind3, kind2_to_kind, kind3_to_kind] with 
        (MagmaUtils = MagmaUtilsGer), (Syntax=SyntaxGer), (Grammar=GrammarGer), (Symbolic=SymbolicGer), (Extend=ExtendGer) 
** open Prelude, ResGer in {
    oper
        -- German Prep is too big for our purposes
        MiniPrep = {
            s: Str;
            c: Case;
        };
        app_mp : MiniPrep -> NP -> Adv = \prep,np -> lin Adv {
            s = prep.s ++ (np.s ! False ! prep.c) ++ np.ext ++ np.rc
        };

    lincat
        -- prepositions depend on whether the argument is a formula or not
        Kind2 = {
            cn : CN;
            prep1 : Bool => MiniPrep;
        };
        Kind3 = {
            cn : CN;
            prep1 : Bool => MiniPrep;
            prep2 : Bool => MiniPrep;
        };

    lin
        kind2_to_kind k2 t1 = {
            cn = k2.cn;
            adv = mergeAdv empty_Adv (app_mp (k2.prep1!t1.just_formula) t1.np);
        };
        kind3_to_kind k3 t1 t2 = {
            cn = k3.cn;
            adv = mergeAdv empty_Adv (mergeAdv (app_mp (k3.prep1!t1.just_formula) t1.np) (app_mp (k3.prep2!t2.just_formula) t2.np));
        };
}
