#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 3 09:55:14 2023

@author: Lars Stenseng
@mail: lars@stenseng.net
"""

from sys import stderr
from time import sleep
from psycopg_pool import ConnectionPool

from settings import IngestSettings


def ingestAnubisFiles(ingestSettings: IngestSettings, dbPool: ConnectionPool) -> None:
    with dbPool.connection() as dbConn:
        for test in range(100):
            dbConn.execute(
                "INSERT INTO gnss_qc_summary"
                "(qc_epoch, qc_file, station_marker) VALUES (NOW(), %s, %s)",
                (f"test{test}", "BUDP"),
            )
            dbConn.commit()
            sleep(0.1)


def ingestAnubisFile(filename: str, dbConn) -> None:
    pass
