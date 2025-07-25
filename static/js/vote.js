function vote(candidate_id) {
    fetch('/api/vote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ candidate_id })
    }).then(res => res.json())
      .then(data => {
        console.log(data);
        updateResults();
    });
}

function updateResults() {
    fetch('/api/results')
    .then(res => res.json())
    .then(data => {
        let total = data.reduce((sum, c) => sum + c.votes, 0);
        data.forEach(candidate => {
            let percent = total ? (candidate.votes / total * 100).toFixed(1) : 0;
            let bar = document.getElementById('bar-' + candidate.id);
            bar.style.width = percent + '%';
            bar.textContent = `${candidate.votes} votes (${percent}%)`;
        });
    });
}

setInterval(updateResults, 5000);
window.onload = updateResults;