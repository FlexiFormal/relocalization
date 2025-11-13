incomplete resource MagmaUtils = open Syntax, ParamX in {
    oper
        _Kind = {cn: CN; adv: Adv};   -- inspired by Aarne's new grammar
        _Ident = {s: Str; num: ParamX.Number};
        _Quantification = { sg: Det; pl: Det };    -- sg if it refers to singular object; can be "some (integer n)" or "all (integers n)"

        mergeAdv : Adv -> Adv -> Adv = \a,b -> lin Adv {s = a.s ++ b.s};

        empty_Adv : Adv = lin Adv {s = ""};
        mkKind = overload {
            mkKind : CN -> _Kind = \cn -> {cn = cn; adv = empty_Adv};
            mkKind : N -> _Kind = \n -> {cn = mkCN n; adv = empty_Adv};
        };

        kind2CN : _Kind -> CN = \k -> mkCN k.cn k.adv;

        indefart : ParamX.Number -> Det = \num -> case num of {
            Sg => a_Det;
            Pl => aPl_Det
        };

        mkQuantification : Det -> Det -> _Quantification = \sgDet, plDet -> { sg = sgDet; pl = plDet };

}
