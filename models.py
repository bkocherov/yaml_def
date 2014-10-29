from django.db import models
import yaml

print models.Model.__module__
yaml_defenitions = yaml.load(open("%s.yaml"%__file__.split('.')[0]).read())
for klass, value in yaml_defenitions.iteritems():
    locals()[klass] = type(klass, (models.Model,),{
                                '__module__':__name__,
                            })
