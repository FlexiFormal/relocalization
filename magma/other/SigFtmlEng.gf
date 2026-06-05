--# -path=../magma:../lexica:../formulae

concrete SigFtmlEng of SigFtml = SigArgsEng, DollarMathEng, XmlMagmaEng ** open RglXmlEng in {
    lin
        -- wrapped_kind tag k = {cn = PREFIX_CN tag k.cn; adv = POSTFIX_Adv tag k.adv};
        wrapped_kind tag k = {cn = WRAP_CN tag k.cn; adv = k.adv};
        wrapped_kind2 tag k2 = {cn = WRAP_CN tag k2.cn; prep1 = k2.prep1};

        wrapped_property2 tag p2 = {ap = WRAP_AP tag p2.ap; prep1 = p2.prep1};

        formula_holds f = lin S {s = f.s ++ "holds"};
}
