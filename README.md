# Este texto esta realizado 100% por IA

# link de github https://github.com/EstebanQuijia/C11T1---Diferencias-entre-sistemas-que-simplemente-funcionan-y-sistemas-de-calidad.git

# Tema 4: Funciones y Procedimientos (Parte 4) - Buenas Prácticas de Ingeniería de Software

Este repositorio contiene la implementación y el análisis comparativo de dos sistemas de ingeniería robustos (Clínica Médica y E-Commerce), diseñados bajo estrictos estándares de calidad de software frente a implementaciones básicas o monolíticas.

---

## Ejercicio 1: Sistema de Gestión de Pacientes para una Clínica

### Decisiones de Desarrollo y Arquitectura
- **Arquitectura en Capas:** Se separó claramente la capa de persistencia/datos (`ClinicaDataLayer`), la capa de lógica de negocio para usuarios (`PacienteService`) y la agenda (`CitaService`). Esto desacopla las reglas del negocio de la forma en que se almacenan los registros.
- **Validación Exhaustiva y Excepciones:** Se implementaron validaciones previas de existencia e integridad, lanzando excepciones nativas (`ValueError`, `KeyError`) en lugar de dejar que el sistema falle silenciosamente.
- **Trazabilidad:** Se integró un sistema de registro (`logging`) para auditoría de acciones críticas.

### Análisis y Respuestas a las Preguntas de Revisión:
1. **¿Se separaron adecuadamente las responsabilidades (pacientes, citas, historiales)?**  
   Sí. Se crearon servicios independientes (`PacienteService` gestiona datos y notas médicas, mientras que `CitaService` administra exclusivamente la agenda y validación de horarios con doctores).
2. **¿Qué sucede si se intenta programar una cita en un horario ya ocupado?**  
   El sistema realiza una validación cruzada en la lista de citas del doctor antes de registrarla. Al detectar coincidencia de horario, interrumpe el flujo y lanza un `ValueError` preventivo evitando solapamientos.
3. **¿El sistema puede extenderse fácilmente para añadir nuevas especialidades médicas?**  
   Sí, altamente escalable. Las especialidades o tipos de doctores pueden agregarse como propiedades en la entidad del doctor o mediante un módulo de catálogos sin modificar la lógica central de agendamiento.
4. **¿Los nombres de las funciones y variables describen claramente su propósito?**  
   Se utilizó nomenclatura explícita y basada en verbos y sustantivos claros en español (`registrar_paciente`, `programar_cita`, `agregar_historial`), eliminando la ambigüedad.
5. **¿Se documentaron adecuadamente las funciones y métodos críticos?**  
   Cada clase y servicio cuenta con comentarios descriptivos de su responsabilidad única (Principio SOLID de Responsabilidad Única).
6. **¿Se eligieron estructuras de datos apropiadas para cada tipo de información?**  
   Se utilizó un diccionario (`dict`) indexado por ID de paciente para búsquedas eficientes en tiempo constante $O(1)$, y una lista orientada a objetos para la trazabilidad secuencial de las citas.

---

## Ejercicio 2: Plataforma de Comercio Electrónico

### Decisiones de Desarrollo y Arquitectura
- **Integridad Transaccional:** Las operaciones críticas como el descuento de stock y el procesamiento de pagos se ejecutan bajo bloques controlados. Si el pago falla o el stock es insuficiente, la transacción se aborta de manera segura.
- **Seguridad y Validación de Datos:** Se implementó autenticación de pagos mediante tokens y validación estricta de parámetros de entrada para evitar accesos indebidos o manipulación de precios.
- **Manejo de Concurrencia:** El control de inventario valida de forma atómica la disponibilidad antes de confirmar la orden de compra.

### Análisis y Respuestas a las Preguntas de Revisión:
1. **¿Se implementaron prácticas seguras para el manejo de información sensible?**  
   Sí, el procesamiento de pagos a través de `CheckoutService` aísla los tokens de pasarelas externas y previene la exposición de lógica interna del negocio.
2. **¿El sistema mantiene la integridad de los datos durante procesos críticos (como pagos)?**  
   Absolutamente. Gracias al diseño estructurado, si ocurre un fallo al verificar el stock o en la pasarela, se captura la excepción e impide un estado inconsistente en la base de datos simulada.
3. **¿Cómo maneja el sistema intentos simultáneos de compra del mismo producto?**  
   Mediante validación estricta de stock disponible en tiempo de ejecución. Si dos procesos intentan adquirir la última unidad simultáneamente, el primero reduce el stock a cero y el segundo lanza una excepción de `ValueError` por insuficiencia.
4. **¿Existe una clara división entre lógica de negocio, presentación y acceso a datos?**  
   Sí, se estructuró en capas desacopladas (`EcommerceDataLayer`, `InventarioService`, `CheckoutService`), lo que permite modificar la interfaz de usuario o la base de datos sin romper los cálculos financieros.
5. **¿Qué tan fácil es modificar parámetros como impuestos, métodos de envío, etc.?**  
   Es directo y centralizado. Al no existir valores hardcodeados dispersos en el código (magic numbers), cualquier cambio fiscal o logístico se ajusta alterando una única función de cálculo o constantes globales del sistema.