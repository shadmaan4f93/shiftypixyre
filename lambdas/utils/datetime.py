from datetime import datetime
from datetime import timedelta
import iso8601


class DateTimeDuration:
    """ Date time duration class. """

    @staticmethod
    def is_iso_formate(iso_date_time_str):
        """ This function is use to check iso8601 datetime formate.

        Args:
            iso_date_time_str (string): DateTime as string.

        Returns:
        Boolean: The return value. """

        try:
            iso8601.parse_date(iso_date_time_str)
            return True
        except iso8601.ParseError:
            return False

    @staticmethod
    def get_datetime_obj(iso_date_time_str):
        """ This function convert iso8601 datetime string into  datetime object.

        Args:
        iso_date_time_str (string): DateTime as string.

        Returns:
        object: The return value. """

        try:
            date_time_obj = iso8601.parse_date(iso_date_time_str)
            return date_time_obj
        except iso8601.ParseError:
            return None

    @staticmethod
    def get_datetime_iso_str(date_time_obj):
        """ This function convert datetime object into iso8601 datetime string.

        Args:
        date_time_obj (object): date_time_obj datetime object formate date time.

        Returns:
        string: The return value. """

        try:
            datetime_ios_str = date_time_obj.isoformat()
            return datetime_ios_str
        except iso8601.ParseError:
            return None

    @staticmethod
    def get_datetime_str(date_time_obj, datetime_format):
        """ This function convert datetime object into datetime string.

        Args:
        date_time_obj (object): date_time_obj datetime object formate date time.

        Returns:
        string: The return value. """

        try:
            date_time_str = datetime.strftime(date_time_obj, datetime_format)
            return date_time_str
        except BaseException:
            return None

    @staticmethod
    def get_duration(start_date_time, end_date_time, difference_in=None):
        """ This function use to get difference between two datetime iso8601 string.

        Args:
        start_date_time (string): iso8601 datetime string.
        end_date_time (string): iso8601 datetime string.

        Returns:
        object/float: Default to difference object. """

        # Initialize return vakue.
        return_value = None
        try:
            start_datetime_obj = iso8601.parse_date(start_date_time)
            end_datetime_obj = iso8601.parse_date(end_date_time)
            duration = end_datetime_obj - start_datetime_obj
            if difference_in == "days":
                return_value = duration.days
            elif difference_in == "hour":
                return_value = (duration.days * 24) + (duration.seconds / 3600)
            elif difference_in == "minutes":
                return_value = ((duration.days * 24) + (duration.seconds / 3600)) * 60
            elif difference_in == "seconds":
                return_value = (((duration.days * 24) + (duration.seconds / 3600)) * 60) * 60
            else:
                return_value = duration
        except BaseException:
            return_value = None
        return return_value

    @staticmethod
    def extend_date_time(iso_date_time_str, increment_value, extend_in):
        """ This function use to get extend datetime.

        Args:
        iso_date_time_str (string): iso8601 datetime string.
        increment_value (int): increment value as int.

        Returns:
        datetimeobject: The return value."""

        # Initialize return value.
        return_value = None
        try:
            date_time_obj = iso8601.parse_date(iso_date_time_str)
            if extend_in == "days":
                return_value = date_time_obj + timedelta(days=increment_value)
            elif extend_in == "hours":
                return_value = date_time_obj + timedelta(hours=increment_value)
            elif extend_in == "minutes":
                return_value = date_time_obj + timedelta(minutes=increment_value)
            else:
                return_value = None
        except BaseException:
            return_value = None
        return return_value

    @staticmethod
    def get_hour_list(start_datetime, end_datetime):
        """ This function use to get list of hours betwwen two times.

        Args:
        hour_range (tupples): hour range as tupples. Example: (12, 22).

        Returns:
        list: The return value."""

        try:
            start_datetime = iso8601.parse_date(start_datetime)
            end_datetime = iso8601.parse_date(end_datetime)
            start_hour = start_datetime.hour
            end_hour = end_datetime.hour
            hour_list = []
            while True:
                hour_list.append(start_hour)
                start_hour = start_hour + 1
                if start_hour == 24:
                    start_hour = 0
                if start_hour == end_hour:
                    hour_list.append(start_hour)
                    break
        except BaseException:
            hour_list = []
        return hour_list

    @staticmethod
    def is_date_match(shifter_datetime, vacated_datetime, match_type=None):
        # Initialize return value.
        return_value = False
        try:
            shifter_start_datetime = DateTimeDuration.get_datetime_obj(shifter_datetime["starttime"])
            shifter_end_datetime = DateTimeDuration.get_datetime_obj(shifter_datetime["endtime"])
            vacated_start_datetime = DateTimeDuration.get_datetime_obj(vacated_datetime["startTime"])
            vacated_end_datetime = DateTimeDuration.get_datetime_obj(vacated_datetime["endTime"])
            if match_type == "date":
                if (shifter_start_datetime.date() == shifter_end_datetime.date() and
                        vacated_start_datetime.date() == vacated_end_datetime.date() and
                        shifter_start_datetime.date() == vacated_start_datetime.date()):
                    return_value = True
            if match_type == "week":
                if (shifter_start_datetime.isocalendar()[1] == shifter_end_datetime.isocalendar()[1] and
                        vacated_start_datetime.isocalendar()[1] == vacated_end_datetime.isocalendar()[1] and
                        shifter_start_datetime.isocalendar()[1] == vacated_start_datetime.isocalendar()[1]):
                    return_value = True
        except BaseException:
            return_value = None
        return return_value
