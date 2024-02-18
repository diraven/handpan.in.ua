import pathlib
import yaml
import random

WORKING_DIRECTORY = pathlib.Path(__file__).parent.absolute()
WORKSHOPS_PATH = (WORKING_DIRECTORY.parent.parent / "content" / "workshops").absolute()
DEFAULT_VALUE = "-"

for file in WORKSHOPS_PATH.glob("*.md"):
    if file.name.startswith("_"):
        continue
    file.unlink()

with open(WORKING_DIRECTORY / "data.yaml", "r") as yaml_file:
    data = yaml.load(yaml_file, Loader=yaml.SafeLoader)
    for workshop in data["workshops"]:
        with open(WORKSHOPS_PATH / f"{workshop['slug']}.md", "w") as file:
            links = "\n".join([f"- {link}" for link in workshop.get("links", [])])
            cover = (
                f"""cover:
  image: "{workshop["cover"]}"
  alt: "{workshop["title"]}"
  caption: "{workshop["title"]}"
  relative: true
  """.strip()
                if "cover" in workshop
                else ""
            )
            file.write(
                f"""---
title: {workshop["title"]}
{cover}
tags: {workshop.get("tags", [])}
weight: {random.randint(1, 100) if "weight" in workshop else random.randint(900, 999)}
---
{"{{< youtube "+workshop.get("promo_video_youtube_id")+" >}}" if workshop.get("promo_video_youtube_id") else ""}

- **Розташування:** {workshop.get("location", DEFAULT_VALUE)}
- **Майстер:** {workshop.get("craftsman_name", DEFAULT_VALUE)}
{links}

{workshop.get("description", "")}"""
            )
