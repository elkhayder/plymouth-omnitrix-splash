#!/usr/bin/env python3
"""Render the preview's Omnitrix spinner and glow animation as PNG frames."""

import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "images" / "omnitrix.svg"
OUTPUT = ROOT / "images"
FRAME_COUNT = 50
FRAME_SIZE = 768
VIEWBOX_SIZE = 1020
EMBLEM_OFFSET = (VIEWBOX_SIZE - 500) / 2
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def cubic_bezier(t, first_control, second_control):
    inverse = 1 - t
    return (
        3 * inverse * inverse * t * first_control
        + 3 * inverse * t * t * second_control
        + t * t * t
    )


def ease_in_out(progress):
    low, high = 0.0, 1.0
    for _ in range(24):
        middle = (low + high) / 2
        if cubic_bezier(middle, 0.42, 0.58) < progress:
            low = middle
        else:
            high = middle
    return cubic_bezier((low + high) / 2, 0, 1)


def pulse_value(frame_index, minimum, maximum):
    phase = frame_index / FRAME_COUNT
    if phase < 0.5:
        progress = ease_in_out(phase * 2)
    else:
        progress = 1 - ease_in_out((phase - 0.5) * 2)
    return minimum + (maximum - minimum) * progress


def make_frame_svg(tree, frame_index):
    root = tree.getroot()
    viewbox_size = VIEWBOX_SIZE
    root.set("viewBox", f"0 0 {viewbox_size} {viewbox_size}")
    root.set("width", str(viewbox_size))
    root.set("height", str(viewbox_size))

    emblem = root.find(f".//{{{SVG_NS}}}g[@id='omnitrix-emblem-group']")
    spinner = root.find(f".//{{{SVG_NS}}}circle[@id='plymouth-ring-arc']")
    if emblem is None or spinner is None:
        raise ValueError(f"{SOURCE} is missing the preview emblem or spinner arc")

    defs = root.find(f"{{{SVG_NS}}}defs")
    if defs is None:
        defs = ET.Element(f"{{{SVG_NS}}}defs")
        root.insert(0, defs)

    filter_element = ET.SubElement(
        defs,
        f"{{{SVG_NS}}}filter",
        {
            "id": "previewGlow",
            "x": "-60%",
            "y": "-60%",
            "width": "220%",
            "height": "220%",
        },
    )
    unit_scale = 500 / 384
    primary_alpha = pulse_value(frame_index, 0.45, 0.9)
    secondary_alpha = pulse_value(frame_index, 0.25, 0.55)
    for name, deviation, color, opacity in (
        ("primaryGlow", 15, "#a3ff12", primary_alpha),
        ("secondaryGlow", 35, "#65d719", secondary_alpha),
    ):
        blur = ET.SubElement(
            filter_element,
            f"{{{SVG_NS}}}feGaussianBlur",
            {
                "in": "SourceAlpha",
                "stdDeviation": f"{deviation * unit_scale:.4f}",
                "result": f"{name}Blur",
            },
        )
        flood = ET.SubElement(
            filter_element,
            f"{{{SVG_NS}}}feFlood",
            {
                "flood-color": color,
                "flood-opacity": f"{opacity:.6f}",
                "result": f"{name}Color",
            },
        )
        ET.SubElement(
            filter_element,
            f"{{{SVG_NS}}}feComposite",
            {
                "in": f"{name}Color",
                "in2": f"{name}Blur",
                "operator": "in",
                "result": name,
            },
        )
    merge = ET.SubElement(filter_element, f"{{{SVG_NS}}}feMerge")
    for result in ("primaryGlow", "secondaryGlow", "SourceGraphic"):
        ET.SubElement(merge, f"{{{SVG_NS}}}feMergeNode", {"in": result})

    emblem.set("transform", f"translate({EMBLEM_OFFSET:g} {EMBLEM_OFFSET:g})")
    emblem.set("filter", "url(#previewGlow)")
    angle = frame_index * 360 / FRAME_COUNT
    spinner.set("transform", f"rotate({angle:.6f} 250 250)")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def main():
    inkscape = shutil.which("inkscape")
    if inkscape is None:
        raise RuntimeError("Inkscape was not found on PATH")
    if not SOURCE.is_file():
        raise FileNotFoundError(f"SVG source not found: {SOURCE}")

    OUTPUT.mkdir(exist_ok=True)
    for frame_index in range(FRAME_COUNT):
        tree = ET.parse(SOURCE)
        svg_data = make_frame_svg(tree, frame_index)
        frame_path = OUTPUT / f"omnitrix-frame-{frame_index}.png"
        with tempfile.NamedTemporaryFile(suffix=".svg") as svg_file:
            svg_file.write(svg_data)
            svg_file.flush()
            subprocess.run(
                [
                    inkscape,
                    svg_file.name,
                    f"--export-filename={frame_path}",
                    f"--export-width={FRAME_SIZE}",
                    f"--export-height={FRAME_SIZE}",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )
        print(f"Rendered {frame_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
