import os
from string import Template
from framework import constants


class Dir:
    def __init__(self, goto, create_if_unexist=True, backto=constants.BASE_DIR):
        """
        Receive those parameters to change dirs back and forth
        :param goto:
        :param backto:
        """
        self.goto = goto
        self.backto = backto

    def __enter__(self):
        try:
            os.chdir(self.goto)
        except:
            os.mkdir(self.goto)
            os.chdir(self.goto)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.backto)




class ProcessTemplateFile:
    EXTENSION = (
        ".template"  # the extension of all template files, for i.e values.yaml.template
    )

    def __init__(self, original_file_name:str):
        self.original_file_name = original_file_name
        self.template_file_name = f"{self.original_file_name}{self.EXTENSION}"

        assert os.path.exists(self.template_file_name), f"Template File not Found! The class searched for the file {self.template_file_name} in the path: {os.getcwd()}. Make sure to point to an existing {self.EXTENSION} file so the original file could be processed."

    def process(self, kvs: dict):
        """
        Creates a destination file with the desired values to replace.
        It's your responsibility when using this method, to know what placeholders
            are given in the .template files, and pass them ar the kws argument
        Returns:
            :file object: Reference to the new file obj
        """
        with open(self.template_file_name, "r", encoding="utf-8") as f:
            src = Template(f.read())
            result = src.safe_substitute(kvs)
        # rewrite the result
        with open(self.original_file_name, "w", encoding="utf-8") as f:
            f.write(result)
            return f

class ProcessRegularFile:
    # TODO: CONCATENATE CLASSES OF PROCESSING TEMPLATES!
    def __init__(self, original_file_name:str):
        self.original_file_name = original_file_name
        assert os.path.exists(self.original_file_name), f"Template File not Found! The class searched for the file {self.original_file_name} in the path: {os.getcwd()}. Make sure to point to an existing file so the original file could be processed."


    def process(self, kvs:dict):
        with open(self.original_file_name, "r", encoding="utf-8") as f:
            src = Template(f.read())
            result = src.safe_substitute(kvs)
        # rewrite the result
        with open(self.original_file_name, "w", encoding="utf-8") as f:
            f.write(result)
            return f