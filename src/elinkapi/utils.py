import re

class Validation:
    _ROR_ID_PATTERN = re.compile("^(?:(?:(http(s?):\/\/)?(?:ror\.org\/)))?(0[a-hj-km-np-tv-z|0-9]{6}[0-9]{2})$")

    @classmethod
    def find_ror_value(cls, value:str) -> str:
        """
        Attempt to match against valid ROR ID patterns.  If matched, return
        the ROR ID value only.
        """
        match = cls._ROR_ID_PATTERN.search(value)
        if match is None:
            raise ValueError("Invalid ROR ID value.")
        
        return match.group(1)
