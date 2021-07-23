from django import forms
from django.core.validators import RegexValidator
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from AgahSurvey.models import Interviewer, Responder, AnswerSheet


class InterviewerForm(forms.ModelForm):
    interviewer_code = forms.CharField(label='کد پرسشگر',
                                       widget=forms.TextInput(
                                           attrs={'class': 'interviewer_code',
                                                  'placeholder': 'کد پرسشگر'}),
                                       validators=[RegexValidator(regex='^[0-9]{5}$',
                                                                  message='تعداد ارقام میبایست حداقل و حداکثر 5 رقم باشند')])
    interviewer_name = forms.CharField(label='نام پرسشگر', max_length=100,
                                       widget=forms.TextInput(
                                           attrs={'class': 'interviewer_name', 'readonly': '',
                                                  'placeholder': 'نام پرسشگر'}),
                                       validators=[
                                           RegexValidator(regex='[ آابپتسجچحخدذرزسشصضطظعغفقکلمنوهی]+',
                                                          message='لطفا از زبان فارسی استفاده نمایید')])

    class Meta:
        model = Interviewer
        fields = ('interviewer_code', 'interviewer_name',)

    def clean(self):
        cleaned_data = self.cleaned_data
        if Interviewer.objects.filter(interviewer_code=cleaned_data.get('interviewer_code')).exists():
            return cleaned_data


class ResponderForm(forms.ModelForm):
    responder_name = forms.CharField(label='نام پاسخگو', max_length=100,
                                     widget=forms.TextInput(
                                         attrs={'class': 'name', 'placeholder': 'نام پاسخگو'}),
                                     validators=[
                                         RegexValidator(regex='[ آابپتسجچحخدذرزسشصضطظعغفقکلمنوهی]+',
                                                        message='لطفا از زبان فارسی استفاده نمایید')])
    responser_family = forms.CharField(label='نام خانوادگی پاسخگو', max_length=100,
                                       widget=forms.TextInput(attrs={'class': 'family',
                                                                     'placeholder': 'نام خانوادگی پاسخگو'}),
                                       validators=[
                                           RegexValidator(regex='[ آابپتسجچحخدذرزسشصضطظعغفقکلمنوهی]+',
                                                          message='لطفا از زبان فارسی استفاده نمایید')])

    responder_mobile = forms.CharField(label='شماره موبایل', max_length=11, widget=forms.TextInput(
        attrs={'class': 'family', 'placeholder': 'شماره موبایل'}), validators=[
        RegexValidator(regex='^09[0-9]{9}$', message='لطفا شماره موبایل را به صورت کامل وارد نمایید')])

    class Meta:
        model = Responder
        fields = ('responder_name', 'responser_family', 'city', 'responder_mobile',)


class AnswerSheetForm(forms.ModelForm):
    # answersheet_date = forms.CharField(label='تاریخ مصاحبه', widget=forms.SelectDateWidget(
    #     attrs={'class': 'date', 'placeholder': 'تاریخ مصاحبه'}))
    answersheet_day = forms.CharField(label='روز هفته', max_length=20,
                                      widget=forms.TextInput(
                                          attrs={'class': 'day', 'readonly': '',
                                                 'placeholder': 'روز مصاحبه'}), )

    class Meta:
        model = AnswerSheet
        fields = ('answersheet_date', 'answersheet_day',)

    def __init__(self,*args,**kwargs):
        super(AnswerSheetForm, self).__init__(*args,**kwargs)
        self.fields['answersheet_date'] = JalaliDateField(label='تاریخ مصاحبه', widget=AdminJalaliDateWidget)
