#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:01:21 2023

@author: Lars Stenseng
@mail: lars@stenseng.net
"""

from dataclasses import dataclass, field


@dataclass
class DbSettings:
    host: str = ""
    port: int = -1
    database: str = ""
    user: str = ""
    password: str = ""


@dataclass
class IngestSettings:
    fileTypes: list[str] = field(default_factory=lambda: [])
    paths: list[str] = field(default_factory=lambda: [])
    recursive: bool = False
    overwrite: bool = False
