CREATE TABLE IF NOT EXISTS ctf_flags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    challenge_name VARCHAR(100) NOT NULL,
    flag VARCHAR(255) NOT NULL
);

INSERT INTO ctf_flags (challenge_name, flag)
SELECT 'WEB-01', 'CTF{DVWA_SQL_INJECTION_2026}'
WHERE NOT EXISTS (
    SELECT 1 FROM ctf_flags WHERE challenge_name = 'WEB-01'
);
