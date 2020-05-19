from setuptools import find_packages, setup

setup(
    name="darkest",
    version="0.1.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["darkest = darkest.__main__:main"]},
    install_requires=[
        "darker @ git+https://github.com/Mystic-Mirage/darker.git@install",
    ],
)