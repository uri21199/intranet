// Para abrir/cerrar menu lateral
$(".menu > ul > li").click(function (e){
  $(this).siblings().removeClass("active");
  $(this).toggleClass("active");
  $(this).find("ul").slideToggle();
  $(this).siblings().find("ul").slideUp();
  $(this).siblings().find("ul").find("li").removeClass("active");
})

//$(".menu-btn").click(function(){
//  $(".sidebar").toggleClass("active");
//})

function validateDates() {
let startDate = new Date(document.getElementById("startDate").value);
let endDate = new Date(document.getElementById("endDate").value);

// Verificar si endDate es menor que startDate
if (endDate < startDate) {
    alert("La fecha final no puede ser menor que la fecha inicial.");
    return false; // Evita que el formulario se envíe si la validación falla
}

// Verificar si startDate y endDate son iguales
if (startDate.getTime() === endDate.getTime()) {
    alert("La fecha inicial y la fecha final no pueden ser iguales. Por favor, solo ingrese la fecha inicial.");
    return false; // Evita que el formulario se envíe si la validación falla
}

return true; // Permite que el formulario se envíe si la validación es exitosa
}

function validarFechas() {
let fechaInicio = document.getElementById("fecha").value;
let fechaFin = document.getElementById("fecha_fin").value;

if (fechaInicio && fechaFin && fechaInicio > fechaFin) {
    alert("La fecha final no puede ser anterior a la fecha inicial.");
    return false; // Evita que el formulario se envíe si la validación falla
}

return true; // Permite que el formulario se envíe si la validación pasa
}

function toggleDropdown() {
var dropdownContent = document.querySelector('.dropdownContent');
dropdownContent.style.display = (dropdownContent.style.display === 'block') ? 'none' : 'block';
}
