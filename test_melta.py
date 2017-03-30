from unittest import TestCase
import unittest
import melta


class meltaTest(TestCase):

    def test_number_of_actions(self):
        list=melta.get_sorted_actions()
        self.assertEqual(len(list),80)


    def test_sort_returns_oldest_p1(self):
        "The sort returns the oldest member of the highest priority class"
        list=melta.get_sorted_actions()
        self.assertEqual(list[0]['action'],"Oldestp1")



if __name__=="__main__":
    melta.NEXTACTIONS_LOC='testinput/nextactions.md'
    unittest.main()
