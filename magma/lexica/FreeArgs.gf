abstract FreeArgs = Magma ** {
    cat
        ArgMarker;      -- "by", "of degree", ...
        -- distinction of Kind and PreKind reduces number of readings (properties can only be applied to PreKind, arguments only to Kind)
        PreKind;        -- "bijective function"

    fun
        prekind_to_kind : PreKind -> Kind;
        property_prekind : Property -> PreKind -> PreKind;

        kind_with_arg : Kind -> ArgMarker -> Term -> Kind;
        property_with_arg : Property -> ArgMarker -> Term -> Property;
        predicate_with_arg : Predicate -> ArgMarker -> Term -> Predicate;

}
