from glob import glob
import os
from setuptools import find_packages, setup

package_name = "rebot_trash_sorting"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (
            os.path.join("share", package_name, "config"),
            glob("config/*.yaml") + glob("config/*.srdf"),
        ),
        (os.path.join("share", package_name, "rviz"), glob("rviz/*.rviz")),
        (os.path.join("share", package_name, "urdf"), glob("urdf/*.xacro")),
        (
            os.path.join("share", package_name, "meshes", "soft_gripper", "visual"),
            glob("meshes/soft_gripper/visual/*.stl"),
        ),
        (
            os.path.join("share", package_name, "meshes", "soft_gripper", "collision"),
            glob("meshes/soft_gripper/collision/*.stl"),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="steel_team",
    maintainer_email="steel_team@todo.todo",
    description="Vision-guided trash sorting pipeline for the Seeed Studio reBot Arm B601-DM.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "check_env = rebot_trash_sorting.check_env_node:main",
            "hardware_gripper_bridge = rebot_trash_sorting.hardware_gripper_bridge_node:main",
        ],
    },
)
