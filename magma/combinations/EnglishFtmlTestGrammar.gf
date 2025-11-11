--# -path=../magma:../formulae:../lexica:../other

abstract EnglishFtmlTestGrammar = TestEngLex, DollarMath, XmlMagma ** {
    fun
        wrapped_prekind : Tag -> PreKind -> PreKind;
}
