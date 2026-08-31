const startBtn = document.getElementById('start-btn');
const feed = document.getElementById('feed');
let counts = { total: 0, recovered: 0, escalated: 0 };

startBtn.addEventListener('click', async () => {
    startBtn.disabled = true;
    startBtn.textContent = 'Agent Running...';
    feed.innerHTML = '';
    
    await fetch('/api/start', { method: 'POST' });
    
    const evtSource = new EventSource('/api/stream');
    evtSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.type === 'ping') return;
        
        if (data.type === 'batch_start') {
            counts.total = data.total;
            document.getElementById('stat-total').textContent = counts.total;
        }
        
        if (data.type === 'audit_event') {
            document.getElementById('progress-bar').style.width = `${data.progress}%`;
            document.getElementById('progress-text').textContent = `${data.progress}%`;
            
            if (data.status === 'recovered' && data.log.node === 'reporter') {
                counts.recovered++;
                document.getElementById('stat-recovered').textContent = counts.recovered;
            } else if ((data.status === 'escalated' || data.status === 'failed') && data.log.node === 'reporter') {
                counts.escalated++;
                document.getElementById('stat-escalated').textContent = counts.escalated;
            }
            
            appendLog(data.txn_id, data.status, data.log);
        }
        
        if (data.type === 'batch_complete') {
            startBtn.disabled = false;
            startBtn.textContent = 'Start Recovery Agent';
            evtSource.close();
        }
    };
});

function appendLog(txnId, status, log) {
    const el = document.createElement('div');
    el.className = `log-entry ${status}`;
    const badge = log.ai_used ? `<span class="log-badge badge-ai">✨ AI JUDGMENT</span>` : `<span class="log-badge badge-rule">⚙️ RULE</span>`;
    
    el.innerHTML = `
        <div class="log-header">
            <span><strong>${txnId}</strong> | ${log.node.toUpperCase()}</span>
            ${badge}
        </div>
        <div class="log-details">${log.details}</div>
    `;
    
    feed.insertBefore(el, feed.firstChild);
    if (feed.children.length > 100) feed.removeChild(feed.lastChild);
}
