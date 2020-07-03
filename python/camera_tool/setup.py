from setuptools import setup, find_packages

setup(
    name='domotz_camera_tool',
    version='0.1',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'tabulate',
        'pillow',
        'jinja2',
    ],
    entry_points='''
        [console_scripts]
        domotz_camera_tool=domotz_camera_tool.main:main
    ''',
)