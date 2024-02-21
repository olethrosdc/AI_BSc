from setuptools import setup

setup(
    name="ai_python",
    version="0.9.12",
    author="David L Poole & ALan K Mackworth",
    description="Package from the Artificial Intelligence 3E book",
    url="https://artint.info/AIPython/",
    packages=["ai_python"],
    python_requires='>=3.8',
    install_requires=[
        "matplotlib"
    ],
)