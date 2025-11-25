incomplete concrete SigArgsFunctor of SigArgs = MagmaFunctor ** open MagmaUtils, Syntax in {
    lincat
        Kind2 = {
            cn : CN;
            prep1 : Prep;
        };
        Kind3 = {
            cn : CN;
            prep1 : Prep;
            prep2 : Prep;
        };
        Property2 = {
            ap : AP;
            prep1 : Prep;
        };
        Predicate2 = {
            vp : VP;
            prep1 : Prep;
        };

    lin
        kind2_to_kind k2 t1 = {
            cn = k2.cn;
            adv = mergeAdv empty_Adv (PrepNP k2.prep1 t1.np);
        };
        kind3_to_kind k3 t1 t2 = {
            cn = k3.cn;
            adv = mergeAdv empty_Adv (mergeAdv (PrepNP k3.prep1 t1.np) (PrepNP k3.prep2 t2.np));
        };
        property2_to_property p2 t1 = AdvAP p2.ap (PrepNP p2.prep1 t1.np);
        predicate2_to_predicate p2 t1 = mkVP p2.vp (PrepNP p2.prep1 t1.np);
}
