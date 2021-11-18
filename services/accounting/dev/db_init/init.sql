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
    public_id UUID,
    assignee_id UUID,
    title VARCHAR(128),
    jira_id VARCHAR(128),
    description VARCHAR(1024),
    status VARCHAR(32),
    fee INTEGER,
    reward INTEGER
);

INSERT INTO tasks (public_id, assignee_id, title, jira_id, description, status, fee, reward)
VALUES
    ('044293c7-7c57-4094-baa1-cb1b170b6680', '044293c7-7c57-4094-baa1-cb1b170b668f', 'task0', 'jira0', 'task0 description','birdie in a cage', 13, 31),
    ('044293c7-7c57-4094-baa1-cb1b170b6681', '044293c7-7c57-4094-baa1-cb1b170b668f', 'task1', 'jira1', 'task1 description','birdie in a cage', 17, 38),
    ('044293c7-7c57-4094-baa1-cb1b170b6682', '044293c7-7c57-4094-baa1-cb1b170b668f', 'task2', 'jira2', 'task2 description','birdie in a cage', 18, 32),
    ('17b1c063-6048-46f5-acce-e9c2a3dec5c0', '17b1c063-6048-46f5-acce-e9c2a3dec5c4', 'task3', 'jira3', 'task3 description','birdie in a cage', 19, 23),
    ('17b1c063-6048-46f5-acce-e9c2a3dec5c1', '17b1c063-6048-46f5-acce-e9c2a3dec5c4', 'task4', 'jira4', 'task4 description','birdie in a cage', 17, 23),
    ('17b1c063-6048-46f5-acce-e9c2a3dec5c2', '17b1c063-6048-46f5-acce-e9c2a3dec5c4', 'task5', 'jira5', 'task5 description','birdie in a cage', 18, 24),
    ('9c2b4119-6ad7-4c1d-aa32-d25c192aa650', '9c2b4119-6ad7-4c1d-aa32-d25c192aa650', 'task6', 'jira6', 'task6 description','birdie in a cage', 13, 26),
    ('9c2b4119-6ad7-4c1d-aa32-d25c192aa651', '9c2b4119-6ad7-4c1d-aa32-d25c192aa650', 'task7', 'jira7', 'task7 description','birdie in a cage', 15, 20),
    ('9c2b4119-6ad7-4c1d-aa32-d25c192aa652', '9c2b4119-6ad7-4c1d-aa32-d25c192aa650', 'task8', 'jira8', 'task8 description','birdie in a cage', 14, 30)
;


CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    public_id UUID,
    user_id UUID,
    description VARCHAR(256),
    type VARCHAR(128),
    debit INTEGER NOT NULL,  -- positive
    credit INTEGER NOT NULL,  -- negative
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);


INSERT INTO transactions (public_id, user_id, description, type, debit, credit, created_at)
VALUES
    ('b762ff24-851d-45ab-ac29-4eaffa2e7b02', '044293c7-7c57-4094-baa1-cb1b170b668f', 'assignment of task: task0 description', 'task_fee', 0, -13, NOW() - interval '1 DAY'),
    ('1707b74e-4366-40a7-abaf-9912cac80af9', '044293c7-7c57-4094-baa1-cb1b170b668f', 'assignment of task: task1 description', 'task_fee', 0, -17, NOW() - interval '1 DAY'),
    ('23c4ea29-9f89-4530-96db-9bffe7da0049', '044293c7-7c57-4094-baa1-cb1b170b668f', 'assignment of task: task2 description', 'task_fee', 0, -18, NOW() - interval '1 DAY'),
    ('7e26fd2f-30d9-4aeb-a7e5-8787e6f1b781', '17b1c063-6048-46f5-acce-e9c2a3dec5c4', 'assignment of task: task3 description', 'task_fee', 0, -19, NOW() - interval '1 DAY'),
    ('8c3c9496-3652-46bf-b640-01c84ff72a0e', '17b1c063-6048-46f5-acce-e9c2a3dec5c4', 'assignment of task: task4 description', 'task_fee', 0, -17, NOW() - interval '1 DAY'),
    ('d1c78476-9c22-45a0-840c-5dee5519a9d3', '17b1c063-6048-46f5-acce-e9c2a3dec5c4', 'assignment of task: task5 description', 'task_fee', 0, -18, NOW() - interval '1 DAY'),
    ('d1c78476-9c22-45a0-840c-5dee5519a9d1', '17b1c063-6048-46f5-acce-e9c2a3dec5c4', 'good job', 'task_reward', 70, 0, NOW()),
    ('9f69998b-4925-48c8-a1e2-bd3028de6363', '9c2b4119-6ad7-4c1d-aa32-d25c192aa650', 'assignment of task: task6 description', 'task_fee', 0, -13, NOW() - interval '1 DAY'),
    ('6db1b203-f52d-4e37-b5c6-474e782b24e1', '9c2b4119-6ad7-4c1d-aa32-d25c192aa650', 'assignment of task: task7 description', 'task_fee', 0, -15, NOW() - interval '1 DAY'),
    ('877ac358-2e6e-4cf1-96cc-4fffa1be561d', '9c2b4119-6ad7-4c1d-aa32-d25c192aa650', 'assignment of task: task8 description', 'task_fee', 0, -14, NOW() - interval '1 DAY')
;


CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    public_id UUID,
    transaction_id UUID,
    status VARCHAR(128)
);


CREATE TABLE balances (
    id SERIAL PRIMARY KEY,
    user_id UUID,
    balance INTEGER,
    for_date DATE
);


INSERT INTO balances (user_id, balance, for_date)
VALUES
    ('044293c7-7c57-4094-baa1-cb1b170b668f', -48, NOW()::DATE),
    ('17b1c063-6048-46f5-acce-e9c2a3dec5c4', -54, NOW()::DATE),
    ('9c2b4119-6ad7-4c1d-aa32-d25c192aa650', -42, NOW()::DATE)
;
