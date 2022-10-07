from setuptools import setup, find_packages
from pathlib import Path

project_dir = Path(__file__).parent
long_description = (project_dir / "README.md").read_text()

setup(
    name="happyjar",
    url="https://github.com/TechWiz-3/happy-jar-cli",
    author="Zac the Wise aka TechWiz-3",
    version='4.0.0',
    description="Keep a happy jar from your terminal",
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        happy=happy.main:cli
    ''',
    instal_requires=["rich"],
)
