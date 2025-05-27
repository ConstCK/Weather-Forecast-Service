
const cityInput = document.getElementById('id_city');
const dataList = document.getElementById('city-options');

cityInput.addEventListener('input', function () {
    const query = this.value;

    if (query.length < 2) return;

    fetch(`/autocomplete/city/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            dataList.innerHTML = '';
            data.forEach(city => {
                const option = document.createElement('option');
                option.value = city;
                dataList.appendChild(option);
            });
        });
});
