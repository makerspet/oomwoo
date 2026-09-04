from setuptools import find_packages, setup

package_name = "oomwoo_baseline"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", ["launch/baseline_record.launch.py"]),
        ("share/" + package_name + "/config", ["config/scenario_registry.yaml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="oomwoo-baseline",
    maintainer_email="oomwoo-contrib@example.com",
    description="Phase-0 reproducible experiment baseline and observability harness for OOMWOO.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "metrics_collector_node = oomwoo_baseline.metrics_collector:main",
            "run_metadata_node = oomwoo_baseline.run_metadata:main",
        ],
    },
)
