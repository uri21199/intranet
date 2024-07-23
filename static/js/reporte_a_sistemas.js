const subcategoriaContainer = document.getElementById('subcategoria-container');
const tipoProblemaContainer = document.getElementById('tipo-problema-container');
const categoriaSelect = document.getElementById('categoria');
const subcategoriaSelect = document.getElementById('subcategoria');
const tipoProblemaSelect = document.getElementById('tipo_problema');

const subcategorias = {
  'Sistemas': ['CRM', 'Infobip', 'Approach', 'Mitrol', 'Audax', 'Outlook'],
  'Equipo físico': ['Computadora', 'Mouse', 'Teclado', 'Monitor', 'Impresora'],
  'Posible virus': ['Mails', 'Notificaciones de virus en computadora'],
  'Notificaciones': ['Notificaciones de licencias'],
  'Requerimientos': ['Creación de Línea', 'Creación de Correo', 'Otros'],
  'Interno': ['Compra de Licencia', 'Compra de Elementos', 'Otros']
};

const tiposProblema = {
  'CRM': ['Acceso denegado', 'Errores de aplicación', 'Problemas de sincronización'],
  'Infobip': ['Mensajes no enviados/recibidos', 'Problemas de conexión', 'Errores de configuración'],
  'Approach': ['Acceso denegado', 'Errores de aplicación', 'Problemas de sincronización'],
  'Mitrol': ['Acceso denegado', 'Errores de aplicación', 'Problemas de conexión'],
  'Outlook': ['Acceso denegado', 'Errores de aplicación', 'Problemas de conexión'],
  'Audax': ['Acceso denegado', 'Errores de aplicación', 'Problemas de sincronización'],
  'Computadora': ['No enciende', 'Lentitud', 'Bloqueos/Reinicios inesperados', 'Fallos de hardware', 'Problemas de software'],
  'Mouse': ['No responde', 'Movimientos erráticos', 'Problemas de conexión'],
  'Teclado': ['Teclas no funcionan', 'Problemas de conexión', 'Respuesta lenta'],
  'Monitor': ['No enciende', 'Pantalla negra', 'Resolución incorrecta', 'Problemas de color o brillo'],
  'Impresora': ['No imprime', 'Atascos de papel', 'Problemas de conexión', 'Calidad de impresión deficiente'],
  'Mails': ['Posible phishing', 'Adjuntos sospechosos', 'Enlaces sospechosos'],
  'Notificaciones de licencias': ['Sitios web', 'Sistemas contratados'],
  'Notificaciones de virus en computadora': ['Detección de virus/malware', 'Comportamiento anómalo', 'Solicitud de escaneo de seguridad'],
  'Creación de Línea': ['Nueva línea telefónica', 'Extensión existente'],
  'Creación de Correo': ['Nuevo correo electrónico', 'Modificación de correo existente'],
  'Otros': ['Cambios de permisos de usuario', 'Asignación de recursos adicionales'],
  'Compra de Licencia': ['Nueva licencia de software', 'Renovación de licencia existente'],
  'Compra de Elementos': ['Mouse/teclado adicionales', 'Equipos adicionales'],
  'Otros': ['Mantenimiento preventivo', 'Asesoría técnica', 'Sugerencias de mejora tecnológica']
};

categoriaSelect.addEventListener('change', function() {
  const categoria = categoriaSelect.value;
  if (categoria) {
    populateDropdown(subcategoriaSelect, subcategorias[categoria]);
    subcategoriaContainer.style.display = 'block';
    subcategoriaSelect.disabled = false;
  } else {
    subcategoriaContainer.style.display = 'none';
    subcategoriaSelect.disabled = true;
    tipoProblemaContainer.style.display = 'none';
    tipoProblemaSelect.disabled = true;
  }
});

subcategoriaSelect.addEventListener('change', function() {
  const subcategoria = subcategoriaSelect.value;
  if (subcategoria) {
    populateDropdown(tipoProblemaSelect, tiposProblema[subcategoria]);
    tipoProblemaContainer.style.display = 'block';
    tipoProblemaSelect.disabled = false;
  } else {
    tipoProblemaContainer.style.display = 'none';
    tipoProblemaSelect.disabled = true;
  }
});

function populateDropdown(select, options) {
  select.innerHTML = '<option value="" selected disabled>Seleccione una opción</option>';
  options.forEach(option => {
    const optionElement = document.createElement('option');
    optionElement.value = option;
    optionElement.textContent = option;
    select.appendChild(optionElement);
  });
}
