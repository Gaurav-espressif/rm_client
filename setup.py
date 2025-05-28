from setuptools import find_packages, setup

setup(
    name="rainmakertest",
    version="0.1",
    packages=find_packages(include=['rainmakertest', 'rainmakertest.*']),
    package_data={
        'rainmakertest': ['*.json', 'templates/*.json'],
    },
    install_requires=[
        "beautifulsoup4~=4.13.4",
        "soupsieve~=2.7",
        "typing_extensions~=4.13.2",
        "cryptography~=45.0.2",
        "mailosaur~=7.19.0",
        "certifi~=2025.4.26",
        "tzlocal~=5.3.1",
        "urllib3~=2.4.0",
        "six~=1.17.0",
        "python-dateutil~=2.9.0.post0",
        "idna~=3.10",
        "charset-normalizer~=3.4.1",
        "requests~=2.32.3",
        "PyJWT==2.8.0",
        "click~=8.1.8",
        "tabulate>=0.9.0",
        "pydantic>=2.0.0"
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'rmcli=rainmakertest.cli:cli',
        ],
    },
)