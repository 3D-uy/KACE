import os
from jinja2 import Environment, FileSystemLoader

def generate_config(parsed_data, user_data):
    """Milestone 2: Jinja2 Template Rendering"""
    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('printer.cfg.j2')
    
    # Render the template with parsed pins and user input
    output = template.render(
        pins=parsed_data,
        user=user_data
    )
    
    # Align inline comments for a professional look
    aligned_lines = []
    comment_col = 48
    for line in output.splitlines():
        if '#' in line and not line.lstrip().startswith('#'):
            # This is an inline comment
            content, comment = line.split('#', 1)
            content = content.rstrip()
            comment = comment.strip()
            # Ensure at least one space before the comment
            padding = max(1, comment_col - len(content))
            aligned_lines.append(f"{content}{' ' * padding}# {comment}")
        else:
            # Regular line or full-line comment
            aligned_lines.append(line)
    
    final_output = "\n".join(aligned_lines)
    
    # Write to printer.cfg
    with open('printer.cfg', 'w') as f:
        f.write(final_output)
