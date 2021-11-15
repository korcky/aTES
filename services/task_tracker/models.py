from dataclasses import dataclass
from datetime import datetime
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


class Status(Enum):
    open = 'birdie in a cage'
    closed = 'millet in a bowl'

    def __str__(self):
        return self.value


@dataclass
class Task:
    public_id: UUID
    assignee_id: UUID
    title: str
    jira_id: Optional[str]
    description: str
    status: Status
    created_at: datetime

    def json_serializable(self):
        dict_rep = self.__dict__
        for filed in ['public_id', 'assignee_id', 'created_at']:
            dict_rep[filed] = str(dict_rep[filed])
        dict_rep['status'] = self.status.value
        return dict_rep
