from prompt_toolkit.styles import Style

custom_style = Style([
    # --- Base ---
    ('', 'nobg'),  # 🔥 evita backgrounds heredados raros

    # --- Pregunta / respuesta ---
    ('qmark', 'fg:#673ab7 bold'),
    ('question', 'bold'),
    ('answer', 'fg:#4caf50 bold'),

    # --- Navegación ---
    ('pointer', 'fg:#f5a623 bold nobg'),

    # --- Estados ---
    ('highlighted', 'fg:#f5a623 bold nobg'),        # item activo (cursor)
    ('selected', 'fg:#4caf50 nobg'),                # item marcado
    ('selected.highlighted', 'fg:#4caf50 bold nobg'),

    # 🔥 FIX REAL (prompt_toolkit internals)
    ('cursor-line', 'nobg'),
    ('cursor-line.selected', 'nobg'),

    # --- Estructura ---
    ('separator', 'fg:#cc5454'),
    ('instruction', 'fg:#888888'),
    ('text', ''),
    ('disabled', 'fg:#858585 italic'),

    # --- Checkbox específicos (defensivo) ---
    ('checkbox', ''),
    ('checkbox-selected', 'fg:#4caf50 nobg'),

    # --- Autocomplete ---
    ('completion-menu', 'bg:#1a1a2e fg:#e0e0e0'),
    ('completion-menu.completion', 'bg:#1a1a2e fg:#e0e0e0'),
    ('completion-menu.completion.current', 'fg:#f5a623 bold nobg'),
    ('completion-menu.meta.completion', 'bg:#1a1a2e fg:#888888'),
    ('completion-menu.meta.completion.current', 'fg:#f5a623'),
])
