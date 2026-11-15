import os
from glob import glob

from setuptools import find_packages, setup

package_name = "rebot_trash_sorting_agent"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml", "README.md", "NOTICE"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        (os.path.join("share", package_name, "scripts"), glob("scripts/*.sh")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="steel_team",
    maintainer_email="steel_team@todo.todo",
    description="VLM-orchestrated pick-and-place agent for the reBot Arm B601-DM.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            # nodes
            "camera_node = rebot_trash_sorting_agent.camera_node:main",
            "agent_node = rebot_trash_sorting_agent.agent_node:main",
            "dashboard_node = rebot_trash_sorting_agent.dashboard_node:main",
            "mujoco_sim_node = rebot_trash_sorting_agent.mujoco_sim_node:main",
            # tools
            "calibrate_table = rebot_trash_sorting_agent.calibrate_table:main",
            "detect_once = rebot_trash_sorting_agent.detect_once:main",
        ],
    },
)
