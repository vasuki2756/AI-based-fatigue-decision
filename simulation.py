import numpy as np

def runs(boolean_array, threshold_seconds, fps=30):
    threshold_frames = int(threshold_seconds * fps)
    padded = np.pad(boolean_array, (1, 1), 'constant', constant_values=False)
    diff = np.diff(padded.astype(int))
    starts = np.where(diff == 1)[0]
    ends = np.where(diff == -1)[0]
    
    events = []
    for s, e in zip(starts, ends):
        if (e - s) >= threshold_frames:
            start_time = s / fps
            end_time = e / fps
            alert_time = start_time + threshold_seconds
            events.append((start_time, end_time, alert_time))
    return events

def detect(t, ear, mar, pit, Tc=1.0, EAR_T=0.22, MAR_T=0.60, Ty=1.5, PIT_T=15.0, Tn=0.4, FPS=30):
    closed = ear < EAR_T
    yawn = mar > MAR_T
    nod = pit > PIT_T
    
    cl = runs(closed, Tc, FPS)
    yw = runs(yawn, Ty, FPS)
    nd = runs(nod, Tn, FPS)
    
    alerts = [("closure", c) for a, b, c in cl]
    yt = [c for a, b, c in yw]
    nt = [c for a, b, c in nd]
    
    alerts += [("yawn", yt[k]) for k in range(1, len(yt)) if yt[k] - yt[k-1] <= 120]
    alerts += [("nod", nt[k]) for k in range(2, len(nt)) if nt[k] - nt[k-2] <= 20]
              
    return sorted(alerts, key=lambda a: a[1])

if __name__ == "__main__":
    print("--- AI-Based Operator Fatigue Detection Simulation ---")
    FPS = 30
    duration_sec = 130
    t = np.linspace(0, duration_sec, duration_sec * FPS)
    
    ear = np.random.normal(0.30, 0.025, len(t))
    mar = np.random.normal(0.40, 0.02, len(t))
    pit = np.random.normal(0.0, 2.0, len(t))
    
    start_idx = int(112 * FPS)
    end_idx = int(115.5 * FPS)
    ear[start_idx:end_idx] = np.random.normal(0.11, 0.01, end_idx - start_idx)
    
    alerts = detect(t, ear, mar, pit, FPS=FPS)
    print(f"Total simulated time: {duration_sec} seconds at {FPS} FPS.")
    print(f"Number of alerts triggered: {len(alerts)}")
