#!/usr/bin/env python3

from setuptools import setup

setup(
    name="srst2",
    version="0.3.0",
    author="Kathryn Holt",
    author_email="drkatholt@gmail.com",
    packages=["srst2"],
    scripts=["scripts/getmlst.py", "scripts/slurm_srst2.py"],
    entry_points={"console_scripts": ["srst2 = srst2.srst2:main"]},
    package_dir={"srst2": "scripts"},
    package_data={"srst2": ["data/resistance.*"]},
    url="http://katholt.github.io/srst2/",
    license="LICENSE.txt",
    description="Short Read Sequence Typing for Bacterial Pathogens",
    long_description=(
        "This program is designed to take Illumina"
        "sequence data, a MLST database and/or a database"
        "of gene sequences (e.g. resistance genes, virulence"
        "genes, etc) and report the presence of STs and/or"
        "reference genes."
    ),
    python_requires=">=3.12",
    install_requires=[
        # Declare the runtime dependencies so pip provisions them, but do not
        # pin lower bounds: srst2.py uses only long-stable scipy.stats APIs
        # (binom, linregress), consensus_alignment.py / database_clustering use
        # Biopython, and database_clustering/align_plot_tree_min3.py plots trees
        # with matplotlib -- none of which need a specific version. Add a lower
        # bound only if a concrete incompatibility ever forces one.
        "numpy",
        "scipy",
        "biopython",
        "matplotlib",
    ],
)
