from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter
from custom.functions import mine_blocks_with_clusters

class MineBlockListFilter(MultipleChoiceListFilter):
    title = 'Mine Block'
    parameter_name = 'mine_block__in'

    def lookups(self, request, model_admin):
        mb =  mine_blocks_with_clusters()
        mb_choices = []
        for mine_block in mb:
            mb_choices.append((mine_block, mine_block))
        return tuple(mb_choices)
