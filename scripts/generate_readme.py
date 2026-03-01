#!/usr/bin/env python3
"""Generate README.md from data/chatbots.yaml."""

import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent

VALUE_MAP = {
    "yes": "Yes \u2705",
    "no": "No \u274c",
    "paid": "Paid \U0001f4b0",
    "free": "Free \u2705",
    "paid_tier": "Paid \u2705",
    "multimodal": "Multimodal \u2705",
    "voice": "Voice only \u2705",
}

# Icon metadata: id -> icon file(s). Use icon_dark/icon_light for theme-aware icons.
CHATBOTS = [
    {"id": "chatgpt",    "icon_dark": "img/icon_chatgpt.png",    "icon_light": "img/icon_chatgpt_light.png"},
    {"id": "claude",     "icon": "img/icon_claude.png"},
    {"id": "gemini",     "icon": "img/icon_gemini.png"},
    {"id": "mistral",    "icon": "img/icon_mistral.png"},
    {"id": "copilot",    "icon": "img/icon_copilot.png"},
    {"id": "meta",       "icon": "img/icon_meta.png"},
    {"id": "grok",       "icon_dark": "img/icon_grok.png",       "icon_light": "img/icon_grok_light.png"},
    {"id": "perplexity", "icon_dark": "img/icon_perplexity.png", "icon_light": "img/icon_perplexity_light.png"},
    {"id": "deepseek",   "icon": "img/icon_deepseek.png"},
    {"id": "qwen",       "icon": "img/icon_qwen.png"},
]

# Ordered list of (yaml_key, display_label)
FEATURES = [
    ("company",                 "Company"),
    ("most_recent_models",      "Most recent models"),
    ("access_to_latest_models", "Access to latest models"),
    ("context_window",          "Context window (tokens) \U0001f4cf"),
    ("reasoning",               "Reasoning \U0001f9e0"),
    ("web_search",              "Web search with source citation \U0001f50d"),
    ("image_generation",        "Image generation \U0001f3a8"),
    ("image_document_analysis", "Analysis of images / documents \U0001f5bc\ufe0f"),
    ("live_mode",               "Live mode \U0001f3a4"),
    ("canvas_edition",          'Online "canvas" edition \U0001f58a\ufe0f'),
    ("personalized_assistants", "Personalized assistants \U0001f4e0"),
    ("agents_with_actions",     "Agents with actions \U0001f916"),
    ("code_interpreter",        "Code interpreter \U0001f4bb"),
    ("personalization_memory",  "Personalization, memory \U0001f9e0"),
    ("data_governance",         "Data governance and regulatory compliance \U0001f512"),
    ("mobile_app",              "Mobile app"),
]

INTRO = """\
# Chatbot Matrix

Chatbot comparison grid.

"""

FOOTER = """

Links: [chatgpt.com](https://chatgpt.com/) / [claude.ai](https://claude.ai/) / [gemini.google.com](https://gemini.google.com/) / [chat.mistral.ai](https://chat.mistral.ai/) / [copilot.microsoft.com](https://copilot.microsoft.com/) / [meta.ai](https://www.meta.ai) / [grok.com](https://grok.com) / [perplexity.ai](https://www.perplexity.ai/) / [deepseek.com](https://www.deepseek.com/) / [chat.qwenlm.ai](https://chat.qwenlm.ai/)

Initial sources: [AppyLearny](https://www.appylearny.fr/), [One Useful Thing](https://www.oneusefulthing.org/).

License: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication.

To the extent possible under law, [Steven Van Vaerenbergh](https://github.com/steven2358) has waived all copyright and related or neighboring rights to this work.
"""


BADGE_MAP = {
    "yes":  "\u2705",
    "no":   "\u274c",
    "paid": "\U0001f4b0",
    "free": "\u2705",
}


def render_value(val):
    if isinstance(val, int):
        return "\u2b50" * val + "/5"
    if isinstance(val, str) and "|" in val:
        label, badge = val.split("|", 1)
        return f"{label} {BADGE_MAP[badge]}"
    if val in VALUE_MAP:
        return VALUE_MAP[val]
    return str(val)


def make_header_cell(bot_data, icon_info):
    name = bot_data["name"]
    url = bot_data["url"]
    if "icon_light" in icon_info:
        img = (
            f'<picture>'
            f'<source media="(prefers-color-scheme: dark)" srcset="{icon_info["icon_light"]}">'
            f'<source media="(prefers-color-scheme: light)" srcset="{icon_info["icon_dark"]}">'
            f'<img src="{icon_info["icon_dark"]}" alt="{name}" width="50">'
            f'</picture>'
        )
    else:
        img = f'<img src="{icon_info["icon"]}" alt="{name}" width="50">'
    return f'{name}<br><a href="{url}">{img}</a>'


def generate_table(chatbots_data, icon_map):
    rows = []

    # Header row
    header_cells = ["Feature"] + [make_header_cell(b, icon_map[b["id"]]) for b in chatbots_data]
    rows.append("| " + " | ".join(header_cells) + " |")

    # Alignment row
    rows.append("|:-" + "|:-" * len(chatbots_data) + "|")

    # Data rows
    for key, label in FEATURES:
        cells = [label] + [render_value(b[key]) for b in chatbots_data]
        rows.append("| " + " | ".join(cells) + " |")

    return "\n".join(rows)


def main():
    yaml_path = ROOT / "data" / "chatbots.yaml"
    readme_path = ROOT / "README.md"

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    chatbots_data = data["chatbots"]
    icon_map = {info["id"]: info for info in CHATBOTS}

    # Verify ordering: YAML order must match CHATBOTS order
    yaml_ids = [b["id"] for b in chatbots_data]
    script_ids = [b["id"] for b in CHATBOTS]
    if yaml_ids != script_ids:
        raise ValueError(f"ID order mismatch.\nYAML:   {yaml_ids}\nScript: {script_ids}")

    table = generate_table(chatbots_data, icon_map)
    content = INTRO + table + FOOTER

    with open(readme_path, "w") as f:
        f.write(content)

    print(f"Written: {readme_path}")


if __name__ == "__main__":
    main()
