CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    public_id UUID,
    email VARCHAR(256),
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    password VARCHAR(64),
    role VARCHAR(32),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO users (public_id, email, first_name, last_name, password, role)
VALUES
    ('cb008039-7a07-4766-9ca9-fb93ddb5b1e8', 'admin@popug.inc', NULL, NULL, '$2b$12$i5pt01RHCEtxOSzvJAwbq.7bpF48VJaqAUMCUDkgascXk0RmydYi6', 'admin'),
    ('9eb41774-7576-4b74-9064-9e8b0a08c823', 'manager@popug.inc', NULL, NULL, '$2b$12$YQbflvVaMebkITkdsX5vY.aBGm1Z5jeT/5RR9GnpGgx2ZdZysvSMa', 'manager'),
    ('3d617854-2685-4edb-ba58-122d170de26e', 'accountant@popug.inc', NULL, NULL, '$2b$12$BYN3Q8g/dB9usVxBtlj9GOPu1x9PC5S28c1FokpfeLxZihDhP1Mq6', 'manager'),
    ('044293c7-7c57-4094-baa1-cb1b170b668f', 'worker0@popug.inc', NULL, NULL, '$2b$12$84KhFXmEyFdHUxpnpzT.BuLxeTVtWBtmV0iE798SyygrA4cEPKwHW', 'worker'),
    ('17b1c063-6048-46f5-acce-e9c2a3dec5c4', 'worker1@popug.inc', NULL, NULL, '$2b$12$y8cCRCP7DHuqtd0q4hTiR.s.GmKaxA6HDdWW5HyNoh0c6hnfn8sk6', 'worker'),
    ('9c2b4119-6ad7-4c1d-aa32-d25c192aa650', 'worker2@popug.inc', NULL, NULL, '$2b$12$vglNRdhsMQQ9yzlQPnX2geanuJCx3RG2Cax1.RzhaUWlPZqesvsD.', 'worker')
;