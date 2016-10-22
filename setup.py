from distutils.core import setup

setup(
    name="panoply_dropbox",
    version="1.0.7",
    description="Panoply Data Source for the Dropbox API",
    author="Roi Avinoam",
    author_email="roi@panoply.io",
    url="http://panoply.io",
    install_requires=[
        "panoply-python-sdk"
    ],

    # place this package within the panoply package namespace
    package_dir={"panoply": ""},
    packages=["panoply.dropbox"]
)