from unittest import TestCase
import unittest
import melta


class meltaTest(TestCase):

    def test_number_of_actions(self):
        list=melta.get_sorted_actions()
        self.assertEqual(len(list),80)


    def test_sort_returns_oldest_p1(self):
        "The sort returns the oldest member of the highest priority class"
        nalist=melta.get_sorted_actions()
        self.assertEqual(nalist[0]['action'],"Oldestp1")

    def test_sort_regression_1(self):
        nalist=melta.get_sorted_actions()
        nalist_formated = [] #   [[melta.action_to_string(x) for x in nalist]]
        for x in nalist:
            nalist_formated.append(melta.action_to_string(x))
        naList_formated_string= "\n".join(nalist_formated)
        self.maxDiff = None
        self.assertMultiLineEqual(open('testinput/nextactions.md.sorted').read().strip(),naList_formated_string.strip())

    def test_completed_mark_on(self):
        nalist=melta.get_sorted_actions()
        self.assertEqual(nalist[0]['completed'],"x")

    def test_output_only_completed_tasks(self):
        nalist=melta.get_sorted_actions()
        parser = melta.setup_argument_list()
        args=parser.parse_args(['sort','-m'])
        nalist=melta.filter_actions(args)
        nalist_formated = [] #   [[melta.action_to_string(x) for x in nalist]]
        for x in nalist:
            nalist_formated.append(melta.action_to_string(x))
        naList_formated_string= "\n".join(nalist_formated)
        self.maxDiff = None
        self.assertMultiLineEqual(open('testinput/nextactions.md.sorted.completed').read().strip(),naList_formated_string.strip())

    def test_output_only_open_tasks(self):
        nalist=melta.get_sorted_actions()
        parser = melta.setup_argument_list()
        args=parser.parse_args(['sort','-o'])
        nalist=melta.filter_actions(args)
        nalist_formated = [] #   [[melta.action_to_string(x) for x in nalist]]
        for x in nalist:
            nalist_formated.append(melta.action_to_string(x))
        naList_formated_string= "\n".join(nalist_formated)
        self.maxDiff = None
        self.assertMultiLineEqual(open('testinput/nextactions.md.sorted.open').read().strip(),naList_formated_string.strip())

    def test_read_last_line_of_file(self):
	filename="testinput/pri.txt"

	pass


    def test_write_extra_line_of_file(self):
	pass




if __name__=="__main__":
    melta.NEXTACTIONS_LOC='testinput/nextactions.md'
    unittest.main()
