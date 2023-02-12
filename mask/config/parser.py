import yaml
from typing import Dict

from mask.models import MaskField, MaskModel, MaskTask


def parse(conf_as_string: str) -> MaskTask:
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
    conf = yaml.safe_load(conf_as_string)
    task = MaskTask(conf.get("locale"))
    m: Dict
    for m in conf["models"]:
        mask_model = MaskModel(path=m["path"])
        for f in m["fields"]:
            mask_field = MaskField(f["name"], f["processor"])
            mask_model.add_field(mask_field)
        task.add_model(mask_model)
    return task
