function openTab(evt, tabName) { var i, tabcontent, tablinks; tabcontent = document.getElementsByClassName("tabcontent"); for (i = 0; i < tabcontent.length; i++) { tabcontent[i].style.display = "none"; } tablinks = document.getElementsByClassName("tablinks"); for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", ""); } document.getElementById(tabName).style.display = "block"; evt.currentTarget.className += " active"; }

var coll = document.getElementsByClassName("collapsible"); var i; for (i = 0; i < coll.length; i++) { coll[i].addEventListener("click", function() { this.classList.toggle("active"); var content = this.nextElementSibling; if (content.style.display === "block") { content.style.display = "none"; } else { content.style.display = "block"; } }); }

document.getElementById("defaultOpen").click();

var i, acc = document.getElementsByClassName("accordion-open"); for (i=0; i<acc.length; i++) acc[i].addEventListener("click",(function(){this.classList.toggle("active"); var panel = this.nextElementSibling; "block" === panel.style.display?panel.style.display="none":panel.style.display="block"}));

var i, acc = document.getElementsByClassName("accordion-closed"); for (i = 0; i < acc.length; i++) { acc[i].addEventListener("click", function() { this.classList.toggle("active"); var panel = this.nextElementSibling; if (panel.style.maxHeight) { panel.style.maxHeight = null; } else { panel.style.maxHeight = panel.scrollHeight + "px"; } }); }

function openAction(evt, actionName) { var i, tabcontent, tablinks; tabcontent = document.getElementsByClassName("tabcontent"); for (i = 0; i < tabcontent.length; i++) { tabcontent[i].style.display = "none"; } tablinks = document.getElementsByClassName("tablinks"); for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", ""); } document.getElementById(tabName).style.display = "block"; evt.currentTarget.className += " active"; }

// function toggleDetailsElements() { const toggleDetailsButton = document.getElementById('toggle-details'); const detailsElements = document.querySelectorAll('details'); detailsElements.forEach(detailsElement => { detailsElement.hidden = !detailsElement.hidden; }); toggleDetailsButton.addEventListener('click', () => { detailsElements.forEach(detailsElement => { detailsElement.hidden = !detailsElement.hidden; }); }); }

function toggleDetailsElements(){const t=document.querySelectorAll("details");t.forEach((t=>{t.hidden=!t.hidden}))}

function toggleAllDetails() { const details = document.getElementsByTagName("details"); for (let i = 0; i < details.length; i++) { if (details[i].hasAttribute("open")) { details[i].removeAttribute("open"); } else { details[i].setAttribute("open", ""); } } }

function removeColor() { var all = document.getElementsByTagName("*"); for (var i=0, max=all.length; i < max; i++) { all[i].style.color = 'initial'; all[i].style.backgroundColor = 'initial'; } }

var originalColors = new Map(); function removeOrRestoreColor() { if (originalColors.size === 0) { var all = document.getElementsByTagName("*"); for (var i=0, max=all.length; i < max; i++) { var computedStyle = window.getComputedStyle(all[i]); originalColors.set(all[i], computedStyle.color); all[i].style.color = "black"; all[i].style.backgroundColor = "white"; } } else { originalColors.forEach((color, element) => { element.style.color = color; }); originalColors.clear(); } }

var overrideStyleSheet = null; function removeOrRestoreColor() { if (overrideStyleSheet === null) { overrideStyleSheet = document.createElement('style'); document.head.appendChild(overrideStyleSheet); var sheet = overrideStyleSheet.sheet; sheet.insertRule("* { color: black !important; background-color: white !important; }", 0); } else { overrideStyleSheet.parentNode.removeChild(overrideStyleSheet); overrideStyleSheet = null; } }

function invertColors() { document.body.classList.toggle('invert-colors'); }
