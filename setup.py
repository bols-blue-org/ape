from setuptools import find_packages, setup

setup(
    name='pid_envaluation',
    version='0.1.0',
    description='Ardupilot pid envaluation tool',
    long_description="",
    author='Hisayoshi Suehiro',
    author_email='bols-blue@lnc.jp',
    url='https://github.com/bols-blue-org/pid_evaluation',
    license=license,
    entry_points={
        'console_scripts': [
            'pid_envaluation = pid_envaluation.data_collection:main',
        ],
    },
    packages=find_packages(exclude=('tests', 'docs'))
)
