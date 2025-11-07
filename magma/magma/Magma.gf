abstract Magma = MagmaFormula ** {
    cat
        Stmt;           -- "there is an odd integer"
        Sentence;       -- "There is an odd integer ."
        Def;            -- "an integer is called odd iff it is not divisible by 2"
        DefCore;        -- "an integer is called odd"
        Assumption;     -- "assume that x is even", "let x be even"

        Quantification; -- "some", "every", "at least one"
        Polarity;       -- positive/negative
        Conj;           -- "and", "iff", ...

        -- distinction of Kind and PreKind reduces number of readings (properties can only be applied to PreKind, arguments only to Kind)
        PreKind;        -- "bijective function"
        Kind;           -- "bijective function ... from X to Y"
        NamedKind;      -- "bijective function f from X to Y"
        Term;           -- "every function f from X to Y"
        Ident;          -- "f", "f, g, and h"
        Property;       -- "divisible by 2"
        ArgMarker;      -- "by", "of degree", ...

        -- predicates
        Predicate;      -- "divides 2", ...

    fun
        -- polarities
        positive_pol : Polarity;
        negative_pol : Polarity;
        negative_pol_v1 : Polarity;

        -- conjunctions
        and_conj : Conj;        -- a ∧ b
        or_conj : Conj;         -- a ∨ b
        iff_conj : Conj;        -- a ⇔ b
        iff_conj_v1 : Conj;
        if_conj : Conj;         -- a ⇐ b
        if_then_conj : Conj;    -- a ⇒ b
        
        -- identifiers
        no_ident : Ident;
        no_idents : Ident;
        math_ident : Formula -> Ident;

        -- prekinds/kinds/named kinds
        prekind_to_kind : PreKind -> Kind;
        name_kind : Kind -> Ident -> NamedKind;
        such_that_named_kind : NamedKind -> Stmt -> NamedKind;
        such_that_named_kind_v1 : NamedKind -> Stmt -> NamedKind;
        such_that_named_kind_v2 : NamedKind -> Stmt -> NamedKind;
        nkind_that_is_property : NamedKind -> Polarity -> Property -> NamedKind;
        property_prekind : Property -> PreKind -> PreKind;
        kind_with_arg : Kind -> ArgMarker -> Term -> Kind;
        formula_named_kind : Formula -> NamedKind;    -- as in "iff there is some n∈N such that ..."

        -- terms
        quantified_nkind : Quantification -> NamedKind -> Term;
        plural_term : NamedKind -> Term;
        math_term : Formula -> Term;

        -- quantifications
        existential_quantification : Quantification;
        existential_quantification_v1 : Quantification;  -- some

        universal_quantification : Quantification;       -- every for sg, all for pl
        universal_quantification_v1 : Quantification;    -- all for sg, all for pl

        -- properties
        property_with_arg : Property -> ArgMarker -> Term -> Property;

        -- statements
        conj_stmt : Conj -> Stmt -> Stmt -> Stmt;
        formula_stmt : Formula -> Stmt;
        stmt_for_term : Stmt -> Term -> Stmt;

        term_has_nkind_stmt : Term -> NamedKind -> Stmt;
        term_is_property_stmt : Term -> Property -> Stmt;
        term_is_term_stmt : Term -> Term -> Stmt;
        term_predicate_stmt : Term -> Predicate -> Stmt;

        let_kind_stmt : Ident -> NamedKind -> Stmt;    -- in practice, NamedKind should be anonymous, but Kind is too restricted (e.g. no "such that")

        exists_nkind : NamedKind -> Stmt;       -- there is a ...
        exists_nkind_v1 : NamedKind -> Stmt;    -- there exists a ...

        -- sentences
        fin_stmt : Stmt -> Sentence;
        def_sentence : Def -> Sentence;

        -- definitions
        define_nkind_as_nkind : NamedKind -> NamedKind -> DefCore;
        define_nkind_as_nkind_v1 : NamedKind -> NamedKind -> DefCore;
        define_formula_prop : Formula -> Property -> DefCore;      -- `t` is called `p`
        define_formula_prop_v1 : Formula -> Property -> DefCore;   -- `t` is said to be `p`
        define_formula_prop_v2 : Formula -> Property -> DefCore;   -- `t` is `p`
        define_nkind_prop : NamedKind -> Property -> DefCore;
        define_nkind_prop_v1 : NamedKind -> Property -> DefCore;
        define_nkind_prop_v2 : NamedKind -> Property -> DefCore;

        plain_defcore : DefCore -> Def;
        defcore_iff_stmt : DefCore -> Stmt -> Def;
        defcore_iff_stmt_v1 : DefCore -> Stmt -> Def;
        -- looking at real-world definitions, "if" could also be a variant of "iff"
        -- even though the prescriptivist in me disagrees
        -- I'll keep it separate to avoid generating "if" as a variant of "iff", which some people would consider wrong
        defcore_if_stmt : DefCore -> Stmt -> Def;
}

