test_gamble_data = {
    "game_id": -1,
    "game_time": "2018-10-20T07:00",
    "gamble_id": -1,
    "game_type": "TEST",
    "guest": {"name": "CHA", "score": 120},
    "host": {"name": "ORL", "score": 88},
    "gamble_info": {
        "national": {
            "total_point": {"threshold": 216.0},
            "spread_point": {"host": -1.0, "response": {"on_hit": 0.5}},
        },
        "local": {
            "total_point": {
                "threshold": 216.5,
                "response": {"under": 1.75, "over": 1.75},
            },
            "spread_point": {"host": -2.5, "response": {"host": 1.75, "guest": 1.75}},
            "original": {"response": {"guest": 1.55, "host": 1.95}},
        },
    },
    "judgement": {
        "game": {
            "national": {"total_point": "under", "spread_point": "guest"},
            "local": {
                "total_point": "under",
                "spread_point": "guest",
                "original": "guest",
            },
        },
        "prediction": [
            {
                "group": "all_member",
                "national": {
                    "total_point": {
                        "matched_info": {
                            "is_major": False,
                            "percentage": 41,
                            "population": 237,
                        }
                    },
                    "spread_point": {
                        "matched_info": {
                            "is_major": True,
                            "percentage": 65,
                            "population": 1042,
                        }
                    },
                },
                "local": {
                    "total_point": {
                        "matched_info": {
                            "is_major": False,
                            "percentage": 43,
                            "population": 250,
                        }
                    },
                    "spread_point": {
                        "matched_info": {
                            "is_major": True,
                            "percentage": 62,
                            "population": 852,
                        }
                    },
                    "original": {
                        "matched_info": {
                            "is_major": True,
                            "percentage": 73,
                            "population": 368,
                        }
                    },
                },
            },
            {
                "group": "all_prefer",
                "national": {
                    "total_point": {
                        "matched_info": {
                            "is_major": True,
                            "percentage": 56,
                            "population": 40,
                        }
                    },
                    "spread_point": {
                        "matched_info": {
                            "is_major": True,
                            "percentage": 69,
                            "population": 221,
                        }
                    },
                },
                "local": {
                    "total_point": {
                        "matched_info": {
                            "is_major": False,
                            "percentage": 44,
                            "population": 32,
                        }
                    },
                    "spread_point": {
                        "matched_info": {
                            "is_major": True,
                            "percentage": 57,
                            "population": 125,
                        }
                    },
                    "original": {
                        "matched_info": {
                            "is_major": True,
                            "percentage": 0,
                            "population": 0,
                        }
                    },
                },
            },
            {
                "group": "more_than_sixty",
                "national": {
                    "total_point": {
                        "matched_info": {
                            "is_major": False,
                            "percentage": 31,
                            "population": 8,
                        }
                    },
                    "spread_point": {
                        "matched_info": {
                            "is_major": True,
                            "percentage": 55,
                            "population": 23,
                        }
                    },
                },
                "local": {
                    "total_point": {
                        "matched_info": {
                            "is_major": False,
                            "percentage": 41,
                            "population": 7,
                        }
                    },
                    "spread_point": {
                        "matched_info": {
                            "is_major": False,
                            "percentage": 36,
                            "population": 9,
                        }
                    },
                    "original": {
                        "matched_info": {
                            "is_major": True,
                            "percentage": 0,
                            "population": 0,
                        }
                    },
                },
            },
            {
                "group": "top_100",
                "national": {
                    "total_point": {
                        "matched_info": {
                            "is_major": False,
                            "percentage": 35,
                            "population": 15,
                        }
                    },
                    "spread_point": {
                        "matched_info": {
                            "is_major": True,
                            "percentage": 53,
                            "population": 26,
                        }
                    },
                },
                "local": {
                    "total_point": {
                        "matched_info": {
                            "is_major": False,
                            "percentage": 35,
                            "population": 15,
                        }
                    },
                    "spread_point": {
                        "matched_info": {
                            "is_major": True,
                            "percentage": 50,
                            "population": 27,
                        }
                    },
                    "original": {
                        "matched_info": {
                            "is_major": True,
                            "percentage": 0,
                            "population": 0,
                        }
                    },
                },
            },
        ],
    },
    "prediction": [
        {
            "group": "all_member",
            "national": {
                "total_point": {
                    "over": {"percentage": 59, "population": 338},
                    "under": {"percentage": 41, "population": 237},
                },
                "spread_point": {
                    "guest": {"percentage": 65, "population": 1042},
                    "host": {"percentage": 35, "population": 553},
                },
            },
            "local": {
                "total_point": {
                    "over": {"percentage": 57, "population": 333},
                    "under": {"percentage": 43, "population": 250},
                },
                "spread_point": {
                    "guest": {"percentage": 62, "population": 852},
                    "host": {"percentage": 38, "population": 524},
                },
                "original": {
                    "guest": {"percentage": 73, "population": 368},
                    "host": {"percentage": 27, "population": 137},
                },
            },
        },
        {
            "group": "all_prefer",
            "national": {
                "total_point": {
                    "over": {"percentage": 44, "population": 32},
                    "under": {"percentage": 56, "population": 40},
                },
                "spread_point": {
                    "guest": {"percentage": 69, "population": 221},
                    "host": {"percentage": 31, "population": 99},
                },
            },
            "local": {
                "total_point": {
                    "over": {"percentage": 56, "population": 40},
                    "under": {"percentage": 44, "population": 32},
                },
                "spread_point": {
                    "guest": {"percentage": 57, "population": 125},
                    "host": {"percentage": 43, "population": 95},
                },
                "original": {
                    "guest": {"percentage": 0, "population": 0},
                    "host": {"percentage": 0, "population": 0},
                },
            },
        },
        {
            "group": "more_than_sixty",
            "national": {
                "total_point": {
                    "over": {"percentage": 69, "population": 18},
                    "under": {"percentage": 31, "population": 8},
                },
                "spread_point": {
                    "guest": {"percentage": 55, "population": 23},
                    "host": {"percentage": 45, "population": 19},
                },
            },
            "local": {
                "total_point": {
                    "over": {"percentage": 59, "population": 10},
                    "under": {"percentage": 41, "population": 7},
                },
                "spread_point": {
                    "guest": {"percentage": 36, "population": 9},
                    "host": {"percentage": 64, "population": 16},
                },
                "original": {
                    "guest": {"percentage": 0, "population": 0},
                    "host": {"percentage": 0, "population": 0},
                },
            },
        },
        {
            "group": "top_100",
            "national": {
                "total_point": {
                    "over": {"percentage": 65, "population": 28},
                    "under": {"percentage": 35, "population": 15},
                },
                "spread_point": {
                    "guest": {"percentage": 53, "population": 26},
                    "host": {"percentage": 47, "population": 23},
                },
            },
            "local": {
                "total_point": {
                    "over": {"percentage": 65, "population": 28},
                    "under": {"percentage": 35, "population": 15},
                },
                "spread_point": {
                    "guest": {"percentage": 50, "population": 27},
                    "host": {"percentage": 50, "population": 27},
                },
                "original": {
                    "guest": {"percentage": 0, "population": 0},
                    "host": {"percentage": 0, "population": 0},
                },
            },
        },
    ],
}
