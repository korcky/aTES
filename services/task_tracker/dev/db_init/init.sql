CREATE TABLE users (
    public_id UUID PRIMARY KEY,
    email VARCHAR(256),
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    role VARCHAR(32),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO users (public_id, email, first_name, last_name, role)
VALUES
    ('cb008039-7a07-4766-9ca9-fb93ddb5b1e8', 'admin@popug.inc', NULL, NULL, 'admin'),
    ('9eb41774-7576-4b74-9064-9e8b0a08c823', 'manager@popug.inc', NULL, NULL, 'manager'),
    ('3d617854-2685-4edb-ba58-122d170de26e', 'accountant@popug.inc', NULL, NULL, 'manager'),
    ('044293c7-7c57-4094-baa1-cb1b170b668f', 'worker0@popug.inc', NULL, NULL, 'worker'),
    ('17b1c063-6048-46f5-acce-e9c2a3dec5c4', 'worker1@popug.inc', NULL, NULL, 'worker'),
    ('9c2b4119-6ad7-4c1d-aa32-d25c192aa650', 'worker2@popug.inc', NULL, NULL, 'worker')
;


CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    public_id UUID,
    assignee_id UUID,
    title VARCHAR(128),
    jira_id VARCHAR(128),
    description VARCHAR(1024),
    status VARCHAR(32),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO tasks (public_id, assignee_id, title, jira_id, description, status, created_at)
VALUES
    ('044293c7-7c57-4094-baa1-cb1b170b6680', '044293c7-7c57-4094-baa1-cb1b170b668f', 'task0', 'jira0', 'task description','birdie in a cage', NOW() - interval '1 DAY'),
    ('044293c7-7c57-4094-baa1-cb1b170b6681', '044293c7-7c57-4094-baa1-cb1b170b668f', 'task1', 'jira1', 'task description','birdie in a cage', NOW() - interval '1 DAY'),
    ('044293c7-7c57-4094-baa1-cb1b170b6682', '044293c7-7c57-4094-baa1-cb1b170b668f', 'task2', 'jira2', 'task description','birdie in a cage', NOW() - interval '1 DAY'),
    ('17b1c063-6048-46f5-acce-e9c2a3dec5c0', '17b1c063-6048-46f5-acce-e9c2a3dec5c4', 'task3', 'jira3', 'task description','birdie in a cage', NOW() - interval '1 DAY'),
    ('17b1c063-6048-46f5-acce-e9c2a3dec5c1', '17b1c063-6048-46f5-acce-e9c2a3dec5c4', 'task4', 'jira4', 'task description','birdie in a cage', NOW() - interval '1 DAY'),
    ('17b1c063-6048-46f5-acce-e9c2a3dec5c2', '17b1c063-6048-46f5-acce-e9c2a3dec5c4', 'task5', 'jira5', 'task description','birdie in a cage', NOW() - interval '1 DAY'),
    ('9c2b4119-6ad7-4c1d-aa32-d25c192aa650', '9c2b4119-6ad7-4c1d-aa32-d25c192aa650', 'task6', 'jira6', 'task description','birdie in a cage', NOW() - interval '1 DAY'),
    ('9c2b4119-6ad7-4c1d-aa32-d25c192aa651', '9c2b4119-6ad7-4c1d-aa32-d25c192aa650', 'task7', 'jira7', 'task description','birdie in a cage', NOW() - interval '1 DAY'),
    ('9c2b4119-6ad7-4c1d-aa32-d25c192aa652', '9c2b4119-6ad7-4c1d-aa32-d25c192aa650', 'task8', 'jira8', 'task description','birdie in a cage', NOW() - interval '1 DAY')
;