import setuptools

setuptools.setup(
    name='aiclib',
    version="0.2",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7', ],
    install_requires=[
        'urllib3',
    ],
    packages=setuptools.find_packages(),
    keywords='kwantum',
    author='Justin Hammond',
    author_email='justin.hammond@rackspace.com',
    license='Apache Software License',
    zip_safe=False,
)
