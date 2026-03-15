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
    
    # Write to printer.cfg
    with open('printer.cfg', 'w') as f:
        f.write(output)
