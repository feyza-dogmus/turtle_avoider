import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'turtle_avoider'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='feyza',
    maintainer_email='feyzadogmus@icloud.com',
    description='Turtlesim wall avoidance node',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        

            'avoider = turtle_avoider.avoider:main',
            'wanderer = turtle_avoider.wanderer:main',
        ],
    },
)
