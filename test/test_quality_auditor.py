"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      SUT para Quality Auditor
AUTOR:       Fisherk2
FECHA:       2026-02-19
DESCRIPCIÓN: Pruebas unitarias e integración para el sistema de auditoría de calidad
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

import os
import sys
from typing import Dict, Any, List

# ⋮⋮⋮⋮⋮⋮⋮⋮ Agrega directorio ruta src para importaciones ⋮⋮⋮⋮⋮⋮⋮⋮
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from quality_auditor.main_auditor import QualityAuditor
from quality_auditor.null_analyzer import NullAnalyzer
from quality_auditor.uniqueness_analyzer import UniquenessAnalyzer
from quality_auditor.statistical_analyzer import StatisticalAnalyzer
from quality_auditor.date_analyzer import DateAnalyzer
from utils.quality_report import QualityReport
from readers.quality_rules_reader import QualityRulesReader
from utils.data_parser import DataParser


class TestQualityAuditor:
    """
    Suit de pruebas para sistema de auditor de calidad.
    """

    # ▁▂▃▄▅▆▇███████ Datos de prueba de ejemplo ███████▇▆▅▄▃▂▁
    _valid_data = [
        {"id": 1, "name": "John", "age": 30, "email": "john@example.com", "salary": 50000.0},
        {"id": 2, "name": "Jane", "age": 25, "email": "jane@example.com", "salary": 45000.0},
        {"id": 3, "name": "Bob", "age": 35, "email": "bob@example.com", "salary": 55000.0}
    ]
    
    _data_with_nulls = [
        {"id": 1, "name": "John", "age": 30, "email": "john@example.com", "salary": 50000.0},
        {"id": 2, "name": None, "age": 25, "email": "jane@example.com", "salary": 45000.0},
        {"id": 3, "name": "Bob", "age": None, "email": "bob@example.com", "salary": 55000.0}
    ]
    
    _empty_data = []
    
    _invalid_data = [
        {"id": "invalid", "name": 123, "age": "thirty", "email": None, "salary": "high"}
    ]

    @staticmethod
    def test_null_analyzer() -> bool:
        """
        Prueba funcionalidad de NullAnalyzer.count_nulls
        :return: ¿Pasa la prueba?
        """
        try:

            # ■■■■■■■■■■■■■ Datos validos ■■■■■■■■■■■■■
            result = NullAnalyzer.count_nulls(TestQualityAuditor._valid_data)
            assert isinstance(result, dict), "Result should be a dictionary"
            assert result == {}, "Valid data should have no nulls"
            
            # ■■■■■■■■■■■■■ Datos con valores nules ■■■■■■■■■■■■■
            result = NullAnalyzer.count_nulls(TestQualityAuditor._data_with_nulls)
            assert isinstance(result, dict), "Result should be a dictionary"
            assert result["name"] == 1, "Should detect 1 null in name column"
            assert result["age"] == 1, "Should detect 1 null in age column"
            assert result["email"] == 0, "Should detect 0 nulls in email column"
            
            # ■■■■■■■■■■■■■ Datos vacios ■■■■■■■■■■■■■
            result = NullAnalyzer.count_nulls(TestQualityAuditor._empty_data)
            assert result == {}, "Empty data should return empty dict"
            
            # ■■■■■■■■■■■■■ Entrada vacia ■■■■■■■■■■■■■
            result = NullAnalyzer.count_nulls(None)
            assert result == {}, "None input should return empty dict"
            
            print("✅ test_null_analyzer PASSED")
            return True
            
        except Exception as e:
            print(f"❌ test_null_analyzer FAILED: {str(e)}")
            return False

    @staticmethod
    def test_uniqueness_analyzer() -> bool:
        """
        Prueba funcionalidad de UniquenessAnalyzer.calculate_uniqueness
        :return: ¿Pasa la prueba?
        """
        try:

            # ■■■■■■■■■■■■■ Datos validos ■■■■■■■■■■■■■
            result = UniquenessAnalyzer.calculate_uniqueness(TestQualityAuditor._valid_data)
            assert isinstance(result, dict), "Result should be a dictionary"
            
            # ■■■■■■■■■■■■■ Los valores deben ser unicos en esta prueba ■■■■■■■■■■■■■
            for column, percentage in result.items():
                assert isinstance(percentage, (int, float)), "Percentage should be numeric"
                assert percentage == 100.0, f"Column {column} should have 100% uniqueness"
            
            # ■■■■■■■■■■■■■ Datos duplicados ■■■■■■■■■■■■■
            duplicate_data = [
                {"id": 1, "name": "John", "age": 30},
                {"id": 2, "name": "John", "age": 25},
                {"id": 3, "name": "Bob", "age": 30}
            ]
            result = UniquenessAnalyzer.calculate_uniqueness(duplicate_data)
            assert result["name"] == 66.67, "Name should have 66.67% uniqueness (2/3 unique)"
            assert result["age"] == 66.67, "Age should have 66.67% uniqueness (2/3 unique)"
            
            print("✅ test_uniqueness_analyzer PASSED")
            return True
            
        except Exception as e:
            print(f"❌ test_uniqueness_analyzer FAILED: {str(e)}")
            return False

    @staticmethod
    def test_statistical_analyzer() -> bool:
        """
        Prueba de funcionalidad de StatisticalAnalyzer.summary_stadistic
        :return: ¿Pasa la prueba?
        """
        try:

            # ■■■■■■■■■■■■■ Datos validos ■■■■■■■■■■■■■
            result = StatisticalAnalyzer.summary_stadistic(TestQualityAuditor._valid_data)
            assert isinstance(result, dict), "Result should be a dictionary"
            
            # ■■■■■■■■■■■■■ Verificar estructura ■■■■■■■■■■■■■
            assert "statistics" in result, "Result should contain statistics"
            assert "out_of_range" in result, "Result should contain out_of_range"
            assert "rules_applied" in result, "Result should contain rules_applied"
            
            # ■■■■■■■■■■■■■ Verificar contenido de estadisticas ■■■■■■■■■■■■■
            stats = result["statistics"]
            assert "age" in stats, "Should analyze age column"
            assert "salary" in stats, "Should analyze salary column"
            
            age_stats = stats["age"]
            assert age_stats["minimum"] == 25, "Age minimum should be 25"
            assert age_stats["maximum"] == 35, "Age maximum should be 35"
            assert age_stats["average"] == 30.0, "Age average should be 30.0"
            
            print("✅ test_statistical_analyzer PASSED")
            return True
            
        except Exception as e:
            print(f"❌ test_statistical_analyzer FAILED: {str(e)}")
            return False

    @staticmethod
    def test_date_analyzer() -> bool:
        """
        Prueba de funcionalidad DateAnalyzer.check_date_coherence
        :return: ¿Pasa la prueba?
        """
        try:

            # ■■■■■■■■■■■■■ Datos validos ■■■■■■■■■■■■■
            date_data = [
                {"id": 1, "name": "John", "birth_date": "1990-01-15"},
                {"id": 2, "name": "Jane", "birth_date": "1995-05-20"},
                {"id": 3, "name": "Bob", "birth_date": "1985-12-10"}
            ]
            result = DateAnalyzer.check_date_coherence(date_data, "birth_date")
            assert isinstance(result, dict), "Result should be a dictionary"
            assert "errors" in result, "Result should contain errors"
            assert "rules_applied" in result, "Result should contain rules_applied"
            assert len(result["errors"]) == 0, "Valid dates should have no errors"
            
            # ■■■■■■■■■■■■■ Fechas futuras ■■■■■■■■■■■■■
            future_date_data = [
                {"id": 1, "name": "John", "birth_date": "2050-01-15"},
                {"id": 2, "name": "Jane", "birth_date": "1995-05-20"}
            ]
            result = DateAnalyzer.check_date_coherence(future_date_data, "birth_date")
            assert len(result["errors"]) > 0, "Future date should generate errors"
            
            print("✅ test_date_analyzer PASSED")
            return True
            
        except Exception as e:
            print(f"❌ test_date_analyzer FAILED: {str(e)}")
            return False

    @staticmethod
    def test_quality_auditor_basic() -> bool:
        """
        Prueba de funcionalidad basica de QualityAuditor.quality_audit
        :return: ¿Pasa la prueba?
        """
        try:

            # ■■■■■■■■■■■■■ Datos validos ■■■■■■■■■■■■■
            result = QualityAuditor.quality_audit(TestQualityAuditor._valid_data)
            assert isinstance(result, dict), "Result should be a dictionary"
            
            # ■■■■■■■■■■■■■ Verifica llaves requeridas ■■■■■■■■■■■■■
            required_keys = ["timestamp", "total_rows", "config_applied", "null_analysis", 
                          "uniqueness_analysis", "statistical_analysis", "count_types", "alerts"]
            for key in required_keys:
                assert key in result, f"Result should contain {key}"
            
            assert result["total_rows"] == 3, "Should count 3 rows"
            assert isinstance(result["config_applied"], dict), "Config applied should be dict"
            
            print("✅ test_quality_auditor_basic PASSED")
            return True
            
        except Exception as e:
            print(f"❌ test_quality_auditor_basic FAILED: {str(e)}")
            return False

    @staticmethod
    def test_quality_auditor_with_config() -> bool:
        """
        Prueba de QualityAuditor.quality_audit con archivo de configuracion
        :return: ¿Pasa la prueba?
        """
        try:
            config_path = "schemas/quality_rules.yaml"
            
            # ■■■■■■■■■■■■■ Configuracion ■■■■■■■■■■■■■
            result = QualityAuditor.quality_audit(TestQualityAuditor._valid_data, config_path)
            assert isinstance(result, dict), "Result should be a dictionary"
            
            # ■■■■■■■■■■■■■ Verificar si la configuracion fue aplicada ■■■■■■■■■■■■■
            config_applied = result["config_applied"]
            assert config_applied["path_quality_rules"] == config_path, "Should track config path"
            assert isinstance(config_applied["original_rows"], int), "Should track original rows"
            assert isinstance(config_applied["filtered_rows"], int), "Should track filtered rows"
            
            print("✅ test_quality_auditor_with_config PASSED")
            return True
            
        except Exception as e:
            print(f"❌ test_quality_auditor_with_config FAILED: {str(e)}")
            return False

    @staticmethod
    def test_quality_rules_reader() -> bool:
        """
        Prueba funcionalidad QualityRulesReader
        :return: ¿Pasa la prueba?
        """
        try:
            config_path = "schemas/quality_rules.yaml"
            
            # ■■■■■■■■■■■■■ Carga de configuracion ■■■■■■■■■■■■■
            config = QualityRulesReader.load_configs(config_path)
            assert isinstance(config, dict), "Config should be a dictionary"
            assert "quality_rules" in config, "Config should contain quality_rules"
            
            # ■■■■■■■■■■■■■ Obteniendo reglas generales ■■■■■■■■■■■■■
            general_rules = QualityRulesReader.get_general_rules(config)
            assert isinstance(general_rules, dict), "General rules should be a dictionary"
            
            # ■■■■■■■■■■■■■ Obteniendo umbrales ■■■■■■■■■■■■■
            thresholds = QualityRulesReader.get_thresholds(config)
            assert isinstance(thresholds, dict), "Thresholds should be a dictionary"
            assert "warning" in thresholds, "Should contain warning thresholds"
            assert "critical" in thresholds, "Should contain critical thresholds"
            
            # ■■■■■■■■■■■■■ Obteniendo reglas de tipo de datos ■■■■■■■■■■■■■
            data_type_rules = QualityRulesReader.get_data_type_rules(config, "null")
            assert isinstance(data_type_rules, dict), "Data type rules should be a dictionary"
            
            print("✅ test_quality_rules_reader PASSED")
            return True
            
        except Exception as e:
            print(f"❌ test_quality_rules_reader FAILED: {str(e)}")
            return False

    @staticmethod
    def test_quality_report_generator() -> bool:
        """
        Prueba funcionalidad QualityReport con diferentes formatos
        :return: ¿Pasa la prueba?
        """
        try:

            # ■■■■■■■■■■■■■ Resultado de pruebas ■■■■■■■■■■■■■
            test_results = {
                "timestamp": "2026-02-19T20:00:00",
                "total_rows": 3,
                "null_analysis": {"name": 1, "age": 0},
                "uniqueness_analysis": {"name": 100.0, "age": 66.67},
                "alerts": ["Test alert 1", "Test alert 2"]
            }
            
            # ■■■■■■■■■■■■■ Reporte JSON ■■■■■■■■■■■■■
            json_report = QualityReport.generate_json_report(test_results)
            assert isinstance(json_report, str), "JSON report should be a string"
            assert "name" in json_report, "JSON report should contain data"
            
            # ■■■■■■■■■■■■■ Reporte resumen ■■■■■■■■■■■■■
            summary_report = QualityReport.generate_summary_report(test_results)
            assert isinstance(summary_report, str), "Summary report should be a string"
            assert "INFORME DE CALIDAD DE DATOS" in summary_report, "Should contain header"
            
            # ■■■■■■■■■■■■■ Reporte detallado ■■■■■■■■■■■■■
            detailed_report = QualityReport.generate_detail_report(test_results)
            assert isinstance(detailed_report, str), "Detailed report should be a string"
            assert "INFORME DETALLADO" in detailed_report, "Should contain header"
            
            print("✅ test_quality_report_generator PASSED")
            return True
            
        except Exception as e:
            print(f"❌ test_quality_report_generator FAILED: {str(e)}")
            return False

    @staticmethod
    def test_data_parser() -> bool:
        """
        Prueba funciones utilitarias de DataParser
        :return: ¿Pasa la prueba?
        """
        try:

            # ■■■■■■■■■■■■■ Validacion numerica ■■■■■■■■■■■■■
            assert DataParser.is_numeric_value(123) == True, "123 should be numeric"
            assert DataParser.is_numeric_value(123.45) == True, "123.45 should be numeric"
            assert DataParser.is_numeric_value("123") == True, "String '123' should be numeric"
            assert DataParser.is_numeric_value("abc") == False, "'abc' should not be numeric"
            
            # ■■■■■■■■■■■■■ Validacion de cadenas ■■■■■■■■■■■■■
            assert DataParser.is_string_value("test") == True, "String should be string"
            assert DataParser.is_string_value(123) == False, "Number should not be string"
            
            # ■■■■■■■■■■■■■ Valinacion de nulos ■■■■■■■■■■■■■
            assert DataParser.is_null_value(None) == True, "None should be null"
            assert DataParser.is_null_value("") == True, "Empty string should be null"
            assert DataParser.is_null_value("N/A") == True, "'N/A' should be null"
            assert DataParser.is_null_value("test") == False, "'test' should not be null"
            
            print("✅ test_data_parser PASSED")
            return True
            
        except Exception as e:
            print(f"❌ test_data_parser FAILED: {str(e)}")
            return False

    @staticmethod
    def test_integration_complete_flow() -> bool:
        """
        Prueba de integracion completa: CSV -> Config -> Audit -> Report -> Save
        :return:
        """
        try:

            # ■■■■■■■■■■■■■ Cargar datos ejemplo reales ■■■■■■■■■■■■■
            csv_path = "data/input/sample_data.csv"
            assert os.path.exists(csv_path), f"Sample data file should exist: {csv_path}"
            
            # ■■■■■■■■■■■■■ Leer datos CSV ■■■■■■■■■■■■■
            sample_data = TestQualityAuditor._load_sample_csv(csv_path)
            assert len(sample_data) > 0, "Should load sample data"
            
            # Run quality audit with configuration
            config_path = "schemas/quality_rules.yaml"
            audit_results = QualityAuditor.quality_audit(sample_data, config_path)
            assert isinstance(audit_results, dict), "Audit should return results"
            
            # Generate report
            report_content = QualityReport.generate_summary_report(audit_results)
            assert isinstance(report_content, str), "Should generate report content"
            assert len(report_content) > 100, "Report should have substantial content"
            
            # Test report saving with timestamp
            output_path = QualityReport.save_report_with_timestamp(
                audit_results, 
                "data/output/test_quality_report", 
                "json"
            )
            assert os.path.exists(output_path), "Should save report file"
            
            # Clean up test file
            if os.path.exists(output_path):
                os.remove(output_path)
            
            print("✅ test_integration_complete_flow PASSED")
            return True
            
        except Exception as e:
            print(f"❌ test_integration_complete_flow FAILED: {str(e)}")
            return False

    @staticmethod
    def test_edge_cases() -> bool:
        """
        Test edge cases and error conditions
        """
        try:
            # Test empty data
            result = QualityAuditor.quality_audit(TestQualityAuditor._empty_data)
            assert result["total_rows"] == 0, "Empty data should have 0 rows"
            assert isinstance(result["null_analysis"], dict), "Should still return structure"
            
            # Test None data
            result = QualityAuditor.quality_audit(None)
            assert result["total_rows"] == 0, "None data should have 0 rows"
            
            # Test non-existent config file
            result = QualityAuditor.quality_audit(
                TestQualityAuditor._valid_data, 
                "non_existent_config.yaml"
            )
            assert isinstance(result, dict), "Should handle missing config gracefully"
            
            # Test invalid data types
            result = NullAnalyzer.count_nulls(TestQualityAuditor._invalid_data)
            assert isinstance(result, dict), "Should handle invalid data types"
            
            print("✅ test_edge_cases PASSED")
            return True
            
        except Exception as e:
            print(f"❌ test_edge_cases FAILED: {str(e)}")
            return False

    @staticmethod
    def _load_sample_csv(csv_path: str) -> List[Dict[str, Any]]:
        """
        Helper method to load sample CSV data for testing
        """
        try:
            data = []
            with open(csv_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
                # Skip header
                for line in lines[1:]:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 6:
                            data.append({
                                "id": int(parts[0]),
                                "nombre": parts[1],
                                "edad": parts[2] if parts[2] else None,
                                "email": parts[3] if parts[3] else None,
                                "fecha_registro": parts[4] if parts[4] else None,
                                "salario": float(parts[5]) if parts[5] else None,
                                "departamento": parts[6] if len(parts) > 6 else None,
                                "activo": parts[7].strip() if len(parts) > 7 else None
                            })
            return data
            
        except Exception as e:
            print(f"Error loading sample CSV: {str(e)}")
            return []

    @staticmethod
    def run_all_tests() -> bool:
        """
        Execute all tests and report overall status
        """
        print("🚀 Starting Quality Auditor Test Suite")
        print("=" * 50)
        
        tests = [
            ("Null Analyzer", TestQualityAuditor.test_null_analyzer),
            ("Uniqueness Analyzer", TestQualityAuditor.test_uniqueness_analyzer),
            ("Statistical Analyzer", TestQualityAuditor.test_statistical_analyzer),
            ("Date Analyzer", TestQualityAuditor.test_date_analyzer),
            ("Quality Auditor Basic", TestQualityAuditor.test_quality_auditor_basic),
            ("Quality Auditor with Config", TestQualityAuditor.test_quality_auditor_with_config),
            ("Quality Rules Reader", TestQualityAuditor.test_quality_rules_reader),
            ("Quality Report Generator", TestQualityAuditor.test_quality_report_generator),
            ("Data Parser", TestQualityAuditor.test_data_parser),
            ("Integration Complete Flow", TestQualityAuditor.test_integration_complete_flow),
            ("Edge Cases", TestQualityAuditor.test_edge_cases)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🧪 Running: {test_name}")
            try:
                if test_func():
                    passed += 1
                else:
                    print(f"   ⚠️  Test failed: {test_name}")
            except Exception as e:
                print(f"   💥 Test error: {test_name} - {str(e)}")
        
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! System is working correctly.")
            return True
        else:
            print(f"⚠️  {total - passed} tests failed. Please review the issues above.")
            return False


if __name__ == "__main__":
    """
    Main entry point for test execution
    """
    success = TestQualityAuditor.run_all_tests()
    sys.exit(0 if success else 1)