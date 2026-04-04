 const ctx = document.getElementById('appStatusChart').getContext('2d');
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Applied', 'Shortlisted', 'Selected', 'Rejected'],
      datasets: [{
        data: [
          {{ status_applied }},
          {{ status_shortlisted }},
          {{ status_selected }},
          {{ status_rejected }}
        ],
        backgroundColor: ['#0d6efd', '#ffc107', '#198754', '#dc3545']
      }]
    }
  });