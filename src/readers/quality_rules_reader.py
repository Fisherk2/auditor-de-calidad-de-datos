"""
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
MÓDULO:      Carga y gestión de configuración YAML
AUTOR:       Fisherk2
FECHA:       2026-02-18
DESCRIPCIÓN: Clase utilitaria para cargar y validar configuraciones de reglas de calidad desde archivos YAML
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""

from typing import Any
import yaml
import os

class QualityRulesReader:
    """
    Clase de utilidad para cargar y gestionar configuraciones YAML
    de reglas de calidad de datos
    """

    @staticmethod
    def load_configs(path_yaml: str) -> dict[str, Any]:
        """
        Lee y parsea un archivo YAML de configuración
        :param path_yaml: Ruta al archivo YAML
        :return: Diccionario con la configuración cargada
        :raises FileNotFoundError: Si el archivo no existe
        :raises yaml.YAMLError: Si hay error en el formato YAML
        :raises PermissionError: Si no hay permisos de lectura
        """
        try:
            if not os.path.exists(path_yaml):
                raise FileNotFoundError(f"Archivo de configuración no encontrado: {path_yaml}")
            
            with open(path_yaml, mode='r', encoding='utf-8') as archivo_yaml:
                configuracion = yaml.safe_load(archivo_yaml)
                return configuracion if configuracion is not None else {}
                
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Archivo de configuración no encontrado: {path_yaml}") from e
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error de formato YAML en archivo {path_yaml}: {str(e)}") from e
        except PermissionError as e:
            raise PermissionError(f"Sin permisos para leer archivo de configuración: {path_yaml}") from e
        except UnicodeDecodeError:
            raise ValueError(f"Error decodificando archivo YAML {path_yaml}")

    @staticmethod
    def get_general_rules(config: dict[str, Any]) -> dict[str, Any]:
        """
        Extrae reglas generales de calidad de la configuración
        :param config: Configuración completa
        :return: Diccionario con reglas generales
        """
        if not config or 'quality_rules' not in config:
            return {}
        
        quality_rules = config['quality_rules']
        general_rules = quality_rules.get('general', {})

        # ■■■■■■■■■■■■■ Valores por defecto si no están definidos ■■■■■■■■■■■■■
        return {
            'max_null_percentage': general_rules.get('max_null_percentage', 50.0),
            'min_uniqueness_percentage': general_rules.get('min_uniqueness_percentage', 5.0),
            'max_uniqueness_percentage': general_rules.get('max_uniqueness_percentage', 95.0)
        }

    @staticmethod
    def get_data_type_rules(config: dict[str, Any], tipo: str) -> dict[str, Any]:
        """
        Obtiene reglas específicas por tipo de dato
        :param config: Configuración completa
        :param tipo: Tipo de dato en específico (null, numeric, text, date)
        :return: Diccionario con reglas para el tipo especificado
        """
        if not config or 'quality_rules' not in config:
            return {}
        
        data_type_rules = config['quality_rules'].get('data_type_rules', {})
        return data_type_rules.get(tipo, {})

    @staticmethod
    def get_thresholds(config: dict[str, Any]) -> dict[str, Any]:
        """
        Extrae umbrales de alerta de la configuración
        :param config: Configuración completa
        :return: Diccionario con umbrales de advertencia y críticos
        """
        if not config or 'quality_rules' not in config:
            return QualityRulesReader._default_thresholds()
        
        thresholds = config['quality_rules'].get('thresholds', {})
        
        return {
            'warning': {
                'null_percentage': thresholds.get('warning', {}).get('null_percentage', 25.0),
                'low_uniqueness': thresholds.get('warning', {}).get('low_uniqueness', 10.0),
                'high_uniqueness': thresholds.get('warning', {}).get('high_uniqueness', 90.0)
            },
            'critical': {
                'null_percentage': thresholds.get('critical', {}).get('null_percentage', 50.0),
                'low_uniqueness': thresholds.get('critical', {}).get('low_uniqueness', 5.0),
                'high_uniqueness': thresholds.get('critical', {}).get('high_uniqueness', 95.0)
            }
        }

    @staticmethod
    def get_exclusions(config: dict[str, Any]) -> dict[str, Any]:
        """
        Obtiene reglas de exclusión de la configuración
        :param config: Configuración completa
        :return: Diccionario con reglas de exclusión
        """
        if not config:
            return {}
        
        exclusions = config.get('exclusions', {})
        
        return {
            'columns_to_ignore': exclusions.get('columns_to_ignore', []),
            'file_patterns_to_ignore': exclusions.get('file_patterns_to_ignore', []),
            'row_filters': exclusions.get('row_filters', [])
        }

    @staticmethod
    def check_config_structure(config: dict[str, Any]) -> bool:
        """
        Verifica que la estructura YAML sea válida
        :param config: Configuración a validar
        :return: True si la estructura es válida, False otherwise
        """
        if not isinstance(config, dict):
            return False
        
        # ■■■■■■■■■■■■■ Verificar estructura principal ■■■■■■■■■■■■■
        if 'quality_rules' not in config:
            return False
        
        quality_rules = config['quality_rules']
        if not isinstance(quality_rules, dict):
            return False

        # ■■■■■■■■■■■■■ Verificar secciones requeridas ■■■■■■■■■■■■■
        required_sections = ['general', 'data_type_rules']
        for section in required_sections:
            if section not in quality_rules:
                return False
            if not isinstance(quality_rules[section], dict):
                return False
        
        # ■■■■■■■■■■■■■ Validar reglas generales ■■■■■■■■■■■■■
        general = quality_rules['general']
        required_general_keys = ['max_null_percentage', 'min_uniqueness_percentage', 'max_uniqueness_percentage']
        for key in required_general_keys:
            if key not in general:
                return False
            if not isinstance(general[key], (int, float)):
                return False
        
        # ■■■■■■■■■■■■■ Validar reglas de tipo de dato ■■■■■■■■■■■■■
        data_type_rules = quality_rules['data_type_rules']
        if not isinstance(data_type_rules, dict):
            return False
        
        return True

    # ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤ ⎡ Advertencia ⎦ ◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤

    @staticmethod
    def apply_default_rules() -> dict[str, Any]:
        """
        TODO: Devuelve configuración por defecto si falla la lectura (Puede sufrir cambios)
        :return: Configuración por defecto
        """
        return {
            'quality_rules': {
                'general': {
                    'max_null_percentage': 50.0,
                    'min_uniqueness_percentage': 5.0,
                    'max_uniqueness_percentage': 95.0
                },
                'data_type_rules': {
                    'null': {
                        'supported_interpretations': ['', 'null', 'none', 'na', 'n/a', '<null>']
                    },
                    'boolean': {
                        'supported_interpretations': ['true', 'false', '1', '0', 'yes', 'no', 'on', 'off']
                    },
                    'numeric': {
                        'allow_negative': True,
                        'min_value': None,
                        'max_value': None,
                        'precision': 2
                    },
                    'text': {
                        'min_length': 1,
                        'max_length': 1000,
                        'allow_empty_strings': False,
                        'allowed_patterns': []
                    },
                    'date': {
                        'allow_future_dates': False,
                        'min_date': None,
                        'max_date': None,
                        'supported_formats': ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S']
                    }
                },
                'cross_field_rules': [],
                'thresholds': {
                    'warning': {
                        'null_percentage': 25.0,
                        'low_uniqueness': 10.0,
                        'high_uniqueness': 90.0
                    },
                    'critical': {
                        'null_percentage': 50.0,
                        'low_uniqueness': 5.0,
                        'high_uniqueness': 95.0
                    }
                }
            },
            'reporting': {
                'enabled': True,
                'detailed': False,
                'format': 'json',
                'include_statistics': True,
                'include_alerts': True
            },
            'exclusions': {
                'columns_to_ignore': [],
                'file_patterns_to_ignore': [],
                'row_filters': []
            }
        }

    @staticmethod
    def _default_thresholds() -> dict[str, Any]:
        """
        Retorna umbrales por defecto
        :return: Umbrales por defecto
        """
        return {
            'warning': {
                'null_percentage': 25.0,
                'low_uniqueness': 10.0,
                'high_uniqueness': 90.0
            },
            'critical': {
                'null_percentage': 50.0,
                'low_uniqueness': 5.0,
                'high_uniqueness': 95.0
            }
        }