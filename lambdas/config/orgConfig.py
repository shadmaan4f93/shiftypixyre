class ConfigLoaders:
    """ This is configuration class to Initialize disqualify and score pattern setting for the Organizations. """
    # Initialize settings.
    setting = {}
    # setting for organizationId = orgid1
    scoring_structures = {
        "hour_match": {
            "pattern": 24,
            "default": 0,
            "weight": 0.11
        },
        "distance": {
            "pattern": [(10, 20, 0.8), (20, 30, 0.7), (30, 50, 0.6), (50, 100, 0.5)],
            "default": 1,
            "no_distance": 0.8,
            "distance_range": (100, 0),
            "weight": 0.11
        },
        "pay_match": {
            "pattern": [(1.5, 1), (1, 0.9), (0.67, 0.5)],
            "default": 0,
            "weight": 0.15
        },
        "profile_score": {
            "pattern": 5,
            "default": 0,
            "weight": 0.06
        },
        "flexibility": {
            "pattern": [(2, 0, 0.5)],
            "default": 0,
            "weight": 0.19
        },
        "reliability": {
            "pattern": [(0, 1), (1, 0.67)],
            "default": 0.67,
            "weight": 0.19
        },
        "convenience": {
            "pattern": [(1, 1.5, 1), (1.5, 2, 0.9)],
            "default": 0.75,
            "no_branch": 0.5,
            "weight": 0.19
        }
    }
    disqualify_structures = {
        "static_data_filter": {
            "vacated_shifter": True,
            "qualify_distance": 100,
            "jp_id_filter": True
        },
        "volatile_data_filter": {
            "shift_overlap": True,
            "day_overtime_risk": {
                "day_overtime_range": 8,
            },
            "week_overtime_risk": {
                "week_overtime_range": 40,
            },
            "duration_difference": {
                "duration_difference_range": 1
            },
            "flexibility_filter": {
                "invited_range": 5,
                "accepted_range": 0,
            },
            "reliability_filter": {
                "noshow_range": 3
            },
            "recommended_filter": {
                "recommended_range": 5,
                "invited_range": 0
            },
            "position_filter": {
                "completed_position_range": 0
            },
        }
    }

    setting["default"] = {
        "scoring_structures": scoring_structures,
        "disqualify_structures": disqualify_structures
    }
    setting["11e91af3559132a6869d0242ac110003"] = {
        "scoring_structures": scoring_structures,
        "disqualify_structures": disqualify_structures
    }

    @classmethod
    def get_organizationsetting(cls, orgId):
        """ This function use to return pattern acording to organization id,

        Args:
        orgId (string): Organization id.

        Returns:
        dict: The return value. """
        try:
            if orgId not in cls.setting:
                orgId = "default"
            return cls.setting[orgId]
        except KeyError:
            return None
