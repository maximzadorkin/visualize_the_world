from typing import List
from datetime import datetime
from gpxpy.geo import Location
from gpxpy.gpx import GPX, GPXTrackSegment


def get_segment_gpx_location_at(segment: GPXTrackSegment, current_time: datetime):
    if not segment.points:
        return None

    if not current_time:
        return None

    first_time = segment.points[0].time
    last_time = segment.points[-1].time

    if not first_time and not last_time:
        return None

    if first_time and current_time and last_time and not first_time <= current_time <= last_time:
        return None

    for index, point in enumerate(segment.points):
        if point.time and current_time <= point.time:
            last_point = segment.points[index - 1] or point
            proportion = (point.time - current_time) / (point.time - last_point.time)
            longitude = (point.longitude - last_point.longitude) * proportion + last_point.longitude
            latitude = (point.latitude - last_point.latitude) * proportion + last_point.latitude
            elevation = (point.elevation - last_point.elevation) * proportion + last_point.elevation
            return Location(
                longitude=longitude,
                latitude=latitude,
                elevation=elevation,
            )

    return None


def get_track_gpx_location_at(track, current_time: datetime):
    result = []
    for track_segment in track.segments:
        location = get_segment_gpx_location_at(track_segment, current_time)
        if location:
            result.append(location)

    return result


def get_gpx_location_at(gpx: GPX, current_time: datetime):
    result: List[Location] = []
    for track in gpx.tracks:
        locations = get_track_gpx_location_at(track, current_time)
        for location in locations:
            result.append(location)

    return result
