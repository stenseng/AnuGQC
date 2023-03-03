CREATE TABLE IF NOT EXISTS gnss_qc_summary (
    qc_id SERIAL,
    qc_file VARCHAR(50),
    qc_epoch TIMESTAMP WITH TIME ZONE NOT NULL,
    qc_sampling NUMERIC(4, 2),
    qc_length_sec NUMERIC(10, 2), 

    station_marker VARCHAR(9),
    station_domes VARCHAR(9),
    station_receiver VARCHAR(20),
    station_receiver_serial VARCHAR(20),
    station_receiver_firmware VARCHAR(20),
    station_antenna VARCHAR(20),
    station_antenna_serial VARCHAR(20),
    station_antenna_ecc_e NUMERIC(7, 4),
    station_antenna_ecc_n NUMERIC(7, 4),
    station_antenna_ecc_u NUMERIC(7, 4),
    station_antenna_ecc_x NUMERIC(7, 4),
    station_antenna_ecc_y NUMERIC(7, 4),
    station_antenna_ecc_z NUMERIC(7, 4),
    station_pos_x NUMERIC(11, 4),
    station_pos_y NUMERIC(11, 4),
    station_pos_z NUMERIC(11, 4)
);

SELECT create_hypertable('gnss_qc_summary', 'qc_epoch', 'station_marker', 2);
-- CREATE INDEX ON gnss_qc_summary(station_marker, sat_id, sat_signal, obs_epoch DESC);
-- CREATE INDEX ON gnss_qc_summary(station_marker, rtcm_msg_type, obs_epoch DESC);
