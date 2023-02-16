#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:01:21 2023

@author: Lars Stenseng
@mail: lars@stenseng.net
"""

from dataclasses import dataclass


@dataclass
class DbSettings:
    host: str = None
    port: int = None
    database: str = None
    user: str = None
    password: str = None


@dataclass
class IngestSettings:
    fileTypes: list[str] = field(default_factory=lambda: [])
    paths: list[str] = field(default_factory=lambda: [])
    recursive: bool = None
    overwrite: bool = None
