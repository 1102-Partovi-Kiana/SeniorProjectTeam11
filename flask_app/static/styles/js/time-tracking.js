const scriptTag = document.currentScript;
const timeLogId = scriptTag ? scriptTag.getAttribute('data-time-log-id') : null;

document.addEventListener('DOMContentLoaded', function() {
    if (!timeLogId) {
        console.error('No time_log_id found on script tag');
        return;
    }

    const startTime = new Date();

    async function sendTimeData(data) {
        try {
            const response = await fetch('/update-time-log', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                console.error('Failed to update time log');
            }
        } catch (error) {
            console.error('Error updating time log:', error);
        }
    }

    window.addEventListener('beforeunload', function() {
        const endTime = new Date();
        const duration = (endTime - startTime) / 1000;

        const timeData = {
            time_log_id: timeLogId,
            end_time: endTime.toISOString(),
            duration: duration
        };

        if (navigator.sendBeacon) {
            const blob = new Blob([JSON.stringify(timeData)], { type: 'application/json' });
            navigator.sendBeacon('/update-time-log', blob);
        } else {
            sendTimeData(timeData);
        }
    });

    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'hidden') {
            const endTime = new Date();
            const duration = (endTime - startTime) / 1000;

            sendTimeData({
                time_log_id: timeLogId,
                end_time: endTime.toISOString(),
                duration: duration
            });
        }
    });
});