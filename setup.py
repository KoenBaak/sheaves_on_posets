import setuptools

setuptools.setup(
    name="sheaves_on_posets",
    version="0.1",
    author="Koen Baak",
    description="SageMath Package for computing the sheaf cohomology of finite locally free sheaves of modules on finite posets",
    long_description = open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KoenBaak/sheaves_on_posets",
    packages=["sheaves_on_posets"],
    install_requires=["sagemath"],
    license='GPLv3+',
    classifiers=[
        "Topic :: Scientific/Engineering :: Mathematics",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    ])
