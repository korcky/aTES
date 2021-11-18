from dataclasses import dataclass
from datetime import datetime, date
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
    assignee_id: Optional[UUID]
    title: str
    jira_id: Optional[str]
    description: str
    status: Status
    fee: int
    reward: int

    def json_serializable(self):
        dict_rep = self.__dict__
        for filed in ['public_id', 'role']:
            dict_rep[filed] = str(dict_rep[filed])
        return dict_rep


class TxType(Enum):
    task_fee = 'task_fee'
    task_reward = 'task_reward'
    yearns_payment = 'yearns_payment'

    def __str__(self):
        return self.value


@dataclass
class Balance:
    user_id: str
    for_date: date
    balance: int


@dataclass
class Transaction:
    public_id: UUID
    user_id: UUID
    description: str
    type: str
    debit: int
    credit: int
    created_at: datetime

