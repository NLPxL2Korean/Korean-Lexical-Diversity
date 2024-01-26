import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="klega",
    version="1.0.6",
    author="Sooyeon Cho",
    author_email="sy.cho2321@gmail.com",
    description="Korean LExico-Grammatical Analyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hksyir/klega_lexdiv",
    project_urls={
        "Bug Tracker": "https://github.com/hksyir/klega_lexdiv",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)