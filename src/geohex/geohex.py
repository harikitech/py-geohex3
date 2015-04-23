# coding=utf-8
import math


h_key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
h_base = 20037508.34
h_deg = math.pi * (30.0 / 180.0)
h_k = math.tan(h_deg)

_zone_cache = {}

__all__ = [
    'get_zone_by_location',
    'get_xy_by_location',
    'get_zone_by_code',
    'get_zone_by_xy',
    'loc2xy',
    'xy2loc',
    'adjust_xy',
]


def int2str(digit, base):
    """

    :param digit:
    :type digit: int
    :param base:
    :type base: int
    :return:
    """
    int2str_table = '0123456789abcdefghijklmnopqrstuvwxyz'

    if not 2 <= base <= 36:
        raise ValueError('base must be 2 <= base < 36')

    result = []

    temp = abs(digit)
    if temp == 0:
        result.append('0')
    else:
        while temp > 0:
            result.append(int2str_table[temp % base])
            temp /= base

    if digit < 0:
        result.append('-')

    return ''.join(reversed(result))


def calc_hex_size(level):
    """

    :param level:
    :type level: int
    :return:
    :rtype: float
    """
    return h_base / math.pow(3, level + 3)


def loc2xy(lon, lat):
    """

    :param lon: longitude of location
    :type lon: float
    :param lat: latitude of location
    :type lat: float
    :return:
    :rtype: dict
    """
    x = lon * h_base / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
    y *= h_base / 180
    return {'x': x, 'y': y}


def xy2loc(x, y):
    """

    :param x:
    :type x: float
    :param y:
    :type y: float
    :return:
    :rtype: dict
    """
    lon = (x / h_base) * 180
    lat = (y / h_base) * 180
    lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180)) - math.pi / 2)
    return {'lon': lon, 'lat': lat}


def adjust_xy(x, y, level):
    """

    :param x:
    :type x: float
    :param y:
    :type y: float
    :param level:
    :type level: int
    :return:
    :rtype: dict
    """
    rev = 0
    max_h_steps = math.pow(3, level + 2)
    h_steps = abs(x - y)
    if h_steps == max_h_steps and x > y:
        tmp = x
        x = y
        y = tmp
        rev = 1
    elif h_steps > max_h_steps:
        dif = h_steps - max_h_steps
        dif_x = math.floor(dif / 2)
        dif_y = dif - dif_x
        if x > y:
            edge_x = x - dif_x
            edge_y = y + dif_y
            h_xy = edge_x
            edge_x = edge_y
            edge_y = h_xy
            x = edge_x + dif_x
            y = edge_y - dif_y
        elif y > x:
            edge_x = x + dif_x
            edge_y = y - dif_y
            h_xy = edge_x
            edge_x = edge_y
            edge_y = h_xy
            x = edge_x - dif_x
            y = edge_y + dif_y
    return {'x': x, 'y': y, 'rev': rev}


class Zone(object):
    def __init__(self, lat, lon, x, y, code):
        self.lat = lat
        self.lon = lon
        self.x = x
        self.y = y
        self.code = code

    def get_level(self):
        """
        :rtype: int
        """
        return len(self.code) - 2

    def get_hex_size(self):
        """
        :rtype: float
        """
        return calc_hex_size(self.get_level())

    def get_hex_coors(self):
        """
        :rtype: dict
        """
        h_lat = self.lat
        h_lon = self.lon
        h_xy = loc2xy(h_lon, h_lat)
        h_x = h_xy['x']
        h_y = h_xy['y']
        h_deg = math.tan(math.pi * (60 / 180))
        h_size = self.get_hex_size()
        h_top = xy2loc(h_x, h_y + h_deg * h_size)['lat']
        h_btm = xy2loc(h_x, h_y - h_deg * h_size)['lat']

        h_l = xy2loc(h_x - 2 * h_size, h_y)['lon']
        h_r = xy2loc(h_x + 2 * h_size, h_y)['lon']
        h_cl = xy2loc(h_x - 1 * h_size, h_y)['lon']
        h_cr = xy2loc(h_x + 1 * h_size, h_y)['lon']

        return [
            {'lat': h_lat, 'lon': h_l},
            {'lat': h_top, 'lon': h_cl},
            {'lat': h_top, 'lon': h_cr},
            {'lat': h_lat, 'lon': h_r},
            {'lat': h_btm, 'lon': h_cr},
            {'lat': h_btm, 'lon': h_cl}
        ]


def get_zone_by_location(lat, lon, level):
    """Returns GEOHEX Zone by location.

    :param lat: latitude of location
    :type lat: float
    :param lon: longitude of location
    :type lon: float
    :param level: geohex level
    :type level: int
    :return:
    :rtype: Zone
    """
    xy = get_xy_by_location(lat, lon, level)
    zone = get_zone_by_xy(xy['x'], xy['y'], level)
    return zone


def get_zone_by_code(code):
    """Returns GEOHEX Zone by GEOHEX Code.

    :param code:
    :type code: str
    :return:
    :rtype: Zone
    """
    xy = get_xy_by_code(code)
    level = len(code) - 2
    zone = get_zone_by_xy(xy['x'], xy['y'], level)
    return zone


def get_xy_by_location(lat, lon, level):
    """

    :param lat: latitude of location
    :type lat: float
    :param lon: longitude of location
    :type lon: float
    :param level: geohex level
    :type level: int
    :return:
    :rtype: dict
    """
    h_size = calc_hex_size(level)
    z_xy = loc2xy(lon, lat)
    lon_grid = z_xy['x']
    lat_grid = z_xy['y']
    unit_x = 6 * h_size
    unit_y = 6 * h_size * h_k
    h_pos_x = (lon_grid + lat_grid / h_k) / unit_x
    h_pos_y = (lat_grid - h_k * lon_grid) / unit_y
    h_x_0 = math.floor(h_pos_x)
    h_y_0 = math.floor(h_pos_y)
    h_x_q = h_pos_x - h_x_0
    h_y_q = h_pos_y - h_y_0
    h_x = round(h_pos_x)
    h_y = round(h_pos_y)

    if h_y_q > -h_x_q + 1:
        if (h_y_q < 2 * h_x_q) and (h_y_q > 0.5 * h_x_q):
            h_x = h_x_0 + 1
            h_y = h_y_0 + 1
    elif h_y_q < -h_x_q + 1:
        if (h_y_q > (2 * h_x_q) - 1) and (h_y_q < (0.5 * h_x_q) + 0.5):
            h_x = h_x_0
            h_y = h_y_0

    inner_xy = adjust_xy(h_x, h_y, level)
    h_x = inner_xy['x']
    h_y = inner_xy['y']
    return {'x': h_x, 'y': h_y}


def get_xy_by_code(code):
    """

    :param code:
    :type code: str
    :return:
    """
    level = len(code) - 2
    h_size = calc_hex_size(level)
    unit_x = 6 * h_size
    unit_y = 6 * h_size * h_k
    h_x = 0
    h_y = 0

    h_dec9 = '' + str(h_key.find(code[0]) * 30 + h_key.find(code[1])) + code[2:]

    if h_dec9[0] in [1, 5] and h_dec9[1] in [1, 2, 5] and h_dec9[2] in [1, 2, 5]:
        if int(h_dec9[0]) == 5:
            h_dec9 = "7" + h_dec9[1:len(h_dec9)]
        elif int(h_dec9[0]) == 1:
            h_dec9 = "3" + h_dec9[1:len(h_dec9)]

    d9xlen = len(h_dec9)
    for i in range(level + 3 - d9xlen):
        h_dec9 = "0" + h_dec9
        d9xlen += 1

    h_dec3 = ""
    for i in range(d9xlen):
        h_dec0 = int2str(int(h_dec9[i]), 3)
        if not h_dec0:
            h_dec3 += "00"
        elif len(h_dec0) == 1:
            h_dec3 += "0"

        h_dec3 += h_dec0

    h_decx = []
    h_decy = []

    for i in range(len(h_dec3) / 2):
        h_decx.append(h_dec3[i * 2])
        h_decy.append(h_dec3[i * 2 + 1])

    for i in range(level + 3):
        h_pow = math.pow(3, level + 2 - i)

        if int(h_decx[i]) == 0:
            h_x -= h_pow
        elif int(h_decx[i]) == 2:
            h_x += h_pow

        if int(h_decy[i]) == 0:
            h_y -= h_pow
        elif int(h_decy[i]) == 2:
            h_y += h_pow

    inner_xy = adjust_xy(h_x, h_y, level)
    h_x = inner_xy['x']
    h_y = inner_xy['y']

    return {"x": h_x, "y": h_y}


def get_zone_by_xy(x, y, level):
    """

    :param x:
    :type x: float
    :param y:
    :type y: float
    :param level:
    :type level: int
    :return:
    :rtype: Zone
    """
    h_size = calc_hex_size(level)

    h_x = x
    h_y = y

    unit_x = 6 * h_size
    unit_y = 6 * h_size * h_k

    h_lat = (h_k * h_x * unit_x + h_y * unit_y) / 2
    h_lon = (h_lat - h_y * unit_y) / h_k

    z_loc = xy2loc(h_lon, h_lat)
    z_loc_x = z_loc['lon']
    z_loc_y = z_loc['lat']

    max_h_steps = math.pow(3, level + 2)
    h_steps = abs(h_x - h_y)

    if h_steps == max_h_steps:
        if h_x > h_y:
            tmp = h_x
            h_x = h_y
            h_y = tmp
        z_loc_x = -180

    h_code = ''
    code3_x = []
    code3_y = []
    code3 = ''
    code9 = ''
    mod_x = h_x
    mod_y = h_y

    for i in range(level + 3):
        h_pow = math.pow(3, level + 2 - i)

        if mod_x >= math.ceil(h_pow / 2):
            code3_x.append(2)
            mod_x -= h_pow
        elif mod_x <= -math.ceil(h_pow / 2):
            code3_x.append(0)
            mod_x += h_pow
        else:
            code3_x.append(1)

        if mod_y >= math.ceil(h_pow / 2):
            code3_y.append(2)
            mod_y -= h_pow
        elif mod_y <= -math.ceil(h_pow / 2):
            code3_y.append(0)
            mod_y += h_pow
        else:
            code3_y.append(1)

        if i == 2 and (z_loc_x == -180 or z_loc_x >= 0):
            if code3_x[0] == 2 and code3_y[0] == 1 and code3_x[1] == code3_y[1] and code3_x[2] == code3_y[2]:
                code3_x[0] = 1
                code3_y[0] = 2
            elif code3_x[0] == 1 and code3_y[0] == 0 and code3_x[1] == code3_y[1] and code3_x[2] == code3_y[2]:
                code3_x[0] = 0
                code3_y[0] = 1

    for i in range(len(code3_x)):
        code3 += ("" + str(code3_x[i]) + str(code3_y[i]))
        code9 += str(int(code3, 3))
        h_code += code9
        code9 = ""
        code3 = ""

    h_2 = h_code[3:]
    h_1 = h_code[:3]
    h_a1 = int(math.floor(int(h_1) / 30))
    h_a2 = int(h_1) % 30
    h_code = h_key[h_a1] + h_key[h_a2] + h_2

    return Zone(z_loc_y, z_loc_x, x, y, h_code)
