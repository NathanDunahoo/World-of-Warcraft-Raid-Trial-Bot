from re import search
from json import load
from definitions import ROOT_DIR
import os

"""Exceptions defined for ErrorHandling"""
class ClassError(Exception):
    pass

class SpecError(Exception):
    pass

class TrialError(Exception):
    pass

class BadDate(Exception):
    pass

def get_wow_data() -> dict:
    """
    Reads json file for WoW Class and Spec data

    :return: dict
    """
    file = os.path.join(ROOT_DIR, 'worldofwarcraft', 'wowdata.json')
    return load(open(file))

class WowData:
    def __init__(self):
        self.wowdata = get_wow_data()
        self.wow_classes = self.get_classes()

    def get_specs_for_class(self, cls) -> dict:
        return self.wowdata[cls][0]['Specs']

    def get_classes(self) -> list:
        return list(self.wowdata.keys())

    def get_logo_for_class(self, cls) -> str:
        return self.wowdata[cls][0]['Logo']

    def check_valid_spec(self, cls: str, spec: str):
        """
        Check is the WoW class and spec are valid.
        :param cls: WoW Class (Paladin, Warlock, Mage)
        :param spec: Coresponding WoW spec to the class (Protection, Affliction, Frost)
        :return: ClassError or SpecError if invalid. None is valid
        """

        if spec not in self.wowdata[cls][0]['Specs']:
            raise SpecError

    def check_valid_class(self, cls):
        if cls not in self.wowdata.keys():
            raise ClassError
        return cls

    def check_valid_date(self, date: str):
        """
        Used regular expression to verify the date is valid
        :param date: Should be in 2021-11-30 format
        :return: str if valid BadDate is invalid
        """
        check = search(r'^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$', date)
        if bool(check):
            return date
        else:
            raise BadDate


if __name__ == '__main__':
    wd = WowData()
    print(wd.get_classes())