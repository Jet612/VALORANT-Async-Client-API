from setuptools import setup
from setuptools import find_namespace_packages

with open("README.md", "r") as readme:
    long_desc = readme.read()

setup(
    name="valorantClientAPI",
    version="0.1.6",
    author="Jet612",
    description="Asynchronous Python wrapper for VALORANT's Client API ",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/Jet612/VALORANT-Async-Client-API",
    project_urls={
        "Documentation": "https://github.com/Jet612/VALORANT-Async-Client-API/tree/main/docs",
        "Bug Tracker": "https://github.com/users/Jet612/projects/8",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
                    'aiohttp==3.8.3',
                    'dataclass_wizard==0.22.2',
                    'requests==2.28.2',
                    'setuptools==65.5.0'
                    ]
)