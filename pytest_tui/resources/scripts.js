function TestSessionStartsButton(){var e=document.getElementById("testsessionstarts");"none"==e.style.display?e.style.display="block":e.style.display="none"}

function ShortTestSummaryButton(){var e=document.getElementById("shortsummary");"none"==e.style.display?e.style.display="block":e.style.display="none"}

function ExecutionInfoButton(){var e=document.getElementById("testexecution");"none"==e.style.display?e.style.display="block":e.style.display="none"}

function EnvironmentButton(){var e=document.getElementById("environment");"none"==e.style.display?e.style.display="block":e.style.display="none"}

function openTab(evt, tabName) { var i, tabcontent, tablinks; tabcontent = document.getElementsByClassName("tabcontent"); for (i = 0; i < tabcontent.length; i++) { tabcontent[i].style.display = "none"; } tablinks = document.getElementsByClassName("tablinks"); for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", ""); } document.getElementById(tabName).style.display = "block"; evt.currentTarget.className += " active"; }

function toggle_tab(evt, tabName) { if (content.style.display === "block") { content.style.display = "none"; } else { content.style.display = "block"; } }

var coll = document.getElementsByClassName("collapsible"); var i; for (i = 0; i < coll.length; i++) { coll[i].addEventListener("click", function() { this.classList.toggle("active"); var content = this.nextElementSibling; if (content.style.display === "block") { content.style.display = "none"; } else { content.style.display = "block"; } }); }

document.getElementById("defaultOpen").click();
