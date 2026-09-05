"""Example build123d box builder with a small STEP-export CLI.

This module is intentionally minimal and dependency-light (only build123d is
imported for geometry) because the scaffold package is meant to be replaced
wholesale by a derived repository.
"""

import argparse
from pathlib import Path

from build123d import Box, Part, export_step


def make_box() -> Part:
    """Return a 10 mm cube centered at the origin as a build123d Part."""
    return Box(10, 10, 10)


def main(argv: list[str] | None = None) -> None:
    """Export the example box to a STEP file under the given output dir."""
    parser = argparse.ArgumentParser(
        description="Export the scaffold example box to a STEP file."
    )
    parser.add_argument(
        "-o",
        "--outdir",
        default="manufacture",
        help="Output directory for the STEP file (default: manufacture)",
    )
    args = parser.parse_args(argv)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / "scaffold_box.step"
    export_step(make_box(), str(outpath))
    print(f"wrote {outpath}")


if __name__ == "__main__":
    main()
