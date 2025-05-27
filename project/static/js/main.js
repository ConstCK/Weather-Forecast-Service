document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('city-input');
    const suggestionsList = document.getElementById('suggestions');

    input.addEventListener('input', async () => {
        const query = input.value.trim();
        if (query.length < 2) {
            suggestionsList.style.display = 'none';
            return;
        }

        try {
            const response = await fetch(`/city-autocomplete/?q=${encodeURIComponent(query)}`);
            const data = await response.json();

            suggestionsList.innerHTML = '';

            if (data.length > 0) {
                data.forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = item.name;
                    li.addEventListener('click', () => {
                        input.value = item.name;
                        suggestionsList.style.display = 'none';
                    });
                    suggestionsList.appendChild(li);
                });
                suggestionsList.style.display = 'block';
            } else {
                suggestionsList.style.display = 'none';
            }
        } catch (error) {
            console.error('Ошибка при получении данных:', error);
        }
    });

    document.addEventListener('click', (event) => {
        if (!input.contains(event.target) && !suggestionsList.contains(event.target)) {
            suggestionsList.style.display = 'none';
        }
    });
});