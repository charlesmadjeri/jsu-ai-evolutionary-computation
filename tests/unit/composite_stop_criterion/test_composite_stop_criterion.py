import unittest
from src.stop_criterions.composite_stop_criterion import AndStopCriterion, OrStopCriterion
from src.stop_criterions.stop_criterion import StopCriterion

class AlwaysTrueCriterion(StopCriterion):
    def check(self, value):
        return True
    def start(self):
        pass
    def end(self):
        pass
    def __str__(self):
        return "AlwaysTrueCriterion"

class AlwaysFalseCriterion(StopCriterion):
    def check(self, value):
        return False
    def start(self):
        pass
    def end(self):
        pass
    def __str__(self):
        return "AlwaysFalseCriterion"

class TestCompositeStopCriterion(unittest.TestCase):

    def test_and_all_true(self):
        criteria = AndStopCriterion([AlwaysTrueCriterion(), AlwaysTrueCriterion()])
        self.assertTrue(criteria.check_continue(0))

    def test_and_one_false(self):
        criteria = AndStopCriterion([AlwaysTrueCriterion(), AlwaysFalseCriterion()])
        self.assertFalse(criteria.check_continue(0))

    def test_or_all_false(self):
        criteria = OrStopCriterion([AlwaysFalseCriterion(), AlwaysFalseCriterion()])
        self.assertFalse(criteria.check_continue(0))

    def test_or_one_true(self):
        criteria = OrStopCriterion([AlwaysFalseCriterion(), AlwaysTrueCriterion()])
        self.assertTrue(criteria.check_continue(0))

    def test_string_output(self):
        and_criterion = AndStopCriterion([AlwaysTrueCriterion(), AlwaysFalseCriterion()])
        s = str(and_criterion)
        self.assertTrue(s.startswith("AND("))
        self.assertIn("AlwaysTrueCriterion", s)
        self.assertIn("AlwaysFalseCriterion", s)
        self.assertTrue(s.endswith(")"))

    def test_init_empty_criteria_raises(self):
        with self.assertRaises(ValueError):
            AndStopCriterion([])
        with self.assertRaises(ValueError):
            OrStopCriterion([])

    def test_check_equals_check_continue(self):
        c = AndStopCriterion([AlwaysTrueCriterion()])
        self.assertEqual(c.check(0), c.check_continue(0))

if __name__ == "__main__":
    unittest.main()
