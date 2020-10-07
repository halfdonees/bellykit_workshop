import setuptools

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except:
    long_description = "bellykit"

setuptools.setup(
    name='bellykit_workshop',
    version='0.1',
    author='Lu Kuan Tsen',
    author_email='40475027h@gapps.ntnu.edu.tw',
    description='bellykit workshop',
    long_description_content_type='text/markdown',
    url='www.bellykit.com',
    packages=setuptools.find_packages(include=['bellykit_workshop', 'bellykit_workshop.*']),
    classfiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.7',
    data_files=[
        ('data', ['data/workshop_data.csv'])],
)
