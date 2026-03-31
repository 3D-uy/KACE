from questionary import Style

# Custom KIAUH-inspired style
custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),       # token in front of the question
    ('question', 'bold'),               # question text
    ('answer', 'fg:#4caf50 bold'),      # submitted answer text behind the question (green after selected)
    ('pointer', 'fg:#f44336 bold'),     # pointer used in select and checkbox prompts (red while selecting)
    ('highlighted', 'fg:#f44336 bold'), # pointed-at choice in select and checkbox prompts (red while selecting)
    ('selected', 'fg:#4caf50'),         # selected choice in checkbox prompts
    ('separator', 'fg:#cc5454'),        # separator in lists
    ('instruction', ''),                # help text for the user
    ('text', ''),                       # any generic text
    ('disabled', 'fg:#858585 italic'),  # disabled choices for select and checkbox prompts
    ('completion-menu', 'bg:#000000 fg:#ffffff'),
    ('completion-menu.completion.current', 'bg:#4caf50 fg:#000000')
])
