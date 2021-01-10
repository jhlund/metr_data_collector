import setuptools
from metr_data_collector_version.version import DATA_COLLECTOR_VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metr_data_collector",
    version=DATA_COLLECTOR_VERSION,
    author="Johan Lund",
    author_email="Johan.H.Lund@gmail.com",
    description="CLI Tool designed for automated data collection from server specified in a config file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=" ",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'metr_data_collector=source.metr_data_collector:cli'
        ],
    },
    install_requires=['click'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
        "Development Status :: 4 - Beta",
        "Environment :: Console"
    ],
    python_requires='>=3.6'
)
