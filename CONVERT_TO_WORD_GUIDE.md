# How to Convert LaTeX to Word (.docx)

This guide explains how we previously converted the main LaTeX manuscript into a Microsoft Word document, and how to do it again for future revisions. The tool used for this is [Pandoc](https://pandoc.org/), a universal document converter.

## Prerequisites

1.  **Pandoc:** Make sure Pandoc is installed on your machine. You can verify this by running `pandoc --version` in your terminal. You can install it on macOS via Homebrew: `brew install pandoc`.
2.  **CSL File (Citation Style Language):** To format citations correctly (e.g., Chicago style footnotes), we use a `.csl` file, specifically `chicago-fullnote-bibliography.csl`. 
3.  **Lua Filter (endnotes.lua):** The submission often requires footnotes to be compiled as endnotes at the end of the manuscript instead of bottom-of-page footnotes, or simply properly numbered notes. A custom Pandoc lua filter (`endnotes.lua`) is used to manage this.
4.  **Bibliography File:** Your `.bib` (e.g., `bib.bib` or `bib_clean.bib`) containing the references.

## The Conversion Command

To execute the conversion from the `revision/` folder, open your terminal, navigate (`cd`) into the `revision/` directory, and run the following command:

```bash
pandoc "revision.tex" -o "revision.docx" \
  --citeproc \
  --bibliography=../bib.bib \
  --csl=chicago-fullnote-bibliography.csl \
  --lua-filter=endnotes.lua \
  -M suppress-bibliography=true
```

### Breakdown of the Command

*   `"revision.tex"`: Your input LaTeX file.
*   `-o "revision.docx"`: The output file you want to create.
*   `--citeproc`: Tells Pandoc to process citations embedded in the text.
*   `--bibliography=../bib.bib`: Points Pandoc to your bibliography file (adjust the path if necessary depending on where the command is run).
*   `--csl=chicago-fullnote-bibliography.csl`: Formats your citations using the Chicago Manual of Style full-note formatting rules.
*   `--lua-filter=endnotes.lua`: Runs the Lua script to format footnotes into endnotes with superscript numbers.
*   `-M suppress-bibliography=true`: Suppresses the auto-generation of a standard bibliography section at the very end if your paper uses footnote-only citations or if you want to control its placement.

## Re-creating The Word File

We have already copied `chicago-fullnote-bibliography.csl` and `endnotes.lua` back into your `revision/` folder so you can start converting to `.docx` whenever you'd like using the command above!
