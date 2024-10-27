from typing import Dict, Generic, List, TypeVar

Tag = TypeVar("Tag")
Value = TypeVar("Value")


class TaggedCollection(Generic[Tag, Value]):
    """Collection where values are indexed by tags."""

    __collection: Dict[Tag, List[Value]] = {}

    def get(self, tag: Tag) -> List[Value]:
        """Get all values indexed with a tag.

        Args:
            tag (Tag): Tag to search for

        Returns:
            List[Value]: List of values indexed with the given tag
        """
        return self.__collection.get(tag, [])

    def append(self, tag: Tag, value: Value) -> None:
        """Append a value to the list of values indexed with the given tag.

        Args:
            tag (Tag): Tag to index the value with
            value (Value): Value to append
        """
        self.__collection[tag] = self.get(tag) + [value]

    def clear(self, tag: Tag) -> None:
        """Clear all values indexed with the given tag.

        Args:
            tag (Tag): Tag to clear
        """
        self.__collection[tag] = []

    def get_all(self) -> List[Value]:
        """Get all values in the collection regardless of the tags.

        Returns:
            List[Value]: List of all values in the collection
        """
        return [value for values in self.__collection.values() for value in values]

    def clear_all(self) -> None:
        """Clear all values in the collection for all tags.

        Returns:
            None
        """
        self.__collection = {}
