- [Awesome Task Exchange System (aTES)](#awesome-task-exchange-system-ates)
  - [Zero-week assignment](#zero-week-assignment)
  - [First-week assignment](#first-week-assignment)
- [Services](#services)
- [Deploy](#deploy)
- [Changes in events and migration process](#changes-in-events-and-migration-process)


# Awesome Task Exchange System (aTES)
Asynchronous architecture studying project. 

[Project context](project_context.md)

### Zero-week assignment

Initial structure: 
[LucidChart](https://lucid.app/documents/view/b3919363-cf69-470f-bb46-f2229c9ccd6f), 
[PDF](https://lucid.app/publicSegments/view/421a9716-0348-4857-9402-c1bf85752616)

### First-week assignment

Business Processes:
[LucidChart](https://lucid.app/documents/view/4102b273-196c-4bd6-9fc7-8c9a7124cdfc),
[PDF](https://lucid.app/publicSegments/view/e4db93e3-bd29-4d11-b0d2-8f7b89c74560)

Domain and models:
[LucidChart](https://lucid.app/documents/view/610aaa29-c45a-4859-a3e0-b9c70ededb16),
[PDF](https://lucid.app/publicSegments/view/0e03c16c-2b54-4f75-b75c-92a5b53703e0)

System events: 
[LucidChart](https://lucid.app/lucidchart/ccc953ce-c152-4de4-9aad-cd5012c8bff0/view),
[PDF](https://lucid.app/publicSegments/view/1a54150b-468a-432e-985c-b39e8a51cb11)


# Services:
1. SSO: [http://localhost:4000/auth](http://localhost:4000/auth)
2. Task tracker: [http://localhost:4100/main](http://localhost:4100/main)
2. Accounting: [http://localhost:4200/main](http://localhost:4200/main)

Credentials:

| email                 | pass        |
| --------------------- | ----------- |
| admin@popug.inc       | admin       |
| manager@popug.inc     | manager     |
| accountant@popug.inc  | accountant  |
| worker0@popug.inc     | worker0     |
| worker1@popug.inc     | worker1     |
| worker2@popug.inc     | worker2     |


# Deploy

1. Deploy `kafka`
   ```bash
   $ docker-compose -f services/kafka/docker-compose.yml up
   ```
2. `broker` often crashed on first launch (for some reason), so better to:
   1. check that `broker` working (after ~1 min after deploying `kafka`):
      ```bash
      $ docker ps
      ```
   2. restart `broker`, if needed:
      ```bash
      $ docker-compose -f services/kafka/docker-compose.yml restart broker
      ```
   ```bash
   $ ./deploy_services
   ```
   

# Changes in events and migration process

### `Task.title`

#### Problem

Popugs creates titles that looks like: `[jira-id] - Title`

#### What needed to do

`title` must be divided on two fields: `title` and `jira-id`

#### Migration process

1. In `event_schema_registry` must be created new version 
of `Task.Created` event
2. Consumers of `Task.Created` event must be updated to be able to 
consume new version and deployed simultaneously with old version
3. Producer of `Task.Created` event must be updated to be able to 
produce new version and deployed (without old version)
4. Shut down old consumer
5. ...
6. profit?


### `Task.status`

#### Problem

Popugs can't figure out what `open`/`closed` tasks status mean

#### What needed to do

`open`/`closed` must be change to `birdie in a cage`/`millet in a bowl`

#### Migration process

1. Code in `Task tracker` must be changed (values in status enum)
2. Migration must be prepared for database, that will map `open`/`closed` to `birdie in a cage`/`millet in a bowl`
3. Shut down old version of `Task tracker`
4. Make migration
5. Deploy new version
6. ...
7. profit?