import shutil
import subprocess
from pathlib import Path
import re

def md_to_pdf(md_path, out_path="Supplement.pdf"):
    toc = True
    number_sections = True
    engine = "xelatex"
    if shutil.which("pandoc") is None: raise RuntimeError("pandoc not found")
    cmd = ["pandoc", str(md_path), "-s", "-o", str(Path(out_path).with_suffix(".pdf")), f"--pdf-engine={engine}"]
    cmd = cmd + ["-V", "geometry=margin=1in"]
    if toc: cmd.append("--toc")
    if number_sections: cmd.append("--number-sections")
    subprocess.run(cmd, check=True)



def friendly_name(name):
    m = re.match(r"C\(([^)]+)\)\[T\.(.+)\]", name)
    if m:
        var, level = m.groups()
        return f"{var} = {level}"
    return name


def _friendly_exog_names(names):
    out = []
    for name in names:
        friendly = friendly_name(name)
        if name == 'days': friendly = 'Days'
        if name == 'const': friendly = 'Intercept'
        out.append(friendly)
    return out


def _friendly_endog_name(name):
    if name and name[0].islower():
        return name[0].upper() + name[1:]
    return name


def model_formula(results):
    """Return an R-style formula string describing the fitted model.

    For models built with statsmodels.formula.api (smf), uses the
    original formula string. For raw sm.OLS/sm.Logit models, synthesises
    one from endog/exog names (the implicit intercept is omitted, and
    lowercase endog names are capitalised so the LHS matches the
    capitalised exog names produced by friendly_name).
    """
    formula = getattr(results.model, 'formula', None)
    if formula:
        return formula
    endog = _friendly_endog_name(results.model.endog_names)
    exog = [n for n in _friendly_exog_names(results.model.exog_names) if n != 'Intercept']
    return f'{endog} ~ ' + ' + '.join(exog)


def model2code(results):
    friendly = _friendly_exog_names(results.model.exog_names)
    for index, name in enumerate(friendly):
        results.model.exog_names[index] = name
    results.cov_kwds['description'] = 'Standard Errors assume correct specification of covariance matrix.'
    code = results.summary().as_text()
    code = "```\n" + code + "\n```"
    return code

