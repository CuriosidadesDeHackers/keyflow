from setuptools import setup, find_packages

setup(
    name="keyflow",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=[
        "PySide6",
        "cryptography",
        "pykeepass",
    ],
    entry_points={
        "console_scripts": [
            "keyflow=main:main",
        ],
    },
    include_package_data=True,
)
