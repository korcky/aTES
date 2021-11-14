from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import UUID


class Role(Enum):
    admin = 'admin'
    worker = 'worker'
    manager = 'manager'
    accountant = 'accountant'

    def __str__(self):
        return self.value


@dataclass
class User:
    public_id: UUID
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: Role
    is_active: bool

    def json_serializable(self):
        dict_rep = self.__dict__
        for filed in ['public_id']:
            dict_rep[filed] = str(dict_rep[filed])
        dict_rep['role'] = self.role.value
        return dict_rep
