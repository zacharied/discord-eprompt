import setuptools

with open('README.md', 'r') as desc:
    long_description = desc.read()

setuptools.setup(
    name='discord-eprompt',
    version='0.2.2',
    author='Zach Day',
    author_email='z@zach.gdn',
    description='Reaction-based user interfaces for discord.py bots',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zacharied/discord-eprompt',
    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ]
)
