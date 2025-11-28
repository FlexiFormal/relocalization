concrete FreeArgsEng of FreeArgs = MagmaEng ** FreeArgsFunctor with 
        (MagmaUtils = MagmaUtilsEng), (Syntax=SyntaxEng), (Grammar=GrammarEng), (Symbolic=SymbolicEng), (Extend=ExtendEng)
** open ParadigmsEng, ResEng in {
    lin
        transitive_predicate pp t = mkVP (mkV2 pp) t.np;
        propertylist_prekind pl pk = mkCN (mkAP (mkConj "" "," singular) pl) pk;
        prekind_argmarker pk marker = lin Prep {
            s = marker.s ++ pk.s ! Sg ! Nom;
            isPre = marker.isPre
        };

}
