class Calculations:
    """ This class is use to get score on the basis of shifter data and score pattern. """

    def execute(self, method, instance, params):
        """ This function is used to call the other function acording to function name.

        Args:
            method (string): Method name to call method Example: "distance".
            instance (dict): Shifter data as dict.
            params  (list): Score pattern.

        Return:
            Method: The return value. """
        try:
            method = getattr(self, method, lambda: 'Invalid')
            return method(instance, params)
        except BaseException:
            return 'Invalid'

    @staticmethod
    def hour_match(instance, params):
        """ This function use to get score on the basis of shifter available hour.

        Args:
        instance (disc): shifter and vacated shifter available hour.
        params (int): hour Example: 24.

        Returns:
        float: The return value. """
        # Initialize return value.
        score = 0
        try:
            shifter_available_hour = instance["shifter_available_hour"]
            vacated_shifter_hour = instance["vacated_shifter_hour"]
            hour_intersect = [value for value in shifter_available_hour if value in vacated_shifter_hour]
            hour_alignment = len(hour_intersect)
            score = round(params["weight"] * (hour_alignment / float(params["pattern"])), 5)
        except BaseException:
            score = round(params["weight"] * params["default"], 5)
        return score

    @staticmethod
    def distance(instance, params):
        """ This function use to get score on tha basis of shifter distance from branch location.

        Args:
        instance (disc): Distance of shifter from branch location
        params (List): Score pattern for distance

        Returns:
        float: The return value. """
        # Initialize return value.
        score = 0
        try:
            distances = instance['distance']
            if not distances:
                score = round(params["weight"] * params["no_distance"], 5)
            elif distances >= params["distance_range"][0]:
                score = round(params["weight"] * params["distance_range"][1], 5)
            else:
                # Loop all patterns to get shifter distance score
                for data in params["pattern"]:
                    # Check if distance bettween given distance score pattern
                    if data[0] <= distances < data[1]:
                        score = round(params["weight"] * data[2], 5)
                        break
                    else:
                        score = round(params["weight"] * params["default"], 5)
        except BaseException:
            score = round(params["weight"] * params["no_distance"], 5)
        return score

    @staticmethod
    def pay_match(instance, params):
        """ This function use to get score on tha basis shifter pay rate for specific day.

        Args:
        instance (disc): shifter salary data
        params (List): Score pattern for pay match

        Returns:
        float: The return value. """
        # Initialize return value.
        score = 0
        try:
            shifter_pref_pay = instance['shifter_pref_pay']
            vacated_shift_pay = instance['vacated_shift_pay']
            pay_type = instance['pay_type']
            if pay_type != "Hourly":
                vacated_shift_pay = round(instance['vacated_shift_pay'] / 176, 5)
            pay_match_percent = 1 + round((vacated_shift_pay - shifter_pref_pay) / float(shifter_pref_pay), 5)
            # Loot all patterns to get shifter pay score
            for data in params["pattern"]:
                if pay_match_percent >= data[0]:
                    score = round(params["weight"] * data[1], 5)
                    break
                else:
                    score = round(params["weight"] * params["default"], 5)
        except BaseException:
            score = round(params["weight"] * params["default"], 5)
        return score

    @staticmethod
    def profile_score(instance, params):
        """ This function use to get score on tha basis of shifetr profile score data.

        Args:
        instance (disc): shifter no show data

        Returns:
        float: The return value. """
        # Initialize return value.
        score = 0
        try:
            shifter_score = instance["shifter_score"]
            shifter_score_type = type(shifter_score).__name__
            if shifter_score_type == 'int':
                score = round(params["weight"] * (shifter_score/params["pattern"]), 5)
            else:
                score = round(params["weight"] * shifter_score, 5)
        except BaseException:
            score = round(params["weight"] * params["default"], 5)
        return score

    @staticmethod
    def flexibility(instance, params):
        """ This function use to get score on tha basis of shifter flexibility to accept vacated shift.

        Args:
        instance (disc): shifter flexibility detail.
        params (disc): Score pattern for flexibility

        Returns:
        float: The return value. """
        # Initialize return value.
        score = 0
        try:
            times_invited = instance["times_invited"]
            times_accepted = instance["times_accepted"]
            for data in params["pattern"]:
                if times_invited <= data[0] and times_accepted == data[1]:
                    score = round(params["weight"] * data[2], 5)
                    break
                else:
                    score = round(params["weight"] * (times_accepted / times_invited), 5)
        except BaseException:
            score = round(params["weight"] * params["default"], 5)
        return score

    @staticmethod
    def reliability(instance, params):
        """ This function use to get score on tha basis of shifetr was not accept vacated shift recommendation.

        Args:
        instance (disc): shifter no show data

        Returns:
        float: The return value. """
        # Initialize return value.
        score = 0
        try:
            shifetr_no_show = instance["shifetr_no_show"]
            for data in params["pattern"]:
                if shifetr_no_show == data[0]:
                    score = round(params["weight"] * data[1], 5)
                    break
                else:
                    score = round(params["weight"] * params["default"], 5)
        except BaseException:
            score = round(params["weight"] * params["default"], 5)
        return score

    @staticmethod
    def convenience(instance, params):
        """ This function use to get score on tha basis of convenience.

        Args:
        instance (disc): shifter flexibility detail

        Returns:
        float: The return value. """
        # Initialize return value.
        score = 0
        try:
            shifter_branch = instance["shifter_branch"]
            vacated_shift_branch = instance["Vacated_shift_branch"]
            if not shifter_branch:
                score = round(params["weight"] * params["no_branch"], 5)
            else:
                shifter_shift_hours = instance["shifter_shift_hour"]
                vacated_shift_hours = instance["vacated_shift_hours"]
                after_shift = min(vacated_shift_hours) - max(shifter_shift_hours)
                if shifter_branch == vacated_shift_branch and after_shift > 0:
                    for data in params["pattern"]:
                        if data[0] <= after_shift <= data[1]:
                            score = round(params["weight"] * data[2], 5)
                            break
                        else:
                            score = round(params["weight"] * params["default"], 5)
                else:
                    score = round(params["weight"] * params["default"], 5)
            return score
        except BaseException:
            return params["no_branch"]
