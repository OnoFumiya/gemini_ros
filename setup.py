import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'gemini_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=False,
    maintainer='shigemori',
    maintainer_email='yasumasashige790@gmail.com',
    description='ROS2 package for running Gemini Action Server',
    license='Apache License 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'gemini_action_server = gemini_ros.gemini_action_server:main',
        ],
    },
)
