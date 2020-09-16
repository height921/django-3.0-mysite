from django.http import HttpResponse
from django.shortcuts import render
from .models import Problem
from .utils.submit_code import HDUSubmit, hdu_get_result
from status.models import Status
from django.shortcuts import get_object_or_404

# Create your views here.


def problems(request):
    '''
    题目列表
    :param request:
    :return:
    '''
    problem_list = Problem.objects.all()
    context = {
        'problems': problem_list,
    }
    return render(request, 'problems.html', context=context)


def problem_detail(request, slug):
    '''
    题目的详细内容
    :param request:
    :param slug:
    :return:
    '''
    # problem = Problem.objects.get(slug=slug)
    problem = get_object_or_404(Problem, slug=slug)
    context = {
        'problem': problem,
    }
    return render(request, 'problem_detail.html', context=context)


def submit_code(request):
    if request.method == 'POST':
        source = request.POST.get('source', '')
        code = request.POST.get('code', '')
        language = request.POST.get('language', '')
        problem_id = request.POST.get('problem_id', '')
        print('source '+ source)
        print('code '+ code)
        print('language '+ language)
        print('problem_id '+ problem_id)
        robot = HDUSubmit(1139571193, 'wzl123')
        robot.login()
        run_id = robot.submit(problem_id, code, language)
        result = hdu_get_result(request.user.username, run_id, 1139571193)
        status = Status.objects.create(result=result.get('result'),
                                       time=result.get('time'),
                                       memory=result.get('memory'),
                                       code_length=result.get('code_length'),
                                       lang=result.get('lang'),
                                       submit_time=result.get('submit_time'),
                                       user=request.user,
                                       )
        Problem.objects.first()
        # status.problem = Problem.objects.get(problem_id=int(problem_id))
        status.problem = get_object_or_404(Problem, problem_id=problem_id)
        status.save()
        return HttpResponse('{"status":"success"}')
    else:
        return HttpResponse('{"status":"success"}')
