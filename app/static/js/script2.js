document.addEventListener("DOMContentLoaded", function() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            // Calculate the difference for each game
            data.forEach(game => {
                const prizesPrinted = parseInt(game['Prizes Printed'].replace(/\D/g, ''));

                // Check if 'Prizes Claimed' is '---', treat it as zero
                const prizesClaimed = game['Prizes Claimed'] === '---' ? 
                                      0 : 
                                      parseInt(game['Prizes Claimed'].replace(/\D/g, ''));

                game.difference = prizesPrinted - prizesClaimed;
            });

            // Group games by ticket price
            const gamesByPrice = data.reduce((acc, game) => {
                const price = game['Ticket Price'];
                if (!acc[price]) {
                    acc[price] = [];
                }
                acc[price].push(game);
                return acc;
            }, {});

            const container = document.getElementById('data-container');

            // Sort each group by the biggest difference and display
            Object.keys(gamesByPrice).forEach(price => {
                const priceSection = document.createElement('section');
                priceSection.className = 'price-group';
                priceSection.innerHTML = `<h2>Ticket Price: $${price}</h2><div class="games-grid"></div>`;
                const gamesGrid = priceSection.querySelector('.games-grid');

                // Sort games within this group by difference
                gamesByPrice[price].sort((a, b) => b.difference - a.difference);

                gamesByPrice[price].forEach((game, index) => {
                    const gameDiv = document.createElement('div');
                    gameDiv.className = 'game';
                    gameDiv.innerHTML = `
                        <h3>${game['Game Name']} (Rank: ${index + 1})</h3>
                        <p>Game Number: ${game['Game Number']}</p>
                        <p>Start Date: ${game['Start Date']}</p>
                        <p>Prize Amount: ${game['Prize Amount']}</p>
                        <p>Prizes Printed: ${game['Prizes Printed']}</p>
                        <p>Prizes Claimed: ${game['Prizes Claimed']}</p>
                        <p>Difference: ${game.difference}</p>
                    `;
                    gamesGrid.appendChild(gameDiv);
                });

                container.appendChild(priceSection);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});
