from mongoengine import Document, StringField, IntField, GeoPointField, QuerySet, ListField
from mongoengine.queryset.visitor import Q


class Qualified(QuerySet):
    def get_shifters(self, vacated_params, disqualify_params):
        branch_location = [vacated_params['jobLocationLong'], vacated_params['jobLocationLat']]
        return self.filter(
            (Q(
                location__within_distance=[branch_location, disqualify_params["qualify_distance"]]
                ) or Q(location=[0, 0])),
            shifterid__ne=vacated_params['vacatedShifterId'],
            existingshifterjpid__iexact=vacated_params['jobProviderId']
            )


class Shifts(Document):
    id = StringField(required=True, primary_key=True)
    shiftid = StringField(required=True)
    jobproviderid = StringField(required=False)
    location = GeoPointField(required=False)
    shiftdetail = ListField(required=False)


class Shifters(Document):
    meta = {'queryset_class': Qualified}
    id = StringField(required=True, primary_key=True)
    shifterid = StringField(required=True)
    existingshifterjpid = StringField(required=False, default=None)
    position = ListField(required=False)
    rating = IntField(required=False)
    location = GeoPointField(required=False)
    shifteravailability = ListField(required=False)
