--# -path=../magma:../formulae:../lexica:../other

concrete EnglishFtmlTestGrammarEng of EnglishFtmlTestGrammar = DollarMathEng, TestEngLexConcr, XmlMagmaEng ** open RglXmlEng in {
    lin
        wrapped_prekind tag pk = WRAP_CN tag pk;
}
