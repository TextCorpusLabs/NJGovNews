import nltk
from setuptools.command.install import install

class InstallOverride(install):
    def run(self):
        super().run()        
        nltk.download('punkt')
