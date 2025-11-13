--# -path=../magma:../formulae:../lexica:../other

abstract XmlMagma = Magma, Xml ** {
    fun
        wrapped_named_kind : Tag -> NamedKind -> NamedKind;
        wrapped_property : Tag -> Property -> Property;
        wrapped_stmt : Tag -> Statement -> Statement;
        wrapped_sentence : Tag -> Sentence -> Sentence;
}
