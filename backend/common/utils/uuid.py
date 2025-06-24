from uuid import uuid4

class UniqueID:
    @classmethod
    async def get_uuid4(cls) -> str:
        """
        This function return unique id.
        """
        return str(uuid4())
    
    @classmethod
    async def get_filename(cls, filename: str) -> str:
        """
        This function return the name of the file
        """
        return filename.split("_", 1)[1]