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
        
        self.assertAlmostEqual(result['coverage_per_hour'], 2.31, places=2)
        self.assertAlmostEqual(result['coverage_per_day'], 18.48, places=2)
        self.assertAlmostEqual(result['coverage_per_week'], 92.40, places=2)

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
        
        self.assertAlmostEqual(result['coverage_per_hour'], 5.71, places=2)
        self.assertAlmostEqual(result['coverage_per_day'], 45.68, places=2)
        self.assertAlmostEqual(result['coverage_per_week'], 228.40, places=2)

if __name__ == '__main__':
    unittest.main()