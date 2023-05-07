from setuptools import find_packages, setup

setup(
    name="BlockFrame",
    version="0.1.5",
    author="Rohaan Ahmed",
    author_email="silent.death3500@gmail.com",
    description="File Chunking Library to work as a data-store solution alongside webapps and software.",
    long_description="",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=["cryptography", "SQLAlchemy", "setuptools", "wheel", "aiosqlite"],
    python_requires=">=3.6",
    url="https://github.com/Wizock/BlockFrame/",
    project_urls={
        "Bug Tracker": "https://github.com/Wizock/BlockFrame/issues",
        "Documentation": "https://blockframe.readthedocs.io/",
        "Source Code": "https://github.com/Wizock/BlockFrame/",
    },
    keywords="file chunking, data-store, webapps, software",
)
