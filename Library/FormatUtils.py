import math


def format_ktest_result_apa(statistic, pvalue, alpha=0.05):
    if statistic == 'NaN': return f"k = NaN, p = NaN"
    if pvalue < alpha:
        formatted_pvalue = "p < " + str(alpha)
    else:
        formatted_pvalue = f"p = {pvalue:.3f}"
    formatted_output = f"ks = {statistic:.3f}, {formatted_pvalue}"
    print(pvalue, formatted_output)
    return formatted_output


def pvalue_to_marker(p, levels=None, markers=None):
    if levels is None:
        levels = [0.001, 0.01, 0.05, 0.1]
    if markers is None:
        markers = ["***", "**", "*", "."]
    if len(levels) != len(markers):
        raise ValueError("Levels and markers must have the same length.")
    for level, marker in zip(levels, markers):
        if p < level:
            return marker
    return "n.s."


def format_pvalue(p, slope=None, levels=None, subscript = ''):
    # Get sign of slope
    sign = ' (+)'
    if slope is None:
        sign = ''
    else:
        if slope < 0: sign = ' (-)'

    if levels is None:
        levels = [0.001, 0.01, 0.05, 0.1]
    levels = sorted(levels)
    for level in levels:
        if p < level:
            return f"$p_{subscript}{sign} < {level}$"
    return f"$p_{subscript}{sign} = {p:.3f}$"


def format_ttest_result_apa(ttest_result, alpha=0.05):
    statistic = ttest_result.statistic
    pvalue = ttest_result.pvalue
    df = ttest_result.df
    formatted_pvalue = format_pvalue(pvalue, [alpha])
    formatted_output = f"t({df:.0f}) = {statistic:.3f}, {formatted_pvalue}"
    return formatted_output
