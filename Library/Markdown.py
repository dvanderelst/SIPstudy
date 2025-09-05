import pypandoc
from pathlib import Path
import subprocess, shutil

def md_to_pdf(md_path, out_path="Supplement.pdf", engine="xelatex"):
    if shutil.which("pandoc") is None:
        raise RuntimeError("pandoc not found")
    subprocess.run(
        ["pandoc", str(md_path), "-s", "-o", out_path, f"--pdf-engine={engine}"],
        check=True
    )
def md_to_odt(md_text: str, out_path: str, reference_odt: str | None = None,
              number_sections: bool = False, toc: bool = False):
    """
    Convert Markdown text to an .odt file using Pandoc.
    - reference_odt: optional path to a template .odt for styles
    - number_sections / toc: add section numbers / table of contents
    """
    args = ["--standalone"]
    if number_sections:
        args.append("--number-sections")
    if toc:
        args.extend(["--toc", "--toc-depth=3"])
    if reference_odt:
        args.extend(["--reference-doc=" + str(reference_odt)])

    out_path = str(Path(out_path).with_suffix(".odt"))
    pypandoc.convert_text(md_text, to="odt", format="md", outputfile=out_path, extra_args=args)
    return out_path

def as_code(text):

    code = "```\n" + text + "\n```"
    code = code.replace('Standard Errors assume that the covariance matrix of the errors is correctly specified', 'St. Err. assume that the cov. matrix of the errors is correctly specified')
    return code