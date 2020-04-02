from typing import Optional

from django.utils.translation import gettext as _


class Case:
    def __init__(self, code: str, name: str, description: Optional[str] = None, example: Optional[str] = None) -> None:
        self.code = code
        self.name = name
        self.description = description
        self.example = example

    def full_description(self) -> str:
        full_description = ''
        if self.description:
            full_description += self.description
        if self.example:
            full_description += ': {}'.format(self.example)
        return full_description


class InflectCases:
    NOMN = 'nomn'
    GENT = 'gent'
    DATV = 'datv'
    ACCS = 'accs'
    ABLT = 'ablt'
    LOCT = 'loct'
    VOCT = 'voct'
    GEN2 = 'gen2'
    ACC2 = 'acc2'
    LOC2 = 'loc2'

    DEFAULT_CASES = tuple((case.code, case) for case in (
        Case(NOMN, _('именительный'), _('Кто? Что?'), _('хомяк ест')),
        Case(GENT, _('родительный'), _('Кого? Чего?'), _('у нас нет хомяка')),
        Case(DATV, _('дательный'), _('Кому? Чему?'), _('сказать хомяку спасибо')),
        Case(ACCS, _('винительный'), _('Кого? Что?'), _('хомяк читает книгу')),
        Case(ABLT, _('творительный'), _('Кем? Чем?'), _('зерно съедено хомяком')),
        Case(LOCT, _('предложный'), _('О ком? О чём?'), _('хомяка несут в корзинке')),
    ))

    AVAILABLE_CASES = DEFAULT_CASES + tuple((case.code, case) for case in (
        Case(VOCT, _('звательный'), _('Его формы используются при обращении к человеку'), _('Саш, пойдем в кино')),
        Case(GEN2, _('второй родительный'), _('частичный'),
             _('ложка сахару (gent - производство сахара); стакан яду (gent - нет яда)')),
        Case(ACC2, _('второй винительный'), example=_('записался в солдаты')),
        Case(LOC2, _('второй предложный'), _('местный'),
             _('я у него в долгу (loct - напоминать о долге); висит в шкафу (loct - монолог о шкафе); '
               'весь в снегу (loct - писать о снеге)')),
    ))

    @classmethod
    def get_case_by_code(cls, case_code: str) -> Case:
        return dict(cls.AVAILABLE_CASES)[case_code]
