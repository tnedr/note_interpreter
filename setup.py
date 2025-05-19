from setuptools import setup, find_packages

setup(
    name="note_interpreter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic",
        "langchain",
        "openai",
        "python-dotenv",
        "langchain-community",
        "langchain-openai",
        "langchain-core",
        "langchain-anthropic",
        "pyyaml",
    ],
    author="Tamas",
    description="An AI-powered note interpretation system",
    python_requires=">=3.8",
) 