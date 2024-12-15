import polars as pl
from pydantic import BaseModel
from typing import Generic, TypeVar, get_args, override

T = TypeVar("T", bound=BaseModel)


class TypedFrame(pl.DataFrame, Generic[T]):

    col_schema: type[T]

    def __getattr__(self, name: str):
        if name == "col_schema":
            return self.get_generic_type()
        try:
            super().__getattribute__(name)
        except:
            if name in self.col_schema.model_fields:
                return pl.col(name)
            else:
                raise AttributeError("blah")
            

    @override
    def __getitem__(self, index: int) -> T:
        return self.get_generic_type()(**self.row(index, named=True))
    

    def get_generic_type(self) -> type[T]:
        # TODO: raise exception if len is 0
        type_args = get_args(self.__orig_class__) 
        if len(type_args) == 0:
            raise RuntimeError("No type assigned to class.")
        return type_args[0]
