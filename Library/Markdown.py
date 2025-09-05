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

def model2code(results):
    names = results.model.exog_names
    for index, name in enumerate(names):
        friendly = friendly_name(name)
        if name == 'days': friendly = 'Days'
        if name == 'const': friendly = 'Intercept'
        results.model.exog_names[index] = friendly
    results.cov_kwds['description'] = 'Standard Errors assume correct specification of covariance matrix.'
    code = results.summary().as_text()
    code = "```\n" + code + "\n```"
    return code

