#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 3 09:55:14 2023

@author: Lars Stenseng
@mail: lars@stenseng.net
"""

from logging import getLogger
from pathlib import Path, PurePath
from psycopg import sql
from psycopg_pool import ConnectionPool

from settings import IngestSettings

logger = getLogger("AnuGQC.anubis")


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
    qcFilePath: Path, ingestSettings: IngestSettings, dbPool: ConnectionPool
) -> None:
    with dbPool.connection() as dbConn:
        with dbConn.cursor() as dbCur:
            qcFilename = PurePath(qcFilePath).stem
            logger.debug(f"Processing qcfile: {qcFilename}")
            dbCur.execute(
                "SELECT COUNT(qc_file) FROM gnss_qc_summary WHERE qc_file=%s;",
                (qcFilename,),
            )
            existing_records = dbCur.fetchall()[0][0]
            logger.debug(f"{qcFilename} occured {existing_records} times.")
            if existing_records > 0:
                if ingestSettings.overwrite:
                    logger.debug(f"{qcFilename} exists and will be overwritten.")
                    dbCur.execute(
                        "DELETE FROM gnss_qc_summary WHERE qc_file=%s;",
                        (qcFilename,),
                    )
                    existing_records = 0
                    dbConn.commit()
                else:
                    logger.debug(f"{qcFilename} exists and will not be overwritten.")
            if existing_records == 0:
                with open(qcFilePath) as qcFile:
                    qcData = qcFile.read().splitlines()
                logger.debug(f"{len(qcData)}")
                if len(qcData) > 0:
                    logger.debug(f"{qcData[0:5]}")
                dbCur.execute(
                    "INSERT INTO gnss_qc_summary"
                    "(qc_epoch, qc_file, station_marker) VALUES (NOW(), %s, %s);",
                    (qcFilename, "BUDP"),
                )
                dbConn.commit()
