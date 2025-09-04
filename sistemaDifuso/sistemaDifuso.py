import reflex as rx
from .SistemaDF import SistemaDifusoTarjetasGraficas
import time

# Variable global para cachear la instancia del sistema difuso
_sistema_difuso_cache = None

def obtener_sistema_difuso():
    """Obtiene la instancia del sistema difuso (singleton pattern)."""
    global _sistema_difuso_cache
    if _sistema_difuso_cache is None:
        _sistema_difuso_cache = SistemaDifusoTarjetasGraficas()
    return _sistema_difuso_cache

class State(rx.State):
    """Estado de la aplicación para el sistema experto de tarjetas gráficas."""
    
    # Variables de estado
    resolucion_seleccionada: str = "1920×1080 (Full HD)"  # Resolución por defecto
    configuracion: list[int] = [50]
    fps_objetivo: list[int] = [60]
    potencia_gpu: list[int] = [50]
    prediccion: str = ""
    regla_activada: str = ""
    cargando: bool = False
    grafico_url: str = "/tmp/uso_gpu_caso.png"
    
    def set_resolucion(self, resolucion: str):
        """Establece la resolución deseada."""
        self.resolucion_seleccionada = resolucion
    
    def set_configuracion(self, configuracion: list[int | float]):
        """Establece la configuración deseada."""
        self.configuracion = configuracion
    
    def set_fps_objetivo(self, fps_objetivo: list[int | float]):
        """Establece el FPS objetivo deseado."""
        self.fps_objetivo = fps_objetivo
    
    def set_potencia_gpu(self, potencia_gpu: list[int | float]):
        """Establece la potencia de GPU deseada."""
        self.potencia_gpu = potencia_gpu
    
    def obtener_prediccion(self):
        """Obtiene la predicción del sistema difuso usando las reglas creadas."""
        # Activar estado de carga
        self.cargando = True
        
        # Usar la instancia cacheada del sistema difuso
        sistema_difuso = obtener_sistema_difuso()
       
        
        # Obtener el valor numérico de la resolución seleccionada
        valor_resolucion = sistema_difuso.obtener_valor_resolucion(self.resolucion_seleccionada)
        
        # Preparar entrada para el sistema difuso
        entrada = {
            'resolucion': valor_resolucion,
            'configuracion': self.configuracion[0],
            'fps_objetivo': self.fps_objetivo[0],
            'potencia_gpu': self.potencia_gpu[0]
        }

        print(entrada)
        
        # Procesar con el sistema difuso usando el método de predicción
        self.prediccion, self.regla_activada = sistema_difuso.obtener_prediccion(entrada)


        # Desactivar estado de carga
        self.cargando = False

def index():
    return rx.hstack(
        # Panel izquierdo: Formulario
        rx.vstack(
            rx.heading("Sistema Difuso de Prediccion del uso de Tarjetas Graficas para Gaming", size="5", color="blue.600"),
            rx.text("Selecciona tus preferencias para obtener la mejor predicción de uso para gaming:", color="gray.600"),

            # Selector de resolución
            rx.vstack(
                rx.text("Resolución:", font_weight="bold", align="left"),
                rx.select(
                    items=[
                        # Resoluciones clásicas (4:3) - BAJA
                        "640×480 (VGA)",
                        "800×600 (SVGA)", 
                        "1024×768 (XGA)",
                        "1280×1024 (SXGA)",
                        "1600×1200 (UXGA)",
                        
                        # Resoluciones HD y widescreen - MEDIA
                        "1366×768 (HD)",
                        "1440×900 (WXGA+)",
                        "1600×900 (HD+)",
                        "1680×1050 (WSXGA+)",
                        "1920×1080 (Full HD)",
                        "1920×1200 (WUXGA)",
                        
                        # Resoluciones 2K, 3K - ALTA
                        "2560×1440 (QHD/2K)",
                        "2560×1600 (WQXGA)",
                        "2880×1800 (3K Retina)",
                        "3200×1800 (QHD+)",
                        
                        # Resoluciones 4K y superiores - ULTRA
                        "3840×2160 (4K UHD)",
                        "4096×2160 (DCI 4K)",
                        "5120×2880 (5K)",
                        "6016×3384 (6K)",
                        "7680×4320 (8K UHD)",
                        
                        # Ultrawide
                        "2560×1080 (UW-FHD)",
                        "3440×1440 (UW-QHD)",
                        "3840×1600 (UW-QHD+)",
                        "5120×1440 (Dual QHD)",
                        "5120×2160 (5K Ultrawide)"
                    ],
                    value=State.resolucion_seleccionada,
                    on_change=State.set_resolucion,
                    width="100%",
                    placeholder="Selecciona una resolución...",
                    is_disabled=State.cargando,
                ),
                rx.text(f"Seleccionada: {State.resolucion_seleccionada}", color="blue.600", font_size="sm"),
                align="start",
                width="100%",
                spacing="2",
            ),
            
            # Selector de configuración
            rx.vstack(
                rx.text("Configuración (0-30): Bajo, (20-50): Medio, (40-70): Alto, (60-100): Ultra:", font_weight="bold", text_align="left"),
                rx.slider(
                    min_=0,
                    max_=100,
                    step=1,
                    value=State.configuracion,
                    on_change=State.set_configuracion,
                    width="100%",
                    is_disabled=State.cargando,
                ),
                rx.text(f"Valor en puntos: {State.configuracion[0]}", color="blue.600", font_size="sm"),
                align="start",
                width="100%",
                spacing="2",
            ),
            
            # Selector de FPS objetivo
            rx.vstack(
                rx.text("FPS Objetivo:", font_weight="bold", text_align="left"),
                rx.slider(
                    min=30,
                    max=240,
                    step=1,
                    value=State.fps_objetivo,
                    on_change=State.set_fps_objetivo,
                    width="100%",
                    is_disabled=State.cargando,
                ),
                rx.text(f"Valor: {State.fps_objetivo[0]} FPS", color="blue.600", font_size="sm"),
                align="start",
                width="100%",
                spacing="2",
            ),
            
            # Selector de potencia de GPU
            rx.vstack(
                rx.text("Potencia de GPU -> Gamas: (0-20) Bajo, (20-50) Medio, (50-70) Alto, 70-100) Ultra", font_weight="bold", text_align="left"),
                rx.slider(
                    min_=0,
                    max_=100,
                    step=1,
                    value=State.potencia_gpu,
                    on_change=State.set_potencia_gpu,
                    width="100%",
                    is_disabled=State.cargando,
                ),
                rx.text(f"Valor: {State.potencia_gpu[0]} puntos", color="blue.600", font_size="sm"),
                align="start",
                width="100%",
                spacing="2",
            ),
            
            rx.button(
                rx.cond(
                    State.cargando,
                    rx.hstack(
                        rx.spinner(size="3"),
                        rx.text("Procesando..."),
                        spacing="2",
                    ),
                    rx.text("Obtener Predicción de uso de GPU y Temperatura"),
                ),
                on_click=State.obtener_prediccion,
                color_scheme="blue",
                size="4",
                width="100%",
                margin_top="1rem",
                is_disabled=State.cargando,
            ),
            
            spacing="4",
            padding="4rem",
            width="55%",
            bg="gray.50",
            border_radius="12px",
            box_shadow="lg",
        ),

        # Panel derecho: Resultados
        rx.box(
            rx.vstack(
                rx.heading("Predicción del Sistema Difuso", size="5", color="green.600"),

                # Mostrar predicción
                rx.cond(
                    State.prediccion,
                    rx.vstack(
                        rx.text("Predicción de Uso de GPU y Temperatura:", font_weight="bold", color="gray.700", text_align="left"),
                        rx.box(
                            rx.text(
                                State.prediccion,
                                font_family="monospace",
                                font_size="0.9rem",
                                color="blue.700",
                                text_align="left",
                            ),
                            bg="blue.50",
                            padding="1rem",
                            border_radius="6px",
                            border="1px solid",
                            border_color="blue.200",
                            width="100%",
                        ),
                        spacing="2",
                        align="start",
                        width="100%",
                    ),
                    rx.box(),
                ),
                
                # Mostrar el estado del sistema difuso
                rx.cond(
                    State.regla_activada,
                    rx.vstack(
                        rx.text("Estado del Sistema Difuso:", font_weight="bold", color="gray.700", text_align="left"),
                        rx.box(
                            rx.vstack(
                                rx.text("Resolución:", font_weight="bold", color="blue.800"),
                                rx.text(f"{State.resolucion_seleccionada}", font_size="0.9rem", color="blue.700"),
                                rx.text("Configuración:", font_weight="bold", color="blue.800"),
                                rx.text(f"{State.configuracion[0]} puntos ((0-30): Bajo, (20-50): Medio, (40-70): Alto, (60-100): Ultra)", font_size="0.9rem", color="blue.700"),
                                rx.text("FPS Objetivo:", font_weight="bold", color="blue.800"),
                                rx.text(f"{State.fps_objetivo[0]} FPS (30-60): Conservador, (60-120): Estándar, (120-180): Competitivo, (180-240): Extremo)", font_size="0.9rem", color="blue.700"),
                                rx.text("Potencia de GPU:", font_weight="bold", color="blue.800"),
                                rx.text(f"{State.potencia_gpu[0]} puntos (0-25): Bajo, (25-55): Medio, (55-80): Alto, (80-100): Ultra)", font_size="0.9rem", color="blue.700"),
                                rx.divider(),
                                rx.text("Estado del Sistema Difuso:", font_weight="bold", color="blue.800"),
                                rx.text(State.regla_activada, font_family="monospace", font_size="0.8rem", color="blue.700", white_space="pre-line"),
                                spacing="1",
                                align="start",
                            ),
                            bg="blue.50",
                            padding="1rem",
                            border_radius="6px",
                            border="1px solid",
                            border_color="blue.200",
                            width="100%",
                        ),
                        spacing="2",
                        align="start",
                        width="100%",
                    ),
                    rx.box(),
                ),




                # Mensaje de ayuda cuando no hay predicción
                rx.cond(
                    ~State.prediccion,
                    rx.vstack(
                        rx.icon("info", size=3, color="blue.400"),
                        rx.text("Selecciona tus preferencias y haz clic en 'Obtener Predicción' para ver la predicción de uso de GPU y temperatura del sistema difuso.", 
                               text_align="center", color="gray.500"),
                        spacing="2",
                        align="center",
                        width="100%",
                        padding="2rem",
                    ),
                    rx.box(),
                ),

                spacing="3",
                align="start",
                width="100%",
            ),
            margin_top="4rem",
            margin_right="2rem",
            border="1px solid",
            border_color="gray.200",
            border_radius="12px",
            align="start",
            width="45%",
            spacing="6",
            padding="2rem",
            bg="gray.100",
            min_height="50vh",
        ),
        
        spacing="6",
        padding="6",
        width="100%",
        min_height="100vh",
    )

# Configuración de la app
app = rx.App()
app.add_page(index, title="Sistema Experto de Usos de Tarjetas Graficas para Gaming")
