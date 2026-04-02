import os
from jinja2 import Environment, FileSystemLoader
from core.translations import translate_comment

# Resolve templates directory relative to this file's location, not the CWD
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TEMPLATES_DIR = os.path.join(_BASE_DIR, 'templates')

def generate_config(parsed_data, user_data):
    """Milestone 2: Jinja2 Template Rendering"""
    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(_TEMPLATES_DIR))
    template = env.get_template('printer.cfg.j2')
    
    # Render the template with parsed pins and user input
    output = template.render(
        pins=parsed_data,
        user=user_data
    )
    
    # Align inline comments for a professional look
    aligned_lines = []
    comment_col = 48
    language = user_data.get('language', 'English')
    for line in output.splitlines():
        # Check if line is a commented setting that contains an inline comment
        is_commented_setting = line.lstrip().startswith('#') and line.count('#') > 1 and (':' in line or ('[' in line and ']' in line))
        if ('#' in line and not line.lstrip().startswith('#')) or is_commented_setting:
            if not is_commented_setting:
                content, comment = line.split('#', 1)
            else:
                first_hash = line.find('#')
                second_hash = line.find('#', first_hash + 1)
                content, comment = line[:second_hash], line[second_hash+1:]

            content = content.rstrip()
            comment = comment.strip()
            
            # Translate if necessary
            comment = translate_comment(comment, language)
            
            # Ensure at least one space before the comment
            padding = max(1, comment_col - len(content))
            aligned_lines.append(f"{content}{' ' * padding}# {comment}")
        else:
            # Regular line or normal full-line comment
            if line.lstrip().startswith('#'):
                comment = line.lstrip()[1:].strip()
                translated = translate_comment(comment, language)
                if comment != translated:
                    # Update translated full line comment
                    line = line.replace(f"# {comment}", f"# {translated}")
            aligned_lines.append(line)
    
    final_output = chr(10).join(aligned_lines)
    
    # Validation: Do not proceed if generic TODO pins are left, preventing Klipper startup errors
    if "TODO" in final_output:
        import sys
        print("\n\033[91mCRITICAL ERROR: Configuration generated with unresolved 'TODO' values!\033[0m")
        print("\033[93mThis usually happens if your board does not map all required pins natively.\033[0m")
        print("\033[91mGeneration aborted to guarantee it starts without errors in Klipper.\033[0m")
        sys.exit(1)
        
    # Write to printer.cfg
    output_path = os.path.expanduser('~/kace')
    os.makedirs(output_path, exist_ok=True)
    
    cfg_file = os.path.join(output_path, 'printer.cfg')
    with open(cfg_file, 'w') as f:
        f.write(final_output)

