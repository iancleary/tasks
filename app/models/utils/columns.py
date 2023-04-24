from typing import List


class StrListConverter:
    DELIMITER = ","

    @staticmethod
    def get_list_from_str(list_str: str) -> List[int]:
        # Handle edge cases
        if len(list_str) == 0:
            return []
        elif list_str == "":
            return []
        elif list_str is None:
            return []
        else:
            pass

        split_list = list_str.split(StrListConverter.DELIMITER)

        list_object = []
        for x in split_list:
            if x:
                list_object.append(int(x))
            else:
                pass
        return list_object

    @staticmethod
    def make_str_from_list(list_object: List[int]) -> str:
        list_str = ""
        for x in list_object:
            list_str = list_str + StrListConverter.DELIMITER + str(x)
        return list_str
