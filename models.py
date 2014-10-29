from django.db import models
import yaml

yaml_defenitions = yaml.load(open("%s.yaml"%__file__.split('.')[0]).read())
for klass, value in yaml_defenitions.iteritems():
    initial_dict =  { '__module__':__name__,}
    for field in value['fields']:
        field_id = field['id']
        field_type = field['type']
        field_title = field['title']
        if field_type == "char":
            initial_dict[field_id] = models.CharField(field_title, max_length=255, null=True)
        elif field_type == "int":
            initial_dict[field_id] = models.IntegerField(field_title, null=True)
        elif field_type == "date":
            initial_dict[field_id] = models.DateTimeField(field_title, null=True)

    locals()[klass] = type(klass, (models.Model,), initial_dict)
