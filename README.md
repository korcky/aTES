# Awesome Task Exchange System (aTES)
Asynchronous architecture studying project 

### Zero-week assignment

Initial structure: 
[LucidChart](https://lucid.app/documents/view/b3919363-cf69-470f-bb46-f2229c9ccd6f), 
[PDF](https://lucid.app/publicSegments/view/421a9716-0348-4857-9402-c1bf85752616)

### First-week assignment

System events: 
[LucidChart](https://lucid.app/lucidchart/ccc953ce-c152-4de4-9aad-cd5012c8bff0/view),
[PDF](https://lucid.app/publicSegments/view/1a54150b-468a-432e-985c-b39e8a51cb11)

Domain and models:
[LucidChart](https://lucid.app/documents/view/610aaa29-c45a-4859-a3e0-b9c70ededb16),
[PDF](https://lucid.app/publicSegments/view/0e03c16c-2b54-4f75-b75c-92a5b53703e0)


## Context of project

This is a studying project. 
Its goal is not to create best task tracker in the world, 
but get a practice (so system is quite limited).

Additionally, the problematic is intentionally hyperbolized, 
so project will be more interesting and the system looks absurd 
from logical point of view.

## Context of requirements

Top-management of UberPopug Inc. faced with a problem of employees performance.
To fix this problem, there were decided to create 
special Awesome Task Exchange System (aTES),
which must increase the performance of employees on indeterminate percentage.

To improve employees ([popugs](https://t.me/addstickers/blyadopapug)), so they 
will learn new staff, top-management come up with innovative idea of assigning
tasks on random employee. To improve motivation of employees top-management 
decides to make a corporate accounting in task tracker, in which employees salary
is determined by amount of tasks completed.


## Task tracker
1. Task tracker must be a separate dashboard and available to every employee of UberPopug Inc.
2. Authorization in task tracker must be provided through corporate authorization service.
3. In task tracker must be only tasks (no projects, scopes and sprints, they are too big to fot a popug brain)
4. New task can be created by anyone. Task must have a description, status (finished or nor) and employee (popug) assigned to this task.
5. Managers or administrators must have a button "Assign tasks" that will randomly assign unfinished tasks to any popug (except managers and administrators):
    - tasks can be assigned to any popug (except managers and administrators),
    - tasks can be reassigned only through "Assign tasks" button,
    - when "Assign tasks" button is pressed, all unfinished tasks will be randomly reassigned between popugs,
    - there is no limits on "Assign tasks" button clicks,
    - one employee could be assigned to any number of tasks (might be 0, might be 10).
6. Every popug can see a list of tasks, assigned to her. Plus, mark task as finished.


## Accounting
1. Accounting must be a separate dashboard. Admins and accountants can see overall statistic (amount of top-management earns by days)
2. Authorization in Accounting dashboard must be provided through corporate authorization service.
3. Regular popugs can see her current balance and audit log (history of fees and rewards, with task description)
4. Task pricing:
    - task price is determine once, when task appears in system:
        - assignment fees `-rand(10..20)$`,
        - completion reward `rand(20..40)$`,
    - fees is paid right after assignment, reward is granted after completion of task,
    - negative balance is carried over to the next day (only way to make it positive -- complete sufficient amount of tasks)
5. Dashboard must show how much money was earned by tom-management: `-1 * (sum(completed tasks reward) + sum(assigned tasks fee))`,
6. At the end of a day:
    - calculate how much money earned employee for a day,
    - send email to employee with this amount,
7. Balance must be set to zero, after payment, and this payment must be an audit log,
8. Dashboard must show info by days. Even only for today will be enough (popugs doesn't remember further).


## Analytics
1. Analytics is a separate dashboard, available only for admins,
2. Must be shown how much top-managers earns (for today) and how much popugs gets balance below zero,
3. Must be shown most expensive task for day, week, month:
   - most expensive tasks is a finished task with the highest price for the period, e.g.:
     ```
     03.03 -- most expensive task -- 28$
     02.03 -- most expensive task -- 38$
     01.03 -- most expensive task -- 23$
     
     01.03 - 03.03 -- most expensive task -- 38$
     ```