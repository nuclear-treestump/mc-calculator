from setuptools import setup, find_packages

setup(
    name="mc_calculator",
    version="0.1.0",
    author="0xIkari",  # Replace with your name
    author_email="ikari@nuclear-treestump.com",  # Replace with your email
    description="A Minecraft recipe calculator",  # Brief description of your package
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # If your README is in Markdown
    url="https://github.com/nuclear-treestump/mc-calculator",  # Replace with the URL of your repo
    packages=find_packages(),
    entry_points={
        "console_scripts": ["mc-calculator=mc_calculator.main:main"],
    },
    classifiers=[
        # Classifiers help users find your project by categorizing it.
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",  # Minimum version requirement of Python
    # include any additional files beside the source code (e.g., data files, documentation)
    include_package_data=True,
)
