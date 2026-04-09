--# -path=../magma:../lexica:../formulae

abstract SigFtml = SigArgs, DollarMath, XmlMagma ** {
    fun
        -- wrapping kinds is probablematic in a free argument setting
        -- but works here
        -- (in free arguments, how should we wrap "power set ... of X" ?)
        wrapped_kind : Tag -> Kind -> Kind;



        -- TODO: this should go somewhere else - maybe an extension of OpaqueFormulae?
        formula_holds : Formula -> Statement;
}
