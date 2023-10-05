function showTooltip(id) {
    const name = "event-description-tooltip-".concat(id.toString());
    const tooltip = document.getElementsByClassName(name)[0];
    tooltip.style.display = "block";
}

function hideTooltip(id) {
    const name = "event-description-tooltip-".concat(id.toString());
    const tooltip = document.getElementsByClassName(name)[0];
    tooltip.style.display = "none";
}

function updateTimeline(event_before, event_after) {
    const losePageEventBefore = document.getElementsByClassName("event-display-before")[0];
    const losePageEventAfter = document.getElementsByClassName("event-display-after")[0];

    if (event_before == "no") {
        losePageEventBefore.style.display = "none";
    }

    if (event_after == "no") {
        losePageEventAfter.style.display = "none";
    }
}
