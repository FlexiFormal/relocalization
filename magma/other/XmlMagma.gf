--# -path=../magma:../formulae:../lexica:../other

abstract XmlMagma = Magma, Xml ** {
    fun
        -- only needed in unusual cases (e.g. "edge such that ...")
        -- otherwise, wrapped_kind does the job
        -- but doubles readings for most annotated Kinds
        -- wrapped_named_kind : Tag -> NamedKind -> NamedKind;
        wrapped_fkind : Tag -> FKind -> FKind;
        wrapped_property : Tag -> Property -> Property;
        wrapped_stmt : Tag -> Statement -> Statement;
        wrapped_sentence : Tag -> Sentence -> Sentence;
        wrapped_term : Tag -> Term -> Term;
}
