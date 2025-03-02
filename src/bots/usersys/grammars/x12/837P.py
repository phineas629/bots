# -*- coding: utf-8 -*-

from bots.botsconfig import *

syntax = {
    "version": "00403",
    "functionalgroup": "HC",
    "envelope": "ISA",
    "field_sep": "*",
    "sub_field_sep": ":",
    "element_sep": "~",
    "record_sep": "\n",
}

structure = [
    {
        ID: "ISA",
        MIN: 1,
        MAX: 1,
        LEVEL: [
            {
                ID: "GS",
                MIN: 1,
                MAX: 99,
                LEVEL: [
                    {
                        ID: "ST",
                        MIN: 1,
                        MAX: 999999,
                        LEVEL: [
                            {ID: "BHT", MIN: 1, MAX: 1},
                            {ID: "NM1", MIN: 1, MAX: 99999},
                            {
                                ID: "HL",
                                MIN: 1,
                                MAX: 99999,
                                LEVEL: [
                                    {ID: "NM1", MIN: 0, MAX: 99999},
                                    {ID: "N3", MIN: 0, MAX: 1},
                                    {ID: "N4", MIN: 0, MAX: 1},
                                    {ID: "DMG", MIN: 0, MAX: 1},
                                    {ID: "SBR", MIN: 0, MAX: 1},
                                    {ID: "PAT", MIN: 0, MAX: 1},
                                    {
                                        ID: "CLM",
                                        MIN: 0,
                                        MAX: 99999,
                                        LEVEL: [
                                            {ID: "DTP", MIN: 0, MAX: 99999},
                                            {
                                                ID: "LX",
                                                MIN: 0,
                                                MAX: 99999,
                                                LEVEL: [
                                                    {ID: "SV1", MIN: 0, MAX: 1},
                                                    {ID: "DTP", MIN: 0, MAX: 99999},
                                                ],
                                            },
                                        ],
                                    },
                                ],
                            },
                            {ID: "SE", MIN: 1, MAX: 1},
                        ],
                    }
                ],
            },
            {ID: "GE", MIN: 1, MAX: 1},
        ],
    },
    {ID: "IEA", MIN: 1, MAX: 1},
]

# Define record definitions and segments
recorddefs = {
    "ISA": [
        ["BOTSID", "M", 3, "AN"],
        ["ISA01", "M", 2, "AN"],
        ["ISA02", "M", 10, "AN"],
        ["ISA03", "M", 2, "AN"],
        ["ISA04", "M", 10, "AN"],
        ["ISA05", "M", 2, "AN"],
        ["ISA06", "M", 15, "AN"],
        ["ISA07", "M", 2, "AN"],
        ["ISA08", "M", 15, "AN"],
        ["ISA09", "M", 6, "DT", "YYMMDD"],
        ["ISA10", "M", 4, "TM", "HHMM"],
        ["ISA11", "M", 1, "AN"],
        ["ISA12", "M", 5, "AN"],
        ["ISA13", "M", 9, "N0"],
        ["ISA14", "M", 1, "N0"],
        ["ISA15", "M", 1, "AN"],
        ["ISA16", "M", 1, "AN"],
    ],
    "GS": [
        ["BOTSID", "M", 2, "AN"],
        ["GS01", "M", 2, "AN"],
        ["GS02", "M", 15, "AN"],
        ["GS03", "M", 15, "AN"],
        ["GS04", "M", 8, "DT", "CCYYMMDD"],
        ["GS05", "M", 4, "TM", "HHMM"],
        ["GS06", "M", 9, "N0"],
        ["GS07", "M", 1, "AN"],
        ["GS08", "M", 12, "AN"],
    ],
    "ST": [
        ["BOTSID", "M", 2, "AN"],
        ["ST01", "M", 3, "AN"],
        ["ST02", "M", 9, "AN"],
        ["ST03", "C", 35, "AN"],
    ],
    "BHT": [
        ["BOTSID", "M", 3, "AN"],
        ["BHT01", "M", 4, "AN"],
        ["BHT02", "M", 2, "AN"],
        ["BHT03", "M", 50, "AN"],
        ["BHT04", "M", 8, "DT", "CCYYMMDD"],
        ["BHT05", "M", 8, "TM", "HHMM"],
        ["BHT06", "M", 2, "AN"],
    ],
    "NM1": [
        ["BOTSID", "M", 3, "AN"],
        ["NM101", "M", 3, "AN"],
        ["NM102", "M", 1, "AN"],
        ["NM103", "C", 60, "AN"],
        ["NM104", "C", 35, "AN"],
        ["NM105", "C", 25, "AN"],
        ["NM106", "C", 10, "AN"],
        ["NM107", "C", 10, "AN"],
        ["NM108", "C", 2, "AN"],
        ["NM109", "C", 80, "AN"],
    ],
    "N3": [
        ["BOTSID", "M", 2, "AN"],
        ["N301", "M", 55, "AN"],
        ["N302", "C", 55, "AN"],
    ],
    "N4": [
        ["BOTSID", "M", 2, "AN"],
        ["N401", "M", 30, "AN"],
        ["N402", "C", 2, "AN"],
        ["N403", "C", 15, "AN"],
    ],
    "DMG": [
        ["BOTSID", "M", 3, "AN"],
        ["DMG01", "M", 3, "AN"],
        ["DMG02", "M", 8, "DT", "CCYYMMDD"],
        ["DMG03", "M", 1, "AN"],
    ],
    "HL": [
        ["BOTSID", "M", 2, "AN"],
        ["HL01", "M", 12, "AN"],
        ["HL02", "C", 12, "AN"],
        ["HL03", "M", 2, "AN"],
        ["HL04", "M", 1, "AN"],
    ],
    "SBR": [
        ["BOTSID", "M", 3, "AN"],
        ["SBR01", "M", 1, "AN"],
        ["SBR02", "C", 2, "AN"],
        ["SBR03", "C", 60, "AN"],
        ["SBR04", "C", 60, "AN"],
    ],
    "PAT": [
        ["BOTSID", "M", 3, "AN"],
        ["PAT01", "M", 2, "AN"],
    ],
    "CLM": [
        ["BOTSID", "M", 3, "AN"],
        ["CLM01", "M", 38, "AN"],
        ["CLM02", "M", 18, "R"],
        ["CLM05-1", "M", 2, "AN"],
        ["CLM05-2", "M", 1, "AN"],
        ["CLM05-3", "M", 1, "AN"],
        ["CLM06", "C", 1, "AN"],
        ["CLM07", "C", 1, "AN"],
        ["CLM08", "C", 1, "AN"],
        ["CLM09", "C", 1, "AN"],
    ],
    "DTP": [
        ["BOTSID", "M", 3, "AN"],
        ["DTP01", "M", 3, "AN"],
        ["DTP02", "M", 2, "AN"],
        ["DTP03", "M", 8, "DT", "CCYYMMDD"],
    ],
    "LX": [
        ["BOTSID", "M", 2, "AN"],
        ["LX01", "M", 6, "N0"],
    ],
    "SV1": [
        ["BOTSID", "M", 3, "AN"],
        ["SV101-1", "M", 2, "AN"],
        ["SV101-2", "M", 48, "AN"],
        ["SV102", "M", 18, "R"],
        ["SV103", "M", 2, "AN"],
        ["SV104", "M", 15, "R"],
    ],
    "SE": [
        ["BOTSID", "M", 2, "AN"],
        ["SE01", "M", 6, "N0"],
        ["SE02", "M", 9, "AN"],
    ],
    "GE": [
        ["BOTSID", "M", 2, "AN"],
        ["GE01", "M", 6, "N0"],
        ["GE02", "M", 9, "N0"],
    ],
    "IEA": [
        ["BOTSID", "M", 3, "AN"],
        ["IEA01", "M", 6, "N0"],
        ["IEA02", "M", 9, "N0"],
    ],
}
