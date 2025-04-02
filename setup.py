from setuptools import setup, find_packages
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="shivonai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        "langchain": ["langchain>=0.1.0"],
        "llamaindex": ["llama-index>=0.1.0"],
        "crewai": ["crewai>=0.1.0"],
        "agno": ["agno>=0.1.0"],
        "all": [
            "langchain>=0.1.0",
            "llama-index>=0.1.0",
            "crewai>=0.1.0",
            "agno>=0.1.0"
        ],
    },
    python_requires=">=3.7",
)