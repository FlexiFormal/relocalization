concrete FreeArgsEng of FreeArgs = MagmaEng ** FreeArgsFunctor with 
        (MagmaUtils = MagmaUtilsEng), (Syntax=SyntaxEng), (Grammar=GrammarEng), (Symbolic=SymbolicEng), (Extend=ExtendEng) 
** open ParadigmsEng in {
    lin
        transitive_predicate pp t = mkVP (mkV2 pp) t.np;

}
