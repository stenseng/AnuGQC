#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 09:34:14 2023

@author: Lars Stenseng
@mail: lars@stenseng.net
"""

from argparse import ArgumentParser
from configparser import ConfigParser
from psycopg_pool import ConnectionPool
from settings import DbSettings, IngestSettings

dbPool = ConnectionPool("", open=False)


def main(dbSettings: DbSettings, ingestSettings: IngestSettings):
    print(dbPool.conninfo)
    dbPool.conninfo = (
        f"host={dbSettings.host} port={dbSettings.port} dbname={dbSettings.database} "
        + f"user={dbSettings.user} password={dbSettings.password}"
    )
    dbPool.open()
    dbPool.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        help="Config file  with database and ingestion settings",
        default="/app/config/ingest.conf",
    )
    parser.add_argument(
        "-p",
        "--path",
        action="append",
        help="Paths to folders with xtr QC files from Anubis. Overrides path list "
        + "in ingest.conf",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        default=False,
        help="Traverse subdirs in the path and process all QC files.",
    )
    parser.add_argument(
        "-e",
        "--filetypes",
        action="append",
        default="xtr",
        help="Ingest files with this file extension. Default is *.xtr",
    )
    args = parser.parse_args()

    config = ConfigParser()
    config.read(args.config)

    dbSettings = DbSettings()
    dbSettings.host = config["DbSettings"]["host"]
    dbSettings.port = config.getint("DbSettings", "port")
    dbSettings.database = config["DbSettings"]["database"]
    dbSettings.user = config["DbSettings"]["user"]
    dbSettings.password = config["DbSettings"]["password"]

    ingestSettings = IngestSettings()
    ingestSettings.fileTypes = list(
        map(str.strip, config["IngestSettings"]["fileTypes"].split(","))
    )
    if ingestSettings.fileTypes == [""]:
        ingestSettings.fileTypes = []
    ingestSettings.paths = list(
        map(str.strip, config["IngestSettings"]["paths"].split(","))
    )
    if ingestSettings.paths == [""]:
        ingestSettings.paths = []
    ingestSettings.recursive = config.getboolean("IngestSettings", "recursive")
    ingestSettings.overwrite = config.getboolean("IngestSettings", "overwrite")
