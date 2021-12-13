import json
import unittest

from google.protobuf.json_format import MessageToDict

from data import load
from parser import parse


class TestParser(unittest.TestCase):
    def test_feb_2018(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_02_2018.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheque-02-2018.html',
                 'src/output_test/sheets/membros-ativos-verbas-indenizatorias-02-2018.html']
                 
        dados = load(files, '2018', '02', 'src/output_test')
        result_data = parse(dados, 'mpmg/01/2018', '02', '2018')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)

        self.assertEqual(expected, result_to_dict)


    def test_jan_2019(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_01_2019.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheque-01-2019.html',
                 'src/output_test/sheets/membros-ativos-verbas-indenizatorias-01-2019.html']

        dados = load(files, '2019', '01', 'src/output_test')
        result_data = parse(dados, 'mpmg/1/2019', '01', '2019')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        
        self.assertEqual(expected, result_to_dict)


    def test_jan_2020(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_01_2020.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheque-01-2020.html',
                 'src/output_test/sheets/membros-ativos-verbas-indenizatorias-01-2020.html']
                 
        dados = load(files, '2020', '01', 'src/output_test')
        result_data = parse(dados, 'mpmg/01/2020', '01', '2020')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
    
        self.assertEqual(expected, result_to_dict)



    def test_may_2020(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_05_2020.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheque-05-2020.html',
                 'src/output_test/sheets/membros-ativos-verbas-indenizatorias-05-2020.html']
                 
        dados = load(files, '2020', '05', 'src/output_test')
        result_data = parse(dados, 'mpmg/05/2020', '05', '2020')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        
        self.assertEqual(expected, result_to_dict)
        

if __name__ == '__main__':
    unittest.main()