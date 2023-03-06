#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 3 09:55:14 2023

@author: Lars Stenseng
@mail: lars@stenseng.net
"""

from glob import iglob
import logging
from pathlib import Path, PurePath
from time import sleep
from psycopg_pool import ConnectionPool

from settings import IngestSettings

logger = logging.getLogger("AnuGQC.anubis")


def ingestAnubisFiles(ingestSettings: IngestSettings, dbPool: ConnectionPool) -> None:
    for qcType in ingestSettings.fileTypes:
        logger.debug(f"Looking for: {qcType}")
        for qcPath in ingestSettings.paths:
            logger.debug(f"Traversing: {qcPath}")
            if ingestSettings.recursive:
                for qcFile in Path(qcPath).glob(f"**/*.{qcType}"):
                    logger.debug(f"Found qcfile: {qcFile.resolve()}")
                    ingestAnubisFile(qcFile.resolve(), ingestSettings, dbPool)
            else:
                for qcFile in Path(qcPath).glob(f"*.{qcType}"):
                    logger.debug(f"Found qcfile: {qcFile.resolve()}")
                    ingestAnubisFile(qcFile.resolve(), ingestSettings, dbPool)


def ingestAnubisFile(
    qcFile: Path, ingestSettings: IngestSettings, dbPool: ConnectionPool
) -> None:
    with dbPool.connection() as dbConn:
        qcFilename = PurePath(qcFile).stem
        logger.debug(f"Processing qcfile: {qcFilename}")
        dbConn.execute(
            "INSERT INTO gnss_qc_summary"
            "(qc_epoch, qc_file, station_marker) VALUES (NOW(), %s, %s)",
            (qcFilename, "BUDP"),
        )
        dbConn.commit()
