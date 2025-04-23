from setuptools import setup, find_packages

setup(
    name='login2fa',
    version='1.0.0',
    description='Sistema de login com dupla autenticação via ntfy e NiceGUI',
    author='Francisco Gonçalves',
    packages=find_packages(),
    install_requires=[
        'nicegui',
        'mysql-connector-python',
        'bcrypt',
        'requests'
    ],
)
