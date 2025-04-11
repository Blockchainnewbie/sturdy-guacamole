from setuptools import setup, find_packages

# README.md als long_description verwenden
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sturdy-guacamole",  # Muss exakt mit dem PyPI-Namen übereinstimmen!
    version="0.1.3",
    author="Blockchainnewbie",
    author_email="mdhab@outlook.com",
    description="Updated Snake Game with GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Blockchainnewbie/sturdy-guacamole",
    project_urls={
        "Bug Tracker": "https://github.com/Blockchainnewbie/sturdy-guacamole/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        # Abhängigkeiten hier auflisten
        "requests>=2.25.1",
    ],
)