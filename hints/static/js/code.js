if (window.history.replaceState) { // hacky way to prevent form resubmission on page refresh (avoiding reveal of hints if button not pressed but F5 is)
    window.history.replaceState(null, null, window.location.href);
}