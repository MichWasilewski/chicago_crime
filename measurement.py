from datetime import datetime

class Measurement:

    def __init__(self, id: str, domestic: bool, arrest: bool, case_number= None, date=None, block=None, iucr=None,
                 primary_type=None, description=None, beat=None, district=None, fbi_code=None, year=None,
                 updated_on=None, community_area=None, ward=None, location=None, location_description=None, **kwargs):
        self.location: dict = {'lat': location['latitude'], 'lon': location['longitude']} if location else {'lat': 0, 'lon': 0}
        self.crime_id: str = id
        self.case_number: str = case_number if case_number else ""
        self.crime_date: str = date if date else ""
        self.block: str = block if block else ""
        self.crime_reporting_code: str = iucr if iucr else ""
        self.primary_type: str = primary_type if primary_type else ""
        self.description: str = description if description else ""
        self.location_description: str = location_description if location_description else ""
        self.arrest: bool = arrest
        self.domestic: bool = domestic
        self.smallest_area_of_operation: str = beat if beat else ""
        self.district: str = district if district else ""
        self.ward: str = ward if ward else ""
        self.community_area: int = community_area if community_area else 0
        self.fbi_code: str = fbi_code if fbi_code else ""
        self.year: int = year if year else 0
        self.updated_on: str = updated_on if updated_on else ""
        self.detail_date = self.detail_date()

    def detail_date(self):
        if self.crime_date != "":
            date_object = datetime.strptime(self.crime_date, '%Y-%m-%dT%H:%M:%S.%f')
            return {'year': date_object.year, 'month': date_object.month, 'day': date_object.day, 'hour': date_object.hour, 'minute': date_object.minute, 'weekday': date_object.weekday()}
        else:
            return {}
    def serialize(self):
        obj_dict = self.__dict__
        return obj_dict

    def headers(self):
        return list(self.serialize().keys())

    def values(self):
        return list(self.serialize().values())