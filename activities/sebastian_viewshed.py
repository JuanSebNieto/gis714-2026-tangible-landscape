#!/usr/bin/env python3

import os
import grass.script as gs


def run_viewshed(scanned_elev, env, points=None, **kwargs):

    if not points:
        points = "points"
        import analyses

        analyses.change_detection(
            "scan_saved",
            scanned_elev,
            points,
            height_threshold=[10, 100],
            cells_threshold=[2, 50],
            add=True,
            max_detected=1,
            debug=True,
            env=env,
        )

    point_list = []
    data = (
        gs.read_command(
            "v.out.ascii",
            input=points,
            type="point",
            format="point",
            separator="comma",
            env=env,
        )
        .strip()
        .splitlines()
    )

    if len(data) < 1:
        return

    point = data[0]
    x, y = [float(p) for p in point.split(",")][:2]

    gs.run_command(
        "r.viewshed",
        input="scan_saved",
        output="viewshed",
        coordinates=f"{x},{y}",
        observer_elevation=2,
        env=env,
    )


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    points = "points"
    gs.write_command(
        "v.in.ascii",
        flags="t",
        input="-",
        output=points,
        separator="comma",
        stdin="638432,220382\n638621,220607",
        env=env,
    )

    run_viewshed(scanned_elev=elev_resampled, env=env, points=points)


if __name__ == "__main__":
    main()
