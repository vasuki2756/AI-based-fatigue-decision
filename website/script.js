let isFatigued = false;

// Simulate normal metrics
function updateMetrics() {
    if(!isFatigued) {
        document.getElementById('ear-val').innerText = (0.28 + Math.random() * 0.05).toFixed(2);
        document.getElementById('mar-val').innerText = (0.35 + Math.random() * 0.05).toFixed(2);
        document.getElementById('pitch-val').innerText = (Math.random() * 5).toFixed(1) + '°';
    }
}

setInterval(updateMetrics, 500);

// Simulate fatigue event button
document.getElementById('sim-fatigue-btn').addEventListener('click', function() {
    isFatigued = true;
    
    // Drop EAR and raise MAR to trigger thresholds
    document.getElementById('ear-val').innerText = "0.15";
    document.getElementById('mar-val').innerText = "0.65";
    document.getElementById('pitch-val').innerText = "18.2°";
    
    // Update UI to Danger
    const status = document.getElementById('current-status');
    status.className = 'alert alert-danger';
    status.innerHTML = '⚠️ PROLONGED EYE CLOSURE DETECTED';
    
    document.getElementById('live-alert').style.display = 'block';
    
    // Add to log
    const log = document.getElementById('alert-log');
    const time = new Date().toLocaleTimeString();
    log.innerHTML = `<li class="log-item danger-log">[${time}] FATIGUE ALERT: EAR fell below 0.22 for >1.0s</li>` + log.innerHTML;
    
    // Reset after 4 seconds
    setTimeout(() => {
        isFatigued = false;
        status.className = 'alert alert-safe';
        status.innerHTML = '✅ OPERATOR ALERT & ACTIVE';
        document.getElementById('live-alert').style.display = 'none';
    }, 4000);
});
