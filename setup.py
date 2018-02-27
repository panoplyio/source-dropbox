from distutils.core import setup

setup(
    name="panoply_dropbox",
    version="1.0.8",
    description="Panoply Data Source for the Dropbox API",
    author="Roi Avinoam",
    author_email="roi@panoply.io",
    url="http://panoply.io",
    install_requires=[
        "panoply-python-sdk"
    ],
    extras_require={
        "test": [
            "pycodestyle==2.3.1",
            "coverage==4.3.4",
            "pytest==3.2.1"
        ]
    },

    # place this package within the panoply package namespace
    package_dir={"panoply": ""},
    packages=["panoply.dropbox"]
)
