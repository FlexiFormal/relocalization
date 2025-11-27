abstract Magma = {
    cat
        Statement;      -- "there is an odd integer"
        TopStatement;   -- "hence, x is even"   (statements that can only appear in specific, high-level places, e.g. after "hence"/"therefore"/"it follows that"/...)
        Sentence;       -- "There is an odd integer ."
        Definition;     -- "an integer is called odd iff it is not divisible by 2"
        DefCore;        -- "an integer is called odd"

        Quantification; -- "some", "every", "at least one"
        Polarity;       -- positive/negative
        Conjunction;    -- "and", "or", ...
        Subjunction;    -- "if", "iff", ...

        Kind;           -- "bijective function ... from X to Y"
        NamedKind;      -- "bijective function f from X to Y"
        Term;           -- "every function f from X to Y"
        Property;       -- "divisible by 2"

        -- declarations
        Declaration;    -- "let x be an integer"
        DeclarationList;

        -- predicates
        Predicate;      -- "divides 2", ...

        -- identifiers
        Identifier;     -- "$f$", "$f, g$"
        Identifiers;    -- "$f$, $g$, and $h$"
        IdentifierList; -- gets finalized into `Identifiers`

    fun
        -- polarities
        positive_pol : Polarity;
        negative_pol : Polarity;
        negative_pol_v1 : Polarity;

        -- conjunctions and subjunctions
        and_conj : Conjunction;        -- a ∧ b
        or_conj : Conjunction;         -- a ∨ b

        iff_subj : Subjunction;        -- a ⇔ b
        iff_subj_v1 : Subjunction;
        if_subj : Subjunction;         -- a ⇐ b

        -- if ... then ... is a weird special case, at least in German
        if_then_stmt : Statement -> Statement -> Statement;    -- a ⇒ b
        if_then_stmt_v1 : Statement -> Statement -> Statement;    -- a ⇒ b
        
        -- identifiers
        no_idents_sg : Identifiers;
        no_idents_pl : Identifiers;
        BaseIdentifierList : Identifier -> Identifier -> IdentifierList;
        ConsIdentifierList : Identifier -> IdentifierList -> IdentifierList;
        finalizeIdentifierList : IdentifierList -> Identifiers;
        finalizeIdentifierList_v1 : IdentifierList -> Identifiers;
        finalizeIdentifierList_v2 : IdentifierList -> Identifiers;
        single_identifier : Identifier -> Identifiers;

        -- kinds/named kinds
        name_kind : Kind -> Identifiers -> NamedKind;
        such_that_named_kind : NamedKind -> Statement -> NamedKind;
        such_that_named_kind_v1 : NamedKind -> Statement -> NamedKind;
        such_that_named_kind_v2 : NamedKind -> Statement -> NamedKind;
        nkind_that_is_property : NamedKind -> Polarity -> Property -> NamedKind;

        -- terms
        quantified_nkind : Quantification -> NamedKind -> Term;

        -- quantifications
        existential_quantification : Quantification;
        existential_quantification_v1 : Quantification;  -- some

        universal_quantification : Quantification;       -- every for sg, all for pl
        universal_quantification_v1 : Quantification;    -- all for sg, all for pl

        -- properties

        -- predicates

        -- statements
        conj_stmt : Conjunction -> Statement -> Statement -> Statement;
        subj_stmt : Subjunction -> Statement -> Statement -> Statement;
        stmt_for_term : Statement -> Term -> Statement;     -- "φ for every x"
        stmt_for_term_v1 : Statement -> Term -> Statement;  -- "for every x, φ"

        term_has_nkind_stmt : Term -> NamedKind -> Statement;
        term_is_property_stmt : Term -> Property -> Statement;
        term_is_term_stmt : Term -> Term -> Statement;
        term_predicate_stmt : Term -> Predicate -> Statement;


        exists_nkind : NamedKind -> Statement;       -- there is a ...
        exists_nkind_v1 : NamedKind -> Statement;    -- there exists a ...

        -- top statements
        therefore_stmt : Statement -> TopStatement;
        therefore_stmt_v1 : Statement -> TopStatement;
        therefore_stmt_v2 : Statement -> TopStatement;
        therefore_stmt_v3 : Statement -> TopStatement;
        therefore_stmt_v4 : Statement -> TopStatement;
        therefore_stmt_v5 : Statement -> TopStatement;
        therefore_stmt_v6 : Statement -> TopStatement;
        therefore_stmt_v7 : Statement -> TopStatement;
        therefore_stmt_v8 : Statement -> TopStatement;

        furthermore_stmt : Statement -> TopStatement;
        furthermore_stmt_v1 : Statement -> TopStatement;
        furthermore_stmt_v2 : Statement -> TopStatement;


        -- declarations
        let_kind_decl : Identifiers -> NamedKind -> Declaration;    -- "let k be an integer"; in practice, NamedKind should be anonymous, but Kind is too restricted (e.g. no "such that")
        let_property_decl : Identifiers -> Property -> Declaration; -- "let k∈N be divisible by 2"
        let_ident_decl : Identifiers -> Declaration;   -- "let k∈K" - in practice, it should be a 'guarded identifier'
        let_such_that : Identifiers -> Statement -> Declaration; -- "let k be such that ..."
        let_such_that_v1 : Identifiers -> Statement -> Declaration; -- "let k be where ..."
        let_such_that_v2 : Identifiers -> Statement -> Declaration; -- "let k be with ..."

        BaseDeclarationList : Declaration -> Declaration -> DeclarationList;
        ConsDeclarationList : Declaration -> DeclarationList -> DeclarationList;
        ConsDeclarationList_v1 : Declaration -> DeclarationList -> DeclarationList;

        -- sentences
        stmt_sentence : Statement -> Sentence;
        def_sentence : Definition -> Sentence;
        declaration_sentence : Declaration -> Sentence;
        declaration_list_sentence : DeclarationList -> Sentence;
        declaration_list_sentence_v1 : DeclarationList -> Sentence;
        declaration_list_sentence_v2 : DeclarationList -> Sentence;
        topstmt_sentence : TopStatement -> Sentence;

        -- definitions
        define_nkind_as_nkind : NamedKind -> NamedKind -> DefCore;   -- an `n1` is called a `n2`
        define_nkind_as_nkind_v1 : NamedKind -> NamedKind -> DefCore;-- an `n1` is said to be a `n2`
        define_nkind_as_nkind_v2 : NamedKind -> NamedKind -> DefCore;-- an `n1` is a `n2`
        define_nkind_as_nkind_v3 : NamedKind -> NamedKind -> DefCore;-- we say that an `n1` is a `n2`

        define_nkind_prop : NamedKind -> Property -> DefCore;
        define_nkind_prop_v1 : NamedKind -> Property -> DefCore;
        define_nkind_prop_v2 : NamedKind -> Property -> DefCore;
        define_nkind_prop_v3 : NamedKind -> Property -> DefCore;

        define_ident_prop : Identifier -> Property -> DefCore;      -- `t` is called `p`
        define_ident_prop_v1 : Identifier -> Property -> DefCore;   -- `t` is said to be `p`
        define_ident_prop_v2 : Identifier -> Property -> DefCore;   -- `t` is `p`
        define_ident_prop_v3 : Identifier -> Property -> DefCore;   -- we say that `t` is `p`

        define_ident_nkind : Identifier -> NamedKind -> DefCore;    -- `t` is called a `n`
        define_ident_nkind_v1 : Identifier -> NamedKind -> DefCore; -- `t` is said to be a `n`
        define_ident_nkind_v2 : Identifier -> NamedKind -> DefCore; -- `t` is a `n`
        define_ident_nkind_v3 : Identifier -> NamedKind -> DefCore; -- we say that `t` is a `n`

        plain_defcore : DefCore -> Definition;
        defcore_iff_stmt : DefCore -> Statement -> Definition;
        defcore_iff_stmt_v1 : DefCore -> Statement -> Definition;
        -- looking at real-world definitions, "if" could also be a variant of "iff"
        -- even though the prescriptivist in me disagrees
        -- I'll keep it separate to avoid generating "if" as a variant of "iff", which some people would consider wrong
        defcore_if_stmt : DefCore -> Statement -> Definition;
}

