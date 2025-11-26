import re

def clean_bib(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    # Function to clean DOI fields
    def clean_doi(match):
        doi_val = match.group(1)
        # Remove https://doi.org/ or http://dx.doi.org/ prefixes
        doi_val = re.sub(r'https?://(dx\.)?doi\.org/', '', doi_val)
        return f'doi = {{{doi_val}}}'

    # Regex to find doi fields
    # Matches: doi = {value} or doi={value}
    # We assume braces are used.
    new_content = re.sub(r'doi\s*=\s*\{([^\}]+)\}', clean_doi, content)

    with open(output_file, 'w') as f:
        f.write(new_content)

clean_bib('bib.bib', 'bib_clean.bib')
