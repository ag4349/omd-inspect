import xml.etree.ElementTree as ET
from pathlib import Path


def sniff_root_tag(path: Path) -> str | None:
    try:
        return ET.parse(path).getroot().tag
    except ET.ParseError:
        return None
