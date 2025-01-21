import django_filters

from form.models import Form


class FormFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="نام فرم")
    course_name = django_filters.CharFilter(label="نام درس")
    year = django_filters.NumberFilter(label="سال تحصیلی")
    semester = django_filters.ChoiceFilter(choices=Form.SEMESTER_CHOICES, label="ترم")

    class Meta:
        model = Form
        fields = [
            'name',
            'course_name',
            'year',
            'semester',
        ]
