import math
from typing import Optional, List
import datetime
import gpxpy
import gpxpy.gpx
from gpxpy.gpx import GPX
from gpxpy.geo import Location
from geo import gauss_kruger_transform, mollweide
from gpx_approx import get_gpx_location_at


class Coordinate:

    def __init__(
        # в сантиметрах
        self,
        x: Optional[float] = 0,
        y: Optional[float] = 0,
        z: Optional[float] = 0,
    ) -> None:
        self.x = x
        self.y = y
        self.z = z


def transform_to_current_xyz(
    last_xyz: Coordinate,
    current_xyz: Coordinate,
    object_xyz: Coordinate,
):
    x = current_xyz.x - object_xyz.x if current_xyz.x < last_xyz.x else current_xyz.x + object_xyz.x
    z = current_xyz.z - object_xyz.z if current_xyz.z < last_xyz.z else current_xyz.z + object_xyz.z
    return Coordinate(x, current_xyz.y + object_xyz.y, z)


class Coordinates:

    def __init__(
        self,
        gpx_file_path,
        offset: Optional[Coordinate] = None
    ) -> None:
        self.last_time = None
        self.last_coord = None
        gpx_file = open(gpx_file_path, 'r')
        gpx: GPX = gpxpy.parse(gpx_file)

        if not gpx:
            raise Exception('Haven\'t gpx data')

        self.gpx: GPX = gpx
        self.offset = offset

    def __get_first_point(self) -> Coordinate:
        gpx_point = self.gpx.tracks[0].segments[0].points[0]
        current_point = gauss_kruger_transform(gpx_point.longitude, gpx_point.latitude)
        return Coordinate(
            current_point['x'],
            gpx_point.elevation,
            current_point['y']
        )

    def __offset(self, point: Coordinate):
        first_point = self.__get_first_point()
        if self.offset:
            print(point.x, first_point.x, self.offset.x)
            return Coordinate(
                x=point.x - (first_point.x - self.offset.x),
                y=point.y - (first_point.y - self.offset.y),
                z=point.z - (first_point.z - self.offset.z),
            )

        return point

    def __approx_coordinate(
        self,
        next_coord: Coordinate,
        current_time: datetime,
        next_time: datetime,
    ) -> Coordinate:
        if self.last_coord is None or self.last_time is None:
            return next_coord

        proportion = (current_time - self.last_time) / (next_time - self.last_time)

        return Coordinate(
            x=self.last_coord.x + (next_coord.x - self.last_coord.x) * proportion,
            y=self.last_coord.y + (next_coord.y - self.last_coord.y) * proportion,
            z=self.last_coord.z + (next_coord.z - self.last_coord.z) * proportion,
        )

    def get_time_coordinate(self, coordinate_time: datetime) -> Coordinate:
        locations: list[Location] = get_gpx_location_at(self.gpx, coordinate_time)  # 2383
        coordinates: list[Coordinate] = []

        location = locations[0]
        point = mollweide(location.longitude, location.latitude)
        coordinates.append(self.__offset(Coordinate(
            point[0],
            point[1],
            location.elevation * 100,
        )))

        self.last_coord = coordinates
        self.last_time = coordinate_time

        return coordinates[0]


coors = Coordinates(".\\testing_data\\GPS.gpx")

# This work CURRENT, YEEE

current_time_point = datetime.datetime(2022, 4, 23, 15, 59, tzinfo=datetime.timezone.utc)
coor = coors.get_time_coordinate(current_time_point)
print("start point:", current_time_point, coor.x, coor.z, coor.y)

random_time_point = datetime.datetime(2022, 4, 23, 16, 00, tzinfo=datetime.timezone.utc)
approx_coor = coors.get_time_coordinate(random_time_point)
print("time between points:", random_time_point, approx_coor.x, approx_coor.z, approx_coor.y)

second_time_point = datetime.datetime(2022, 4, 23, 16, 30, tzinfo=datetime.timezone.utc)
coor2 = coors.get_time_coordinate(second_time_point)
print("end point:", second_time_point, coor2.x, coor2.z, coor2.y)

print("distance between end and start:", math.sqrt(pow(coor2.x - coor.x, 2.0) + pow(coor2.z - coor2.z, 2.0)))