from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.urls import reverse

from AgahSurvey.forms import ResponderForm, InterviewerForm, AnswerSheetForm
from AgahSurvey.models import Survey, Interviewer, AnswerSheet, Answer, Question, Child, Option, Limit, Responder
from AgahSurvey.serializer import Brand_Serializer, Question_Serializer


def welcome(request):
    if request.method == 'GET':
        survey = Survey.objects.first()
        return render(request, 'questions/welcome.html', context={'survey': survey})


def SurveyView(request, title):
    survey = get_object_or_404(Survey, survey_title__exact=title)
    if request.method == 'GET':
        interviewer_form = InterviewerForm(request.GET)
        responder_form = ResponderForm(request.GET)
        answerSheet_form = AnswerSheetForm(request.GET)
        context = {'interviewer_form': interviewer_form,
                   'responder_form': responder_form,
                   'answerSheet_form': answerSheet_form,
                   'title': survey.survey_title}

    else:
        interviewer_form = InterviewerForm(request.POST)  # done
        responder_form = ResponderForm(request.POST)  # done
        answerSheet_form = AnswerSheetForm(request.POST)  # done
        if interviewer_form.is_valid() and responder_form.is_valid() and answerSheet_form.is_valid():
            interviewer = get_object_or_404(Interviewer,
                                            interviewer_code=interviewer_form.cleaned_data.get('interviewer_code'))
            responder = responder_form.save()
            answerSheet = answerSheet_form.save(commit=False)
            answerSheet.interviewer_id = interviewer.pk
            answerSheet.responser_id = responder.pk
            answerSheet.survey_id = survey.pk
            answerSheet.save()
            request.session['answersheet'] = answerSheet.pk
            return redirect(reverse('Survey:PersonalQuestion'))
        else:
            interviewer_form = InterviewerForm(request.POST)
            responder_form = ResponderForm(request.POST)
            answerSheet_form = AnswerSheetForm(request.POST)
            context = {'interviewer_form': interviewer_form,
                       'responder_form': responder_form,
                       'answerSheet_form': answerSheet_form}

    return render(request=request, template_name='questions/survey.html', context=context)


def age(answer):
    from persiantools.jdatetime import JalaliDate
    today_year = JalaliDate.today().year
    if today_year < int(answer):
        raise ValueError('سال وارد شده معتبر نمی باشد')
    else:
        result = today_year - int(answer)
        if 18 <= result <= 24:
            return 1
        elif 25 <= result <= 29:
            return 2
        elif 30 <= result <= 34:
            return 3
        elif 35 <= result <= 39:
            return 4
        elif 40 <= result <= 44:
            return 5
        elif 45 <= result <= 49:
            return 6
        elif 50 <= result <= 54:
            return 7
        elif 55 <= result <= 59:
            return 8
        elif 60 <= result < 64:
            return 9
        else:
            return 0


def children(data, count, responder_id):
    from persiantools.jdatetime import JalaliDate
    year = JalaliDate.today().year
    for i in range(1, count + 1):
        temp_year = int(data.get(f'year_{i}'))
        temp_gender = data.get(f'gender_{i}')
        child = Child(child_birthday_year=temp_year, child_gender=temp_gender, responder_id=responder_id,
                      child_age=year - temp_year)
        child.save()


def check_for_capacity(age_answer, marriage_answer):
    try:
        limit = get_object_or_404(Limit, marital_status=marriage_answer, age=age_answer)
        if limit.check_():
            return True
        else:
            return False
    except:
        return True


def Personal_Question_View(request):
    answersheet = get_object_or_404(AnswerSheet, pk=request.session.get('answersheet'))
    age_question = answersheet.survey.questions.get(is_first=True)
    marriage_question = answersheet.survey.questions.get(pk=age_question.question_next.pk)
    children_question = answersheet.survey.questions.get(pk=marriage_question.question_next.pk)
    if request.method == 'GET':
        current = datetime.now().time().strftime('%p')
        AmOrPm = ''
        if current == 'AM':
            AmOrPm = 'صبح'
        else:
            AmOrPm = 'عصر'

        Who_is = answersheet.interviewer.interviewer_name

        context = {'age_question': age_question, 'marriage_question': marriage_question,
                   'children_question': children_question, 'AmOrPm': AmOrPm, 'Who_is': Who_is,
                   'survey_title': answersheet.survey.survey_title}
        return render(request, 'questions/question.html', context=context)
    else:
        age_answer = request.POST.get('age_answer')
        marriage_answer = request.POST.get('marriage_answer')
        children_answer = request.POST.get('children_answer')
        if age_answer and marriage_answer:
            age_answer = age(age_answer)
            # چک برای اتمام سهمیه
            if not check_for_capacity(age_answer, marriage_answer):
                if AnswerSheet.objects.filter(pk=request.session['answersheet']).exists:
                    answersheet=AnswerSheet.objects.get(pk=request.session['answersheet'])
                    answersheet.responser.delete()
                    answersheet.delete()
                del request.session['answersheet']
                raise ValueError('نظرسنجی به اتمام رسیده است(ظرفیت گروه سنی مشخص شده تمام شده است)')
            # چک که تاهل 0 هست یا سن
            if int(marriage_answer) == 0 or age_answer == 0:
                if AnswerSheet.objects.filter(pk=request.session['answersheet']).exists:
                    answersheet=AnswerSheet.objects.get(pk=request.session['answersheet'])
                    answersheet.responser.delete()
                    answersheet.delete()
                    del request.session['answersheet']
                    raise ValueError('نظرسنجی به اتمام رسیده است(کاربر امتناع از ورود وضعیت تاهل داشته است یا سن در رنج مشخص شده نبوده است)')
            try:
                children_answer = int(children_answer)
                if int(children_answer) > 0:
                    children(request.POST, int(children_answer), answersheet.responser.pk)
            except:
                children_answer = 0
            marriage_answer = Answer(question=marriage_question, answersheet=answersheet,
                                     option=marriage_question.options.get(option_value=int(marriage_answer)))
            age_answer = Answer(option=age_question.options.get(option_value=age_answer), question=age_question,
                                answersheet=answersheet)
            children_answer = Answer(answer=children_answer, question=children_question, answersheet=answersheet)
            marriage_answer.save()
            age_answer.save()
            children_answer.save()
            request.session['question'] = children_question.question_next.pk
            return redirect(reverse('Survey:SocialQuestion'))
        else:
            context = {'age_question': age_question, 'marriage_question': marriage_question,
                       'children_question': children_question}
    return render(request, 'questions/question.html', context=context)


def Social_class(request):
    answersheet = AnswerSheet.objects.get(pk=request.session.get('answersheet'))
    home_question = Question.objects.get(pk=request.session.get('question'))
    job_question = home_question.question_next
    region_question = job_question.question_next
    if request.method == 'GET':
        region = answersheet.responser.city.regions.all()
        context = {'home_question': home_question, 'job_question': job_question, 'region_question': region_question,
                   'region': region}
    else:
        try:
            home_answer = Answer(question=home_question,
                                 option=home_question.options.get(option_value=int(request.POST.get('home'))),
                                 answersheet=answersheet,
                                 point=home_question.options.get(
                                     option_value=int(request.POST.get('home'))).option_point)
            region_answer = Answer(question=region_question,
                                   answer=region_question.regions.get(region_value=int(request.POST.get('region')),
                                                                      city=answersheet.responser.city).region_value,
                                   answersheet=answersheet,
                                   point=region_question.regions.get(region_value=int(request.POST.get('region')),
                                                                     city=answersheet.responser.city).region_point)
            job_answer = Answer(question=job_question,
                                option=job_question.options.get(option_value=int(request.POST.get('job'))),
                                point=job_question.options.get(option_value=int(request.POST.get('job'))).option_point,
                                answersheet=answersheet)
            home_answer.save()
            job_answer.save()
            region_answer.save()
            answersheet.calculate_total_point()
            request.session['question'] = region_question.question_next.pk
            return redirect(reverse('Survey:brand'))
        except:
            region = answersheet.responser.city.regions.all()
            context = {'home_question': home_question, 'job_question': job_question, 'region_question': region_question,
                       'region': region, 'error': 'لطفااز لیست مشاغل انتخاب نمایید'}
    return render(request, 'questions/social.html', context=context)


def Brand_View(request):
    answersheet = AnswerSheet.objects.get(pk=request.session.get('answersheet'))
    question = Question.objects.get(pk=request.session.get('question'))
    if request.method == 'GET':
        questions = Question.objects.filter(pk__gte=question.pk, pk__lt=question.pk + 10)
        context = {'answersheet': answersheet.pk,
                   'last_question': questions.last().pk,
                   'first_question': questions.first().pk,
                   }
        return render(request, 'questions/brand.html', context=context)
    else:
        #question = get_object_or_404(Question, pk=request.POST.get('last_question'))
        #request.session['question'] = question.question_next.pk
        return redirect(reverse('Survey:sentence'))


def option_list_ajax(request):
    if request.method == 'GET' and request.is_ajax:
        question = get_object_or_404(Question, pk=int(request.GET.get('first_question')))
        options = question.options.all()
        serializer = Brand_Serializer(options, many=True)
        context = {'options': serializer.data}
        return JsonResponse(context, safe=True, status=200)


def get_interviewer_name(request):
    if request.is_ajax and request.method == "GET":
        try:
            interviewer = Interviewer.objects.get(pk=int(request.GET.get('interviewer_code')))
            context = {'name': interviewer.interviewer_name}
            return JsonResponse(context, safe=True, status=200)
        except:
            context = {'error': 'کد پرسشگر وارد شده نامعتبر است'}
            return JsonResponse(context, status=400)


def get_age_ajax(request):
    if request.is_ajax and request.method == "GET":
        if request.GET.get('year_1'):
            year = int(request.GET.get('year_1'))
        if request.GET.get('year_2'):
            year = int(request.GET.get('year_2'))
        if request.GET.get('year_3'):
            year = int(request.GET.get('year_3'))
        from persiantools.jdatetime import JalaliDate
        today_year = JalaliDate.today().year
        if today_year < year:
            context = {'error': 'تاریخ تولد وارد شده نامعتبر است'}
            return JsonResponse(context, status=400)
        else:
            context = {'age': today_year - year}
            return JsonResponse(context, status=200)


def question_list_ajax(request):
    if request.method == 'GET' and request.is_ajax:
        questions = Question.objects.filter(pk__gte=int(request.GET.get('first_question')),
                                            pk__lt=int(request.GET.get('first_question')) + 10)
        serializer = Question_Serializer(questions, many=True)
        context = {'questions': serializer.data}
        return JsonResponse(context, status=200)


def answer_brand_questions_ajax(request):
    import json
    if request.is_ajax and request.method == 'GET':
        list_data = ['A1', 'A2', 'A4', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12']
        answersheet = get_object_or_404(AnswerSheet, pk=request.session.get("answersheet"))
        first_question = json.loads(request.GET.get("first_question"))
        for item in list_data:
            question = get_object_or_404(Question, pk=first_question)
            save(json.loads(request.GET.get(item)), question, answersheet)
            first_question += 1
        question = get_object_or_404(Question, pk=int(request.GET.get('last_question')))
        request.session['question'] = question.question_next.pk
        request.session["A6"] = request.GET.get('A6')
        return JsonResponse({},status=200)


def save(data, question, answersheet):
    for item in data:
        answer = Answer(question=question, answersheet=answersheet, answer=data[item],
                        option=Option.objects.get(option_title=item))
        answer.save()


def sentences(request):
    answersheet = AnswerSheet.objects.get(pk=request.session.get('answersheet'))
    question = Question.objects.get(pk=request.session.get('question'))
    if request.method == 'GET':
        import json
        A6 = json.loads(request.session.get('A6'))
        pklist = list()
        for item in A6.keys():
            pklist.append(item)
        main_question = question
        A6 = Option.objects.filter(option_title__in=pklist)
        del pklist
        last = question.pk + 8
        other_questions = get_list_or_404(Question, pk__gte=main_question.question_next_id, pk__lte=last)
        context = {'main_question': main_question, 'other_question': other_questions, 'A6': A6, 'last_question': last,
                   'first_question': main_question.question_next_id}
        return render(request, 'questions/sentence.html', context=context)
    else:
        first_question = int(request.POST.get('first_question'))
        last_question = int(request.POST.get('last_question'))
        answers = dict(request.POST)
        for i in range(first_question, last_question + 1):
            question = get_object_or_404(Question, pk=i)
            for option in answers[str(i)]:
                answer = Answer(answer=int(option), answersheet=answersheet,
                                question=question)
                answer.save()
            if request.session.exists('answersheet'):
                del request.session['answersheet']
            if request.session.exists('question'):
                del request.session['question']
        return render(request, 'questions/end.html')


def f_name_suggest_ajax(request):
    if 'term' in request.GET:
        name = request.GET.get('term')
        names = Responder.objects.filter(responder_name__startswith=name)
        names_result = []
        for name in names:
            names_result.append(name.responder_name)
        return JsonResponse(names_result, safe=False, status=200)


def l_name_suggest_ajax(request):
    if 'term' in request.GET:
        family = request.GET.get('term')
        families = Responder.objects.filter(responser_family__startswith=family)
        family_list = []
        for family in families:
            family_list.append(family.responser_family)
        return JsonResponse(family_list, safe=False, status=200)
