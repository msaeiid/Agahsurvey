from django.core.validators import RegexValidator
from django.db import models


class City(models.Model):
    '''
    شهر پاسخگو
    '''

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهر'
        ordering = ['-city_population']

    city_name = models.CharField(verbose_name='نام شهر', max_length=30, blank=False, editable=True, null=False,
                                 validators=[
                                     RegexValidator(regex='[ آابپتسجچحخدذرزسشصضطظعغفقکلمنوهی]+',
                                                    message='لطفا از زبان فارسی استفاده نمایید')])
    city_population = models.PositiveBigIntegerField(verbose_name='جمعیت', blank=False, null=False, editable=True)
    is_important = models.BooleanField(verbose_name='شهر اصلی است؟', default=False)

    def __str__(self):
        return self.city_name


class Region(models.Model):
    class Meta:
        verbose_name = 'ناحیه'
        verbose_name_plural = 'ناحیه'
        ordering = ['city', '-region_point']

    city = models.ForeignKey(verbose_name='شهر', to=City, on_delete=models.CASCADE, related_name='regions')
    question = models.ForeignKey(verbose_name='پرسش', to='Question', on_delete=models.CASCADE, related_name='regions',
                                 editable=True)
    region_title = models.CharField(verbose_name='عنوان', max_length=50)
    region_value = models.PositiveSmallIntegerField(verbose_name='مقدار')
    region_point = models.PositiveSmallIntegerField(verbose_name='امتیاز')

    def __str__(self):
        return f'{self.region_title}'


class Interviewer(models.Model):
    '''
    پرسشگر
    '''

    class Meta:
        verbose_name = 'پرسشگر'
        verbose_name_plural = 'پرسشگر'

    interviewer_code = models.CharField(verbose_name='کد پرسشگر', primary_key=True, unique=True, blank=False,
                                        null=False,
                                        max_length=5, editable=True, validators=[
            RegexValidator(regex='^[0-9]{5}$', message='تعداد ارقام میبایست حداقل و حداکثر 5 رقم باشند')])
    interviewer_name = models.CharField(verbose_name='نام پرسشگر', max_length=100, blank=False, editable=True,
                                        null=False,
                                        validators=[
                                            RegexValidator(regex='[ آابپتسجچحخدذرزسشصضطظعغفقکلمنوهی]+',
                                                           message='لطفا از زبان فارسی استفاده نمایید')
                                        ])

    def __str__(self):
        return self.interviewer_name


class Responder(models.Model):
    '''
    پاسخگو
    '''

    class Meta:
        verbose_name = 'پاسخگو'
        verbose_name_plural = 'پاسخگو'

    responder_name = models.CharField(verbose_name='نام پاسخگو', max_length=100, editable=True, blank=False, null=False,
                                      validators=[RegexValidator(regex='[ آابپتسجچحخدذرزسشصضطظعغفقکلمنوهی]+',
                                                                 message='لطفا از زبان فارسی استفاده نمایید')])
    responser_family = models.CharField(verbose_name='نام خانوادگی پاسخگو', max_length=100, editable=True, blank=False,
                                        null=False, validators=[
            RegexValidator(regex='[ آابپتسجچحخدذرزسشصضطظعغفقکلمنوهی]+', message='لطفا از زبان فارسی استفاده نمایید')])
    city = models.ForeignKey(verbose_name='نام شهر', on_delete=models.PROTECT, to=City)
    responder_mobile = models.CharField(verbose_name='شماره موبایل', max_length=11, validators=[
        RegexValidator(regex='^09[0-9]{9}$', message='لطفا شماره موبایل را به صورت کامل وارد نمایید')])

    def __str__(self):
        return f'{self.responder_name} {self.responser_family}'


class Child(models.Model):
    class Meta:
        verbose_name = 'فرزند'
        verbose_name_plural = 'فرزند'
        ordering = ['-child_birthday_year']

    responder = models.ForeignKey(to=Responder, on_delete=models.CASCADE, verbose_name='پاسخگو',
                                  related_name='children')
    gender_choices = (('male', 'پسر'),
                      ('female', 'دختر'),)
    child_gender = models.CharField(verbose_name='جنسیت', choices=gender_choices, max_length=7)
    child_birthday_year = models.IntegerField(verbose_name='سال تولد', validators=[
        RegexValidator(regex='^1[0-9]{3}$', message='لطفا سال تولد را صحیح و کامل وارد نمایید')])
    child_age = models.IntegerField(verbose_name='محسابه سن اتومات', default=0, editable=False)

    def __str__(self):
        return f'فرزندان' \
               f'{self.responder.responder_name}'


class Survey(models.Model):
    '''
    پرسشنامه
    '''

    class Meta:
        verbose_name = 'پرسشنامه'
        verbose_name_plural = 'پرسشنامه'

    survey_title = models.CharField(verbose_name='عنوان', max_length=20)

    def __str__(self):
        return f'{self.survey_title}'


class Question(models.Model):
    '''
    سوالات
    '''

    class Meta:
        verbose_name = 'پرسش'
        verbose_name_plural = 'پرسش'
        ordering = ['pk']

    survey = models.ForeignKey(verbose_name='پرسشنامه', to=Survey, on_delete=models.PROTECT, related_name='questions')
    question_title = models.TextField(verbose_name='عنوان')
    question_next = models.ForeignKey(verbose_name='سوال بعدی', to='Question', on_delete=models.PROTECT, null=True,
                                      blank=True)
    is_first = models.BooleanField(verbose_name='اولین پرسش است؟', default=False)

    def __str__(self):
        return f'{self.question_title}'


class Option(models.Model):
    class Meta:
        verbose_name = 'گزینه'
        verbose_name_plural = 'گزینه'
        ordering = ['pk']

    question = models.ForeignKey(verbose_name='پرسش', to=Question, on_delete=models.CASCADE, related_name='options')
    option_title = models.TextField(verbose_name='عنوان')
    option_value = models.PositiveSmallIntegerField(verbose_name='مقدار')
    option_point = models.PositiveSmallIntegerField(verbose_name='امتیاز')

    def __str__(self):
        return f'{self.option_title}'


class AnswerSheet(models.Model):
    '''
    پاسخ های مصاحبه شونده
    '''

    class Meta:
        verbose_name = 'پاسخنامه'
        verbose_name_plural = 'پاسخنامه'

    interviewer = models.ForeignKey(verbose_name='پرسشگر', on_delete=models.PROTECT, to=Interviewer)
    responser = models.ForeignKey(verbose_name='پاسخگو', on_delete=models.CASCADE, to=Responder)
    survey = models.ForeignKey(verbose_name='پرسشنامه', to='Survey', on_delete=models.CASCADE)
    answersheet_date = models.DateField(verbose_name='تاریخ مصاحبه', editable=True)
    answersheet_day = models.CharField(verbose_name='روز هفته', max_length=20, editable=True)
    answersheet_total_point = models.PositiveSmallIntegerField(verbose_name='مجموع امتیاز', default=0, editable=False)
    social_class = models.CharField(verbose_name='کلاس اجتماعی', max_length=1, editable=False)

    def __str__(self):
        return f'{self.responser.responder_name} {self.responser.responser_family}'

    def calculate_total_point(self):
        temp = [p.point for p in self.answers.all()]
        self.answersheet_total_point = sum(temp)
        if self.responser.city.is_important:
            if 15 <= self.answersheet_total_point:
                self.social_class = 'A'
            elif 8 <= self.answersheet_total_point <= 14:
                self.social_class = 'B'
            else:
                self.social_class = 'C1'
        else:
            if 8 < self.answersheet_total_point:
                self.social_class = 'A'
            elif 5 <= self.answersheet_total_point <= 8:
                self.social_class = 'B'
            else:
                self.social_class = 'C1'

        self.save()


class Answer(models.Model):
    class Meta:
        verbose_name = 'پاسخ'
        verbose_name_plural = 'پاسخ'
        ordering = ['answersheet', 'question']

    question = models.ForeignKey(verbose_name='پرسش', to=Question, on_delete=models.CASCADE)
    answersheet = models.ForeignKey(verbose_name='پاسخنامه', to=AnswerSheet, related_name='answers',
                                    on_delete=models.CASCADE)
    answer = models.CharField(verbose_name='پاسخ', max_length=10, default=None, null=True, blank=True)
    point = models.PositiveSmallIntegerField(verbose_name='امتیاز', editable=False, null=False, blank=False, default=0)
    option = models.ForeignKey(verbose_name='گزینه', on_delete=models.CASCADE, to=Option, null=True, blank=True)

    def __str__(self):
        return  f'{self.answer}                 {self.option.option_title}'


class Limit(models.Model):
    class Meta:
        verbose_name = 'محدودیت'
        verbose_name_plural = 'محدودیت'
        ordering = ['marital_status', 'age']

    marital_status_choices = ((1, 'مجرد'),
                              (2, 'متاهل'),
                              (3, 'مطلقه'),
                              (4, 'بیوه'))

    marital_status = models.IntegerField(verbose_name='وضعیت تاهل', choices=marital_status_choices,
                                         editable=True, null=False, blank=False)
    age_choices = ((1, '24-18'),
                   (2, '29-25'),
                   (3, '34-30'),
                   (4, '39-35'),)
    age = models.IntegerField(verbose_name='بازه سنی', choices=age_choices, editable=True, blank=False, null=False)
    maximum = models.PositiveSmallIntegerField(verbose_name='تعداد سهمیه', editable=True, blank=False, null=False)
    capacity = models.PositiveSmallIntegerField(verbose_name='تعداد ثبت نام شده', editable=True, default=0)

    def __str__(self):
        return f'{self.marital_status}          {self.age}'

    def check_(self):
        if self.maximum > self.capacity:
            self.capacity += 1
            self.save()
            return True
        else:
            return False
