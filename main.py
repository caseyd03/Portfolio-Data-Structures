from typing import *
from dataclasses import dataclass
import unittest
import math

calpoly_email_addresses = ["chartl03@calpoly.edu"]

"""
    Signature: area(self) -> float

    Header: result = GlobeRect(30, 31, 24, 25).area()
            self.assertEqual(result, 12309) -> True

            result = GlobeRect(26, 27.4, -101, 101.5).area()
            self.assertEqual(result, 100) -> False

            result = GlobeRect("hello", 4, 0.2, 1).area() -> "Error"

    Purpose: calculate an area in km given two latitude points and two longitude points

"""


@dataclass(frozen=True)
class GlobeRect:
    llat: float
    ulat: float
    wlong: float
    elong: float

    def area(self):
        lat_diff = self.ulat - self.llat
        height_km = lat_diff * 110.574
        long_diff = self.elong - self.wlong
        length_km = long_diff * (111.320 * math.cos(lat_diff))
        area = height_km * length_km
        return area


@dataclass(frozen=True)
class Region:
    globerect: GlobeRect
    name: str
    terrain: str


def region_desc(self):
    print(self.name and self.terrain)


@dataclass(frozen=True)
class RegionCondition:
    region: Region
    year: int
    population: int
    c02emissions: int


def region_cond(self):
    print(self.region and self.year and self.pop and self.emissions)


def emissions_per_capita(self):
    per_cap = self.emissions / self.pop
    return per_cap


def emissions_per_square_km(self):
    emissions = self.emissions / self.region.globerect.area()
    return emissions


example_region_conditions = [
    RegionCondition(Region(GlobeRect(55.4, 55.8, 36.3, 36.8), "Moscow", "other"), 2022, 12700000, 230000000),
    RegionCondition(Region(GlobeRect(41.4, 41.6, 272.7, 273), "Chicago", "other"), 2020, 2740000, 39300000),
    RegionCondition(Region(GlobeRect(-5.6, -5, 106.6, 107.1), "Jakarta", "ocean"), 2020, 10700000, 22800000),
    RegionCondition(Region(GlobeRect(34.4, 35.5, 239.3, 239.6), "Cal Poly", "mountain"), 2017, 20907, 47114)
]

"""
    Signature: densest(region_conditions) -> string

    Header: result = densest([RegionCondition(Region(GlobeRect(55.4, 55.8, 36.3, 36.8), "Moscow", "other"), 2022, 12700000, 230000000),
    RegionCondition(Region(GlobeRect(41.4, 41.6, 272.7, 273), "Chicago", "other"), 2020, 2740000, 39300000)])
            self.assertEqual(result, Moscow) -> True

            result = densest([RegionCondition(Region(GlobeRect(-5.6, -5, 106.6, 107.1), "Jakarta", "ocean"), 2020, 10700000, 22800000),
    RegionCondition(Region(GlobeRect(34.4, 35.5, 239.3, 239.6), "Cal Poly", "mountain"), 2017, 20907, 47114)])
            self.assertEqual(result, Cal Poly) -> False

            result = densest(0, 20, "mini") -> "Error"

    Purpose: Find the densest region of a list of RegionCondition objects

"""

"""
Line    i    density    densest_value    densest_region    return
60      -	    -	          -	               -	         -
61	    0	   None						
63	    0				
64		      5600								
66			                 5600		
67				                              Moscow	
63	    1				
64		      3785																	
63	    2				
64		      3510																		
63	    3				
64		       11																		
68					                                        Moscow


"""


def densest(region_conditions):
    densest_value = 0
    densest_region = "string"
    for i in region_conditions:
        density = i.pop / i.region.globerect.area()
        if density > densest_value:
            densest_value = density
            densest_region = i.region.name
    return densest_region


"""
    Signature: project_condition(region_condition, years) -> RegionCondition

    Header: result = project_condition(RegionCondition(Region(GlobeRect(-5.6, -5, 106.6, 107.1), "Jakarta", "ocean"), 2020, 10700000, 22800000), 3)
            self.assertEqual(result, RegionCondition(Region(GlobeRect(-5.6, -5, 106.6, 107.1), "Jakarta", "ocean"), 2020, 10704280, 22800000)) -> True

            result = project_condition(RegionCondition(Region(GlobeRect(-5.6, -5, 106.6, 107.1), "Jakarta", "ocean"), 2020, 10700000, 22800000), 6)
            self.assertEqual(result, RegionCondition(Region(GlobeRect(-5.6, -5, 106.6, 107.1), "Jakarta", "ocean"), 2020, 11720000, 22800000)) -> False

            result = project_condition(Region(GlobeRect(-5.6, -5, 106.6, 107.1), "Jakarta", "ocean"), 2020, 10700000, 22800000), -5) -> "Error"

    Purpose: Calculate the projected population of a region over an inputted number of years

"""


def project_condition(region_condition, years):
    final_pop = 0
    if region_condition.region.terrain == "ocean":
        f_pop = region_condition.pop
        for i in range(years):
            f_pop = f_pop * 1.0001
        final_pop = f_pop
    elif region_condition.region.terrain == "mountain":
        f_pop = region_condition.pop
        for i in range(years):
            f_pop = f_pop * 1.0005
        final_pop = f_pop
    elif region_condition.region.terrain == "forest":
        f_pop = region_condition.pop
        for i in range(years):
            f_pop = f_pop * 0.99999
        final_pop = f_pop
    elif region_condition.region.terrain == "other":
        f_pop = region_condition.pop
        for i in range(years):
            f_pop = f_pop * 1.00003
        final_pop = f_pop

    future_region = RegionCondition(
        region_condition.region, region_condition.year, final_pop, region_condition.emissions)

    return future_region


# put all test cases in the "Tests" class.
class Tests(unittest.TestCase):
    def test_area_1(self):
        result = GlobeRect(30, 31, 24, 25).area()
        self.assertEqual(result, 12309)

    def test_area_2(self):
        result = GlobeRect(26, 27.4, -101, 101.5).area()
        self.assertEqual(result, 100)

    def test_area_3(self):
        result = GlobeRect("hello", 4, 0.2, 1).area()
        self.assertEqual(result, "Error")

    def test_densest_1(self):
        result = densest(
            [RegionCondition(Region(GlobeRect(55.4, 55.8, 36.3, 36.8), "Moscow", "other"), 2022, 12700000, 230000000),
             RegionCondition(Region(GlobeRect(41.4, 41.6, 272.7, 273), "Chicago", "other"), 2020, 2740000, 39300000)])
        self.assertEqual(result, "Moscow")

    def test_densest_2(self):
        result = densest(
            [RegionCondition(Region(GlobeRect(-5.6, -5, 106.6, 107.1), "Jakarta", "ocean"), 2020, 10700000, 22800000),
             RegionCondition(Region(GlobeRect(34.4, 35.5, 239.3, 239.6), "Cal Poly", "mountain"), 2017, 20907, 47114)])
        self.assertEqual(result, "Cal Poly")

    def test_densest_3(self):
        result = densest(0, 20, "mini")
        self.assertEqual(result, "Error")

    def test_project_1(self):
        result = project_condition(
            RegionCondition(Region(GlobeRect(-5.6, -5, 106.6, 107.1), "Jakarta", "ocean"), 2020, 10700000, 22800000), 3)
        self.assertEqual(result,
                         RegionCondition(Region(GlobeRect(-5.6, -5, 106.6, 107.1), "Jakarta", "ocean"), 2020, 10704280,
                                         22800000))

    def test_project_2(self):
        result = project_condition(
            RegionCondition(Region(GlobeRect(-5.6, -5, 106.6, 107.1), "Jakarta", "ocean"), 2020, 10700000, 22800000), 6)
        self.assertEqual(result,
                         RegionCondition(Region(GlobeRect(-5.6, -5, 106.6, 107.1), "Jakarta", "ocean"), 2020, 11720000,
                                         22800000))

    def test_project_3(self):
        result = project_condition(Region(GlobeRect(-5.6, -5, 106.6, 107.1), "Jakarta", "ocean"), -5)
        self.assertEqual(result, "Error")


if (__name__ == '__main__'):
    unittest.main()