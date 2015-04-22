#!/usr/bin/env python
# coding: utf-8

import json
import os
import unittest


class TestGeohex(unittest.TestCase):
    def setUp(self):
        self.tests = json.load(open(os.path.join(os.path.dirname(__file__), 'hex_v3.2_test_code2HEX.json'), 'r'))

    def test_consts(self):
        from geohex import geohex

        self.assertEqual(geohex.h_deg, 0.5235987755982988)
        self.assertAlmostEqual(geohex.h_k, 0.5773502691896257, 15)

    def test_calc_hex_size(self):
        from geohex import geohex

        cases = [
            247376.6461728395,
            82458.88205761317,
            27486.29401920439,
            9162.098006401464,
            3054.0326688004875,
            1018.0108896001626,
            339.3369632000542,
            113.11232106668473,
            37.70410702222824,
            12.56803567407608,
            4.189345224692027,
            1.3964484082306756,
            0.4654828027435586,
            0.15516093424785285,
            0.05172031141595095,
            0.017240103805316983,
            0.005746701268438995
        ]

        for idx, case in enumerate(cases):
            self.assertAlmostEqual(geohex.calc_hex_size(idx + 1), case, 15)

    def test_loc2xy(self):
        from geohex import geohex

        xy = geohex.loc2xy(139.745433, 35.65858)
        self.assertEqual(xy['x'], 15556390.440080063)
        self.assertEqual(xy['y'], 4253743.631945749)

    def test_xy2loc(self):
        from geohex import geohex

        loc = geohex.xy2loc(15556390.440080063, 4253743.631945749)
        self.assertEqual(loc['lon'], 139.745433)
        self.assertEqual(loc['lat'], 35.65858)

    def test_adjust_xy(self):
        from geohex import geohex

        self.assertEqual(geohex.adjust_xy(15556390.440080063, 4253743.631945749, 1), {'x': 15556363.440080062, 'y': 4253770.63194575, 'rev': 0})
        self.assertEqual(geohex.adjust_xy(15556390.440080063, 4253743.631945749, 17), {'x': 15556390.440080063, 'y': 4253743.631945749, 'rev': 0})

    def test_get_xy_by_location(self):
        from geohex import geohex

        xy = geohex.get_xy_by_location(35.65858, 139.745433, 11)
        self.assertEqual(xy['x'], 912000)
        self.assertEqual(xy['y'], -325774)

    def test_get_zone_by_xy(self):
        from geohex import geohex

        zone = geohex.get_zone_by_xy(912000, -325774, 11)

        self.assertEqual(zone.code, 'XM48854457273')
        self.assertAlmostEqual(zone.lat, 35.658618718910624, 11)
        self.assertAlmostEqual(zone.lon, 139.7454091799466, 11)
        self.assertEqual(zone.x, 912000)
        self.assertEqual(zone.y, -325774)

    def test_get_xy_by_code(self):
        from geohex import geohex

        xy = geohex.get_xy_by_code('XM48854457273')
        self.assertEqual(xy, {'x': 912000, 'y': -325774})

    def test_get_zone_by_location(self):
        from geohex import geohex

        zone = geohex.get_zone_by_location(35.65858, 139.745433, 11)
        self.assertIsInstance(zone, geohex.Zone)
        self.assertEqual(zone.get_hex_size(), 4.189345224692027)
        self.assertEqual(zone.get_level(), 11)

        for geohex_val, latitude, longitude in self.tests:
            zone = geohex.get_zone_by_location(latitude, longitude, len(geohex_val))
            self.assertTrue(zone.code.startswith(geohex_val))

    def test_get_zone_by_code(self):
        from geohex import geohex

        zone = geohex.get_zone_by_code('XM48854457273')
        self.assertEqual(zone.get_level(), 11)
        self.assertEqual(zone.get_hex_size(), 4.189345224692027)
        self.assertEqual(zone.x, 912000)
        self.assertEqual(zone.y, -325774)
        self.assertAlmostEqual(zone.lat, 35.658618718910624)
        self.assertAlmostEqual(zone.lon, 139.7454091799466)

        for geohex_val, latitude, longitude in self.tests:
            zone = geohex.get_zone_by_code(geohex_val)
            self.assertAlmostEqual(latitude, zone.lat)
            self.assertAlmostEqual(longitude, zone.lon)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestGeohex))
    return suite

