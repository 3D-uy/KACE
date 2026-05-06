from questionary import Style

# Custom KIAUH-inspired style
custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),            # token in front of the question
    ('question', 'bold'),                    # question text
    ('answer', 'fg:#4caf50 bold'),           # submitted answer text behind the question (green after selected)
    ('pointer', 'fg:#f5a623 bold'),          # pointer used in select and checkbox prompts
    # highlighted: must contrast against both light and dark terminals.
    # bg:#f5a623 (amber) + black text gives maximum contrast regardless of terminal theme.
    ('highlighted', 'bg:#f5a623 fg:#000000 bold'),  # active item in select / checkbox
    ('selected', 'fg:#4caf50'),              # selected choice in checkbox prompts
    ('separator', 'fg:#cc5454'),             # separator in lists
    ('instruction', 'fg:#888888'),           # help text for the user
    ('text', ''),                            # any generic text
    ('disabled', 'fg:#858585 italic'),       # disabled choices for select and checkbox prompts
    # Autocomplete dropdown
    ('completion-menu', 'bg:#1a1a2e fg:#e0e0e0'),
    ('completion-menu.completion', 'bg:#1a1a2e fg:#e0e0e0'),
    ('completion-menu.completion.current', 'bg:#f5a623 fg:#000000 bold'),
    ('completion-menu.meta.completion', 'bg:#1a1a2e fg:#888888'),
    ('completion-menu.meta.completion.current', 'bg:#f5a623 fg:#000000'),
])
