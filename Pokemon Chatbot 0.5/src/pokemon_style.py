TYPE_STYLES = {
    "normal":    ("gray", "⬜"),
    "fire":      ("red", "🔥"),
    "water":     ("blue", "💧"),
    "electric":  ("gold", "⚡"),
    "grass":     ("green", "🍃"),
    "ice":       ("aqua", "❄️"),
    "fighting":  ("brown", "🥊"),
    "poison":    ("purple", "☠️"),
    "ground":    ("sienna", "🌍"),
    "flying":    ("skyblue", "🕊️"),
    "psychic":   ("deeppink", "🔮"),
    "bug":       ("olivedrab", "🐛"),
    "rock":      ("darkgoldenrod", "🪨"),
    "ghost":     ("indigo", "👻"),
    "dragon":    ("darkslateblue", "🐉"),
    "dark":      ("black", "🌑"),
    "steel":     ("lightgray", "⚙️"),
    "fairy":     ("pink", "🧚"),
}
def render_types(types: list) -> str:
    """
    Given a list of type strings, return an HTML string with icons and colors.
    """
    parts = []
    for t in types:
        color, icon = TYPE_STYLES.get(t.lower(), ("gray", "❓"))
        parts.append(f"<span style='color:{color}; font-weight:bold;'>{icon} {t.title()}</span>")
    return " &nbsp; ".join(parts)
