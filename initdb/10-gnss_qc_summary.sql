CREATE TABLE IF NOT EXISTS gnss_qc_summary (
    qc_id SERIAL,
    qc_epoch TIMESTAMP WITH TIME ZONE NOT NULL,
    qc_file VARCHAR(50),

    site_marker VARCHAR(20),
    site_domes VARCHAR(2),
    rtcm_package_id  INTEGER,
    rtcm_msg_type SMALLINT NOT NULL,
    mountpoint VARCHAR(50),
    sat_id CHAR(4),
    sat_signal CHAR(3),
    obs_code NUMERIC(13, 10),
    obs_phase NUMERIC(14, 11),
    obs_doppler NUMERIC(8, 4),
    obs_snr NUMERIC(6, 4),
    obs_lock_time_indicator INTEGER
);

SELECT create_hypertable('gnss_observations', 'obs_epoch', 'mountpoint', 2);
CREATE INDEX ON gnss_qc_summary(mountpoint, sat_id, sat_signal, obs_epoch DESC);
CREATE INDEX ON gnss_qc_summary(mountpoint, rtcm_msg_type, obs_epoch DESC);
