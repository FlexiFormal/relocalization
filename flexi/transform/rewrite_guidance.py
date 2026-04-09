from flexi.parsing.mast import MAst
from flexi.transform.rewrite_rules import RewritingContext, RewriteRule, RewritePullKindIntoUnivQuant

GREEDY_REWRITING_DEFAULT_RULES: list[RewriteRule] = [RewritePullKindIntoUnivQuant()]


def greedy_rewriting(mast: MAst, rules: list[RewriteRule], ctx: RewritingContext) -> MAst | None:
    """ Naively applies the rewrite rules until none is applicable anymore.

     The rules have to be selected carefully to ensure convergence.
     Returns ``None`` if no rules could be applied.
     """

    modified: bool = False
    iterate_again: bool = True
    while iterate_again:
        iterate_again = False

        for rule in rules:
            while True:
                new = rule.apply_somewhere(mast, ctx)
                try:
                    mast = next(iter(new))
                    modified = True
                    iterate_again = True
                except StopIteration:
                    break

    return mast if modified else None


