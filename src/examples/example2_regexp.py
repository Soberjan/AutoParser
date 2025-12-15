import json
from pathlib import Path
import re
from typing import Dict

from docx import Document


def extract_values(content: str, *args: str) -> Dict[str, str]:
    res = {}
    for key in args:
        found = re.search(f"{key}:(.*)", content)
        res[key] = found.group(1).strip()
    return res


def main():
    data_folder = Path(__file__).parent.parent.parent / "data"
    input_doc_path = data_folder / "cv_examples" / "Васильев Дмитрий Андреевич.docx"

    doc = Document(input_doc_path)
    content = "\n".join([p.text for p in doc.paragraphs])
    keys = ["Email", "Телефон", "Вакансия"]
    res = extract_values(content, *keys)

    # Export to json
    with (data_folder / "scratch" / f"{input_doc_path.stem}_re.json").open(
        "w", encoding="utf-8"
    ) as fp:
        json.dump(res, fp, ensure_ascii=False)


if __name__ == "__main__":
    main()
