import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import itertools
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



class SistemaDifusoTarjetasGraficas:
    """Clase que maneja toda la lógica del sistema difuso para recomendación de tarjetas gráficas."""

    def __init__(self):
        self.res_labels = ['baja', 'media', 'alta', 'ultra']
        self.conf_labels = ['baja', 'media', 'alta', 'ultra']
        self.fps_labels = ['conservador', 'estandar', 'competitivo', 'extremo']
        self.gpu_labels = ['baja', 'media', 'alta', 'ultra']

        self.uso_labels = ['baja', 'media', 'alta', 'critico']
        self.temp_labels = ['normal', 'tibio', 'caliente', 'critica']

        # Diccionario de resoluciones con sus valores en el universo difuso
        self.resoluciones = {
            # Resoluciones clásicas (4:3) - BAJA (0-30)
            "640×480 (VGA)": 10,
            "800×600 (SVGA)": 15,
            "1024×768 (XGA)": 20,
            "1280×1024 (SXGA)": 25,
            "1600×1200 (UXGA)": 30,
            
            # Resoluciones HD y widescreen (16:9/16:10) - MEDIA (20-50)
            "1366×768 (HD)": 35,
            "1440×900 (WXGA+)": 40,
            "1600×900 (HD+)": 45,
            "1680×1050 (WSXGA+)": 50,
            "1920×1080 (Full HD)": 55,
            "1920×1200 (WUXGA)": 60,
            
            # Resoluciones 2K, 3K - ALTA (40-70)
            "2560×1440 (QHD/2K)": 65,
            "2560×1600 (WQXGA)": 70,
            "2880×1800 (3K Retina)": 75,
            "3200×1800 (QHD+)": 80,
            
            # Resoluciones 4K y superiores - ULTRA (60-100)
            "3840×2160 (4K UHD)": 85,
            "4096×2160 (DCI 4K)": 90,
            "5120×2880 (5K)": 95,
            "6016×3384 (6K)": 98,
            "7680×4320 (8K UHD)": 100,
            
            # Ultrawide
            "2560×1080 (UW-FHD)": 50,
            "3440×1440 (UW-QHD)": 70,
            "3840×1600 (UW-QHD+)": 80,
            "5120×1440 (Dual QHD)": 85,
            "5120×2160 (5K Ultrawide)": 95
        }

        self._configurar_universos()
        self._configurar_variables()
        self._configurar_conjuntos_difusos()
        self._configurar_salidas()
        self.reglas_detalladas, self.rules = self._generar_reglas()
        sistema_ctrl = ctrl.ControlSystem(self.rules)
        self.simulador = ctrl.ControlSystemSimulation(sistema_ctrl)

    def _configurar_universos(self):
        self.resolucion_universe = np.arange(0, 101, 1)
        self.configuracion_universe = np.arange(0, 101, 1)
        self.fps_objetivo_universe = np.arange(30, 241, 1)
        self.potencia_gpu_universe = np.arange(0, 101, 1)
    
    def _configurar_variables(self):
        self.resolucion = ctrl.Antecedent(self.resolucion_universe, 'resolucion')
        self.configuracion = ctrl.Antecedent(self.configuracion_universe, 'configuracion')
        self.fps_objetivo = ctrl.Antecedent(self.fps_objetivo_universe, 'fps_objetivo')
        self.potencia_gpu = ctrl.Antecedent(self.potencia_gpu_universe, 'potencia_gpu')
    
    def _configurar_conjuntos_difusos(self):
        self.resolucion['baja'] = fuzz.trapmf(self.resolucion.universe,[0, 0, 20,30])
        self.resolucion['media'] = fuzz.trapmf(self.resolucion.universe, [20, 30, 40, 50])
        self.resolucion['alta'] = fuzz.trapmf(self.resolucion.universe, [40, 50, 60, 70])
        self.resolucion['ultra'] = fuzz.trapmf(self.resolucion.universe, [60, 70, 100, 100])
        
        self.configuracion['baja'] = fuzz.trapmf(self.configuracion.universe, [0, 0, 20, 30])
        self.configuracion['media'] = fuzz.trapmf(self.configuracion.universe, [20, 30, 40, 50])
        self.configuracion['alta'] = fuzz.trapmf(self.configuracion.universe, [40, 50, 60, 70])
        self.configuracion['ultra'] = fuzz.trapmf(self.configuracion.universe, [60, 70, 100, 100])
        
        self.fps_objetivo['conservador'] = fuzz.trapmf(self.fps_objetivo.universe, [30, 30, 45, 60])
        self.fps_objetivo['estandar'] = fuzz.trapmf(self.fps_objetivo.universe, [55, 60, 100, 120])
        self.fps_objetivo['competitivo'] = fuzz.trapmf(self.fps_objetivo.universe, [110, 120, 160, 180])
        self.fps_objetivo['extremo'] = fuzz.trapmf(self.fps_objetivo.universe, [170, 180, 240, 240])
        
        self.potencia_gpu['baja'] = fuzz.trapmf(self.potencia_gpu.universe, [0, 0, 20, 25])
        self.potencia_gpu['media'] = fuzz.trapmf(self.potencia_gpu.universe, [20, 25, 50, 55])
        self.potencia_gpu['alta'] = fuzz.trapmf(self.potencia_gpu.universe, [50, 55, 75, 80])
        self.potencia_gpu['ultra'] = fuzz.trapmf(self.potencia_gpu.universe, [75, 80, 100, 100])
    
    def _configurar_salidas(self):
        self.uso_gpu = ctrl.Consequent(np.arange(0, 101, 1), 'uso_gpu')
        self.temperatura = ctrl.Consequent(np.arange(40, 101, 1), 'temperatura')

        self.uso_gpu['baja'] = fuzz.trapmf(self.uso_gpu.universe, [0, 0, 20, 25])
        self.uso_gpu['media'] = fuzz.trapmf(self.uso_gpu.universe, [20, 25, 45, 50])
        self.uso_gpu['alta'] = fuzz.trapmf(self.uso_gpu.universe, [45, 50, 70, 75])
        self.uso_gpu['critico'] = fuzz.trapmf(self.uso_gpu.universe, [70, 75, 100, 100])

        self.temperatura['normal'] = fuzz.trapmf(self.temperatura.universe, [40, 40, 55, 60])
        self.temperatura['tibio'] = fuzz.trapmf(self.temperatura.universe, [55, 60, 65, 70])
        self.temperatura['caliente'] = fuzz.trapmf(self.temperatura.universe, [65, 70, 80, 85])
        self.temperatura['critica'] = fuzz.trapmf(self.temperatura.universe, [80, 85, 100, 100])

    def _evaluar_salida_(self, res, conf, fps, gpu):
        mapping = {
            'baja': 1, 'media': 2, 'alta': 3, 'ultra': 4,
            'conservador': 1, 'estandar': 2, 'competitivo': 3, 'extremo': 4
        }

        # CASOS ESPECIALES PRIORITARIOS 
        if res == 'baja' and conf == 'baja' and fps == 'conservador':
            if gpu == 'baja':
                return 'media', 'normal'
            elif gpu == 'media':
                return 'baja', 'normal'      # GPU media con todo bajo = uso muy bajo
            elif gpu == 'alta':
                return 'baja', 'normal'      # GPU alta con todo bajo = uso muy bajo
            else:  # gpu == 'ultra'
                return 'baja', 'normal'      # GPU ultra con todo bajo = uso muy bajo
        
        # 2. CASO TODO ULTRA: res=ultra, conf=ultra, fps=extremo
        if res == 'ultra' and conf == 'ultra' and fps == 'extremo':
            if gpu == 'baja':
                return 'critico', 'critica'  # GPU baja con todo ultra = imposible
            elif gpu == 'media':
                return 'critico', 'critica'  # GPU media con todo ultra = sobrecarga
            elif gpu == 'alta':
                return 'critico', 'caliente' # GPU alta con todo ultra = sobrecarga
            else:  # gpu == 'ultra'
                return 'alta', 'caliente'    # GPU ultra con todo ultra = alta carga
        
        # 3. CASO TODO MEDIO: res=media, conf=media, fps=estandar
        if res == 'media' and conf == 'media' and fps == 'estandar':
            if gpu == 'baja':
                return 'alta', 'tibio'       # GPU baja con todo medio = sobrecarga
            elif gpu == 'media':
                return 'media', 'normal'     # GPU media con todo medio = balanceado
            elif gpu == 'alta':
                return 'baja', 'normal'      # GPU alta con todo medio = cómodo
            else:  # gpu == 'ultra'
                return 'baja', 'normal'      # GPU ultra con todo medio = muy cómodo
        
        if res == 'alta' and conf == 'alta' and fps == 'competitivo':
            if gpu == 'baja':
                return 'critico', 'critica'  # GPU baja con todo alto = imposible
            elif gpu == 'media':
                return 'critico', 'caliente' # GPU media con todo alto = sobrecarga
            elif gpu == 'alta':
                return 'alta', 'tibio'       # GPU alta con todo alto = balanceado
            else:  # gpu == 'ultra'
                return 'media', 'normal'     # GPU ultra con todo alto = cómodo
        
        # 5. CASOS DE RESOLUCIÓN ULTRA (cualquier configuración)
        if res == 'ultra':
            if gpu == 'baja':
                return 'critico', 'critica'  # GPU baja nunca puede manejar ultra
            elif gpu == 'media':
                if conf == 'ultra' or fps == 'extremo':
                    return 'critico', 'critica'  # Sobreconfiguración
                else:
                    return 'critico', 'caliente' # Sobrecarga pero manejable
            elif gpu == 'alta':
                if conf == 'ultra' and fps == 'extremo':
                    return 'critico', 'caliente' # Límite de capacidad
                else:
                    return 'alta', 'caliente'    # Alta carga pero estable
            else:  # gpu == 'ultra'
                if conf == 'ultra' and fps == 'extremo':
                    return 'alta', 'caliente'    # Máximo rendimiento
                else:
                    return 'media', 'tibio'      # Cómodo para GPU ultra
        
        # 6. CASOS DE GPU BAJA (limitaciones críticas)
        if gpu == 'baja':
            if res in ['alta', 'ultra'] or conf in ['alta', 'ultra'] or fps in ['competitivo', 'extremo']:
                return 'critico', 'critica'  # GPU baja no puede manejar cargas altas
            elif res == 'media' or conf == 'media':
                return 'alta', 'caliente'    # GPU baja con configuraciones medias
        
        # 7. CASOS DE FPS EXTREMO (demandas altas)
        if fps == 'extremo':
            if gpu == 'baja':
                return 'critico', 'critica'  # Imposible
            elif gpu == 'media':
                if res in ['alta', 'ultra'] or conf in ['alta', 'ultra']:
                    return 'critico', 'critica'  # Sobreconfiguración
                else:
                    return 'critico', 'caliente' # Sobrecarga
            elif gpu == 'alta':
                if res == 'ultra' or conf == 'ultra':
                    return 'critico', 'caliente' # Límite
                else:
                    return 'alta', 'caliente'    # Alta carga
            else:  # gpu == 'ultra'
                if res == 'ultra' and conf == 'ultra':
                    return 'alta', 'caliente'    # Máximo rendimiento
                else:
                    return 'media', 'tibio'      # Cómodo
        
        peso_res = 1.8
        peso_conf = 1.0
        peso_fps = 1.3

        exigencia = (mapping[res] * peso_res + 
                    mapping[conf] * peso_conf + 
                    mapping[fps] * peso_fps)

        potencia = mapping[gpu] * 2.2

        balance = exigencia - potencia

        if balance <= -4:
            uso, temp = 'baja', 'normal'
        elif balance <= -2:
            uso, temp = 'media', 'normal'
        elif balance <= -0.5:
            uso, temp = 'media', 'tibio'
        elif balance <= 1:
            uso, temp = 'alta', 'tibio'
        elif balance <= 2.5:
            uso, temp = 'alta', 'caliente'
        elif balance <= 4:
            uso, temp = 'critico', 'caliente'
        else:
            uso, temp = 'critico', 'critica'

        if gpu == 'ultra' and res == 'baja' and conf == 'baja' and fps == 'conservador':
            uso, temp = 'baja', 'normal'
        
        if gpu in ['alta', 'ultra'] and res in ['baja', 'media'] and conf in ['baja', 'media']:
            if temp == 'critica':
                temp = 'caliente'
            if temp == 'caliente' and fps == 'conservador':
                temp = 'tibio'

        return uso, temp 

    def _generar_reglas(self):
        
        rules = []
         
        reglas_detalladas = []

        for i, (res, conf, fps, gpu) in enumerate(itertools.product(self.res_labels, self.conf_labels, self.fps_labels, self.gpu_labels)):
            uso, temp = self.evaluar_salida(res, conf, fps, gpu)

            
            # Crear descripción de la regla
            descripcion = (f"Regla {i+1}: SI resolución={res} Y configuración={conf} "
                        f"Y fps={fps} Y gpu={gpu} ENTONCES uso={uso} Y temperatura={temp}")
            
            reglas_detalladas.append({
                'id': i+1,
                'entradas': {'res': res, 'conf': conf, 'fps': fps, 'gpu': gpu},
                'salidas': {'uso': uso, 'temp': temp},
                'descripcion': descripcion
            })

            # Crear regla difusa (descomenta si tienes las variables definidas)
            
            rule = ctrl.Rule(
                antecedent=(self.resolucion[res] & self.configuracion[conf] & self.fps_objetivo[fps] & self.potencia_gpu[gpu]),
                consequent=[self.uso_gpu[uso], self.temperatura[temp]]
            )
            rules.append(rule)
            

    

        return reglas_detalladas, rules

    def evaluar_salida(self, res, conf, fps, gpu):
        """Método público para evaluar la salida del sistema difuso."""
        return self._evaluar_salida_(res, conf, fps, gpu)
  
    def convertir_a_etiqueta(self, valor, tipo):
        """Convierte un valor numérico a su etiqueta difusa correspondiente."""
        if tipo == 'resolucion':
            if valor <= 30:
                return 'baja'
            elif valor <= 50:
                return 'media'
            elif valor <= 70:
                return 'alta'
            else:
                return 'ultra'
                
        elif tipo == 'configuracion':
            if valor <= 30:
                return 'baja'
            elif valor <= 50:
                return 'media'
            elif valor <= 70:
                return 'alta'
            else:
                return 'ultra'
                
        elif tipo == 'fps_objetivo':
            if valor <= 60:
                return 'conservador'
            elif valor <= 120:
                return 'estandar'
            elif valor <= 180:
                return 'competitivo'
            else:
                return 'extremo'
                
        elif tipo == 'potencia_gpu':
            if valor <= 25:
                return 'baja'
            elif valor <= 55:
                return 'media'
            elif valor <= 80:
                return 'alta'
            else:
                return 'ultra'

    def obtener_prediccion(self, entrada):
        """Obtiene la predicción específica de uso de GPU y temperatura usando el simulador de control."""
        
        # Resetear el simulador para evitar acumulación de estado entre ejecuciones
        self.simulador.reset()
        # Configurar las entradas del simulador
        self.simulador.input['resolucion'] = entrada['resolucion']
        self.simulador.input['configuracion'] = entrada['configuracion']
        self.simulador.input['fps_objetivo'] = entrada['fps_objetivo']
        self.simulador.input['potencia_gpu'] = entrada['potencia_gpu']
        
        # Ejecutar el cálculo del sistema difuso
        self.simulador.compute()

        # Ejecutar el simulador
        self.uso_gpu.view(sim=self.simulador)
        plt.savefig(f"/tmp/uso_gpu_caso.png")
        plt.close()

        self.temperatura.view(sim=self.simulador)
        plt.savefig(f"/tmp/temperatura_caso.png")
        plt.close()

        
        
        # Obtener los valores de salida
        uso_gpu_valor = self.simulador.output['uso_gpu']
        temperatura_valor = self.simulador.output['temperatura']
        
        # Convertir valores numéricos a etiquetas
        uso_gpu_label = self._convertir_uso_gpu_a_etiqueta(uso_gpu_valor)
        temperatura_label = self._convertir_temperatura_a_etiqueta(temperatura_valor)
        
        # Crear predicción detallada
        prediccion = "El Uso de GPU es " + uso_gpu_label + " (" + str(uso_gpu_valor.round(2)) + "%) y la Temperatura es " + temperatura_label + " (" + str(temperatura_valor.round(2)) + "°C)"
        
        regla_activada = ""

        # Mostrar activación en las entradas
        r_baja = fuzz.interp_membership(self.resolucion.universe, self.resolucion['baja'].mf, entrada["resolucion"])
        r_media = fuzz.interp_membership(self.resolucion.universe, self.resolucion['media'].mf, entrada["resolucion"])
        r_alta = fuzz.interp_membership(self.resolucion.universe, self.resolucion['alta'].mf, entrada["resolucion"])
        r_ultra = fuzz.interp_membership(self.resolucion.universe, self.resolucion['ultra'].mf, entrada["resolucion"])
        regla_activada += f"\n   Resolución activaciones: baja={r_baja:.2f}, media={r_media:.2f}, alta={r_alta:.2f}, ultra={r_ultra:.2f}"

        c_baja = fuzz.interp_membership(self.configuracion.universe, self.configuracion['baja'].mf, entrada["configuracion"])
        c_media = fuzz.interp_membership(self.configuracion.universe, self.configuracion['media'].mf, entrada["configuracion"])
        c_alta = fuzz.interp_membership(self.configuracion.universe, self.configuracion['alta'].mf, entrada["configuracion"])
        c_ultra = fuzz.interp_membership(self.configuracion.universe, self.configuracion['ultra'].mf, entrada["configuracion"])
        regla_activada += f"\n   Configuración activaciones: baja={c_baja:.2f}, media={c_media:.2f}, alta={c_alta:.2f}, ultra={c_ultra:.2f}"

        f_conservador = fuzz.interp_membership(self.fps_objetivo.universe, self.fps_objetivo['conservador'].mf, entrada["fps_objetivo"])
        f_estandar = fuzz.interp_membership(self.fps_objetivo.universe, self.fps_objetivo['estandar'].mf, entrada["fps_objetivo"])
        f_competitivo = fuzz.interp_membership(self.fps_objetivo.universe, self.fps_objetivo['competitivo'].mf, entrada["fps_objetivo"])
        f_extremo = fuzz.interp_membership(self.fps_objetivo.universe, self.fps_objetivo['extremo'].mf, entrada["fps_objetivo"])
        regla_activada += f"\n    FPS activaciones: conservador={f_conservador:.2f}, estandar={f_estandar:.2f}, competitivo={f_competitivo:.2f}, extremo={f_extremo:.2f}"

        g_baja = fuzz.interp_membership(self.potencia_gpu.universe, self.potencia_gpu['baja'].mf, entrada["potencia_gpu"])
        g_media = fuzz.interp_membership(self.potencia_gpu.universe, self.potencia_gpu['media'].mf, entrada["potencia_gpu"])
        g_alta = fuzz.interp_membership(self.potencia_gpu.universe, self.potencia_gpu['alta'].mf, entrada["potencia_gpu"])
        g_ultra = fuzz.interp_membership(self.potencia_gpu.universe, self.potencia_gpu['ultra'].mf, entrada["potencia_gpu"])
        regla_activada += f"\n    GPU activaciones: baja={g_baja:.2f}, media={g_media:.2f}, alta={g_alta:.2f}, ultra={g_ultra:.2f}"

        print(prediccion)
        
        return prediccion, regla_activada



    def generar_grafico_resultado(self, ruta_salida="/tmp/resultado.png"):
        """Genera la gráfica de uso_gpu y temperatura con estilo .view"""
        try:
            fig, axes = plt.subplots(2, 1, figsize=(8, 6))

            # Uso GPU
            self.uso_gpu.view(sim=self.simulador, ax=axes[0])
            axes[0].set_title("Uso de GPU")
            axes[0].set_xlabel("uso_gpu")
            axes[0].set_ylabel("Membership")

            # Temperatura
            self.temperatura.view(sim=self.simulador, ax=axes[1])
            axes[1].set_title("Temperatura")
            axes[1].set_xlabel("temperatura")
            axes[1].set_ylabel("Membership")

            fig.tight_layout()
            fig.savefig(ruta_salida, bbox_inches='tight')
            plt.close(fig)
            return ruta_salida
        except Exception:
            plt.close('all')
            raise


    def _convertir_uso_gpu_a_etiqueta(self, valor):
        """Convierte un valor numérico de uso de GPU a su etiqueta correspondiente."""
        if valor <= 25:
            return 'baja'
        elif valor <= 50:
            return 'media'
        elif valor <= 75:
            return 'alta'
        else:
            return 'critico'

    def _convertir_temperatura_a_etiqueta(self, valor):
        """Convierte un valor numérico de temperatura a su etiqueta correspondiente."""
        if valor <= 60:
            return 'normal'
        elif valor <= 70:
            return 'tibio'
        elif valor <= 85:
            return 'caliente'
        else:
            return 'critica'

    def obtener_resoluciones_disponibles(self):
        """Retorna una lista de todas las resoluciones disponibles."""
        return list(self.resoluciones.keys())
    
    def obtener_valor_resolucion(self, nombre_resolucion):
        """Obtiene el valor numérico de una resolución por su nombre."""
        return self.resoluciones.get(nombre_resolucion, 50)  
    
    def obtener_nombre_resolucion_por_valor(self, valor):
        """Obtiene el nombre de la resolución más cercana a un valor numérico."""
        # Encuentra la resolución con el valor más cercano
        resolucion_cercana = min(self.resoluciones.items(), 
                               key=lambda x: abs(x[1] - valor))
        return resolucion_cercana[0]

