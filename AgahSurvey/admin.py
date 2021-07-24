from django.contrib import admin

from AgahSurvey.models import City, Responder, Interviewer, Question, Survey, AnswerSheet, Option, Answer, Region, \
    Child, Limit


class AnswerSheetCustom(admin.ModelAdmin):
    list_display = (
        'interviewer', 'responser', 'survey', 'answersheet_date', 'answersheet_day', 'answersheet_total_point',
        'social_class',)


class CityCustom(admin.ModelAdmin):
    list_display = ('city_name', 'city_population', 'is_important',)
    list_editable = ('city_population', 'is_important',)


class InterviewerCustom(admin.ModelAdmin):
    list_display = ('interviewer_name', 'interviewer_code',)


class ResponderCustom(admin.ModelAdmin):
    list_display = ('responder_name', 'responser_family', 'city', 'responder_mobile',)
    list_editable = ('city', 'responder_mobile',)


class SurveyCustom(admin.ModelAdmin):
    list_display = ('survey_title',)


class QuestionCustom(admin.ModelAdmin):
    list_display = ('survey', 'question_title', 'question_next', 'is_first',)
    list_editable = ('question_next', 'is_first',)


class OptionCustom(admin.ModelAdmin):
    list_display = ('question', 'option_title', 'option_value', 'option_point',)
    list_editable = ('option_value', 'option_point',)


class AnswerCustom(admin.ModelAdmin):
    list_display = ('answersheet','question', 'answer','option','point')


class RegionCustom(admin.ModelAdmin):
    list_display = ('city', 'region_title', 'region_value', 'region_point',)
    list_editable = ('region_title', 'region_value', 'region_point',)


class ChildCustom(admin.ModelAdmin):
    list_display = ('responder', 'child_gender', 'child_birthday_year',)
    list_editable = ('child_gender', 'child_birthday_year',)


class LimitCustom(admin.ModelAdmin):
    list_display = ('marital_status', 'age', 'maximum', 'capacity',)


admin.site.register(City, CityCustom)
admin.site.register(Interviewer, InterviewerCustom)
admin.site.register(Responder, ResponderCustom)
admin.site.register(Survey, SurveyCustom)
admin.site.register(Question, QuestionCustom)
admin.site.register(AnswerSheet, AnswerSheetCustom)
admin.site.register(Option, OptionCustom)
admin.site.register(Answer, AnswerCustom)
admin.site.register(Region, RegionCustom)
admin.site.register(Child, ChildCustom)
admin.site.register(Limit, LimitCustom)

# Register your models here.
