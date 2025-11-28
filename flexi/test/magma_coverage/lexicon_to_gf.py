import json

with open('lexicon.json', 'r') as fp:
    lexicon = json.load(fp)

with open('../../../magma/lexica/TestCoverageLexicon.gf', 'w') as abstract, \
        open('../../../magma/lexica/TestCoverageLexiconEng.gf', 'w') as concrete:
    abstract.write('''abstract TestCoverageLexicon = FreeArgs ** {
    fun
        lex_argmark_by : ArgMarker;
        lex_argmark_of : ArgMarker;
        lex_argmark_from : ArgMarker;
        lex_argmark_to : ArgMarker;
        lex_argmark_on : ArgMarker;
        lex_argmark_under : ArgMarker;
        lex_with_respect_to : ArgMarker;
        lex_with_respect_to_v1 : ArgMarker;
''')

    concrete.write('''concrete TestCoverageLexiconEng of TestCoverageLexicon = FreeArgsEng ** open ParadigmsEng, SyntaxEng, GrammarEng in {
    lin
        lex_argmark_by = mkPrep "by";
        lex_argmark_of = mkPrep "of";
        lex_argmark_from = mkPrep "from";
        lex_argmark_to = mkPrep "to";
        lex_argmark_on = mkPrep "on";
        lex_argmark_under = mkPrep "under";
        lex_with_respect_to = mkPrep "with respect to";
        lex_with_respect_to_v1 = mkPrep "w.r.t.";
''')

    abstract.write('\n-- Prekinds\n')
    for noun, forms in lexicon['N'].items():
        symb = f'pk_lex_{noun}'
        abstract.write(f'    {symb} : PreKind;\n')
        concrete.write(f'    {symb} = mkCN (mkN "{forms[0]}" "{forms[1]}");\n')

    abstract.write('\n-- PrePredicates\n')
    for verb, forms in lexicon['V'].items():
        symb = f'pp_lex_{verb}'
        abstract.write(f'    {symb} : PrePredicate;\n')
        concrete.write(f'    {symb} = mkV "{forms[0]}" "{forms[1]}";\n')

    abstract.write('\n-- Properties\n')
    for adj, forms in lexicon['A'].items():
        symb = f'prop_lex_{adj}'
        abstract.write(f'    {symb} : Property;\n')
        concrete.write(f'    {symb} = mkAP (mkA "{forms[0]}");\n')

    # abstract.write('\n-- ProperNames\n')

    abstract.write('}\n')
    concrete.write('}\n')


    
