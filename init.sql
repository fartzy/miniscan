-- Create the scan_data table to store response data
CREATE TABLE scan_data (
    id SERIAL PRIMARY KEY,
    response_bytes_utf8 BYTEA,
    response_str TEXT
);

-- Create the scans table to store scan metadata
CREATE TABLE scans (
    id SERIAL PRIMARY KEY,
    ip VARCHAR(15) NOT NULL,
    port INTEGER NOT NULL,
    service VARCHAR(50) NOT NULL,
    timestamp BIGINT NOT NULL,
    data_version INTEGER NOT NULL,
    data_id INTEGER,
    FOREIGN KEY (data_id) REFERENCES scan_data(id)
);
