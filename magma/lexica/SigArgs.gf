abstract SigArgs = Magma ** {
    cat
        Kind2;      -- requires an argument
        Kind3;      -- requires two arguments
        Property2;  -- requires an argument
        Predicate2; -- requires an argument
        Predicate3; -- requires two arguments

    fun
        kind2_to_kind: Kind2 -> Term -> Kind;
        kind3_to_kind: Kind3 -> Term -> Term -> Kind;
        property2_to_property: Property2 -> Term -> Property;
        predicate2_to_predicate: Predicate2 -> Term -> Predicate;
        predicate3_to_predicate: Predicate3 -> Term -> Term -> Predicate;
}
