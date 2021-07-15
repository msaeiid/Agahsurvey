from django.urls import path

from AgahSurvey import views

app_name = 'Survey'

urlpatterns = [
    path('survey/<str:title>/', views.SurveyView, name='survey'),
    path('question/<int:answersheet_pk>/', views.Personal_Question_View, name='PersonalQuestion'),
    path('social_question/<int:answersheet_pk>/<int:question_pk>', views.Social_class, name='SocialQuestion'),
    path('brand/<int:answersheet_pk>/<int:question_pk>', views.Brand_View, name='brand'),
    path('brands/', views.brand_list_ajax, name='brand_list_ajax'),
    path('interviewer/get_name/', views.get_interviewer_name, name='interviewer_get_name_ajax'),
    path('question/get_age/', views.get_age_ajax, name='question_get_age')
]
