# https://ru.wikibooks.org/wiki/Реализации_алгоритмов/Перевод_географических_координат_в_прямоугольные_в_прямоугольные_координаты_проекции_Гаусса-Крюгера


# Географические координаты точки (в градусах)
import numpy as np
from pyproj import Proj


def gauss_kruger_transform(dLon, dLat):
    # Перевод географических координат (широты и долготы) точки в прямоугольные
    # координаты проекции Гаусса-Крюгера (на примере координат Москвы).

    # Номер зоны Гаусса-Крюгера (если точка рассматривается в системе
    # координат соседней зоны, то номер зоны следует присвоить вручную)
    zone = int(dLon / 6.0 + 1)

    # Импорт математических функций
    from math import sin, cos, tan, pi

    # Параметры эллипсоида Красовского
    a = 6378245.0  # Большая (экваториальная) полуось
    b = 6356863.019  # Малая (полярная) полуось
    e2 = (a ** 2 - b ** 2) / a ** 2  # Эксцентриситет
    n = (a - b) / (a + b)  # Приплюснутость

    # Параметры зоны Гаусса-Крюгера
    F = 1.0  # Масштабный коэффициент
    Lat0 = 0.0  # Начальная параллель (в радианах)
    Lon0 = (zone * 6 - 3) * pi / 180  # Центральный меридиан (в радианах)
    N0 = 0.0  # Условное северное смещение для начальной параллели
    E0 = zone * 1e6 + 500000.0  # Условное восточное смещение для центрального меридиана

    # Перевод широты и долготы в радианы
    Lat = dLat * pi / 180.0
    Lon = dLon * pi / 180.0

    # Вычисление переменных для преобразования
    v = a * F * (1 - e2 * (sin(Lat) ** 2)) ** -0.5
    p = a * F * (1 - e2) * (1 - e2 * (sin(Lat) ** 2)) ** -1.5
    n2 = v / p - 1
    M1 = (1 + n + 5.0 / 4.0 * n ** 2 + 5.0 / 4.0 * n ** 3) * (Lat - Lat0)
    M2 = (3 * n + 3 * n ** 2 + 21.0 / 8.0 * n ** 3) * sin(Lat - Lat0) * cos(Lat + Lat0)
    M3 = (15.0 / 8.0 * n ** 2 + 15.0 / 8.0 * n ** 3) * sin(2 * (Lat - Lat0)) * cos(2 * (Lat + Lat0))
    M4 = 35.0 / 24.0 * n ** 3 * sin(3 * (Lat - Lat0)) * cos(3 * (Lat + Lat0))
    M = b * F * (M1 - M2 + M3 - M4)
    I = M + N0
    II = v / 2 * sin(Lat) * cos(Lat)
    III = v / 24 * sin(Lat) * (cos(Lat)) ** 3 * (5 - (tan(Lat) ** 2) + 9 * n2)
    IIIA = v / 720 * sin(Lat) * (cos(Lat) ** 5) * (61 - 58 * (tan(Lat) ** 2) + (tan(Lat) ** 4))
    IV = v * cos(Lat)
    V = v / 6 * (cos(Lat) ** 3) * (v / p - (tan(Lat) ** 2))
    VI = v / 120 * (cos(Lat) ** 5) * (5 - 18 * (tan(Lat) ** 2) + (tan(Lat) ** 4) + 14 * n2 - 58 * (tan(Lat) ** 2) * n2)

    # Вычисление северного и восточного смещения (в метрах)
    N = I + II * (Lon - Lon0) ** 2 + III * (Lon - Lon0) ** 4 + IIIA * (Lon - Lon0) ** 6
    E = E0 + IV * (Lon - Lon0) + V * (Lon - Lon0) ** 3 + VI * (Lon - Lon0) ** 5

    to_sm = 100

    return {'x': E * to_sm, 'y': N * to_sm}


from math import sin, cos, pi, sqrt, asin, log

sqrt2 = sqrt(2)


def solveNR(lat, epsilon=1e-6):
    """Solve the equation $2\theta\sin(2\theta)=\pi\sin(\mathrm{lat})$
 using Newtons method"""
    if abs(lat) == pi / 2:
        return lat  # avoid division by zero
    theta = lat
    while True:
        nexttheta = theta - (
                (2 * theta + sin(2 * theta) - pi * sin(lat)) /
                (2 + 2 * cos(2 * theta))
        )
        if abs(theta - nexttheta) < epsilon:
            break
        theta = nexttheta
    return nexttheta


def checktheta(theta, lat):
    return 2 * theta + sin(2 * theta), pi * sin(lat)


def mollweide(lat, lon, lon_0=0, R=1):
    # if degrees:
    #     lat = lat * pi / 180
    #     lon = lon * pi / 180
    #     lon_0 = lon_0 * p / 180  # convert to radians
    theta = solveNR(lat)
    return (R * 2 * sqrt2 * (lon - lon_0) * cos(theta) / pi,
            R * sqrt2 * sin(theta))


# point1 = mollweide(55.755994, 37.714076)#55.756097, 37.714105)
# point2 = mollweide(55.755995, 37.714659)#55.756412, 37.714501)
# print(point2['x'] - point1['x'], point2['y'] - point1['y'])
# print(point2[0] - point1[0], point2[1] - point1[1])

# p1 = np.array(Proj(ellps='WGS84')(55.756003, 37.714076))
# p2 = np.array(Proj(ellps='WGS84')(55.756004, 37.714676))

# x2, y2 = pyproj.transform(p1, p2, x1, y1, radians=True)

# print(p2[0] - p1[0], p2[1] - p1[1])
# print(np.linalg.norm(p2 - p1))


from pyproj import Transformer

transformer = Transformer.from_crs("epsg:4326", "epsg:32650")
p1 = np.array(transformer.transform(55.756052, 37.714084)) * 100
p2 = np.array(transformer.transform(53.652519, 47.094888)) * 100

print("Расстояние(в сантиметрах): ", int(np.linalg.norm(p2 - p1)))
