from setuptools import setup, find_packages

setup(
    name="mc_calculator",
    version="0.3.2",
    author="0xIkari",
    author_email="ikari@nuclear-treestump.com",
    description="A Minecraft recipe calculator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nuclear-treestump/mc-calculator",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["mc-calculator=mc_calculator.__main__:main"],
    },
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    include_package_data=True,
)
