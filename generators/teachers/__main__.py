import pathlib
import yaml
import random

WORKING_DIRECTORY = pathlib.Path(__file__).parent.absolute()
TEACHERS_PATH = (WORKING_DIRECTORY.parent.parent / "content" / "teachers").absolute()
DEFAULT_VALUE = "-"

for file in TEACHERS_PATH.glob("*.md"):
    if file.name.startswith("_"):
        continue
    file.unlink()

with open(WORKING_DIRECTORY / "data.yaml", "r") as yaml_file:
    data = yaml.load(yaml_file, Loader=yaml.SafeLoader)
    for teacher in data["teachers"]:
        with open(TEACHERS_PATH / f"{teacher['slug']}.md", "w") as file:
            links = "\n".join([f"- {link}" for link in teacher.get("links", [])])
            file.write(
                f"""---
title: {teacher["title"]}
tags: {teacher.get("tags", [])}
weight: {random.randint(1, 100) if "weight" in teacher else random.randint(900, 999)}
---
{"{{< youtube "+teacher.get("promo_video_youtube_id")+" >}}" if teacher.get("promo_video_youtube_id") else ""}

{links}

{teacher.get("description", "")}"""
            )
