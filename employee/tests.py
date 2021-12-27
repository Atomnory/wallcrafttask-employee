from django.test import TestCase
from django.urls import reverse
from .models import Department, Employee
from .services import AlphabeticalGrouper, AlphabetBestGroupCalculator, get_employees_by_last_name_group
from .filters import EmployeeFilter


def create_department() -> Department:
    return Department.objects.create(name='D')


def create_second_department() -> Department:
    return Department.objects.create(name='Administration')


def create_employee() -> Employee:
    d = create_department()
    return Employee.objects.create(first_name='Greg',
                                   last_name='Berg',
                                   patronymic_name='Erikson',
                                   birth_date='1900-01-01',
                                   email='e@e.com',
                                   phone_number='709',
                                   job_start_date='1900-01-01',
                                   job_end_date='1900-01-01',
                                   job_title='Jjjj Tttt',
                                   department=d)

def create_second_employee() -> Employee:
    d = create_second_department()
    return Employee.objects.create(first_name='Lewis',
                                   last_name='Hamilton',
                                   patronymic_name='Antony',
                                   birth_date='1988-03-21',
                                   email='lh44@mercedes.eu',
                                   phone_number='+1999',
                                   job_start_date='2004-03-28',
                                   job_end_date='2021-12-15',
                                   job_title='Driver',
                                   department=d)


class DepartmentModelTests(TestCase):
    def test_str_return_name(self):
        dpt = create_department()
        self.assertIs(str(dpt), dpt.name)


class EmployeeModelTests(TestCase):
    def test_str_return_name(self):
        e = create_employee()
        self.assertTrue(str(e) == f'{e.first_name} {e.last_name}')

    def test_get_absolute_url(self):
        e = create_employee()
        self.assertTrue(e.get_absolute_url() == f'/{e.pk}')

    def test_get_full_name(self):
        e = create_employee()
        self.assertTrue(e.get_full_name() == f'{e.last_name} {e.first_name} {e.patronymic_name}')


class EmployeeFilterListViewTests(TestCase):
    def test_no_employee(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Нет ни одного сотрудника.')
        self.assertQuerysetEqual(response.context['page_obj'], [])
        self.assertIsInstance(response.context['filter'], EmployeeFilter)

    def test_one_employee(self):
        e = create_employee()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Berg')
        self.assertQuerysetEqual(response.context['page_obj'], [e])
        self.assertIsInstance(response.context['filter'], EmployeeFilter)

    def test_two_employees(self):
        e1 = create_employee()
        e2 = create_second_employee()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Berg')
        self.assertContains(response, 'Hamilton')
        self.assertQuerysetEqual(response.context['page_obj'], [e1, e2])
        self.assertIsInstance(response.context['filter'], EmployeeFilter)


class EmployeeDetailViewTests(TestCase):
    def test_wrong(self):
        response = self.client.get(reverse('employee', args=(1,)))
        self.assertEqual(response.status_code, 404)

    def test_employee(self):
        e = create_employee()
        response = self.client.get(reverse('employee',args=(e.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Berg')
        self.assertEqual(response.context['object'], e)


class AlphabeticalEmployeeListViewEmptyTests(TestCase):
    def test_get_groups_with_empty_db(self):
        response = self.client.get(reverse('alphabetical'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['groups'], [])


class AlphabeticalEmployeeListViewOneRowTests(TestCase):
    fixtures = ['dump_one_row.json']

    def test_get_groups_with_one_row_db(self):
        response = self.client.get(reverse('alphabetical'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['groups'], ['H'])


class AlphabeticalEmployeeListViewThreeGroupsTests(TestCase):
    fixtures = ['dump_fortythree_rows.json']

    def test_get_groups_with_three_groups_db(self):
        response = self.client.get(reverse('alphabetical'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['groups'], [['H'], ['S'], ['Б', 'Х']])


class AlphabeticalNameListViewEmptyTests(TestCase):
    def test_get_groups_with_empty_db(self):
        self.client.get(reverse('alphabetical'))
        response = self.client.get(reverse('alphabet_list', args=('a',)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['groups'], [])
       

class AlphabeticalNameListViewOneRowTests(TestCase):
    fixtures = ['dump_one_row.json']

    def test_get_groups_with_one_row_db(self):
        self.client.get(reverse('alphabetical'))
        response = self.client.get(reverse('alphabet_list', args=('H',)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['groups'], ['H'])
        self.assertEqual(response.context['employees'], [Employee.objects.get(last_name='Hucknall')])
        self.assertContains(response, 'Hucknall')

    def test_chosen_group_wrong(self):
        self.client.get(reverse('alphabetical'))
        with self.assertRaisesMessage(Exception, 'Trying to get employees with wrong letter of last name group.'):
            self.client.get(reverse('alphabet_list', args=('B',)))


class AlphabeticalNameListViewThreeGroupsTests(TestCase):
    fixtures = ['dump_fortythree_rows.json']

    def test_get_h_group(self):
        self.client.get(reverse('alphabetical'))
        response = self.client.get(reverse('alphabet_list', args=('H',)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['groups'], [['H'], ['S'], ['Б', 'Х']])
        self.assertEqual(response.context['employees'], [Employee.objects.get(last_name='Hucknall')])
        self.assertContains(response, 'Hucknall')

    def test_get_bx_group(self):
        self.client.get(reverse('alphabetical'))
        response = self.client.get(reverse('alphabet_list', args=('Б',)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['groups'], [['H'], ['S'], ['Б', 'Х']])
        self.assertEqual(response.context['employees'], [Employee.objects.get(last_name='Бженджешчикевич'),
                                                         Employee.objects.get(last_name='Хэмильтон')])
        self.assertContains(response, 'Гжегож')
        self.assertContains(response, 'Льюис')

    def test_get_s_group(self):
        self.client.get(reverse('alphabetical'))
        response = self.client.get(reverse('alphabet_list', args=('S',)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['groups'], [['H'], ['S'], ['Б', 'Х']])
        self.assertContains(response, 'Sotley')


class AlphabeticalGrouperWithoutFixturesTests(TestCase):
    def test_get_groups_with_empty_db(self):
        self.assertEqual(AlphabeticalGrouper().get_alphabetical_groups(), [])


class AlphabeticalGrouperWithOneRowFixtureTests(TestCase):
    fixtures = ['dump_one_row.json']

    def test_get_groups_with_one_row_to_split(self):
        self.assertEqual(AlphabeticalGrouper().get_alphabetical_groups(), ['H'])


class AlphabeticalGrouperWithThreeRowFixtureTests(TestCase):
    fixtures = ['dump_three_row.json']

    def test_get_groups_with_min_amount_of_rows_to_split(self):
        self.assertEqual(AlphabeticalGrouper().get_alphabetical_groups(), [['H'], ['Б'], ['Х']])


class AlphabeticalGrouperWithOneLetterFixtureTests(TestCase):
    fixtures = ['dump_one_letter.json']
  
    def test_get_groups_with_three_rows_in_one_letter_to_split(self):
        self.assertEqual(AlphabeticalGrouper().get_alphabetical_groups(), ['S'])


class AlphabeticalGrouperWithFortyThreeLetterFixtureTests(TestCase):
    fixtures = ['dump_fortythree_rows.json']
   
    def test_get_groups_with_three_one_groups_and_one_forty_rows_to_split(self):
        self.assertEqual(AlphabeticalGrouper().get_alphabetical_groups(), [['H'], ['S'], ['Б', 'Х']])


class AlphabeticalGrouperTests(TestCase):
    fixtures = ['dumpdata.json']

    def test_get_alphabetical_groups(self):
        self.assertEqual(AlphabeticalGrouper().get_alphabetical_groups(),
                         [['A', 'B', 'C'],
                          ['D', 'E', 'F'],
                          ['G', 'H', 'I', 'J', 'L'],
                          ['M', 'N', 'P'],
                          ['R', 'S', 'T', 'V', 'W', 'Y', 'Б', 'Х']])


class AlphabetGroupsCalculatorTests(TestCase):
    def test_weights_little_less_number_names(self):
        weights = [10, 12, 17, 6, 3]
        g = AlphabetBestGroupCalculator(49)
        with self.assertRaisesMessage(Exception, 'Number of names: 49 and alphabet weights of that names: [10, 12, 17, 6, 3] are not match.'):
            g.find_best_grouping_method(weights)

    def test_weights_more_than_number_names(self):
        weights = [10, 12, 17, 6, 3]
        g = AlphabetBestGroupCalculator(20)
        with self.assertRaisesMessage(Exception, 'Number of names: 20 and alphabet weights of that names: [10, 12, 17, 6, 3] are not match.'):
            g.find_best_grouping_method(weights)
            
    def test_weights_equal_number_names(self):
        weights = [10, 12, 17, 6, 3]
        g = AlphabetBestGroupCalculator(48)
        g.find_best_grouping_method(weights)
        self.assertEqual(g.best_delimeter, 4)
        self.assertEqual(g.best_groups, [10, 12, 17, 9])


class GetEmployeesBLNGFullDumpTests(TestCase):
    fixtures = ['dumpdata.json']
    groups = [['A', 'B', 'C'],
              ['D', 'E', 'F'],
              ['G', 'H', 'I', 'J', 'L'],
              ['M', 'N', 'P'],
              ['R', 'S', 'T', 'V', 'W', 'Y', 'Б', 'Х']]

    def test_all_parameters_correct(self):
        e = []
        e.extend(list(Employee.objects.filter(last_name__startswith='A')))
        e.extend(list(Employee.objects.filter(last_name__startswith='B')))
        e.extend(list(Employee.objects.filter(last_name__startswith='C')))
        self.assertEqual(get_employees_by_last_name_group(self.groups, 'A'), e)

    def test_chosen_group_is_lower(self):
        with self.assertRaisesMessage(Exception, 'Trying to get employees with wrong letter of last name group.'):
            get_employees_by_last_name_group(self.groups, 'a')

    def test_wrong_chosen_group(self):
        with self.assertRaisesMessage(Exception, 'Trying to get employees with wrong letter of last name group.'):
            get_employees_by_last_name_group(self.groups, 'K')


class GetEmployeesBLNG43RowsTests(TestCase):
    fixtures = ['dump_fortythree_rows.json']
    groups = [['H'], ['S'], ['Б', 'Х']]

    def test_chosen_group_have_two_letters(self):
        e = []
        e.extend(list(Employee.objects.filter(last_name__startswith='Б')))
        e.extend(list(Employee.objects.filter(last_name__startswith='Х')))
        self.assertEqual(get_employees_by_last_name_group(self.groups, 'Б'), e)

    def test_chosen_group_have_one_letter(self):
        e = []
        e.extend(list(Employee.objects.filter(last_name__startswith='S')))
        self.assertEqual(get_employees_by_last_name_group(self.groups, 'S'), e)

    def test_chosen_group_have_one_row(self):
        e = []
        e.extend(list(Employee.objects.filter(last_name__startswith='H')))
        self.assertEqual(get_employees_by_last_name_group(self.groups, 'H'), e)


class GetEmployeesBLNGOneRowsTests(TestCase):
    fixtures = ['dump_one_row.json']
    groups = ['H']

    def test_chosen_group_have_one_row(self):
        e = []
        e.extend(list(Employee.objects.filter(last_name__startswith='H')))
        self.assertEqual(get_employees_by_last_name_group(self.groups, 'H'), e)


class GetEmployeesBLNGEmptyTests(TestCase):
    groups = []

    def test_groups_empty(self):
        self.assertEqual(get_employees_by_last_name_group(self.groups, ''), [])
