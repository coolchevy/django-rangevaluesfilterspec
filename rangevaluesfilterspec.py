"""
Adds filtering by ranges of dates birth in the admin filter sidebar.

Example:

from django.db import models
import rangevaluesfilterspec
 
class Person(models.Model):
    dateofbirth = models.DateField()
    dateofbirth.age_filter_range = [18,21,30,40]

    class Admin:
        list_filter = ['dateofbirth']
"""

__author__ = "Vitalii Kulchevych  <coolchevy@gmail.com>"
__date__ = "01 Feb 2011"


from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.contrib.admin.filterspecs import FilterSpec

class RangeValuesFilterSpec(FilterSpec):

    def __init__(self, f, request, params, model, model_admin):
        super(RangeValuesFilterSpec, self).__init__(f, request, params, model, model_admin)
        self.field_generic = '%s__' % self.field.name
        self.parsed_params = dict([(k, v) for k, v in params.items() if k.startswith(self.field_generic)])
        self.links = [(_('All'), {})]
        last_value = None
        for max_value in sorted(f.list_filter_range):
            max_value = str(max_value)
            if last_value == None:
                label = '&lt; ' + max_value
                range = {'%s__lt' % f.name: max_value}
            else:
                label = last_value + ' - ' + max_value
                range = {'%s__gte' % self.field.name: last_value, '%s__lt' % f.name: max_value}
            self.links.append((_(mark_safe(label)), range))
            last_value = max_value
        self.links.append((_(mark_safe('&ge; ' + max_value)), {'%s__gte' % f.name: max_value}))

    def choices(self, cl):
        for title, param_dict in self.links:
            yield {'selected': self.parsed_params == param_dict,
                   'query_string': cl.get_query_string(param_dict, [self.field_generic]),
                   'display': title}

# register the filter
FilterSpec.filter_specs.insert(0, (lambda f: hasattr(f, 'list_filter_range'), RangeValuesFilterSpec))
