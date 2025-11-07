# `MAGMa`

MAGMa (multi-lingual application grammar for mathematics)
is a modular GF grammar for matematics.

The core `MAGMa` grammar is not useful on its own, but there
are various extensions that can be combined with it.
The extensions are indicated by prefixes of the file names in the `combinations` directory.
The following extensions currently exist:

* `D` (**D**ollar math): `$...$` can be parsed as a placeholder for formulae.
* `LTen` (**L**exicon: **T**est; **`en`**nglish): a small lexicon for testing purposes.
* `X` (**X**ML): certain nodes can be wrapped in placeholder XML tags (e.g. `< 0 > ... </ 0 >`).



## Getting started

Install GF and the RGL, in the GF shell, enter
```
i combinations/DLTenMagmaEng.gf
gr -cat=Stmt -number=10 | l
```
to get a few example sentences.

