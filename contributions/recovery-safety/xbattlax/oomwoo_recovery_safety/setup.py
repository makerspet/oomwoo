from setuptools import find_packages, setup


package_name = "oomwoo_recovery_safety"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", ["launch/recovery_safety.launch.py"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="xbattlax",
    maintainer_email="xbattlax@gmail.com",
    description="Bounded recovery ladder and safety pause node for OOMWOO.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "recovery_safety_node = oomwoo_recovery_safety.recovery_node:main",
        ],
    },
)
