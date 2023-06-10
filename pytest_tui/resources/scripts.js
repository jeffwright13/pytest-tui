function openTab(evt, tabName) { var i, tabcontent, tablinks; tabcontent = document.getElementsByClassName("tabcontent"); for (i = 0; i < tabcontent.length; i++) { tabcontent[i].style.display = "none"; } tablinks = document.getElementsByClassName("tablinks"); for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", ""); } document.getElementById(tabName).style.display = "block"; evt.currentTarget.className += " active"; }

var coll = document.getElementsByClassName("collapsible"); var i; for (i = 0; i < coll.length; i++) { coll[i].addEventListener("click", function() { this.classList.toggle("active"); var content = this.nextElementSibling; if (content.style.display === "block") { content.style.display = "none"; } else { content.style.display = "block"; } }); }

document.getElementById("defaultOpen").click();

var i, acc = document.getElementsByClassName("accordion-open"); for (i=0; i<acc.length; i++) acc[i].addEventListener("click",(function(){this.classList.toggle("active"); var panel = this.nextElementSibling; "block" === panel.style.display?panel.style.display="none":panel.style.display="block"}));

var i, acc = document.getElementsByClassName("accordion-closed"); for (i = 0; i < acc.length; i++) { acc[i].addEventListener("click", function() { this.classList.toggle("active"); var panel = this.nextElementSibling; if (panel.style.maxHeight) { panel.style.maxHeight = null; } else { panel.style.maxHeight = panel.scrollHeight + "px"; } }); }

function openAction(evt, actionName) { var i, tabcontent, tablinks; tabcontent = document.getElementsByClassName("tabcontent"); for (i = 0; i < tabcontent.length; i++) { tabcontent[i].style.display = "none"; } tablinks = document.getElementsByClassName("tablinks"); for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", ""); } document.getElementById(tabName).style.display = "block"; evt.currentTarget.className += " active"; }

// function toggleDetailsElements() { const toggleDetailsButton = document.getElementById('toggle-details'); const detailsElements = document.querySelectorAll('details'); detailsElements.forEach(detailsElement => { detailsElement.hidden = !detailsElement.hidden; }); toggleDetailsButton.addEventListener('click', () => { detailsElements.forEach(detailsElement => { detailsElement.hidden = !detailsElement.hidden; }); }); }

function toggleSummaryElements(){const t=document.querySelectorAll("summary");t.forEach((t=>{t.hidden=!t.hidden}))}

function toggleDetailsElements(){const t=document.querySelectorAll("details");t.forEach((t=>{t.hidden=!t.hidden}))}

function toggleAllDetails() { const details = document.getElementsByTagName("details"); for (let i = 0; i < details.length; i++) { if (details[i].hasAttribute("open")) { details[i].removeAttribute("open"); } else { details[i].setAttribute("open", ""); } } }

function removeColor() { var all = document.getElementsByTagName("*"); for (var i=0, max=all.length; i < max; i++) { all[i].style.color = 'initial'; all[i].style.backgroundColor = 'initial'; } }

var originalColors = new Map(); function removeOrRestoreColor() { if (originalColors.size === 0) { var all = document.getElementsByTagName("*"); for (var i=0, max=all.length; i < max; i++) { var computedStyle = window.getComputedStyle(all[i]); originalColors.set(all[i], computedStyle.color); all[i].style.color = "black"; all[i].style.backgroundColor = "white"; } } else { originalColors.forEach((color, element) => { element.style.color = color; }); originalColors.clear(); } }

var overrideStyleSheet = null; function removeOrRestoreColor() { if (overrideStyleSheet === null) { overrideStyleSheet = document.createElement('style'); document.head.appendChild(overrideStyleSheet); var sheet = overrideStyleSheet.sheet; sheet.insertRule("* { color: black !important; background-color: white !important; }", 0); } else { overrideStyleSheet.parentNode.removeChild(overrideStyleSheet); overrideStyleSheet = null; } }

function invertColors() { document.body.classList.toggle('invert-colors'); }

var originalColor = document.body.style.backgroundColor; function toggleBackground() { var body = document.getElementsByTagName("body")[0]; var currentColor = body.style.backgroundColor; if (currentColor === "" || currentColor === "white") { body.style.backgroundColor = "black"; } else if (currentColor === "black") { body.style.backgroundColor = originalColor; } else { body.style.backgroundColor = "white"; } }

var preSection = document.getElementById("preSection"); var originalBackgroundColor = preSection.style.backgroundColor; var originalTextColor = preSection.style.color; function togglePreBackground() { preSection.classList.toggle("pre-bg-black"); if (preSection.classList.contains("pre-bg-black")) { preSection.style.backgroundColor = originalBackgroundColor; preSection.style.color = originalTextColor; } else { preSection.style.backgroundColor = "black"; preSection.style.color = "white"; } }



// var button = document.getElementById("toggleBackground"); var preElements = document.querySelectorAll("pre"); button.addEventListener("click", function() { for (var i = 0; i < preElements.length; i++) { preElements[i].style.backgroundColor = this.checked ? "#E6E6E6" : "#ffffff"; } });


// document.querySelector(".button-43").addEventListener("click", togglePreBackground); function togglePreBackground() { var preElements = document.querySelectorAll("pre"); for (var i = 0; i < preElements.length; i++) { preElements[i].style.backgroundColor = this.checked ? "#E6E6E6" : "#ffffff"; } }


// document.querySelector(".button-43").addEventListener("click", togglePreBackground); function togglePreBackground() { var preElements = document.querySelectorAll("pre"); for (var i = 0; i < preElements.length; i++) { preElements[i].style.backgroundColor = this.value ? "#E6E6E6" : "#000000"; } }


// var isBackgroundBlack = false; function togglePreBackground() { var preElements = document.querySelectorAll("pre"); for (var i = 0; i < preElements.length; i++) { preElements[i].style.backgroundColor = isBackgroundBlack ? "#E6E6E6" : "#000000"; } isBackgroundBlack = !isBackgroundBlack; }


var isBackgroundBlack = false; function togglePreBackground() { var preElements = document.querySelectorAll("pre"); for (var i = 0; i < preElements.length; i++) { if (isBackgroundBlack) { preElements[i].style.backgroundColor = "#E6E6E6"; preElements[i].style.color = "#000000"; } else { preElements[i].style.backgroundColor = "#000000"; preElements[i].style.color = "#FFFFFF"; } } isBackgroundBlack = !isBackgroundBlack; }
