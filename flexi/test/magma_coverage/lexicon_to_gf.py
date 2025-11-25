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
''')

    concrete.write('''concrete TestCoverageLexiconEng of TestCoverageLexicon = FreeArgsEng ** open ParadigmsEng, SyntaxEng, GrammarEng in {
    lin
        lex_argmark_by = mkPrep "by";
        lex_argmark_of = mkPrep "of";
        lex_argmark_from = mkPrep "from";
        lex_argmark_to = mkPrep "to";
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


    
