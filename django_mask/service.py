from django.db.models import Model as DjangoModel

from django_mask.mask_models import MaskTask, MaskModel, UpdateTask
# from mask.fake import new_faker


def create_update_tasks(msk_model: MaskModel, chunks: int):
    update_tasks = []
    dj_model: DjangoModel = msk_model.dj_model
    table_name = dj_model._meta.tablename
    start = 0
    stop = chunks
    while True:
        ids = dj_model.objects.values_list('id', flat=True)[start:stop]
        if not ids:
            break
        task = UpdateTask(table_name, ids, msk_model.func_map)
        update_tasks.append(task)
        start = stop
        stop += chunks
    return update_tasks


def run(cls, task: MaskTask, chunks=500, commit=True) -> None:
    # fkr = new_faker(task.locale)
    for m in task.models:
        if m.is_empty:
            continue
        create_update_tasks(m, chunks)
