async function predictWeather() {
    const form = document.getElementById('weather-form');
    const resultDiv = document.getElementById('result');

    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    const response = await fetch('/letspredict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    const result = await response.json();
    resultDiv.textContent = `Prediction: ${result.prediction}`;
}
