import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ferramenta-tecnica", # Replace with your own username
    version="0.0.1",
    author="Ferramenta Técnica",
    author_email="alencarr@gmail.com",
    description="sistema de cadastro de mapa de carga",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)