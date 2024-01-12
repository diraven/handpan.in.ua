import pathlib
import yaml

WORKING_DIRECTORY = pathlib.Path(__file__).parent.absolute()
WORKSHOPS_PATH = (WORKING_DIRECTORY.parent.parent / "content" / "workshops").absolute()
DEFAULT_VALUE = "-"

for file in WORKSHOPS_PATH.glob("*.md"):
    if file.name.startswith("_"):
        continue
    file.unlink()

with open(WORKING_DIRECTORY / "data.yaml", "r") as yaml_file:
    data = yaml.load(yaml_file, Loader=yaml.SafeLoader)
    for w in data["workshops"]:
        with open(WORKSHOPS_PATH / f"{w['slug']}.md", "w") as file:
            links = "\n".join([f"- {link}" for link in w.get("links", [])])
            file.write(
                f"""---
title: {w["title"]}
tags: {w.get("tags", [])}
weight: {w.get("weight", 1000)}
---
{w.get("description", "")}
- **Розташування:** {w.get("location", DEFAULT_VALUE)}
- **Майстер:** {w.get("craftsman_name", DEFAULT_VALUE)}
{links}
"""
            )
