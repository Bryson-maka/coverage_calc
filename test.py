import unittest
from app import calculate_coverage

class TestCoverageCalculator(unittest.TestCase):
    def test_calculate_coverage_metric(self):
        result = calculate_coverage(
            machine_width=10,
            machine_speed=5,
            field_length=1000,
            turn_around_time=2,
            operational_hours_per_day=8,
            operational_days_per_week=5,
            is_metric=True
        )
        
        self.assertAlmostEqual(result['coverage_per_hour'], 4.29, places=2)
        self.assertAlmostEqual(result['coverage_per_day'], 34.29, places=2)
        self.assertAlmostEqual(result['coverage_per_week'], 171.43, places=2)

    def test_calculate_coverage_imperial(self):
        result = calculate_coverage(
            machine_width=32.8084,  # 10 meters in feet
            machine_speed=3.10686,  # 5 km/h in mph
            field_length=3280.84,   # 1000 meters in feet
            turn_around_time=2,
            operational_hours_per_day=8,
            operational_days_per_week=5,
            is_metric=False
        )
        
        self.assertAlmostEqual(result['coverage_per_hour'], 10.59, places=2)
        self.assertAlmostEqual(result['coverage_per_day'], 84.72, places=2)
        self.assertAlmostEqual(result['coverage_per_week'], 423.61, places=2)

    def test_calculate_coverage_with_transportation(self):
        result = calculate_coverage(
            machine_width=10,
            machine_speed=5,
            field_length=1000,
            turn_around_time=2,
            operational_hours_per_day=8,
            operational_days_per_week=5,
            is_metric=True,
            transportation_trips_per_day=2,
            transportation_time_per_trip=30  # 30 minutes per trip
        )
        
        # Transportation should reduce effective hours from 8 to 7 (1 hour transportation)
        self.assertAlmostEqual(result['effective_hours_per_day'], 7.0, places=2)
        self.assertAlmostEqual(result['transportation_time_per_day'], 1.0, places=2)
        self.assertAlmostEqual(result['transportation_time_per_week'], 5.0, places=2)
        
        # Coverage should be reduced proportionally
        self.assertAlmostEqual(result['coverage_per_day'], 30.0, places=1)

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            calculate_coverage(
                machine_width=0,  # Invalid: should be > 0
                machine_speed=5,
                field_length=1000,
                turn_around_time=2,
                operational_hours_per_day=8,
                operational_days_per_week=5,
                is_metric=True
            )
        
        with self.assertRaises(ValueError):
            calculate_coverage(
                machine_width=10,
                machine_speed=-1,  # Invalid: should be > 0
                field_length=1000,
                turn_around_time=2,
                operational_hours_per_day=8,
                operational_days_per_week=5,
                is_metric=True
            )

    def test_transportation_edge_cases(self):
        # Test with no transportation
        result = calculate_coverage(
            machine_width=10,
            machine_speed=5,
            field_length=1000,
            turn_around_time=2,
            operational_hours_per_day=8,
            operational_days_per_week=5,
            is_metric=True,
            transportation_trips_per_day=0,
            transportation_time_per_trip=0
        )
        
        self.assertEqual(result['transportation_time_per_day'], 0.0)
        self.assertEqual(result['effective_hours_per_day'], 8.0)
        self.assertEqual(result['coverage_lost_per_day'], 0.0)
        
        # Test transportation time exceeding operational hours
        result = calculate_coverage(
            machine_width=10,
            machine_speed=5,
            field_length=1000,
            turn_around_time=2,
            operational_hours_per_day=8,
            operational_days_per_week=5,
            is_metric=True,
            transportation_trips_per_day=10,
            transportation_time_per_trip=60  # 10 hours of transportation
        )
        
        self.assertEqual(result['effective_hours_per_day'], 0.0)
        self.assertEqual(result['coverage_per_day'], 0.0)
        self.assertGreater(result['coverage_lost_per_day'], 0.0)

if __name__ == '__main__':
    unittest.main()