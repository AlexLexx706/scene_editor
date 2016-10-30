from setuptools import setup, find_packages

setup(
    name='scene_editor',
    version='0.1',
    author='alexlexx',
    author_email='alexlexx1@gmail.com',
    packages=find_packages(),
    license='GPL',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'scene_editor = scene_editor.widgets.main_window:main'
        ],
    },
    package_data={
        'scene_editor': [
            'images/*.png',
            'images/objects/*.png',
            'images/textures/*.png',
            'widgets/*.ui']
    },
)
