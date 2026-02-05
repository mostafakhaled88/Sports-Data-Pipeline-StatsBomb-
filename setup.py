from setuptools import setup, find_packages

setup(
    name="sports_data_pipeline",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "apache-beam[gcp]==2.53.0", # Updated to match newer stable release
        "requests",
        "pandas",
        "google-cloud-bigquery",
    ],
)