# SPDX-FileCopyrightText: 2022 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import setuptools

AUTHOR = 'Espressif Systems'
MAINTAINER = 'ALToast'
EMAIL = ''

NAME = 'check-copyright'
SHORT_DESCRIPTION = 'The script for checking ESPRESSIF MIT license header'
LICENSE = 'Espressif MIT'
URL = 'https://github.com/ALToast/check-copyright'
REQUIRES = [
    'pyyaml == 6.0.1'
]

setuptools.setup(
    
    name=NAME,
    description=SHORT_DESCRIPTION,
    long_description_content_type='text/markdown',
    license=LICENSE,
    version='0.0.1',
    author=AUTHOR,
    maintainer=MAINTAINER,
    author_email=EMAIL,
    url=URL,
    install_requires=REQUIRES,
    py_modules=['check_copyright'],
    scripts=['check_copyright.py'],
    entry_points={'console_scripts': ['check-copyright=check_copyright:main']},
)
