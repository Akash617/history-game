function showTooltip(id) {
    const name = "event-description-tooltip-".concat(id.toString())
    const tooltip = document.getElementsByClassName(name)[0]
    tooltip.style.display = "block";
}

function hideTooltip(id) {
    const name = "event-description-tooltip-".concat(id.toString())
    const tooltip = document.getElementsByClassName(name)[0]
    tooltip.style.display = "none";
}
