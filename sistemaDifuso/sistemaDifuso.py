import reflex as rx
from .SistemaDF import SistemaDifusoTarjetasGraficas

class State(rx.State):
    """Estado de la aplicación para el sistema experto de tarjetas gráficas."""
    
    # Variables de estado
    resolucion: str = ""
    configuracion: str = ""
    fps_objetivo: str = ""
    potencia_gpu: str = ""
    recomendacion: str = ""
    regla_activada: str = ""
    hechos_activados: str = ""
    
    def set_resolucion(self, resolucion: str):
        """Establece la resolución deseada."""
        self.resolucion = resolucion
    
    def set_configuracion(self, configuracion: str):
        """Establece la configuración deseada."""
        self.configuracion = configuracion
    
    def set_fps_objetivo(self, fps_objetivo: str):
        """Establece el FPS objetivo deseado."""
        self.fps_objetivo = fps_objetivo
    
    def set_potencia_gpu(self, potencia_gpu: str):
        """Establece la potencia de GPU deseada."""
        self.potencia_gpu = potencia_gpu
    
    def obtener_recomendacion(self):
        """Obtiene la recomendación del sistema difuso."""
        # Crear instancia del sistema difuso
        sistema_difuso = SistemaDifusoTarjetasGraficas()
        
        # Preparar entrada para el sistema difuso
        entrada = {
            'resolucion': self.resolucion,
            'configuracion': self.configuracion,
            'fps_objetivo': self.fps_objetivo,
            'potencia_gpu': self.potencia_gpu
        }
        
        # Procesar con el sistema difuso
        self.recomendacion, self.regla_activada, self.hechos_activados = sistema_difuso.procesar_entrada(entrada)

def index():
    return rx.hstack(
        # Panel izquierdo: Formulario
        rx.vstack(
            rx.heading("Sistema Experto de Prediccion del uso de Tarjetas Graficas para Gaming", size="5", color="blue.600"),
            rx.text("Selecciona tus preferencias para obtener la mejor predicción de uso para gaming:", color="gray.600"),

            # Selector de resolución
            rx.vstack(
                rx.text("Resolución:", font_weight="bold", align="left"),
                rx.select(
                    ["baja", "media", "alta", "ultra"],
                    value=State.resolucion,
                    on_change=State.set_resolucion,
                    placeholder="Selecciona la resolución",
                    width="100%",
                ),
                align="start",
                width="100%",
                spacing="2",
            ),
            
            # Selector de configuración
            rx.vstack(
                rx.text("Configuración:", font_weight="bold", text_align="left"),
                rx.select(
                    ["baja", "media", "alta", "ultra"],
                    value=State.configuracion,
                    on_change=State.set_configuracion,
                    placeholder="Selecciona la configuración",
                    width="100%",
                ),
                align="start",
                width="100%",
                spacing="2",
            ),
            
            # Selector de FPS objetivo
            rx.vstack(
                rx.text("FPS Objetivo:", font_weight="bold", text_align="left"),
                rx.select(
                    ["conservador", "estandar", "competitivo", "extremo"],
                    value=State.fps_objetivo,
                    on_change=State.set_fps_objetivo,
                    placeholder="Selecciona el FPS objetivo",
                    width="100%",
                ),
                align="start",
                width="100%",
                spacing="2",
            ),
            
            # Selector de potencia de GPU
            rx.vstack(
                rx.text("Potencia de GPU:", font_weight="bold", text_align="left"),
                rx.select(
                    ["baja", "media", "alta", "ultra"],
                    value=State.potencia_gpu,
                    on_change=State.set_potencia_gpu,
                    placeholder="Selecciona la potencia de GPU",
                    width="100%",
                ),
                align="start",
                width="100%",
                spacing="2",
            ),
            
            rx.button(
                "Obtener Predicción de uso de GPU y Temperatura",
                on_click=State.obtener_recomendacion,
                color_scheme="blue",
                size="4",
                width="100%",
                margin_top="1rem",
            ),
            
            spacing="4",
            padding="4rem",
            width="40%",
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
                    State.recomendacion,
                    rx.vstack(
                        rx.text("Predicción:", font_weight="bold", color="gray.700", text_align="left"),
                        rx.box(
                            rx.text(
                                State.recomendacion,
                                font_family="monospace",
                                font_size="0.9rem",
                                color="blue.700",
                                text_align="center",
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
                            rx.text(
                                State.regla_activada,
                                font_family="monospace",
                                font_size="0.9rem",
                                color="blue.700",
                                text_align="center",
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
                
                # Mostrar los resultados del sistema difuso
                rx.cond(
                    State.hechos_activados,
                    rx.vstack(
                        rx.text("Resultados del Sistema Difuso:", font_weight="bold", color="gray.700", text_align="left"),
                        rx.box(
                            rx.text(
                                State.hechos_activados,
                                font_family="monospace",
                                font_size="0.9rem",
                                color="blue.700",
                                text_align="center",
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

                # Mensaje de ayuda cuando no hay recomendación
                rx.cond(
                    ~State.recomendacion,
                    rx.vstack(
                        rx.icon("info", size=3, color="blue.400"),
                        rx.text("Selecciona tus preferencias y haz clic en 'Obtener Recomendación' para ver la sugerencia del sistema difuso.", 
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
            width="60%",
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
