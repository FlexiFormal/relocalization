--# -path=../magma:../lexica:../formulae

concrete SigFtmlEng of SigFtml = SigArgsEng, DollarMathEng, XmlMagmaEng ** open RglXmlEng in {
    lin
        wrapped_kind tag k = {cn = WRAP_CN tag k.cn; adv = k.adv};

        formula_holds f = lin S {s = f.s ++ "holds"};
}
