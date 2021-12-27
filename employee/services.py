from .models import Employee
from typing import List

# TODO: add readme to deploy, git and deploy

class AlphabeticalGrouper:
    def __init__(self) -> None:
        self._employees = Employee.objects.order_by('last_name')
        self._number_of_names = Employee.objects.count()

        self._groups_calculator = AlphabetBestGroupCalculator(self._number_of_names)
        self._alphabet = []
        self._alphabet_weights = []
        self._alphabetical_result_groups = [[]]

    def get_alphabetical_groups(self):
        self._define_alphabet_and_weights()

        if self._is_employees_less_min_groups_amount():
            return self._alphabet

        self._groups_calculator.find_best_grouping_method(self._alphabet_weights)

        if self._is_last_name_first_letters_less_min_groups_amount():
            return self._alphabet
 
        self._regroup_alphabet_with_best_grouping_method()
        return self._alphabetical_result_groups

    def _is_employees_less_min_groups_amount(self):
        if len(self._employees) < self._groups_calculator.min_groups_number:
            return True
        return False

    def _is_last_name_first_letters_less_min_groups_amount(self):
        if self._groups_calculator.best_delimeter == 0:
            return True
        return False

    def _define_alphabet_and_weights(self):
        for row in self._employees:
            first_letter_last_name = row.last_name[0]
            if first_letter_last_name in self._alphabet:
                i = self._alphabet.index(first_letter_last_name)
                self._alphabet_weights[i] += 1
            else:
                self._alphabet.append(first_letter_last_name)
                self._alphabet_weights.append(1)

    def _regroup_alphabet_with_best_grouping_method(self):
        counter = 0
        i = 0
        j = 0

        while i < len(self._alphabet_weights) and j < len(self._alphabet_weights):
            counter += self._alphabet_weights[i]
            self._alphabetical_result_groups[j].append(self._alphabet[i])
            i += 1
            if counter == self._groups_calculator.best_groups[j]:
                j += 1
                counter = 0
                if i < len(self._alphabet_weights) and j < len(self._alphabet_weights):
                    self._alphabetical_result_groups.append([])


class AlphabetBestGroupCalculator:
    def __init__(self, number_of_names: int) -> None:
        self._min_groups_number = 3
        self._max_groups_number = 7

        self._number_of_names = number_of_names
        self._alphabet_weights = 0

        self._best_delimeter = 0
        self._best_groups = []
        self._best_diff_epsilon = self._number_of_names

    def find_best_grouping_method(self, alphabet_weights: List[int]):
        self._check_alphabet_weights(alphabet_weights)
        self._alphabet_weights = alphabet_weights
        for delimeter in range(self._min_groups_number, self._max_groups_number+1):
            if len(self._alphabet_weights) < delimeter:
                break

            average_number_names = self._number_of_names / delimeter
            groups = [0 for _ in range(delimeter)]

            self._calculate_groups(average_number_names, groups)
            diff_epsilon = self._find_diff_epsilon(average_number_names, groups)
            if diff_epsilon <= self._best_diff_epsilon:
                self._best_delimeter = delimeter
                self._best_groups = groups
                self._best_diff_epsilon = diff_epsilon

    def _check_alphabet_weights(self, alphabet_weights: List[int]):
        sum = 0
        for i in alphabet_weights:
            sum += i
        if self._number_of_names != sum:
            raise Exception(f'Number of names: {self._number_of_names} and alphabet weights of that names: {alphabet_weights} are not match.')

    def _calculate_groups(self, average_number_names: float | int, groups: List[int]):
        i = 0
        j = 0

        while j < len(self._alphabet_weights):
            if groups[i] + self._alphabet_weights[j] > average_number_names:
                low_epsilon = abs(groups[i] - average_number_names)
                high_epsilon = low_epsilon + self._alphabet_weights[j]

                if high_epsilon > low_epsilon and i + 1 < len(groups):
                    i += 1

            groups[i] += self._alphabet_weights[j]
            j += 1

    def _find_diff_epsilon(self, average_number_names: float | int, groups: List[int]) -> float | int:
        max_epsilon = 0
        min_epsilon = self._number_of_names
        for group in groups:
            epsilon = abs(average_number_names - group)
            max_epsilon = max(max_epsilon, epsilon)
            min_epsilon = min(min_epsilon, epsilon)
        return abs(max_epsilon - min_epsilon)

    @property
    def min_groups_number(self) -> int:
        return self._min_groups_number

    @property
    def best_delimeter(self) -> int:
        return self._best_delimeter

    @property
    def best_groups(self) -> List[int]:
        return self._best_groups


def get_employees_by_last_name_group(groups: List[List[str]], chosen_group: str) -> List[Employee]:
    """
    Return List of Employee that first letter of 'last_name' of Employee is in 'chosen_group' of 'groups'.

    'chosen_group' is a first letter of some group from 'groups'.
    """
    if not groups:
        return groups
    result_last_names = []
    for group in groups:
        if chosen_group == group[0]:
            for i in group:
                result_last_names.extend(list(Employee.objects.filter(last_name__startswith=i)))
            break
    if not result_last_names:
        raise Exception('Trying to get employees with wrong letter of last name group.')

    return result_last_names
