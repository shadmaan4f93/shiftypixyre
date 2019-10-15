from lambdas.config.config import logger


class QualifyFilter:
    """ This class is use to filter a shifter on the basis of disqulify params and vacated shift. """

    def execute(self, method, instance):
        """ This method is used to call the class method acording to method name.

        Args:
            method (string): Method name to call method Example: "shift_overlap".
            instance (dict): Shifter, vacated shift data as dict.

        Return:
            Method: The return value. """
        try:
            method = getattr(self, method, lambda: 'Invalid')
            return method(instance)
        except BaseException:
            return 'Invalid'

    @staticmethod
    def shift_overlap(instance):
        """ This function used to filter shifter shift time and vacated shift time overlap each other.

        Args:
            instance (dict): {
                shifter_hour_list: List of hours between shifter start and end time.
                vacated_hour_list: List of hours between vacated start and end time.
                disqualify_params: Status to filter Example: True/False
            }

        Returns:
            boolean: The disqualify status. """
        # Initialize return value.
        return_value = "qualified"
        try:
            disqualify_params = instance["disqualify_params"]
            overlap = []
            if disqualify_params:
                shifter_hour_list = instance["shifter_hour_list"]
                vacated_hour_list = instance["vacated_hour_list"]
                overlap = [value for value in shifter_hour_list if value in vacated_hour_list]
            if overlap:
                logger.info("Disqualified Reason: shift_overlap")
                return_value = "disqualified"
        except BaseException as ex:
            logger.error("Disqualified Reason: EXCEPTION in shift_overlap: %s", str(ex))
            return_value = "disqualified"
        return return_value

    @staticmethod
    def day_overtime_risk(instance):
        """ This function used to filter shifter shift and vacated shift over time risk for same day.

        Args:
            instance (dict): {
                shifter_day_hour: shifter shift duration from start to end.
                vacated_hour: vacated shift duration from start to end.
                disqualify_params: params for filter overtime risk for the same day.
            }

        Returns:
            boolean: The filter status. """
        # Initialize return value.
        return_value = "qualified"
        try:
            shifter_shift_hour = instance["shifter_day_hour"]
            vacated_shift_hour = instance["vacated_hour"]
            disqualify_params = instance["disqualify_params"]
            shift_duration_count = shifter_shift_hour + vacated_shift_hour
            if shift_duration_count > disqualify_params["day_overtime_range"]:
                logger.info("Disqualified Reason: day_overtime_risk")
                return_value = "disqualified"
        except BaseException as ex:
            logger.error("Disqualified Reason: EXCEPTION in day_overtime_risk: %s", str(ex))
            return_value = "disqualified"
        return return_value

    @staticmethod
    def week_overtime_risk(instance):
        """ This function used to filter shifter shift and vacated shift over time risk for a week.

        Args:
        instance (dict): {
            shifter_week_hour: Total conformed shift duration hour in week.
            vacated_hour: vacated shift duration from start to end.
            disqualify_params: params for filter week over time risk.

        Returns:
            boolean: The filter status. """
        # Initialize return value.
        return_value = "qualified"
        try:
            shifter_week_hour = instance["shifter_week_hour"]
            vacated_shift_hour = instance["vacated_hour"]
            disqualify_params = instance["disqualify_params"]
            week_duration = shifter_week_hour + vacated_shift_hour
            if week_duration > disqualify_params["week_overtime_range"]:
                logger.info("Disqualified Reason: week_overtime_risk")
                return_value = "disqualified"
        except BaseException as ex:
            logger.error("Disqualified Reason: EXCEPTION in week_overtime_risk: %s", str(ex))
            return_value = "disqualified"
        return return_value

    @staticmethod
    def duration_difference(instance):
        """ This function used to filter shifter shift and vacated shift difference time risk.

        Args:
        instance (dict): shifter, vacated shift data.

        Returns:
        boolean: The return value. """
        # Initialize return value
        return_value = "qualified"
        try:
            duration_difference_list = instance["duration_difference_list"]
            disqualify_params = instance["duration_difference_range"]
            for difference in duration_difference_list:
                if difference <= disqualify_params:
                    logger.info("Disqualified Reason: duration_difference")
                    return_value = "disqualified"
        except BaseException as ex:
            logger.error("Disqualified Reason: EXCEPTION in duration_difference: %s", str(ex))
            return_value = "disqualified"
        return return_value

    @staticmethod
    def position_filter(instance):
        """ This function used to filter shift position completed for vacated shift.

        Args:
        shifter (dict): shifter, vacated shift data.

        Returns:
        boolean: The return value. """
        # Initialize return value.
        return_value = "qualified"
        try:
            completed_position_count = instance["completed_position_count"]
            completed_position_range = instance["completed_position_range"]
            if completed_position_count == completed_position_range:
                logger.info("Disqualified Reason: position_filter")
                return_value = "disqualified"
        except BaseException as ex:
            logger.error("Disqualified Reason: EXCEPTION in position_filter: %s", str(ex))
            return_value = "disqualified"
        return return_value

    @staticmethod
    def recommended_filter(instance):
        """ This function used to filter shifter recommended on the basis of recommended count.

        Args:
        shifter (dict): shifter, vacated shift data.

        Returns:
        boolean: The return value. """
        # Initialize return value.
        return_value = "qualified"
        try:
            recommended_count = instance["recommendedcount"]
            invited_count = instance["invitedcount"]
            recommended_range = instance["recommended_range"]
            invited_range = instance["invited_range"]
            if recommended_count >= recommended_range and invited_count == invited_range:
                logger.info("Disqualified Reason: recommend_filter")
                return_value = "disqualified"
        except BaseException as ex:
            logger.error("Disqualified Reason: EXCEPTION in recommend_filter: %s", str(ex))
            return_value = "disqualified"
        return return_value

    @staticmethod
    def flexibility_filter(instance):
        """ This function used to check flexibility of shifter on the basis of invited and accepted count.

        Args:
        instance (dict): shifter, vacated shift data.

        Returns:
        boolean: The return value. """
        # Initialize return value.
        return_value = "qualified"
        try:
            invited_count = instance["invitedcount"]
            accepted_count = instance["acceptedcount"]
            accepted_range = instance["accepted_range"]
            invited_range = instance["invited_range"]
            if invited_count >= invited_range and accepted_count == accepted_range:
                logger.info("Disqualified Reason: day_overtime_risk")
                return_value = "disqualified"
        except BaseException as ex:
            logger.error("Disqualified Reason: EXCEPTION in flexibility_filter: %s", str(ex))
            return_value = "disqualified"
        return return_value

    @staticmethod
    def reliability_filter(instance):
        """ This function used to check reliability of shifter on the basis of nowshow count.

        Args:
        shifter (dict): shifter, vacated shift data.

        Returns:
        boolean: The return value. """
        # Initialize return value.
        return_value = "qualified"
        try:
            noshow_count = instance["noshowcount"]
            noshow_range = instance["noshow_range"]
            if noshow_count >= noshow_range:
                logger.info("Disqualified Reason: reliability_filter")
                return_value = "disqualified"
        except BaseException as ex:
            logger.error("Disqualified Reason: EXCEPTION in reliability_filter: %s", str(ex))
            return_value = "disqualified"
        return return_value
