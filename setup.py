import setuptools

with open("README.md", "r") as fh:
    long_description=fh.read()

"""
https://stackoverflow.com/questions/1612733/including-non-python-files-with-setup-py
"""
    
setuptools.setup(
    name="weeblog",
    version="0.0.9",
    author="jhw",
    author_email="justin.worrall@gmail.com",
    description="Weeblog blogging framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhw/weeblog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=['setuptools_scm'],
    include_package_data=True
)
