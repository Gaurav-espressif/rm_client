from setuptools import find_packages, setup

setup(
    name="rainmakertest",
    version="0.1",
    packages=find_packages(include=['rainmakertest', 'rainmakertest.*']),
    package_data={
        'rainmakertest': ['*.json', 'templates/*.json'],
    },
    install_requires=[
        "click>=8.0",
        "requests>=2.26",
        "tabulate>=0.8.9",
        "mailosaur"
    ],
    entry_points={
        'console_scripts': [
            'rmcli=rainmakertest.cli:cli',
        ],
    },
)