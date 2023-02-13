from django_mask.mask_models import MaskTask, UpdateTask
from django_mask.fake import new_faker


class MaskService:

    @classmethod
    def create_update_tasks(cls, msk_model, chunks, faker):
        update_tasks = []
        dj_model = msk_model.dj_model
        table_name = dj_model._meta.db_table
        start = 0
        stop = chunks
        while True:
            ids = dj_model.objects.values_list('id', flat=True)[start:stop]
            if not ids:
                break
            task = UpdateTask(table_name, ids, msk_model.func_map, faker)
            update_tasks.append(task)
            start = stop
            stop += chunks
        return update_tasks

    @classmethod
    def run(cls, task: MaskTask, chunks=500, commit=True) -> None:
        fkr = new_faker(task.locale)
        tasks = []
        for m in task.models:
            if m.is_empty:
                continue
            tasks.extend(cls.create_update_tasks(m, chunks, fkr))
        for t in tasks:
            t.process()
