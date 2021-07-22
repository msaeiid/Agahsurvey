from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.urls import reverse

from AgahSurvey.forms import ResponderForm, InterviewerForm, AnswerSheetForm
from AgahSurvey.models import Survey, Interviewer, AnswerSheet, Answer, Question, Child, Option
from AgahSurvey.serializer import Brand_Serializer, Question_Serializer


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
            return redirect(reverse('Survey:PersonalQuestion', args=[answerSheet.pk]))
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
        elif 60 <= result <= 64:
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


def Personal_Question_View(request, answersheet_pk):
    answersheet = get_object_or_404(AnswerSheet, pk=answersheet_pk)
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
            return redirect(reverse('Survey:SocialQuestion', args=[answersheet.pk, children_question.question_next.pk]))
        else:
            context = {'age_question': age_question, 'marriage_question': marriage_question,
                       'children_question': children_question}
    return render(request, 'questions/question.html', context=context)


def Social_class(request, answersheet_pk, question_pk):
    answersheet = AnswerSheet.objects.get(pk=answersheet_pk)
    home_question = Question.objects.get(pk=question_pk)
    job_question = home_question.question_next
    region_question = job_question.question_next
    if request.method == 'GET':
        region = answersheet.responser.city.regions.all()
        context = {'home_question': home_question, 'job_question': job_question, 'region_question': region_question,
                   'region': region}
    else:
        home_answer = Answer(question=home_question,
                             option=home_question.options.get(option_value=int(request.POST.get('home'))),
                             answersheet=answersheet,
                             point=home_question.options.get(option_value=int(request.POST.get('home'))).option_point)
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
        return redirect(reverse('Survey:brand', args=[answersheet.pk, region_question.question_next.pk]))
    return render(request, 'questions/social.html', context=context)


def Brand_View(request, answersheet_pk, question_pk):
    if request.method == 'GET':
        questions = Question.objects.filter(pk__gte=question_pk, pk__lt=question_pk + 10)
        context = {'answersheet': answersheet_pk,
                   'last_question': questions.last().pk,
                   'first_question': questions.first().pk,
                   }
        return render(request, 'questions/brand.html', context=context)
    else:
        return redirect(reverse('Survey:sentence', args=[answersheet_pk, request.POST.get('last_question')]))


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
        answersheet = get_object_or_404(AnswerSheet, pk=json.loads(request.GET.get("answersheet")))
        last_question = json.loads(request.GET.get("last_question"))
        last_question = get_object_or_404(Question, pk=last_question)
        first_question = json.loads(request.GET.get("first_question"))
        for item in list_data:
            question = get_object_or_404(Question, pk=first_question)
            save(json.loads(request.GET.get(item)), question, answersheet)
            first_question += 1
        request.session["A6"] = request.GET.get('A6')


def save(data, question, answersheet):
    for item in data:
        answer = Answer(question=question, answersheet=answersheet, answer=data[item],
                        option=Option.objects.get(option_title=item))
        answer.save()


def sentences(request, answersheet_pk, question_pk):
    if request.method == 'GET':
        import json
        A6 = json.loads(request.session.get('A6'))
        pklist = list()
        for item in A6.keys():
            pklist.append(item)
        main_question = get_object_or_404(Question, pk=question_pk)
        A6 = Option.objects.filter(option_title__in=pklist)
        del pklist
        last = question_pk + 8
        other_questions = get_list_or_404(Question, pk__gte=main_question.question_next_id, pk__lte=last)
        context = {'main_question': main_question, 'other_question': other_questions, 'A6': A6, 'last_question': last,
                   'first_question': main_question.question_next_id}
        return render(request, 'questions/sentence.html', context=context)
