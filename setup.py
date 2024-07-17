from setuptools import setup, find_packages

setup(
    name="ffxicrafting",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "ffxicrafting=ffxicrafting.main:main",
        ],
    },
)
