from setuptools import setup
from pathlib import Path

project_dir = Path(__file__).parent
long_description = (project_dir / "README.md").read_text()

setup(
    name="happyjar",
    version='1.0.0',
    description="Keep a happy jar from your terminal",
    long_description_content_type='text/markdown',
    long_description=long_description,
    scripts=["happy"]
)
