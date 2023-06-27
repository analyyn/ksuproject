
import json
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import CourseEvaluation
from .forms import CourseEvaluationForm, SearchForm
from django.urls import reverse_lazy
from django.contrib.auth.views import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.


@login_required(login_url='login')
def HomePage(request):
    return render(request, 'index.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')
    return render(request, 'signup.html')

# Create your views here.


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html', {'user': request.user})


def LogoutPage(request):
    logout(request)
    return redirect('login')


def evaluation(request):
    if request.method == 'POST':
        form = CourseEvaluationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('evaluation_list')
    else:
        form = CourseEvaluationForm()
    return render(request, 'evaluation.html', {'form': form})


def edit_evaluation(request, pk):
    template_name = 'evaluation.html'
    success_url = reverse_lazy('evaluation_list')
    evaluation = get_object_or_404(CourseEvaluation, pk=pk)
    if request.method == 'POST':
        form = CourseEvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            return redirect('evaluation_list')
    else:
        form = CourseEvaluationForm(instance=evaluation)
    return render(request, template_name, {'form': form})


def delete_evaluation(request, pk):
    template_name = 'delete_evaluation.html'
    success_url = reverse_lazy('evaluation_list')
    evaluation = get_object_or_404(CourseEvaluation, pk=pk)
    if request.method == 'POST':
        evaluation.delete()
        return redirect('evaluation_list')
    return render(request, template_name, {'evaluation_list': evaluation})


def evaluation_list(request):
    evaluations = CourseEvaluation.objects.all()
    return render(request, 'evaluation_list.html', {'evaluations': evaluations})


def dashboard(request):
    return render(request, 'index.html')


def student(request):
    return render(request, 'student.html')


def evaluate(request):
    if request.method == 'POST':
        # rank_form = RankForm(request.POST)
        # course_form = CourseForm(request.POST)
        # subject_form = SubjectForm(request.POST)
        # year_form = Year
        form = CourseEvaluationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('evaluation_list')
    else:
        form = CourseEvaluationForm()
    return render(request, 'evaluation.html', {'form': form, })


def account(request):
    return render(request, 'account.html')


def add_class(request):
    return render(request, 'add_class.html'),


def add_questionnaire(request):
    return render(request, 'add_questionnaire.html'),


def add_student(request):
    return render(request, 'add_student.html'),


def manage_class(request):
    return render(request, 'manage_class.html'),


def manage_student(request):
    return render(request, 'manage_student.html'),


def search_ajax_view(request):
    query = request.GET.get('query')
    results = CourseEvaluation.objects.filter(
        faculty_Lname__icontains=query)  # Adjust the field name as needed

    data = []
    for result in results:
        data.append({
            'faculty_Lname': result.faculty_Lname,
            'faculty_Fname': result.faculty_Fname,
            'faculty_Mname': result.faculty_Mname,
            'faculty_rank': result.faculty_rank,
            'semester': result.semester,
            'subject_code': result.subject_code,
            'total_average': result.total_average,
            'year': result.year,
            'student_name': result.student_name,
        })

    return JsonResponse(data, safe=False)


def studentsView(request):
    cs_no = CourseEvaluation.objects.filter(student_course='ComScie').count()
    cs_no = int(cs_no)
    print('Number of Comscie are', cs_no)

    it_no = CourseEvaluation.objects.filter(student_course='BSIT').count()
    it_no = int(it_no)
    print('Number of IT are', it_no)

    is_no = CourseEvaluation.objects.filter(student_course='BSIS').count()
    is_no = int(is_no)
    print('Number of IS are', is_no)

    ce_no = CourseEvaluation.objects.filter(student_course='CompEng').count()
    ce_no = int(ce_no)
    print('Number of CompEng are', ce_no)

    course_list = ['Computer Science', 'BSIT', 'BSIS', 'CompEng']
    number_list = [cs_no, it_no, is_no, ce_no]
    data = {
        'labels': course_list,
        'data': number_list,
    }

    context = {
        'chart_data': json.dumps(data),
    }
    return render(request, 'index.html', context)
