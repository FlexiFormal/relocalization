abstract FreeArgs = Magma ** {
    cat
        ArgMarker;      -- "by", "of degree", ...
        -- distinction of Kind and PreKind reduces number of readings (properties can only be applied to PreKind, arguments only to Kind)
        PreKind;        -- "bijective function"

        -- we need prepredicates to support transitive verbs (with "invisible" argument markers)
        -- e.g. "x divides y"
        -- If we added an invisible argument marker,
        -- we would get problems in other places.
        -- For example, "integer n" could be read as "n" being an
        -- argument with an invisible marker to the property "integer".
        PrePredicate;

    fun
        prekind_to_kind : PreKind -> Kind;
        property_prekind : Property -> PreKind -> PreKind;

        kind_with_arg : Kind -> ArgMarker -> Term -> Kind;
        property_with_arg : Property -> ArgMarker -> Term -> Property;
        predicate_with_arg : Predicate -> ArgMarker -> Term -> Predicate;

        transitive_predicate : PrePredicate -> Term -> Predicate;
        intransitive_predicate : PrePredicate -> Predicate;
}
