from django.urls import path

from AgahSurvey import views

app_name = 'Survey'

urlpatterns = [
    path('survey/<str:title>/', views.SurveyView, name='survey'),
    path('question/<int:answersheet_pk>/', views.Personal_Question_View, name='PersonalQuestion'),
    path('social_question/<int:answersheet_pk>/<int:question_pk>', views.Social_class, name='SocialQuestion'),
    path('brand/<int:answersheet_pk>/<int:question_pk>', views.Brand_View, name='brand'),
    path('interviewer/get_name/', views.get_interviewer_name, name='interviewer_get_name_ajax'),
    path('question/get_age/', views.get_age_ajax, name='question_get_age'),
    path('brands_brands_list/', views.option_list_ajax, name='brands_brands_list'),
    path('brands_questions_list/', views.question_list_ajax, name='brands_questions_list'),
    path('brands_answer_questions/', views.answer_brand_questions_ajax, name='answer_brand_questions_ajax'),
    path('sentences/<int:answersheet_pk>/<int:question_pk>', views.sentences, name='sentence')
]
