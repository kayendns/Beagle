function search(event) {
    if (event.key === "Enter") {
        var query = event.target.value;
        fetch('http://localhost:5000/search?query=' + encodeURIComponent(query))
        .then(response => response.json())
        .then(data => {
            document.getElementById('search-results').innerHTML = '';
            data.forEach(itemData => {
                const filePath = itemData[0];
                const similarity = itemData[1];

                const item = document.createElement('div');
                item.className = 'grid-item';

                const img = document.createElement('img');
                img.src = filePath;
                img.alt = 'Image';
                img.style.width = '100%';
                img.onclick = function() { openPopup(filePath); };

                const similarityText = document.createElement('p');
                similarityText.textContent = `Similarity: ${similarity.toFixed(2)}`;

                item.appendChild(img);
                item.appendChild(similarityText);
                document.getElementById('search-results').appendChild(item);
            });
        })
        .catch(error => console.error('Error:', error));
    }
}


function openPopup(filePath) {
    document.getElementById('popup-img').src = filePath;
    document.getElementById('image-popup').style.display = 'flex';
}

function closePopup() {
    document.getElementById('image-popup').style.display = 'none';
}
