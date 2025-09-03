import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from typing import Dict, Tuple, Any


class SistemaDifusoTarjetasGraficas:
    """Clase que maneja toda la lógica del sistema difuso para recomendación de tarjetas gráficas."""
    
    def __init__(self):
        """Inicializa el sistema difuso con todas las variables y conjuntos difusos."""
        self._configurar_universos()
        self._configurar_variables()
        self._configurar_conjuntos_difusos()
        self._configurar_mapeo_valores()
        self._configurar_salidas()
    
    def _configurar_universos(self):
        """Configura los universos de discurso para cada variable."""
        self.resolucion_universe = np.arange(0, 101, 1)
        self.configuracion_universe = np.arange(0, 101, 1)
        self.fps_objetivo_universe = np.arange(30, 241, 1)
        self.potencia_gpu_universe = np.arange(0, 101, 1)
    
    def _configurar_variables(self):
        """Configura las variables difusas del sistema."""
        self.resolucion = ctrl.Antecedent(self.resolucion_universe, 'resolucion')
        self.configuracion = ctrl.Antecedent(self.configuracion_universe, 'configuracion')
        self.fps_objetivo = ctrl.Antecedent(self.fps_objetivo_universe, 'fps_objetivo')
        self.potencia_gpu = ctrl.Antecedent(self.potencia_gpu_universe, 'potencia_gpu')
    
    def _configurar_conjuntos_difusos(self):
        """Configura todos los conjuntos difusos para cada variable."""
        # Conjuntos difusos para resolución
        self.resolucion['baja'] = fuzz.trapmf(self.resolucion.universe,[0, 0, 20,30])
        self.resolucion['media'] = fuzz.trapmf(self.resolucion.universe, [20, 30, 40, 50])
        self.resolucion['alta'] = fuzz.trapmf(self.resolucion.universe, [40, 50, 60, 70])
        self.resolucion['ultra'] = fuzz.trapmf(self.resolucion.universe, [60, 70, 100, 100])
        
        # Conjuntos difusos para configuración
        self.configuracion['baja'] = fuzz.trapmf(self.configuracion.universe, [0, 0, 20, 30])
        self.configuracion['media'] = fuzz.trapmf(self.configuracion.universe, [20, 30, 40, 50])
        self.configuracion['alta'] = fuzz.trapmf(self.configuracion.universe, [40, 50, 60, 70])
        self.configuracion['ultra'] = fuzz.trapmf(self.configuracion.universe, [60, 70, 100, 100])
        
        # Conjuntos difusos para FPS objetivo
        self.fps_objetivo['conservador'] = fuzz.trapmf(self.fps_objetivo.universe, [30, 30, 45, 60])
        self.fps_objetivo['estandar'] = fuzz.trapmf(self.fps_objetivo.universe, [55, 60, 100, 120])
        self.fps_objetivo['competitivo'] = fuzz.trapmf(self.fps_objetivo.universe, [110, 120, 160, 180])
        self.fps_objetivo['extremo'] = fuzz.trapmf(self.fps_objetivo.universe, [170, 180, 240, 240])
        
        # Conjuntos difusos para potencia de GPU
        self.potencia_gpu['baja'] = fuzz.trapmf(self.potencia_gpu.universe, [0, 0, 20, 25])
        self.potencia_gpu['media'] = fuzz.trapmf(self.potencia_gpu.universe, [20, 25, 50, 55])
        self.potencia_gpu['alta'] = fuzz.trapmf(self.potencia_gpu.universe, [50, 55, 75, 80])
        self.potencia_gpu['ultra'] = fuzz.trapmf(self.potencia_gpu.universe, [75, 80, 100, 100])
    
    def _configurar_salidas(self):
        """Configura las variables de salida difusas del sistema."""
        self.uso_gpu = ctrl.Consequent(np.arange(0, 101, 1), 'uso_gpu')
        self.temperatura = ctrl.Consequent(np.arange(40, 101, 1), 'temperatura')

        # Conjuntos difusos para uso de GPU
        self.uso_gpu['baja'] = fuzz.trapmf(self.uso_gpu.universe, [0, 0, 20, 25])
        self.uso_gpu['media'] = fuzz.trapmf(self.uso_gpu.universe, [20, 25, 45, 50])
        self.uso_gpu['alta'] = fuzz.trapmf(self.uso_gpu.universe, [45, 50, 70, 75])
        self.uso_gpu['critico'] = fuzz.trapmf(self.uso_gpu.universe, [70, 75, 100, 100])

        # Conjuntos difusos para temperatura
        self.temperatura['normal'] = fuzz.trapmf(self.temperatura.universe, [40, 40, 55, 60])
        self.temperatura['tibio'] = fuzz.trapmf(self.temperatura.universe, [55, 60, 65, 70])
        self.temperatura['caliente'] = fuzz.trapmf(self.temperatura.universe, [65, 70, 80, 85])
        self.temperatura['critica'] = fuzz.trapmf(self.temperatura.universe, [80, 85, 100, 100])

    def _reglas(self):
        """Define las reglas difusas del sistema."""
        reglas = []

        
        return reglas    
