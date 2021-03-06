from shutil import copyfile

import os
import stat
import urllib.request
import re


class Setup:


    def __init__(self):
        self.devkitPath = os.path.expanduser("~")+"/.devkit";
        self.binaryPath = "/usr/local/bin/devkit";


    """ Execute the setup """
    def run(self):
        print("Installing the devkit...");
        # copy the installer to the local binary folder
        copyfile('./installer.py', self.binaryPath);
        # get current permissions of the devkit
        st = os.stat(self.binaryPath);
        # change permission to executable
        os.chmod(self.binaryPath, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH);

        # If the devkit folder does not exists, create it
        if not os.path.exists(self.devkitPath):
            print("Creating the devkit folder...");
            os.makedirs(self.devkitPath);


        print("Moving the default files to the devkit folder...");
        # Copy the ruleset and the commit hook to the .devkit folder
        copyfile('./codesniffer/ruleset.xml', self.devkitPath+"/ruleset.xml");
        copyfile('./codesniffer/pre-commit', self.devkitPath+"/pre-commit");

        # Read the content of the config file
        file = open('./codesniffer/config', 'r+');
        content = file.read();
        # Replace the placeholders with the .devkit location
        content = re.sub(r'(\[\[ BINPATH \]\])', self.devkitPath+"/phpcs.phar", content); 
        content = re.sub(r'(\[\[ RULESETPATH \]\])', self.devkitPath+"/ruleset.xml", content); 

        # Create a new config file inside the .devkit folder and insert the data
        file = open(self.devkitPath+'/config', 'w');
        file.write(content);
        file.close();

        print("Downloading the phpcs.phar and moving it to the devkit folder...");
        # Downlaod phpcs and move it to the .devkit folder
        urllib.request.urlretrieve("https://squizlabs.github.io/PHP_CodeSniffer/phpcs.phar", self.devkitPath+"/phpcs.phar");

        # Make sure the phpcs file is executable
        st = os.stat(self.devkitPath+"/phpcs.phar");
        os.chmod(self.devkitPath+"/phpcs.phar", st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH);

        print("");
        print("Installation complete!");


setup = Setup();
setup.run();
