from unittest import TestCase
import unittest
import melta


class meltaTest(TestCase):

    def test_number_of_actions(self):
        list=melta.get_sorted_actions()
        self.assertEqual(len(list),80)






if __name__=="__main__":
    melta.NEXTACTIONS_LOC='testinput/nextactions.md'
    unittest.main()
