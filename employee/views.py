from django.forms.formsets import MAX_NUM_FORM_COUNT
from django.views.generic import ListView, DetailView
from .models import Employee
from .filters import EmployeeFilter
from django_filters.views import FilterView
from django.shortcuts import render



class EmployeeFilterListView(FilterView):
    template_name = 'employee/employee_list.html'
    model = Employee
    paginate_by = 15
    filterset_class = EmployeeFilter


class EmployeeDetailView(DetailView):
    model = Employee


class AlphabeticalEmployeeListView(ListView):
    pass

# TODO: move into generic view
# TODO: refactor to services
# TODO: check all pages have bootstrap
# TODO: add tests to all views
# TODO: add readme to deploy, git and deploy 
def alphabetical_list_view(request):
    employees = Employee.objects.order_by('last_name')
    # counter = Employee.objects.count()
    # print(counter)
    
    alphabet = []
    values = []
    for row in employees:
        first_letter_last_name = row.last_name[0]
        if first_letter_last_name in alphabet:
            i = alphabet.index(first_letter_last_name)
            values[i] += 1
        else:
            alphabet.append(first_letter_last_name)
            values.append(1)
            
    counter = 0
    for i in values:
        counter += i
    print('Values:', values)
            
    MIN_GROUPS_AMOUNT = 3
    MAX_GROUPS_AMOUNT = 7
    
    best_delimeter = 0
    best_groups = []
    best_diff_epsilon = counter
    
    # TODO: test if rows < 3
    for delimeter in range(MIN_GROUPS_AMOUNT, MAX_GROUPS_AMOUNT+1):
        print('D:', delimeter)
        groups = [0 for x in range(delimeter)]
        print('Groups:', groups)
        average_names = counter / delimeter
        print('Average names:', average_names)
        
        i = 0   # groups
        j = 0   # values
        
        if j + 1 > len(values):
            raise Exception('Empty employee list')
        while True:
            
            if groups[i] + values[j] <= average_names:
                groups[i] += values[j]
                if j + 1 < len(values):
                    j += 1
                else:
                    if i + 1 < len(groups):
                        raise Exception(f'Over splitting with {delimeter}')
                    else:
                        break
            else:
                high_epsilon = abs(groups[i] + values[j] - average_names)
                low_epsilon = abs(groups[i] - average_names)
                if high_epsilon <= low_epsilon:
                    groups[i] += values[j]
                    if j + 1 < len(values):
                        j += 1
                    else:
                        if i + 1 < len(groups):
                            raise Exception(f'Over splitting with {delimeter}')
                        else:
                            break
                elif high_epsilon > low_epsilon:
                    if i + 1 < len(groups):
                        i += 1
                        groups[i] += values[j]
                        if j + 1 < len(values):
                            j += 1
                        else:
                            if i + 1 < len(groups):
                                raise Exception(f'Over splitting with {delimeter}')
                            else:
                                break
                    else:
                        groups[i] += values[j]
                        if j + 1 < len(values):
                            j += 1
                        else:
                            break
        
        print('Groups after splitting:', groups)
        check_sum = 0
        max_epsilon = 0.0
        min_epsilon = float(counter)
        for l in groups:
            check_sum += l
            max_epsilon = max(max_epsilon, abs(average_names - float(l)))
            min_epsilon = min(min_epsilon, abs(average_names - float(l)))
        
        if check_sum != counter:
            raise Exception(f'Under splitting with {delimeter}')

        diff_epsilon = abs(max_epsilon - min_epsilon)
        print('Max epsilon:', max_epsilon)
        print('Min epsilon:', min_epsilon)
        print('Difference epsilon:', diff_epsilon)
        
        if diff_epsilon <= best_diff_epsilon:
            best_delimeter = delimeter
            best_groups = groups
            best_diff_epsilon = diff_epsilon
               
    best_delimeter
    best_groups
    best_diff_epsilon
    print('Best delimeter:', best_delimeter)
    print('Best difference epsilon:', best_diff_epsilon)
    
    result_groups = [[]]
    increm = 0
    i = 0
    n = 0
        
    while n < len(values) and i < len(values):
        increm += values[n]
        result_groups[i].append(alphabet[n])
        n += 1
        if increm == best_groups[i]:
            i += 1
            increm = 0
            if n < len(values) and i < len(values):
                result_groups.append([])
        
    print('Result groups:', result_groups)
    request.session['result_groups'] = result_groups
    
    page_data = {
        'groups': result_groups
    }

    return render(request, 'employee/alphabetical_employee_list.html', page_data)


def alpha_list(request, letter):
    result_groups = request.session.get('result_groups')
    
    result_name_query = []
    for group in result_groups:
        if letter == group[0]:
            for i in group:
                result_name_query.extend(list(Employee.objects.filter(last_name__startswith=i)))
            break
            
        
    page_data = {
        'groups': result_groups,
        'employees': result_name_query
    }
    
    return render(request, 'employee/alphabetical_employee_list.html', page_data)
