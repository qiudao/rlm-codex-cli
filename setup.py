from setuptools import find_packages, setup


setup(
    name="rlm-codex-cli",
    version="0.1.0",
    description="Recursive long-context CLI that delegates reasoning to Codex CLI.",
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={"console_scripts": ["rlm-codex=rlm_codex_cli.cli:main"]},
    python_requires=">=3.9",
)
