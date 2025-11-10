incomplete concrete FreeArgsFunctor of FreeArgs = MagmaFunctor ** open MagmaUtils, Syntax in {
    lincat
        ArgMarker = Prep;
        PreKind = CN;
    lin
        prekind_to_kind pk = mkKind pk;
        property_prekind pp pk = mkCN pp pk;
        kind_with_arg k am t = {
            cn = k.cn;
            adv = mergeAdv k.adv (PrepNP am t);
        };
        property_with_arg p am t = AdvAP p (PrepNP am t);
        predicate_with_arg pred am t = mkVP pred (PrepNP am t);

}
