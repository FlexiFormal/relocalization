concrete FreeArgsEng of FreeArgs = MagmaEng ** FreeArgsFunctor with 
        (MagmaUtils = MagmaUtilsEng), (Syntax=SyntaxEng), (Grammar=GrammarEng), (Symbolic=SymbolicEng), (Extend=ExtendEng)
** open ParadigmsEng, ResEng in {
    oper
        _ap_agr_with_comma : (Agr => Str) -> (Agr => Str) = \orig -> table { agr => (orig ! agr) ++ "," };
    lin
        transitive_predicate pp t = mkVP (mkV2 pp) t.np;
        property_prekind_v1 pp pk = mkCN (lin AP {
            -- s = table { agr => (pp.s ! agr) ++ "," };
            s = _ap_agr_with_comma pp.s;
            isPre = pp.isPre;
        }) pk;
}
