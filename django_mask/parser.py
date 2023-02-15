import yaml
from yaml.parser import ParserError

from django_mask.mask_models import MaskField, MaskModel, MaskTask
from django_mask.error import invalid_file_content_error


def parse_config(conf_as_string):
    """
    Парсит "*.yaml" конфиг в формате:
    ----------------------------------------
    version: "1"

    locale: "ru"

    models:
      - path: "agora.core.models.User"
        fields:
          - email: "email"
          - name: "name"
          - username: "username"
      - path: "agora.company.models.Company"
        fields:
          - inn: "inn"
          - kpp: "kpp"
          ...
      ...
    ----------------------------------------
    """
    errors = []
    try:
        conf = yaml.safe_load(conf_as_string)
        task = MaskTask(conf.get("locale"))
        for m in conf["models"]:
            mask_model, error = MaskModel.new(path=m["path"])
            if error is not None:
                errors.append(error)
                continue
            for f in m["fields"]:
                mask_field = MaskField(f["name"], f["processor"])
                mask_model.add_field(mask_field)
            task.add_model(mask_model)
        if errors:
            task = None
        return task, errors
    except (AttributeError, TypeError, ParserError) as exc:
        error = invalid_file_content_error(exc)
        errors.append(error)
        return None, errors
