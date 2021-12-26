from django.test import TestCase
from .services import AlphabeticalGrouper, get_employees_by_last_name_group
from .models import Department, Employee


class DepartmentModelTests(TestCase):
    def test_str_return_name(self):
        dpt_name = 'TeSt DePArtMEnt nAmE'
        dpt = Department(name=dpt_name)
        self.assertIs(str(dpt), dpt_name)


class GetAlphabeticalGroupsServicesWithoutFixturesTests(TestCase):
    def test_get_groups_with_empty_db(self):
        self.assertEqual(AlphabeticalGrouper().get_alphabetical_groups(), [])
    
    
class GetAlphabeticalGroupsServicesWithOneRowFixtureTests(TestCase):
    fixtures = ['dump_one_row.json']
        
    def test_get_groups_with_one_row_to_split(self):
        self.assertEqual(AlphabeticalGrouper().get_alphabetical_groups(), ['H'])


class GetAlphabeticalGroupsServicesWithThreeRowFixtureTests(TestCase):
    fixtures = ['dump_three_row.json']
        
    def test_get_groups_with_min_amount_of_rows_to_split(self):
        self.assertEqual(AlphabeticalGrouper().get_alphabetical_groups(), [['H'], ['Б'], ['Х']])
        

class GetAlphabeticalGroupsServicesWithOneLetterFixtureTests(TestCase):
    fixtures = ['dump_one_letter.json']
        
    def test_get_groups_with_three_rows_in_one_letter_to_split(self):
        self.assertEqual(AlphabeticalGrouper().get_alphabetical_groups(), ['S'])


class GetAlphabeticalGroupsServicesWithFortyThreeLetterFixtureTests(TestCase):
    fixtures = ['dump_fortythree_rows.json']
        
    def test_get_groups_with_three_one_groups_and_one_forty_rows_to_split(self):
        self.assertEqual(AlphabeticalGrouper().get_alphabetical_groups(), [['H'], ['S'], ['Б', 'Х']])


class GetAlphabeticalGroupsServicesTests(TestCase):
    fixtures = ['dumpdata.json']

    def test_get_groups_is_works(self):
        self.assertEqual(AlphabeticalGrouper().get_alphabetical_groups(), 
                         [['A', 'B', 'C'], 
                          ['D', 'E', 'F'], 
                          ['G', 'H', 'I', 'J', 'L'], 
                          ['M', 'N', 'P'], 
                          ['R', 'S', 'T', 'V', 'W', 'Y', 'Б', 'Х']])
