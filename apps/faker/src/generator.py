
from typing import Any, TypeVar

from faker import Faker
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import class_mapper
from sqlalchemy.types import Enum

from domain.repositories.base import Base

T = TypeVar("T", bound=Base)


class Generator:
    def __init__(self):
        self.fake = Faker()
        self.foreigh_key_map: dict[str, list[Any]] = {}

    def generate(self, model_class: type[T]) -> T:
        field_values = {}

        for column in class_mapper(model_class).columns:
            print(column.name)

            field_values[column.name] = self._generate_column_value(column)

        return model_class(**field_values)

    def _generate_column_value(self, column: Column[Any]):
        if column.primary_key:
            return None

        column_type = column.type

        match column_type:
            case Integer():
                return self.fake.random_int()
            case Enum():
                enum_cls = column_type.enum_class
                if enum_cls is not None:
                    return self.fake.enum(enum_cls)
            case String():
                return self.fake.word()
            case DateTime():
                return self.fake.date_time()
