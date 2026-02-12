import re

def add_figure_numbers(tex_file, output_file):
    with open(tex_file, 'r') as f:
        content = f.read()

    # Find all figure environments and number their captions
    # This is a simple regex approach; it assumes standard LaTeX formatting
    
    new_content = ""
    fig_count = 0
    
    # Split by lines to process sequentially
    lines = content.split('\n')
    
    for line in lines:
        if r'\begin{figure}' in line:
            fig_count += 1
            
        if r'\caption{' in line and 'Figure' not in line:
            # Check if it's inside a figure environment (simplified check)
            # We'll just replace \caption{ with \caption{Figure X: 
            # This might affect tables if they use \caption too, but usually tables are distinct.
            # Let's be safer: only do this if we've seen a begin{figure} recently? 
            # Actually, let's just replace it. Most captions in this file are figures.
            # But wait, subfigures use \caption too. We don't want "Figure X: (a)..."
            # Subfigures usually are inside \begin{subfigure}.
            
            # Let's refine: only replace if it's NOT a subcaption. 
            # Subcaptions are often just \caption{...} inside a subfigure.
            # The user's subfigures use \caption{...}.
            
            # If we just number the main figures, that's what matters.
            # The main figures are usually direct children of \begin{figure}.
            
            # Let's use a counter approach.
            pass

    # Better approach: Regex replacement with a callback function
    
    def replace_caption(match):
        # Check if this is likely a main figure caption
        # We can't easily know context with simple regex.
        # But we can look at the file content.
        return match.group(0)

    # Let's try a different strategy:
    # Read the file, track if we are in a figure or subfigure.
    
    final_lines = []
    in_figure = False
    in_subfigure = False
    fig_counter = 0
    
    for line in lines:
        stripped_line = line.strip()
        
        # Skip commented out lines
        if stripped_line.startswith('%'):
            final_lines.append(line)
            continue
            
        if r'\begin{figure}' in line:
            in_figure = True
            fig_counter += 1
        if r'\end{figure}' in line:
            in_figure = False
            
        if r'\begin{subfigure}' in line:
            in_subfigure = True
        if r'\end{subfigure}' in line:
            in_subfigure = False
            
        if r'\caption{' in line:
            if in_figure and not in_subfigure:
                # This is a main figure caption
                # Check if it already has "Figure X:" to avoid double numbering if run multiple times
                if not re.search(r'\\caption\{Figure \d+:', line):
                    line = line.replace(r'\caption{', f'\\caption{{Figure {fig_counter}: ')
        
        final_lines.append(line)

    with open(output_file, 'w') as f:
        f.write('\n'.join(final_lines))

add_figure_numbers('main (2).tex', 'main_numbered.tex')
