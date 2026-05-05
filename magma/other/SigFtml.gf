--# -path=../magma:../lexica:../formulae

abstract SigFtml = SigArgs, DollarMath, XmlMagma ** {
    fun
        -- in the free argument setting, we can wrap PreKinds,
        -- but we don't have PreKinds here, so Kinds must be wrappable.
        wrapped_kind : Tag -> Kind -> Kind;
        wrapped_kind2 : Tag -> Kind2 -> Kind2;



        -- TODO: this should go somewhere else - maybe an extension of OpaqueFormulae?
        formula_holds : Formula -> Statement;
}
