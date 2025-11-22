"""
Setup script for dog_bark_detector package.
"""

from setuptools import setup, find_packages
import os


def read_requirements():
    """Read requirements from requirements.txt."""
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    with open(requirements_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f
                if line.strip() and not line.startswith('#')]


def read_readme():
    """Read README file."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''


setup(
    name='dog_bark_detector',
    version='1.0.0',
    author='Claude AI',
    description='High-performance AI-powered dog bark detection system',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/dog-bark-detector',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'detect-bark=detect_bark:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords='dog bark detection audio analysis machine-learning ai yamnet',
    project_urls={
        'Documentation': 'https://github.com/yourusername/dog-bark-detector#readme',
        'Source': 'https://github.com/yourusername/dog-bark-detector',
        'Tracker': 'https://github.com/yourusername/dog-bark-detector/issues',
    },
)
