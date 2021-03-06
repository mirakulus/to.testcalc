import os
import pytest
import allure
import xml.etree.ElementTree as ET
from api import drivers
from api.calcpage import CalcPage

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
SCENARIOS_XML = os.path.join(SCRIPT_DIR, 'test_funcitonal_scenarios.xml')

def get_scenarios(source):
    ''' Парсит источник со сценариями и возвращает кортеж вида (scanario_name, { arg_name:arg_value }) '''
    scenarios = ET.parse(source).getroot()
    scenarios = [ scenario.attrib for scenario in scenarios ]
    return scenarios

def pytest_generate_tests(metafunc):
    ''' (pytest test-generation feature) генерация сценариев по массиву кортежей из get_scenarios() '''
    idlist = []
    argvalues = []
    print('----------------')
    print('metafunc.cls.scenarios')
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario['name'])
        scenario.pop('name', None)
        items = scenario.items()
        argnames = [x[0] for x in items]
        argvalues.append(([x[1] for x in items]))
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")

class TestFunctional(object):
    scenarios = get_scenarios(SCENARIOS_XML)

    def setup_class(cls):
        cls.calc = CalcPage(drivers.chrome(True), 'http://www.sberbank.ru/ru/quotes/converter')

    def test_calc(self, sum, cur_from, cur_to, expect):
        ''' параметризированный тест на правильность подсчета '''
        self.calc.summa = sum
        self.calc.currency_from = cur_from
        self.calc.currency_to = cur_to
        assert self.calc.convert() == expect

